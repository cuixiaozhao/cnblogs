from django.shortcuts import render, HttpResponse, redirect

# Create your views here.

from django.http import JsonResponse
from django.contrib import auth
from blog.Myforms import UserForm
from blog.models import UserInfo
from blog import models
from django.db.models import Count


def login(request):
	"""
	登录；
	:param request:
	:return:
	"""
	if request.method == "POST":
		response = {"user": None, "msg": None}
		user = request.POST.get("user")
		pwd = request.POST.get("pwd")
		valid_code = request.POST.get("valid_code")

		valid_code_str = request.session.get("valid_code_str")
		if valid_code.upper() == valid_code_str.upper():
			user = auth.authenticate(username=user, password=pwd)
			if user:
				auth.login(request, user)
				response["user"] = user.username
			else:
				response["msg"] = "用户名或者密码错误！"
		else:
			response["msg"] = "验证码错误!"
		return JsonResponse(response)
	return render(request, "login.html")


def index(request):
	"""
	首页；
	:param request:
	:return:
	"""
	article_list = models.Article.objects.all()

	return render(request, "index.html", {"article_list": article_list})


def logout(request):
	auth.logout(request)  # 等同于request.session.flush()
	return redirect("/login/")


def get_valid_code_img(request):
	"""
	基于PIL模块动态生成响应状态码图片；
	:param request:
	:return:
	"""
	from blog.utils.validCode import get_valid_code_img
	data = get_valid_code_img(request)
	return HttpResponse(data)


def register(request):
	"""
	注册；
	:param request:
	:return:
	"""
	# if request.method == "POST":
	if request.is_ajax():
		# print(request.POST)
		form = UserForm(request.POST)

		response = {"user": None, "msg": None}
		if form.is_valid():
			response["user"] = form.cleaned_data.get("user")
			# 生成一条用户记录；
			user = form.cleaned_data.get("user")
			pwd = form.cleaned_data.get("pwd")
			email = form.cleaned_data.get("email")
			avatar_obj = request.FILES.get("avatar")
			'''
			if avatar_obj:
				user_obj = UserInfo.objects.create_user(username=user,password=pwd,email=email,avatar = avatar_obj )
			else:
				user_obj = UserInfo.objects.create_user(username=user, password=pwd, email=email)
			'''
			extra = {}

			if avatar_obj:
				extra["avatar"] = avatar_obj
			UserInfo.objects.create_user(username=user, password=pwd, email=email, **extra)
		else:
			# print(form.cleaned_data)
			# print(form.errors)
			response["msg"] = form.errors
		return JsonResponse(response)
	form = UserForm()
	return render(request, "register.html", {"form": form})


def home_site(request, username):
	"""
	个人站点视图函数；
	:param request:
	:return:
	"""
	print("username", username)
	user = UserInfo.objects.filter(username=username).first()
	# 判断用户是否存在；
	if not user:
		return render(request, "not_found.html")
	# 查询当前站点对象：
	blog = user.blog
	# 当前用户或者当前站点对应的所有文章；
	# 基于对象查询；
	# article_list = user.article_set.all()
	# 基于双下划线的查询；
	article_list = models.Article.objects.filter(user=user)

	# 每一个后表的模型.objedts.values("pk").annotate(聚合函数(关联表__统计字段)).values("表模型的所有字段以及统计字段")

	# 1、查询每一个分类名称以及对应的文章数;
	ret1 = models.Category.objects.values("pk").annotate(c=Count("article__title")).values("title", "c")
	print(ret1)
	# 2、查询当前站点的每一个分类名称以及对应的文章数；
	cate_list = models.Category.objects.filter(blog=blog).values("pk").annotate(c=Count("article__title")).values_list(
		"title", "c")
	print(cate_list)

	# 3、查询当前站点的每一个标签名称对应的文章数；
	"""
	方式1：
	tag_list = models.Tag.objects.filter(blog=blog).values("pk").annotate(c=Count("article")).values_list("title", "c")
	print(tag_list)
	#4、查询当前站点每一个年月的名称以及对应的文章数之extra函数；
	ret2 = models.Article.objects.extra(select={"is_recent":"create_time > '2018-08-26'"}).values("title","is_recent")
	print(ret2)
	date_list = models.Article.objects.filter(user=user).extra(select={"y_m_date":"date_format(create_time,'%%Y-%%m')"}).values("y_m_date").annotate(c = Count("nid")).values("y_m_date","c")
	print("这里是date_list",date_list)
	"""

	"""
	方式2：
	"""
	from django.db.models.functions import TruncMonth
	ret4 = models.Article.objects.filter(user=user).annotate(month=TruncMonth("create_time")).values("month").annotate(
		c=Count("nid")).values_list("month", "c")
	print("ret----->", ret4)

	return render(request, "home_site.html", {"username": username, "blog": blog, "article_list": article_list})
