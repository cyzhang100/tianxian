from PIL import Image
img=Image.open("dianji.jpg")  
w,h=img.size
print(w,h)
img.thumbnail((w//3, h//3))
img.save("dianji1.jpg","jpeg")  