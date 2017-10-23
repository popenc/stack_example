from django.shortcuts import render
from django.template.loader import render_to_string
# Create your views here.
from django.http import HttpResponse


def test_page(request):
	return render(request, "ws_test_page.html")