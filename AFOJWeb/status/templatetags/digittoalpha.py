from django.template import Node
from django.template import TemplateSyntaxError, Library
from AFOJWeb.config import VERDICT_NAME,LANGUAGE,CONTEST_ALPHA
register = Library()
@register.filter
def digittoalpha(value):
	return CONTEST_ALPHA[value][1]


# register.filter('digittoname',digittoname)
