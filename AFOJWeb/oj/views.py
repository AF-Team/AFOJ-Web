#encoding=utf-8
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from oj.models import	*
# Create your views here.
def index(request):
	return render_to_response("index.html",RequestContext(request));
def news_list_show(request):
	newitems=News.objects.order_by('-time')
	print newitems
	news_pages=Paginator(newitems,20)
	page=request.GET.get('page')
	try:
		items=news_pages.page(page)
	except PageNotAnInteger:
		items=news_pages.page(1)
	except EmptyPage:
		items=news_pages.page(news_pages.num_pages)
	return render_to_response("oj/news/news_list.html",RequestContext(request,{"newses":items}))

def news_show(request,nid):
	try:
		newsitem=News.objects.get(id=nid)
	except ObjectDoesNotExist:
		error=u"新闻不存在"
		return render_to_response("error.html",RequestContext(request,{'error':error}))
	return render_to_response("oj/news/news.html",RequestContext(request,{"news":newsitem}))
