from django.test import TestCase

# Create your tests here.
from problemlist.models import *

class problemTestCase(TestCase):
	def SetUp(self):
		Problem.objects.crete(problem_id=10021,description="fdafkfadjsklfajs")