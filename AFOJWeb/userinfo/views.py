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

# Create your views here.

from account.models import *
from problemlist.models import *
from status.models import *


def userinfo(request,username):
	if request.method=="GET":
		try:
			u=UserOJ.objects.get(user__username=username)
		except ObjectDoesNotExist:
			error="用户不存在"
			return render_to_response("error.html",RequestContext(request,{"error":error}))

		status_list=Solution.objects.filter(user__user__username=username)
		ac_problem_list=status_list.filter(result=5).order_by('problem_id').values_list('problem_id')
		unsolved_list=status_list.exclude(result=5).order_by('problem_id').values_list('problem_id')
		unsolved_list_count=unsolved_list.count()
		unsolved_list=list(set(unsolved_list)-set(ac_problem_list))
		unsolved_list.sort(key=lambda pid:pid[0])


		# for unsolved in unsolved_list:
		# 	for ac in ac_problem_list:
		# 		if ac[0]!=unsolved[0]:
		# 			temp_unsolved_list.append(unsolved[0])
		print ac_problem_list
		print unsolved_list
		return render_to_response("userinfo/userinfo.html",RequestContext(request,{'ac_problem_list':ac_problem_list,'unsolved_list':unsolved_list,'userinfo':u,'unsolved_list_count':unsolved_list_count}))