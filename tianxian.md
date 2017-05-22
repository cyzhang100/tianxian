# 天线伺服系统
        
****
## 大纲
> * 关于硬件     
> * 关于软件
> * 算法实现  
   
### 硬件篇

　　整个天线伺服平台由天线转台、电机、驱动器、工控机（这里使用DSP）、码盘等构成。
　　天线转台分为方位轴和俯仰轴。分别由不同电机驱动其转动，再由码盘得到其相对位置进行控制。

![tianxian](https://raw.githubusercontent.com/cyzhang100/tianxian/master/picture/tianxian1.jpg)    

	图为天线整体结构，其中与伺服系统相关其后得到说明。其余部分主要在于与卫星连接、定位等不予具体说明。

　　转台由电机驱动，电机选则maxon公司产品，自带码盘。如下图，其中线一端为电源，一端通过CAN传输信号。

![tianxian](https://raw.githubusercontent.com/cyzhang100/tianxian/master/picture/dianji1.jpg)    

　　驱动器选择ELMO公司产品，使用之前通过elmo composer软件对其参数进行初始化。其中接口分别为电源、通信、限位以及限位电源。    


![tianxian](https://raw.githubusercontent.com/cyzhang100/tianxian/master/picture/qudongqi1.jpg) 
	
	此图为方位轴驱动器（平台右边黑盒子），由于方位轴需要360度旋转，所以不需要限位。
	俯仰轴应该设置限位，当前时刻（2017/5/21 23:06:07）由于驱动器内单片机未抹去，暂未实现。

　　码盘测量反馈信号，这里由于俯仰轴码盘*波特率*不一直，选择使用电机自带码盘。

　　	DSP为接受输入与测量信号，并计算出控制信号，分别使方位轴与俯仰轴转动，使天线对准指定位置。接口分别为接口、两路CAN以及JTAG调试。
![tianxian](https://raw.githubusercontent.com/cyzhang100/tianxian/master/picture/dsp1.jpg) 
   

### 软件篇

> - CCS(编写C程序，并将程序烧录进DSP)
> - CAN monitor（上位机，在线调试）
> - elmo composer（调试驱动器内部参数）
> - labwindow\CVI（编写上位机程序）

　　这里主要使用CCS以及CAN monitor，在设置好ELMO参数后（另有文档说明方法）。将程序烧入DSP进行在线调试。编者对于CVI不熟，不再具体说明。对于CCS软件的安装与使用另有文件说明。**特别说明请勿将DSP中一些参数抹去，即：sector A,F,G,H（除BCDE外）**


	软件方面不再另行截图，后编者应将这些软件与文档打包进同一文件夹。
　　

### 程序篇

　　这里说明一些程序的大概流程图，编者不对其进行具体说明。    

	对于CAN通信以及信号传递编者并不精通，本文默认信号传播无误。

　　主程序为：
```c
void main()
{
	User_InitSysCtrl();									//系统初始化
	InitGlobalVar();									//初始化全局变量
														
	for (;;)
	{
		ServiceDog();													//喂狗

		CANARevHandle(gi8a_CANART, gu16a_CANABuf, gu16a_CANACount, gu16a_CANACntCache);		//CANA数据接收处理
		CANBRevHandle(gi8a_CANBRT, gu16a_CANBBuf, gu16a_CANBCount, gu16a_CANBCntCache);		//CANB数据接收处理
		
		//0.5ms定时计数
		if (gst_TimerPar.stu16_tmr500uscnt)
		{			
			gst_TimerPar.stu16_tmr500uscnt = 0;			
		}

		//1ms定时计数
		if (gst_TimerPar.stu16_tmr1mscnt)
		{			
			gst_TimerPar.stu16_tmr1mscnt = 0;
			ElmoSetHandleFun(gu16a_CANBBuf);											//20170301-Elmo:映射配置
	
			WRKMODHandle(&gst_CMD, &gst_PAR, &gst_STUS, &gst_TempVal, &gst_DrvCtl);	//工作模式处理
		}

		//2ms定时计数
		if (gst_TimerPar.stu16_tmr2mscnt)
		{			
			gst_TimerPar.stu16_tmr2mscnt = 0;
		}

		//5ms定时计数
		if (gst_TimerPar.stu16_tmr5mscnt)
		{			
			gst_TimerPar.stu16_tmr5mscnt = 0;

			StatusSend1(&gst_STUS);															//状态自动上报(5ms)
			DGS_COMDetect(gu16a_CANACount, gu16a_CANBCount, &gst_STUS, &gst_TempVal);		//通讯检测
			DGS_ElmoFaultDetect(&gst_STUS, gst_AZElmoSet, gst_ELElmoSet, gst_CROElmoSet);	//故障检测
	
		}

		//10ms定时计数
		if (gst_TimerPar.stu16_tmr10mscnt)
		{
			gst_TimerPar.stu16_tmr10mscnt = 0;
			ElmoFaultHandle(&gst_STUS);													//驱动器故障处理

			AntTypeJudge(&gst_PAR, &gst_STUS, &gst_TempVal);			//天线座架形式判断
			DGS_DataJudgeSelect(&gst_PAR, &gst_STUS, &gst_ClinRoll, &gst_ClinPitch);//当前使用的数据判断选择
			DckAngToGeoAng(&gst_STUS, &gst_TempVal);					//甲板角转变为地理角
			StatusSend2(&gst_STUS);										//状态自动上报(10ms)
		}
	
		//20ms定时计数
		if (gst_TimerPar.stu16_tmr20mscnt)
		{
			gst_TimerPar.stu16_tmr20mscnt = 0;

			StatusSend3(&gst_PAR, &gst_STUS);							//状态自动上报(20ms)
		}

		//50ms定时计数
		if (gst_TimerPar.stu16_tmr50mscnt)
		{
			gst_TimerPar.stu16_tmr50mscnt = 0;			
			
			DGS_SoftLimitJudge(&gst_PAR, &gst_STUS);					//软件限位判断	
		}

		//100ms定时计数
		if (gst_TimerPar.stu16_tmr100mscnt)
		{
			gst_TimerPar.stu16_tmr100mscnt = 0;	

			ElmoWorkModeRequre();														//Elmo驱动器工作模式查询
		}

		//200ms定时计数
		if (gst_TimerPar.stu16_tmr200mscnt)
		{
			gst_TimerPar.stu16_tmr200mscnt = 0;
		}

		//1s定时计数
		if (gst_TimerPar.stu16_tmr1scnt)
		{
			gst_TimerPar.stu16_tmr1scnt = 0;			

			CANReSendStart(&gst_TempVal);								//重新发送CAN启动命令
			WrkMOD_Reset(&gst_CMD, FALSE);								//当参数保存时，系统工作状态切换到待机，之后再恢复
			User_InitCan();												//CAN复位
		}
	}
}
```

- 程序初始化
- 初始化全局变量
- 进入循环
    - 处理CAN的数据
	- ELMO映射
	- 工作模式处理
		- 模式选择
			- 调试
				- 给定速度
			- 正常
				- 通过位置计算给定速度
		- 保护
		- 运动控制

具体流程方式从程序中读取。

### 算法篇


**海因莱茵:**
> There's no such thing as a **free lunch**. 

选择合适的算法，权衡算法的优劣。对其做出取舍。

这里使用ADRC算法对其在进行控制，具体程序写在loop.c文件中。


$$\dot{z}_1(t)=z_2(t)+\beta_1e_1(t)+b_0u_a(t)+a_1q(t)$$   
$$\dot{z}_2(t)=\beta_2e_1(t)+a_2q(t)$$
$$u_a(t)=k_1(r_a(t)-z_1(t))$$



对于其为何选择二阶ESO以及一些设计问题可以在以下论文中得到解答
> Linear Active Disturbance Rejection Control with Anti-Windup Compensation for Antenna Servo System

参数的调试在相同文件夹中的*参数选择.RAR*中。

Author->张超洋    
[TOC]


 
