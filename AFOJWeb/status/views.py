#encoding=utf-8
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from markdown import markdown  
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from status.models import *
from contest.models import *
from AFOJWeb import config

from string import ascii_uppercase
# Create your views here.

def index(request):
	if request.method=="POST":
		pid=request.POST.get('pid',None)
		username=request.POST.get('username',None)
		lang=request.POST.get('lang',None)
		result=request.POST.get('result',None)
		status_list=Solution.objects.all()
		# print username
		if pid:
			status_list=status_list.filter(problem=pid)
		if username:
			status_list=status_list.filter(user__user__username=username)
		if lang!='A':
			status_list=status_list.filter(language=lang)
		if result!='A':
			status_list=status_list.filter(result=result)
		status_pages=Paginator(status_list.order_by('-id'),20)
		page=request.GET.get('page')
		try:
			statuses=status_pages.page(page)
		except PageNotAnInteger:
			statuses=status_pages.page(1)
		except EmptyPage:
			statuses=status_pages.page(status_pages.num_pages)
		return render_to_response("status/status_list.html",RequestContext(request,{'statuses':statuses}))


	if request.method=="GET":
		status_list=Solution.objects.all()
		status_pages=Paginator(status_list.order_by('-id'),20)
		page=request.GET.get('page')
		try:
			statuses=status_pages.page(page)
		except PageNotAnInteger:
			statuses=status_pages.page(1)
		except EmptyPage:
			statuses=status_pages.page(status_pages.num_pages)
		return render_to_response("status/status_list.html",RequestContext(request,{'statuses':statuses}))

def contest_status_list(request):
	cid=request.GET.get('cid',None)
	try:
		contests=Contest.objects.get(id=cid)
	except ObjectDoesNotExist:
		error="这个比赛不存在"
		return render_to_response("error.html",RequestContext(request,{"error":error}))
	con_problems=Contest_problem.objects.all().filter(contest_id=cid).order_by('num')
	if request.method=='POST':
		pid=request.POST.get('pid',None)
		username=request.POST.get('username',None)
		lang=request.POST.get('lang',None)
		result=request.POST.get('result',None)
		status_list=Solution.objects.filter(contest_id=cid)
		for status in status_list:
			for con_prox in con_problems:
				if status.problem_id==con_prox.problem_id:
					status.problem_id=con_prox.num

		if pid!='A':
			pid=int(pid)
			for con_pro in con_problems:
				if con_pro.num==pid:
					print con_pro.problem_id
					pid=con_pro.problem.problem_id
					break
			status_list=status_list.filter(problem=pid)
		if username:
			status_list=status_list.filter(user__user__username=username)
		if lang!='A':
			status_list=status_list.filter(language=lang)
		if result!='A':
			status_list=status_list.filter(result=result)
		status_pages=Paginator(status_list.order_by('-id'),20)
		page=request.GET.get('page')
		try:
			statuses=status_pages.page(page)
		except PageNotAnInteger:
			statuses=status_pages.page(1)
		except EmptyPage:
			statuses=status_pages.page(status_pages.num_pages)
		return render_to_response("status/contest_status_list.html",RequestContext(request,{'statuses':statuses,'contest':contests,'con_problems':con_problems}))
	if request.method=='GET':
		status_list=Solution.objects.filter(contest_id=cid)
		status_pages=Paginator(status_list.order_by('-id'),20)
		page=request.GET.get('page')
		try:
			statuses=status_pages.page(page)
		except PageNotAnInteger:
			statuses=status_pages.page(1)
		except EmptyPage:
			statuses=status_pages.page(status_pages.num_pages)
		return render_to_response("status/contest_status_list.html",RequestContext(request,{'statuses':statuses,'contest':contests,'con_problems':con_problems}))

def code_show(request):
	if request.method=="GET":
		run_id=request.GET.get('run_id',None)
		cid=request.GET.get('cid',None)
		run_id=int(run_id)
		try:
			sol=Solution.objects.get(id=run_id)
		except ObjectDoesNotExist:
			
			error="没有这条记录"
			return render_to_response("error.html",RequestContext(request,{"error":error}))
		try: 
			source_code=Source_code.objects.get(solution=sol)
		except ObjectDoesNotExist:
			error="没有这条记录"
			return render_to_response("error.html",RequestContext(request,{"error":error}))

		try:
			compile_error=Compile_info.objects.get(solution=sol)
		except:
			compile_error=None


		username=request.user.username
		show_flag=False
		try:
			user_authority=Privilege.objects.get(user__user__username=username).authority
			if user_authority==config.ADMIN:
				show_flag=True
		except ObjectDoesNotExist:
			show_flag=False
		# print sol.user
		if sol.user==username:
			show_flag=True
	return render_to_response("status/code_show.html",RequestContext(request,{'solution':sol,'source_code':source_code,'compile_error':compile_error,'show_flag':show_flag}))