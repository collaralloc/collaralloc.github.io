from PIL import Image
def splitpic(src,fold):
	img=Image.open(src);
	print(img.size)
	print(type(img.size))
	x = img.size[0]/3
	y = img.size[1]/3
	id = 0
	for i in range(3):
		for j in range(3):
			cropped = img.crop((x*i,y*j,x*(i+1),y*(j+1)))
			id+=1
			cropped.save("./"+fold+"/0"+str(id)+".png");
for i in range(4):
	src="u"+str(i+1)+".png"
	fold = str(i)
	splitpic(src,fold)