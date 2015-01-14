from django.shortcuts import render
from django.shortcuts import render_to_response,RequestContext

# Create your views here.
def index(request):
	return render_to_response("dashboard/dashboard.html",RequestContext(request,))