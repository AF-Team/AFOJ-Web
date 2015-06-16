from django.template import Node
from django.template import TemplateSyntaxError, Library
from AFOJWeb.config import VERDICT_NAME,LANGUAGE
register = Library()
@register.filter
def digittoname(value):
	if value==-1:
		return u"BUG"
	return VERDICT_NAME[value][2]
	
@register.filter
def digittolanguage(value):
	if value==-1:
		return u"BUG"
	return LANGUAGE[value][1]

# register.filter('digittoname',digittoname)
