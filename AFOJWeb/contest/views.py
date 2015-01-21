#encoding=utf-8

import re
from django.db import IntegrityError
from django.contrib.auth.models import User
from datetime import *

from django.shortcuts import render_to_response,RequestContext
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from util import request_method_only
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from problemlist.models import *
from contest.models import *
from status.models import *
from account.models import Privilege,UserOJ
from AFOJWeb import config
# Create your views here.
def contest_list(request):
	if request.method=='GET':
		username=request.user.username
		try:
			user_authority=Privilege.objects.get(user__user__username=username).authority
			if user_authority==config.ADMIN:
				contests=Contest.objects.all()
			else:
				contests=Contest.objects.filter(Q(visible=True) | (Q(user__user__username=username) & Q(visible=False)))
		except ObjectDoesNotExist:
			contests=Contest.objects.filter(Q(visible=True) | (Q(user__user__username=username) & Q(visible=False)))
		for contest in contests:
			if (contest.start_or_not() and contest.end_or_not):
				contest.status=1
			if contest.start_or_not==False:
				contest.status=0
			if contest.end_or_not==False:
				contest.status=2
			contest.save()
		print datetime.now()
		contest_pages=Paginator(contests,10)
		page=request.GET.get('page')
		try:
			contest_e_page=contest_pages.page(page)
		except PageNotAnInteger:
			contest_e_page=contest_pages.page(1)
		except EmptyPage:
			contest_e_page=contest_pages.page(contest_pages.num_pages)
		return render_to_response("contest/contest_list.html",RequestContext(request,{'contests':contest_e_page}))		

def contest_problem_list(request):
	if request.method=='GET':
		cid=request.GET.get('cid',None)
		now=datetime.now()
		if cid!=None:
			try:
				contest=Contest.objects.get(id=cid)
				problems=Contest_problem.objects.filter(contest__id=cid).values_list('problem',flat=True).order_by('num')
				username=request.user.username
				problem_list=Problem.objects.filter(problem_id=problems)
				# for item in problems:
				# for item in problem_list:
				# 	print item.title
				# 	print item.problem__id
				# print type(contest.start_time)
				# print contest.end_time
				try:
					user_authority=Privilege.objects.get(user__user__username=username).authority
					if user_authority==config.ADMIN:
						return render_to_response("contest/contest_detail.html",RequestContext(request,{'contest':contest,'problems':problem_list,'now':now}))
					else:
						error="你没有权限查看这次比赛"
               					return render_to_response("error.html",RequestContext(request,{'error':error}))

				except ObjectDoesNotExist:
					if contest.user.user.username==username:
						return render_to_response("contest/contest_detail.html",RequestContext(request,{'contest':contest,'problems':problem_list,'now':now}))
					if contest.user.user.username!=username:
						if contest.private==1:
							if contest.visible==False:
								error="你没有权限查看这次比赛"
			               				return render_to_response("error.html",RequestContext(request,{'error':error}))
			               			if contest.visible==True:
			               				try:
			               					ContestPrivilege.objects.get(user__user__username=username,contest_id=cid)
									return render_to_response("contest/contest_detail.html",RequestContext(request,{'contest':contest,'problems':problem_list,'now':now}))
								except ObjectDoesNotExist:
									error="你没有被邀请这次比赛"
			               					return render_to_response("error.html",RequestContext(request,{'error':error}))
 						if contest.private!=1:
 							# print 'test'
 							if contest.visible==False:
 								rror="你没有权限查看这次比赛"
			               				return render_to_response("error.html",RequestContext(request,{'error':error}))
			               			if contest.visible==True:
								return render_to_response("contest/contest_detail.html",RequestContext(request,{'contest':contest,'problems':problem_list,'now':now}))

			except ObjectDoesNotExist:
				error="比赛不存在"
				return render_to_response("error.html",RequestContext(request,{'error':error}))


# def contest_rank(request):
# 	if request.method=='GET':
# 		cid=request.GET.get('cid',None)
# 		try:
# 			contest=Contest.objects.get(id=cid)
# 		except ObjectDoesNotExist:
# 			error="比赛不存在"
# 			return render_to_response("error.html",RequestContext(request,{'error':error}))
# 		contest_user_id_list=Solution.objects.filter(contest_id=cid).order_by('user__user__id').values_list('user__user__id',flat=True).distinct()
# 		#contest_user_list 是一个只包含参加这次比赛的用户id的list
# 		contest_user_list=UserOJ.objects.filter(user__id__in=contest_user_id_list)
# 		# 经过这一步过滤 contest_user_list 是参加这次比赛的用户的UserOJ对象
# 		contest_problem_list=Contest_problem.objects.filter(contest_id=cid)
# 		solutions=Solution.objects.filter(contest_id=cid)

# 		contest_time=contest.start_time
# 		contest_info=[]
# 		for contest_user in contest_user_list:
# 			accepted=0
# 			user_problem=[]
# 			total_time=datetime.timedelta()
# 			for problem in contest_problem_list:
# 				# 对每道题目提交的记录进行筛选
# 				all_solution=solutions.filter(problem__id=problem.problem.problem_id,user__user__id=contest_user.user.id)
# 				ac_solution=solutions.filter(result=5).order_by('id')

# 				unsolved_num=all_solution.exclude(result=5).count()
# 					# unsolved是提交代码错误的次数
# 				if  ac_solution:
# 					ac_time=ac_solution[0].in_date-contest_time
# 					# 如果记录中存在用户的提交通过的情况,取第一个成功的计时
# 					wise_time=datetime.timedelta(minutes=unsolved*20)
# 					user_problem.append({
# 						'submit':1,
# 						'ac_time':ac_time,
# 						'unsolved':unsolved,
# 						})
# 					total_time=total_time+ac_time+wise_time
# 					accepted+=1
# 				else:
# 					user_problem.append({
# 						'submit':0,
# 						'unsolved':unsolved_num
# 						})
# 		 	contest_loop = []
# 		      	contest_loop.append(contest_user.user.username)
# 			contest_loop.append(accepted)
# 		        	contest_loop.append(total_time)
# 		        	contest_loop.append(user_problem)

# 		        	contest_info.append(contest_loop)
# 		contest_info.sort(key=lambda t: (-t[1], t[2]))
# 		return render_to_response('contest/contest_rank.html',RequestContext(request,{'user_list':contest_info}))