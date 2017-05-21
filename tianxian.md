# 天线伺服系统
        
****
## 大纲
> * 关于硬件     
> * 关于软件
> * 算法实现  
   
### 硬件篇

　　整个天线伺服平台由天线转台、电机、驱动器、工控机（这里使用DSP）、码盘等构成。
　　天线转台分为方位轴和俯仰轴。分别由不同电机驱动其转动，再由码盘得到其相对位置进行控制。

![tianxian](https://raw.xgithubusercontent.com/cyzhang100/tianxian/master/picture/tianxian1.jpg)    

	图为天线整体结构，其中与伺服系统相关其后得到说明。其余部分主要在于与卫星连接、定位等不予具体说明。

　　转台由电机驱动，电机选则maxon公司产品，自带码盘。如下图，其中线一端为电源，一端通过CAN传输信号。

![tianxian](https://raw.xgithubusercontent.com/cyzhang100/tianxian/master/picture/dianji1.jpg)    

　　驱动器选择ELMO公司产品，使用之前通过elmo composer软件对其参数进行初始化。其中接口分别为电源、通信、限位以及限位电源。    


![tianxian](https://raw.xgithubusercontent.com/cyzhang100/tianxian/master/picture/qudongqi1.jpg) 
	
	此图为方位轴驱动器（平台右边黑盒子），由于方位轴需要360度旋转，所以不需要限位。
	俯仰轴应该设置限位，当前时刻（2017/5/21 23:06:07）由于驱动器内单片机未抹去，暂未实现。

　　码盘测量反馈信号，这里由于俯仰轴码盘*波特率*不一直，选择使用电机自带码盘。

　　	DSP为接受输入与测量信号，并计算出控制信号，分别使方位轴与俯仰轴转动，使天线对准指定位置。接口分别为接口、两路CAN以及JTAG调试。
![tianxian](https://raw.xgithubusercontent.com/cyzhang100/tianxian/master/picture/dsp1.jpg) 
   

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



**海因莱茵:**
> There's no such thing as a **free lunch**. 

Author->张超洋    
[TOC]


    
```sequence
此图为方位轴驱动器（平台右边黑盒子），由于方位轴需要360度旋转，所以不需要限位。
俯仰轴应该设置限位，当前时刻（2017/5/21 23:06:07）由于驱动器内单片机未抹去，暂未实现。
张三->李四: 嘿，小四儿, 写博客了没?
Note right of 李四: 李四愣了一下，说：
李四-->张三: 忙得吐血，哪有时间写。
```

```flow
st=>start: 开始
e=>end: 结束
op=>operation: 我的操作
cond=>condition: 确认？

st->op->cond
cond(yes)->e
cond(no)->op
```
```js
function fancyAlert(arg) {
  if(arg) {
    $.facebox({div:'#foo'})
  }

}
```

第一格表头 | 第二格表头
--------- | -------------
内容单元格 第一列第一格 | 内容单元格第二列第一格
内容单元格 第一列第二格 多加文字 | 内容单元格第二列第二格


块级公式：
$$  x = \dfrac{-b \pm \sqrt{b^2 - 4ac}}{2a} $$

\\[ \frac{1}{\Bigl(\sqrt{\phi \sqrt{5}}-\phi\Bigr) e^{\frac25 \pi}} =
1+\frac{e^{-2\pi}} {1+\frac{e^{-4\pi}} {1+\frac{e^{-6\pi}}
{1+\frac{e^{-8\pi}} {1+\ldots} } } } \\]

行内公式： $\Gamma(n) = (n-1)!\quad\forall n\in\mathbb N$
[TOC]

```flow
st=>start: 开始
e=>end: 结束
op=>operation: 我的操作
cond=>condition: 确认？

st->op->cond
cond(yes)->e
cond(no)->op
```
