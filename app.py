import streamlit as st
import pickle
import numpy as np

# 앱 제목과 설명
st.title("🏃‍♂️ AI 활동량 기반 칼로리 예측기")
st.write("오렌지3 인공지능 모델을 활용하여 오늘 당신의 활동 점수를 분석합니다.")

# 1. 모델 파일 불러오기 (파일명은 본인이 저장한 이름으로 수정하세요)
try:
    with open('Calories_model.pkcls', 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    st.error("모델 파일('Calories_model.pkcls')을 찾을 수 없습니다. 파일명을 확인해 주세요.")

# 2. 사용자 입력 섹션
st.sidebar.header("오늘의 활동량 입력")
steps = st.sidebar.number_input("총 걸음 수 (TotalSteps)", min_value=0, value=5000)
very_active = st.sidebar.number_input("고강도 활동 시간 (VeryActiveMinutes)", min_value=0, value=20)
fairly_active = st.sidebar.number_input("중강도 활동 시간 (FairlyActiveMinutes)", min_value=0, value=30)
lightly_active = st.sidebar.number_input("저강도 활동 시간", min_value=0, value=150)
sedentary = st.sidebar.number_input("앉아 있는 시간 (SedentaryMinutes)", min_value=0, value=600)
    
# 3. 인공지능 예측 및 결과 출력
if st.button("AI 분석 결과 보기"):
    # 입력 데이터를 모델 형식에 맞게 변환
    input_data = np.array([[steps, very_active, fairly_active, lightly_active, sedentary]]) 
    prediction = model.predict(input_data)
    
    st.divider()
    st.subheader(f"🔥 AI 예측 소모 칼로리: {prediction[0]:.1f} kcal")
    
    # 분석 코멘트
    if prediction[0] > 2500:
        st.success("대단해요! 오늘은 정말 활기찬 하루를 보내셨군요.")
    elif prediction[0] > 1800:
        st.info("평균적인 활동량입니다. 건강을 잘 유지하고 계시네요!")
    else:
        st.warning("오늘은 조금 더 움직여보는 건 어떨까요? 가벼운 산책을 추천합니다.")
