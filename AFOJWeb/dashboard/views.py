from django.shortcuts import render
#encoding=utf-8
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from markdown import markdown  
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist

from account.models import *
from problemlist.models import *
from AFOJWeb import config
# Create your views here.
def index(request):
	return render_to_response("dashboard/dashboard.html",RequestContext(request,))
def dashboard_problem(request):
	if request.method=='GET':
		username=request.user.username
		try:
			user_authority=Privilege.objects.get(user__user__username=username).authority
			if user_authority==config.ADMIN:
				problem_list=Problem.objects.all()
			else:
				problem_list=Problem.objects.filter(visible=True)
		except ObjectDoesNotExist:
			problem_list=Problem.objects.all()# Pagitor
	pid=request.GET.get('pid',None)
	if pid:
		try:
			pro=Problem.objects.get(problem_id=pid)
			pro.visible= not pro.visible
			pro.save()
			HttpResponseRedirect('/dashboard/problem')
		except ObjectDoesNotExist:
			error="题目不存在"
			return render_to_response("error.html",RequestContext(request,{'error':error}))
	problem_pages=Paginator(problem_list,10)
	problems=[]
	page=request.GET.get('page')
	try:
		problems=problem_pages.page(page)
	except PageNotAnInteger:
		problems=problem_pages.page(1)
	except EmptyPage:
		problems=problem_pages.page(problem_pages.num_pages)
	return render_to_response("dashboard/dashboard_problem.html",RequestContext(request,{'problems':problems}))

def dashboard_add_problem(request):
	if request.method=="GET":	
		return render_to_response("dashboard/dashboard_add_problem.html",RequestContext(request,))
	if request.method=="POST":
		title=request.POST.get('title',None)
		description=request.POST.get('description',None)
		input=request.POST.get('input',None)
		output=request.POST.get('output',None)
		sample_input=request.POST.get('sample_input',None)
		sample_output=request.POST.get('sample_output',None)
		source=request.POST.get('source',None)
		hint=request.POST.get('hint',None)
		if title==None:
			error="这提交的东西也太少了吧"
			return render_to_response("error.html",RequestContext(request,{"error":error}))
		pro=Problem()
		try:
			temp=Problem.objects.order_by('-problem_id')[0].problem_id+1
		except:
			temp=1000
		pro.problem_id=temp
		pro.title=title
		pro.description=description
		pro.pro_input=input
		pro.pro_output=output
		pro.sample_input=sample_input
		pro.sample_output=sample_output
		pro.hint=hint
		pro.source=source
		pro.time_limit=1000
		pro.memory_limit=65536
		pro.save()
		return HttpResponseRedirect("/problemlist")
