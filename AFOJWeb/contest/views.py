#encoding=utf-8

import re
from django.db import IntegrityError
from django.contrib.auth.models import User
from datetime import *
from django.utils import timezone

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
			flag_one=contest.start_time<=timezone.now()
			flag_two=contest.end_time>timezone.now()
			if (flag_one and flag_two):
				# print "status=1"
				contest.status=1
			if flag_one==False:
				print "status=0"
				contest.status=0
			if flag_two==False:
				print "status=2"
				contest.status=2
			contest.save()
			print contest.id
			# print contest.end_time
			# print timezone.now()
			print contest.start_time<=timezone.now()
			print contest.end_time>timezone.now()


			print '\n'
		# print datetime.now()
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
				problem_list=Contest_problem.objects.select_related().filter(contest__id=cid).order_by('num')
				solutions=Solution.objects.filter(contest_id=cid)
				for problem in problem_list:
					problem.submit=solutions.filter(problem__problem_id=problem.problem.problem_id).count()
					problem.ac=solutions.filter(problem__problem_id=problem.problem.problem_id).filter(result=5).count()
				username=request.user.username
				# problem_list=Problem.objects.filter(problem_id__in=problems)
				# for item in problem_list:
				# 	print item.problem.problem_id
				temp=0
				for item in problem_list:
					item.num=temp
					temp=temp+1
				# 	print item.problem__id
				# print type(contest.start_time)
				# print contest.end_time
				contest_rank_info=contest_rank(cid)

				try:
					user_authority=Privilege.objects.get(user__user__username=username).authority
					# print 'authority'
					if user_authority==config.ADMIN:
						return render_to_response("contest/contest_detail.html",RequestContext(request,{'contest':contest,'problems':problem_list,'now':now,'contest_rank_info':contest_rank_info}))
					else:
						error="你没有权限查看这次比赛"
               					return render_to_response("error.html",RequestContext(request,{'error':error}))

				except ObjectDoesNotExist:
					if contest.user.user.username==username:
						return render_to_response("contest/contest_detail.html",RequestContext(request,{'contest':contest,'problems':problem_list,'now':now,'contest_rank_info':contest_rank_info}))

					if contest.user.user.username!=username:
						if contest.private==1:
							if contest.visible==False:
								error="你没有权限查看这次比赛"
			               				return render_to_response("error.html",RequestContext(request,{'error':error}))
			               			if contest.visible==True:
			               				try:
			               					ContestPrivilege.objects.get(user__user__username=username,contest_id=cid)
									return render_to_response("contest/contest_detail.html",RequestContext(request,{'contest':contest,'problems':problem_list,'now':now,'contest_rank_info':contest_rank_info}))

								except ObjectDoesNotExist:
									error="你没有被邀请这次比赛"
			               					return render_to_response("error.html",RequestContext(request,{'error':error}))
 						if contest.private!=1:
 							# print 'test'
 							if contest.visible==False:
 								print 'fads'
 								error="你没有权限查看这次比赛"
			               				return render_to_response("error.html",RequestContext(request,{'error':error}))
			               			if contest.visible==True:
								return render_to_response("contest/contest_detail.html",RequestContext(request,{'contest':contest,'problems':problem_list,'now':now,'contest_rank_info':contest_rank_info}))


			except ObjectDoesNotExist:
				error="比赛不存在"
				return render_to_response("error.html",RequestContext(request,{'error':error}))


def contest_rank(cid):
		try:
			contest=Contest.objects.get(id=cid)
		except ObjectDoesNotExist:
			error="比赛不存在"
			return render_to_response("error.html",RequestContext(request,{'error':error}))
		contest_user_id_list=Solution.objects.filter(contest_id=cid).order_by('user__user__id').values_list('user__user__id',flat=True).distinct()
		#contest_user_list 是一个只包含参加这次比赛的用户id的list
		contest_user_list=UserOJ.objects.filter(user__id__in=contest_user_id_list)
		# 经过这一步过滤 contest_user_list 是参加这次比赛的用户的UserOJ对象
		contest_problem_list=Contest_problem.objects.filter(contest_id=cid).order_by('num')
		for item in contest_problem_list:
			print item.problem.problem_id
		solutions=Solution.objects.filter(contest_id=cid)

		contest_time=contest.start_time
		contest_info=[]
		for contest_user in contest_user_list:
			accepted=0
			user_problem=[]
			total_time=timedelta()
			for problem in contest_problem_list:
				# 对每道题目提交的记录进行筛选
				all_solution=solutions.filter(problem__problem_id=problem.problem.problem_id,user__user__id=contest_user.user.id)
				ac_solution=all_solution.filter(result=5).order_by('id')

				unsolved_num=all_solution.exclude(result=5).count()
				for item in ac_solution:
					print contest_user.user.username+str(item.id)+' '+str(problem.problem.problem_id)
					# unsolved是提交代码错误的次数
				if  ac_solution:
					ac_time=ac_solution[0].in_date-contest_time
					# 如果记录中存在用户的提交通过的情况,取第一个成功的计时
					wise_time=timedelta(minutes=unsolved_num*20)
					user_problem.append({
						'submit':1,
						'ac_time':ac_time,
						'unsolved':unsolved_num,
						})
					total_time=total_time+ac_time+wise_time
					accepted+=1
				else:
					user_problem.append({
						'submit':0,
						'ac_time':None,
						'unsolved':unsolved_num
						})
		 	contest_loop = []
		      	contest_loop.append(contest_user.user.username)
			contest_loop.append(accepted)
			contest_loop.append(total_time)
			contest_loop.append(user_problem)

			contest_info.append(contest_loop)
		contest_info.sort(key=lambda t: (-t[1], t[2]))
		return contest_info