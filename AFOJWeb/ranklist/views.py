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


from account.models import *
from problemlist.models import *
from status.models import *
# Create your views here.
def index(request):
	if request.method=='GET':
		status_list=Solution.objects.all()
		user_list=UserOJ.objects.all()
		problem_list=Problem.objects.all()

		# status_list.filter(result=5).distinct()
		problem_ac_item=status_list.filter(result=5)
		for x in problem_ac_item:
			print x.problem_id
		print '------------------------'
		for user_item in user_list:
			# print user_item.user.username
			user_status_item=status_list.filter(user=user_item).filter(result=5).distinct()
			for x in user_status_item:
				print x.problem_id
			print '****************'
			submit=status_list.filter(user=user_item).count()
			solved=user_status_item.count()
			user_item.solved=solved
			user_item.submit=submit



			# user_item.update(solved=solved,submit=submit)
			temp=0
			for item in user_status_item:
				try:
					score=Score.objects.get(problem_id=item.problem_id).score
				except ObjectDoesNotExist:
					score=0
				temp+=score
			user_item.scoreOne=temp
			user_item.save()

			user_list_pages=Paginator(user_list.order_by('-scoreOne'),20)
			page=request.GET.get('page')
			try:
				user_lists=user_list_pages.page(page)
			except PageNotAnInteger:
				user_lists=user_list_pages.page(1)
			except EmptyPage:
				user_lists=user_list_pages.page(user_list_pages.num_pages)
		# user_list.order_by('submit')
		return render_to_response("ranklist/rank_list.html",RequestContext(request,{'user_list':user_lists}))