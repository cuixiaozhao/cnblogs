#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# __Author__:TQTL911
# Version:python3.6.6
# Time:2018/8/24 14:41
from django import forms
from django.forms import widgets
from django.http import JsonResponse
from blog.models import UserInfo
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError


class UserForm(forms.Form):
	user = forms.CharField(max_length=32, error_messages={"required": "该字段不能为空！"}, label="用户名",
						   widget=widgets.TextInput(attrs={"class": "form-control"}))
	pwd = forms.CharField(max_length=32, label="密码", widget=widgets.PasswordInput(attrs={"class": "form-control"}))
	r_pwd = forms.CharField(max_length=32, label="确认密码", widget=widgets.PasswordInput(attrs={"class": "form-control"}))
	email = forms.EmailField(max_length=32, label="注册邮箱", widget=widgets.EmailInput(attrs={"class": "form-control"}))

	def clean_user(self):
		val = self.cleaned_data.get("user")
		user = UserInfo.objects.filter(username=val).first()

		if not user:
			return val
		else:
			raise ValidationError("该用户已经注册")

	def clean(self):
		pwd = self.cleaned_data.get("pwd")
		r_pwd = self.cleaned_data.get("r_pwd")

		if pwd and r_pwd:
			if pwd == r_pwd:
				return self.cleaned_data
			else:
				raise ValidationError("两次密码不一致！")
		else:
			return self.cleaned_data

# def clean_email(self):
# 	val = self.cleaned_data.get("email")
# 	email = UserInfo.objects.filter(email=val).first()
# 	if not email:
# 		return val
# 	else:
# 		raise ValidationError("邮箱已注册！")
