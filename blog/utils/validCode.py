#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# __Author__:TQTL911
# Version:python3.6.6
# Time:2018/8/23 21:30

import random

def get_random_color():
	return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def get_valid_code_img(request):
	# 方式1-with open方法；
	# with open("lufei.jpg","rb") as f:
	# 	data = f.read()

	# 方式2；pip install pillow;
	# from PIL import Image
	# img = Image.new("RGB",(270,40),color=get_random_color())
	# with open("validCode.png","wb") as f:
	# 	img.save(f,"png")
	# with open("validCode.png","rb") as f:
	# 	data = f.read()

	# 方式3：将数据放置于内存中，加快处理速度；
	# from PIL import Image
	# from io import BytesIO
	#
	# img = Image.new("RGB",(270,40),color=get_random_color())
	# f = BytesIO()
	# img.save(f,"png")
	# data = f.getvalue()

	# 方式4-向图像区域他添加噪点，和字符串；
	from PIL import Image, ImageDraw, ImageFont
	from io import BytesIO
	import random
	char = str(random.randint(0, 9))

	img = Image.new("RGB", (270, 40), color=get_random_color())
	draw = ImageDraw.Draw(img)
	kumo_font = ImageFont.truetype("static/font/BASKVILL.TTF", size=28)

	# 保存随机字符串；
	valid_code_str = ""
	# 生成随机字符串；
	# 方法1：
	for i in range(0, 5):
		import string
		random_char = '  '.join(
			random.sample(string.ascii_lowercase + string.ascii_uppercase, 1))  # d4}5c+/m|97e@"16]s
		draw.text((i * 50 + 20, 5), random_char, get_random_color(), font=kumo_font)
		# 保存验证码字符串；
		valid_code_str += random_char

	# 方法2：
	# for i in range(500):
	# 	random_num = str(random.randint(0,9))
	# 	random_lowercase = chr(random.randint(95,122))
	# 	random_uppercase = chr(random.randint(65,90))
	# 	random_char = random.choice([random_num,random_lowercase,random_uppercase])
	# 	draw.text((i*50+20,5),random_char,get_random_color(),font=kumo_font)

	# 进行画图；
	# draw.line()
	# draw.point()

	# 给图片添加上噪点；
	width = 270
	height = 40
	for i in range(5):
		x1 = random.randint(0, width)
		x2 = random.randint(0, width)
		y1 = random.randint(0, height)
		y2 = random.randint(0, height)
		draw.line((x1, y1, x2, y2), fill=get_random_color())

	for i in range(10):
		draw.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
		x = random.randint(0, width)
		y = random.randint(0, height)
		draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())
	print("valid_code_str", valid_code_str)

	request.session["valid_code_str"] = valid_code_str
	'''
	1、生成随机字符串；
	2、COOKIE{"sessionid":fdsfdsfds}
	3、django-session表生成记录；
	'''
	f = BytesIO()
	img.save(f, "png")
	data = f.getvalue()
	return data
