
#encoding=utf-8
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from markdown import markdown  
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist

from xml.etree.ElementTree import *
from xml.etree.ElementTree import fromstring as fs
import os
from datetime import datetime
from account.models import *
from problemlist.models import *
from contest.models import *
from status.models import *
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
			error=u"题目不存在"
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


def dashboard_contest(request):
	if request.method=='GET':
		username=request.user.username
		try:
			user_authority=Privilege.objects.get(user__user__username=username).authority
			if user_authority==config.ADMIN:
				contest_list=Contest.objects.all()
			else:
				contest_list=Contest.objects.filter(visible=True)
		except ObjectDoesNotExist:
			contest_list=Contest.objects.all()# Pagitor
	cid=request.GET.get('cid',None)
	if cid:
		try:
			con=Contest.objects.get(id=cid)
			con.visible= not con.visible
			con.save()
			HttpResponseRedirect('/dashboard/contest')
		except ObjectDoesNotExist:
			error="比赛不存在"
			return render_to_response("error.html",RequestContext(request,{'error':error}))
	contest_pages=Paginator(contest_list,20)
	contests=[]
	page=request.GET.get('page')
	try:
		contests=contest_pages.page(page)
	except PageNotAnInteger:
		contests=contest_pages.page(1)
	except EmptyPage:
		contests=contest_pages.page(contest_pages.num_pages)
	return render_to_response("dashboard/dashboard_contest.html",RequestContext(request,{'contests':contests}))


def dashboard_add_contest(request):
	if request.method=="GET":
		return render_to_response("dashboard/dashboard_add_contest.html",RequestContext(request,))
	if request.method=="POST":
		title=request.POST.get('title',None)
		description=request.POST.get('description',None)
		problems=request.POST.get('problems',None)
		start_time=request.POST.get('start_time',None)
		end_time=request.POST.get('end_time',None)
		private=request.POST.get('private',None)
		username=request.user.username
		# print request.user
		if title==None:
			error="这提交的东西也太少了吧"
			return render_to_response("error.html",RequestContext(request,{"error":error}))
		con=Contest()
		con.title=title
		con.start_time=start_time
		con.end_time=end_time
		con.description=description
		try:
			contest_user_add=UserOJ.objects.get(user__username=username)
			con.user=contest_user_add
			# print contest_user_add
		except ObjectDoesNotExist:
			error="账户信息有问题"
			return render_to_response("error.html",RequestContext(request,{"error":error}))
		
		con_pro=Contest_problem()
		problems=problems.split(',')
		con.save()
		i=0
		for item in problems:
			try:
				pro=Problem.objects.get(problem_id=item)
			except ObjectDoesNotExist:
				error="这个题目不存在"
				return render_to_response("error.html",RequestContext(request,{"error":error}))	
			con_pro=Contest_problem()
			con_pro.problem=pro
			con_pro.contest=con
			con_pro.num=i
			i=i+1
			print i
			con_pro.save()
		return HttpResponseRedirect('/dashboard/contest')
		# con.user=request.user.username
		# print con.user
		# print title,description,problems,start_time,end_time,private

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

def fps_upload(request):
	if request.method=="POST":

		handle_fps(request.FILES['file'],request)
		return HttpResponseRedirect('/dashboard/problem')
	if request.method=='GET':
		return render_to_response("dashboard/dashboard_upload_fps.html",RequestContext(request,))
		



def handle_fps(fpsxml,request):
	username=request.user.username
	fps=fpsxml.read()
	root=fs(fps)
	# print fps
	list=root.getiterator('item')
	# print list
	for item in list:
		time_limit=item.find('time_limit')
		title=item.find('title')
		# print title
		memory_limit=item.find('memory_limit')
		description=item.find('description')
		pro_input=item.find('input')
		pro_output=item.find('output')
		sample_input=item.find('sample_input')
		sample_output=item.find('sample_output')
		hint=item.find('hint')
		source=item.find('source')
		sol=item.find('solution')
		test_input=item.find('test_input')
		test_output=item.find('test_output')
		img=item.find('base64')
		src=item.find('src')
		print img,src
		pro=Problem()
		try:
			pid=Problem.objects.order_by('-problem_id')[0].problem_id+1
		except:
			pid=1000
		pro.problem_id=pid
		pro.title=title.text
		pro.description=description.text
		pro.time_limit=time_limit.text
		pro.memory_limit=memory_limit.text
		pro.pro_input=pro_input.text
		pro.pro_output=pro_output.text
		pro.sample_input=sample_input.text
		pro.sample_output=sample_output.text
		if hint:
			pro.hint=hint.text
		pro.source=source.text
		pro.in_date=datetime.now()
		pro.save()
		path=os.path.join('/home/blade/data/',str(pid))
		# print path
		os.mkdir(path)
		path1in=os.path.join(path,'test0.in')
		path2in=os.path.join(path,'test0.out')
		f1=open(path1in,'w')
		f2=open(path2in,'w')
		f1.write(test_input.text)
		# temp=unicode(test_output.text,"utf8")
		f2.write(test_output.text)
		f1.close()
		f2.close()
		print 'sol'
		print sol
		if sol!=None:
			print "Solution is Ture"
			s=Solution()
			code=Source_code()
			try:
				run_id=solutiorun_.objects.order_by('-id')[0].solution_id+1
			except:
				run_id=1
			s.solution_id=run_id
			s.problem_id=pid
			s.user=UserOJ.objects.get(user__username=username)
			s.contest_id=None
			s.code_length=len(sol.text)
			s.save()
			code.solution_id=run_id
			code.source=sol.text
			code.save()

