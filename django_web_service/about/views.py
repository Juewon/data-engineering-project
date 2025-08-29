from django.shortcuts import render
import numpy as np
import pandas as pd
from deep_app.modules.data_anal import image_classify
from django.core.files.storage import FileSystemStorage
import os
import base64
from collections import OrderedDict
from .fusioncharts import FusionCharts
from django.views.generic import View

from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

def outline(request):
    return render(request, 'about/outline.html')

