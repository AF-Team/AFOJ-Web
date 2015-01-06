from django.shortcuts import render
from django.shortcuts import render_to_response,RequestContext
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# Create your views here.
def index(request):
	return render_to_response("index.html",RequestContext(request));