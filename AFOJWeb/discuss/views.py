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
def index(requset):
	return render_to_response("games.html",RequestContext(requset,))