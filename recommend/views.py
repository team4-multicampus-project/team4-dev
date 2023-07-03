from django.shortcuts import render, redirect
from django.http import HttpResponse
from recommend.alco_re import *
from recommend.rec import *
import numpy as np
import pandas as pd 
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from scipy.spatial import distance_matrix
from scipy.spatial.distance import squareform
from sklearn.preprocessing import MinMaxScaler
from string import punctuation
import csv
import re
import json
# Create your views here.

def index(request) :    
    alco_search = request.GET.get("alco", '')
    if alco_search is not None:
        result = recom(alco_search)
        context = {"result" : result}
        return render(request, 'recc/search_rec.html', context)
    else:
        return render(request, 'recc/search_rec.html')


def weather(request):
    user_location = request.GET.get("city")
    print(user_location)
    if user_location is not None:
        sky_description, pty, t1h = get_loc(user_location)
        recommendation, temp_drink, pty_drink = recom_weather(t1h, pty)

        
        context = {
        "city": user_location,
        "weather":[sky_description, pty, t1h],
        "recc":[temp_drink, pty_drink],
        }
        
        return render(request, "recc/weather_rec.html", context)
    else:
        return render(request, "recc/weather_rec.html")




