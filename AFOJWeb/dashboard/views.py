
#encoding=utf-8
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from markdown import markdown  
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist

from xml.etree.ElementTree import *
from xml.etree.ElementTree import fromstring as fs
from base64 import *
import os
from datetime import datetime
from account.models import *
from problemlist.models import *
from contest.models import *
from status.models import *
from oj.models import *
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
		pid=request.GET.get('pid',None)
		if pid!=None:
			try:
				pro=Problem.objects.get(problem_id=pid)
			except ObjectDoesNotExist:
				error=u"题目不存在"
				return render_to_response("error.html",RequestContext(request,{'error':error}))

			return render_to_response("dashboard/dashboard_add_problem.html",RequestContext(request,{'problem':pro}))
		return render_to_response("dashboard/dashboard_add_problem.html",RequestContext(request,))

	if request.method=="POST":
		pid=request.GET.get('pid',None)
		title=request.POST.get('title',None)
		description=request.POST.get('description',None)
		input=request.POST.get('input',None)
		output=request.POST.get('output',None)
		sample_input=request.POST.get('sample_input',None)
		sample_output=request.POST.get('sample_output',None)
		source=request.POST.get('source',None)
		hint=request.POST.get('hint',None)
		print pid
		if title==None:
			error="这提交的东西也太少了吧"
			return render_to_response("error.html",RequestContext(request,{"error":error}))
		if pid!=None:
			try:
				pro=Problem.objects.get(problem_id=pid)
			except ObjectDoesNotExist:
				error=u"题目不存在"
				return render_to_response("error.html",RequestContext(request,{'error':error}))
				
		if pid==None:
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
		print pro.hint
		pro.save()
		return HttpResponseRedirect("/problemlist/problem/"+str(pro.problem_id))


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
		cid=request.GET.get('cid',None)
		if cid!=None:
			try:
				con=Contest.objects.get(id=cid)
				problem_list=Contest_problem.objects.select_related().filter(contest__id=cid).order_by('num')
			except ObjectDoesNotExist:
				error="比赛不存在"
				return render_to_response("error.html",RequestContext(request,{'error':error}))
			return render_to_response("dashboard/dashboard_add_contest.html",RequestContext(request,{'contest':con,'problem_list':problem_list}))
		return render_to_response("dashboard/dashboard_add_contest.html",RequestContext(request,))
	if request.method=="POST":
		cid=request.GET.get('cid',None)
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
		if cid!=None:
			try:
				con=Contest.objects.get(id=cid)


			except ObjectDoesNotExist:
				error="比赛不存在"
				return render_to_response("error.html",RequestContext(request,{'error':error}))
			con_prolems=Contest_problem.objects.filter(contest=cid)
			for item in con_prolems:
				item.delete()
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
				# print i
				con_pro.save()
			return HttpResponseRedirect('/contest/contest?cid='+str(con.id))
		if cid==None:
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
				# print i
				con_pro.save()
			return HttpResponseRedirect('/contest/contest?cid='+str(con.id))
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
		description=item.find('description').text
		pro_input=item.find('input')
		pro_output=item.find('output')
		sample_input=item.find('sample_input')
		sample_output=item.find('sample_output')
		hint=item.find('hint')
		source=item.find('source')
		sol=item.find('solution')
		test_input=item.find('test_input')
		test_output=item.find('test_output')

		
		pro=Problem()
		try:
			pid=Problem.objects.order_by('-problem_id')[0].problem_id+1
		except:
			pid=1000
		img_id=1
		for x in item:
			if x.tag=='img':
				src=x.find('src').text
				hz=os.path.splitext(src)
				base64=b64decode(x.find('base64').text)
				imgpath=os.path.join('static/upload/img',str(pid))
				if not os.path.exists(imgpath):
					os.mkdir(imgpath)
				imgname=str(pid)+'_'+str(img_id)+hz[1]
				imgpath=os.path.join(imgpath,imgname)
				fp=open(imgpath,'w')
				fp.write(base64)
				fp.close()
				imgpath='/'+imgpath
				description=description.replace(src,imgpath)
				img_id+=1




		pro.problem_id=pid
		pro.title=title.text
		pro.description=description
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
			s.problem_id=pid
			s.user=UserOJ.objects.get(user__username=username)
			s.contest_id=None
			s.code_length=len(sol.text)
			s.save()
			code.solution_id=s.id
			code.source=sol.text
			code.save()

def dashboard_add_news(request):
	username=request.user.username
	if request.method=='GET':
		nid=request.GET.get('nid',None)
		if nid!=None:
			try:
				ne=News.objects.get(id=nid)
			except ObjectDoesNotExist:
				error="这个新闻不存在"
				return render_to_response("error.html",RequestContext(request,{"error":error}))
			return render_to_response("dashboard/dashboard_add_news.html",RequestContext(request,{'news':ne}))
		return render_to_response("dashboard/dashboard_add_news.html",RequestContext(request,))
	if request.method=='POST':
		nid=request.GET.get('nid',None)
		title=request.POST.get('title',None)
		description=request.POST.get('description',None)
		if nid!=None:
			try:
				new=News.objects.get(id=nid)
			except ObjectDoesNotExist:
				error="这个新闻不存在"
				return render_to_response("error.html",RequestContext(request,{"error":error}))
		if nid==None:		
			new=News()
		new.title=title
		new.content=description
		new.user=UserOJ.objects.get(user__username=username)
		new.save()
		return HttpResponseRedirect('/dashboard/news')
		# return render_to_response("dashboard/dashboard_add_news.html",RequestContext(request,))
def dashboard_news(request):
	if request.method=='GET':
		newitems=News.objects.all().order_by('-time')
		news_pages=Paginator(newitems,20)
		contests=[]
		page=request.GET.get('page')
		try:
			news=news_pages.page(page)
		except PageNotAnInteger:
			news=news_pages.page(1)
		except EmptyPage:
			news=news_pages.page(news_pages.num_pages)
		return  render_to_response("dashboard/dashboard_news.html",RequestContext(request,{'news':news}))