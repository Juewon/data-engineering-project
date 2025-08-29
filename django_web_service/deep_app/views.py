from django.shortcuts import render
import numpy as np
import pandas as pd
from deep_app.modules.data_anal import image_classify, get_res_map
from django.core.files.storage import FileSystemStorage
from operator import itemgetter
from .models import *
import os
import base64

# Create your views here.

def input_image(request):
    return render(request, 'deep_app/input_image.html')

def result(request):
    return render(request, 'deep_app/result.html')

def file_upload(request) :
    if request.method == "POST" :
        file = request.FILES.get('imgFile') # 클라이언트 전송한 파일 추출하는 코드
        fs = FileSystemStorage() # 파일 저장 객체 생성
        fs.save(file, file) # 전송된 파일을 저장

        # 모든 분석과 관련된 모듈은 deep_app>modules>data_ana.py
        class_name = image_classify(file) # 분류예측 모듈 호출 결과 반환, 이미지 분류 카테고리명을 반환
        img_name = file.name # 클라이언트 전송한 이미지 이름
        print(f"저장한 사진: {img_name}")

        # 음식이름, 정보, 재료, taboo 가져오기
        food_info = FoodInfoWithTaboo.objects.get(food=class_name)
        food = food_info.food
        info = food_info.info
        ingredient = food_info.ingredient
        taboo_ingredient = food_info.taboo_ingredient

        # 추출된 음식의 각 음식점별로 추천수 더하기
        restaurant_info_list = RestaurantInfo.objects.filter(food=food_info)
        rank_review_list = RankReview.objects.filter(res__in=restaurant_info_list)
        
        count_sum_by_res = {}

        for rank_review_instance in rank_review_list:
            res_value = rank_review_instance.res
            cnt_value = rank_review_instance.cnt

            # None이 아닌 경우에만 연산
            if res_value is not None and cnt_value is not None:
                # res_value가 이미 딕셔너리에 있으면 기존 값에 더하기, 없으면 추가
                if res_value in count_sum_by_res:
                    count_sum_by_res[res_value] += cnt_value
                else:
                    count_sum_by_res[res_value] = cnt_value
        
        # 추천수 많은 상위 5개 음식점 추출
        sorted_res_by_count = sorted(count_sum_by_res.items(), key=itemgetter(1), reverse=True)
        top_5_res = sorted_res_by_count[:5]

        # 상위 5개 음식점의 정보 추출
        rank5_info_list = []
        for res_value, count_sum in top_5_res:
            restaurant_info_instance = RestaurantInfo.objects.get(id=res_value.id)
            visitor_review_instance = VisitorReview.objects.get(id=restaurant_info_instance.id)

            rank5_info_list.append({
                'addr' : restaurant_info_instance.addr,
                'store_name' : restaurant_info_instance.store_name,
                'tel' : restaurant_info_instance.tel,
                're_visitor' : visitor_review_instance.re_visitor,
                'x' : restaurant_info_instance.x,
                'y' : restaurant_info_instance.y,
            }
            )

        context = { # 클라이언트 페이지에 전달된 dic(이미지 분류명, 이미지 파일명)
            'class_name' : class_name,
            'img_name' : img_name,
            'food' : food,
            'info' : info,
            'ingredient' : ingredient,
            'taboo_ingredient' : taboo_ingredient,
            'rank5_info_list' : rank5_info_list,
        }
        
    return render(request, 'deep_app/result.html', context)

def food_map_form(request) :

    seoul_res_loc_df = pd.read_csv('about/data/korea_np.csv', encoding = 'UTF-8')
    res_food_list = seoul_res_loc_df['food'].unique()
    res_food_list = sorted(res_food_list)
    return render(request, 'deep_app/food_map_form.html', {'res_food_list' : res_food_list})

def show_res_map(request) :
    if request.method == 'POST' :
        food_name = request.POST['food_name']
        smap = get_res_map(food_name)
    return render(request, 'deep_app/res_map_result.html', {'smap' : smap})