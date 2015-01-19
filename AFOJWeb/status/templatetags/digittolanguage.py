from django.template import Node
from django.template import TemplateSyntaxError, Library
from AFOJWeb.config import VERDICT_NAME,LANGUAGE
register = Library()


@register.filter
def digittolanguage(value):
	return LANGUAGE[value][1]

# register.filter('digittoname',digittoname)
