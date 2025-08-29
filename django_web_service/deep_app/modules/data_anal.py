# 데이터분석(시각화, 모델 예측 등) 관련 프로그램을 함수화
from django.conf import settings
import pandas as pd
import joblib
from PIL import Image
import numpy as np
from keras.models import load_model
import folium
import json
import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""

def get_res_map(food_name): # 호출시 전달된 서울시 자치구에 대한 지도 시각화 하는 함수
    seoul_res_loc_df = pd.read_csv('about/data/korea_np.csv', encoding='UTF-8') # 자치구별 공원 현황 및 위경도 데이터 읽어오기
    food_res_loc_df = seoul_res_loc_df[seoul_res_loc_df['food'] == food_name] # 파라미터로 전달된 자치구 데이터만 추출
    smap = folium.Map(location=[37.5502, 126.982], zoom_start=11) # 기준 지도 생성

    for i in food_res_loc_df.index: ## 반복문 이용해서 자치구 공원의 위경도 위치에 마커 추가   
        folium.Marker([food_res_loc_df['위도'][i], 
                    food_res_loc_df['경도'][i]],
                    popup = food_res_loc_df['store_name'][i],
                    tooltip = food_res_loc_df['store_name'][i]).add_to(smap)

    return smap._repr_html_() # html코드를 추출 후 반환, folium 객체가 아닌 html 코드가 반환됨

# 한 개의 이미지에 대해 분류 예측 후 분류 카테고리를 반환하는 함수
def image_classify(file):
    file_path = settings.BASE_DIR / 'deep_app' / 'modules' 
    loaded_model = load_model(file_path / 'inceptionv3_model_final.h5')  # 사용모델 로딩, 모델이 저장되어 있는 경로에 한글이 있으면 에러발생 

    # 이미지 전처리
    imgs = []

    image_size = 299  # 학습할때 사용한 이미지 사이즈와 동일하게
    img = Image.open(file)  # 이미지 정보 추출
    print(f"Image opened successfully: {img.size}, Mode: {img.mode}")
    img = img.convert("RGB")  # RGB로 색상값 배치 수정
    img = img.resize((image_size, image_size))  # 이미지 사이즈 학습이미지와 동일하게 수정
    data = np.asarray(img) # array 로 변환
    data = data.astype('float32') / 255  # 픽셀 표준화
    imgs.append(data)  # 이미지 데이터 차원으로 변경 : 학습 차원과 동일한 형태로 구성
    imgs = np.array(imgs)  # 리스트를 array로 변환

    pred_prob = loaded_model.predict(imgs)
    # predict_value = np.argmax(pred_prob[0])
    predict_value = pred_prob.argmax()  # 확률이 가장 높은 인덱스 추출
    categories = ['간장게장', '갈비찜', '갈비탕', '감자전', '감자탕', '곱창구이', '김밥', '김치전', '김치찌개',\
                '닭갈비', '닭볶음탕', '도토리묵', '된장찌개', '떡볶이', '막국수', '물냉면', '물회', '미역국',\
                '배추김치', '불고기', '비빔냉면', '비빔밥', '삼겹살', '삼계탕', '설렁탕', '순대', '순두부찌개',\
                '양념게장', '양념치킨', '육회', '잡채', '제육볶음', '족발', '주꾸미볶음', '짜장면', '칼국수',\
                '파전', '해물찜', '황태구이', '후라이드치킨']    

    return categories[predict_value]  # 카테고리 내의 추출된 인덱스에 맞는 결과값 추출