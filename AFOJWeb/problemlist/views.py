#encoding=utf-8

import re
from django.db import IntegrityError
from django.contrib.auth.models import User

from django.shortcuts import render_to_response,RequestContext
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from util import request_method_only
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist

# from account.models import *
from problemlist.models import *
from contest.models import *
from status.models import *
from django.db.models import Q
from account.models import Privilege,UserOJ
from AFOJWeb import config
# Create your views here.
# @request_method_only('GET')
def index(request):
	if request.method=='GET':
		username=request.user.username
		try:
			user_authority=Privilege.objects.get(user__user__username=username).authority
			if user_authority==config.ADMIN:
				problem_list=Problem.objects.all()
			else:
				problem_list=Problem.objects.filter(visible=True)
		except ObjectDoesNotExist:
			problem_list=Problem.objects.filter(visible=True)# Pagitor
	problem_pages=Paginator(problem_list,10)
	problems=[]
	page=request.GET.get('page')
	try:
		problems=problem_pages.page(page)
	except PageNotAnInteger:
		problems=problem_pages.page(1)
	except EmptyPage:
		problems=problem_pages.page(problem_pages.num_pages)
	# print problems
	# for item in problems:
	# 	print item.problem_id

	return render_to_response("problemlist/problemlist.html",RequestContext(request,{"problems":problems}))

def problem_show(request,pid):
	if request.method=='GET':
		cid=request.GET.get('cid',None)
		username=request.user.username
		print 'user_id'
		print request.user.id
		 # problem 不属于 contest的情况
		try:
			authority=Privilege.objects.get(user_id=request.user.id).authority

		except ObjectDoesNotExist:
			authority=None
			if cid==None:
				try:
					problem=Problem.objects.get(problem_id=pid)
				except ObjectDoesNotExist:
					error="这个题目不存在哦"
					return render_to_response("error.html",RequestContext(request,{"error":error}))
				if authority==config.ADMIN or problem.visible is True:
					return render_to_response("problemlist/problem.html",RequestContext(request,{"problem":problem})) 	
				else:
					error="这个题目不存在哦"
					return render_to_response("error.html",RequestContext(request,{"error":error}))

		#problem 属于 contest的情况
		try:
			problem=Problem.objects.get(problem_id=pid)
		except ObjectDoesNotExist:
			error="这个题目不存在哦"
			return render_to_response("error.html",RequestContext(request,{"error":error}))
		if cid!=None:
			try:
				Contest_problem.objects.get(contest_id=cid,problem_id=pid)
			except ObjectDoesNotExist:
				error="这个比赛或者题目不存在哦"
				return render_to_response("error.html",RequestContext(request,{"error":error}))
			try:
				contest=Contest.objects.get(id=cid)
			except ObjectDoesNotExist:
				error="这个比赛不存在哦"
				return render_to_response("error.html",RequestContext(request,{"error":error}))
			if authority==config.ADMIN or problem.visible is True:
				return render_to_response("problemlist/problem.html",RequestContext(request,{"problem":problem,"cid":cid}))
			if contest.start_or_not():		
				if contest.private==0:
					return render_to_response("problemlist/problem.html",RequestContext(request,{"problem":problem,"cid":cid}))
				else:
					try:
						ContestPrivilege.objects.get(contest_id=cid,user__user__username=username)
						return render_to_response("problemlist/problem.html",RequestContext(request,{"problem":problem,"cid":cid}))
					except ObjectDoesNotExist:
						error="你不允许参加这个比赛，联系下管理员吧"
						return render_to_response("error.html",RequestContext(request,{"error":error}))

			else:
				error="比赛还没有开始哟"
				return render_to_response("error.html",RequestContext(request,{"error":error}))
		else:
			return render_to_response("problemlist/problem.html",RequestContext(request,{"problem":problem}))

@login_required(login_url='account')
@request_method_only('POST')
def submit_code(request):
	if request.method=='POST':
		code=request.POST.get('code',None)
		language=request.POST.get('language',None)
		pid=request.POST.get('pid',None)
		cid=request.POST.get('cid',None)
		try:
			problem=Problem.objects.get(problem_id=pid)
		except ObjectDoesNotExist:
			error="这个题目不存在哦"
			return render_to_response("error.html",RequestContext(request,{"error":error}))
		username=request.user.username
		try:
			authority=Privilege.objects.get(user__user__username=username).authority
		except ObjectDoesNotExist:
			authority=None
		if cid==None:
			if problem.visible==False and authority!=config.ADMIN:
				error="这个题目 NO可用哦"
				return render_to_response("error.html",RequestContext(request,{"error":error}))
		if cid!=None:
			try:
				contest=Contest.objects.get(id=cid)
			except ObjectDoesNotExist:
				error="这个比赛不存在哦"
				return render_to_response("error.html",RequestContext(request,{"error":error}))
			if contest.start_or_not ==False or contest.end_or_not ==False:
				if not(authority==config.ADMIN or contest.user.user.username==username):
					error="这个比赛还没开始 或者已经结束了"
					return render_to_response("error.html",RequestContext(request,{"error":error}))
			else:
				if contest.private:
					try:
						ContestPrivilege.objects.get(contest_id=cid,user__user__username=username)
					except ObjectDoesNotExist:
						if not(authority==config.ADMIN or contest.user.user.username==username):
							error="你不允许提交代码"
							return render_to_response("error.html",RequestContext(request,{"error":error}))


		if len(code) == 0:
	             		error = u"你的代码 有点太短小精悍了吧!"
			# return render_to_response("error.html",RequestContext(request,{"error":error}))
		if cid!=None:
			problem_obj=Contest_problem.objects.get(contest_id=cid,problem_id=pid)
			submit_dic={
			'user':request.user.useroj,
			'problem':problem,
			'ip':request.META.get('REMOTE_ADDR'),
			'code_length':len(code),
			'language':language,
			'num':problem_obj.num
			}
		if cid==None:
			submit_dic={
			'user':request.user.useroj,
			'problem':problem,
			'ip':request.META.get('REMOTE_ADDR'),
			'code_length':len(code),
			'language':language,
			}
		if cid !=None:
			try:
				contest=Contest.objects.get(id=cid)
				submit['contest']=contest
			except ObjectDoesNotExist:
				error="这个比赛不存在哦"
				return render_to_response("error.html",RequestContext(request,{"error":error}))
		solution=Solution.objects.create(**submit_dic)
		Source_code.objects.create(solution=solution,source=code)
		if cid==None:
			return HttpResponseRedirect('/status/')
		if cid!=None:
			return HttpResponseRedirect('/')