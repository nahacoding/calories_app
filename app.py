import streamlit as st
import pickle
import numpy as np

# 앱 제목과 설명
st.set_page_config(page_title="AI 칼로리 예측기", layout="centered") # 화면 설정
st.title("🏃‍♂️ AI 활동량 기반 칼로리 예측기")
st.write("오렌지3 인공지능 모델을 활용하여 오늘 당신의 활동 점수를 분석합니다.")

# 1. 모델 파일 불러오기
try:
    with open('Calories_model.pkcls', 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    st.error("모델 파일('Calories_model.pkcls')을 찾을 수 없습니다. 파일명을 확인해 주세요.")
    st.stop() # 모델이 없으면 실행 중단

# 2. 사용자 입력 섹션 (메인 화면 배치)
st.divider()
st.subheader("📊 오늘의 활동량 입력")

# 입력을 깔끔하게 배치하기 위해 2개의 컬럼으로 나눔
col1, col2 = st.columns(2)

with col1:
    steps = st.number_input("총 걸음 수 (TotalSteps)", min_value=0, value=5000)
    very_active = st.number_input("고강도 활동 시간 (VeryActiveMinutes)", min_value=0, value=20)
    fairly_active = st.number_input("중강도 활동 시간 (FairlyActiveMinutes)", min_value=0, value=30)

with col2:
    lightly_active = st.number_input("저강도 활동 시간", min_value=0, value=150)
    sedentary = st.number_input("앉아 있는 시간 (SedentaryMinutes)", min_value=0, value=600)

# 3. 인공지능 예측 및 결과 출력
st.write("") # 간격 조절
if st.button("🔥 AI 분석 결과 보기", use_container_width=True): # 버튼을 가로로 길게
    # 입력 데이터를 모델 형식에 맞게 변환
    input_data = np.array([[steps, very_active, fairly_active, lightly_active, sedentary]]) 
    prediction = model.predict(input_data)
    
    st.divider()
    st.markdown(f"### 예측 소모 칼로리: <span style='color: #ff4b4b;'>{prediction[0]:.1f} kcal</span>", unsafe_allow_html=True)
    
    # 분석 코멘트
    if prediction[0] > 2500:
        st.success("대단해요! 오늘은 정말 활기찬 하루를 보내셨군요.")
    elif prediction[0] > 1800:
        st.info("평균적인 활동량입니다. 건강을 잘 유지하고 계시네요!")
    else:
        st.warning("오늘은 조금 더 움직여보는 건 어떨까요? 가벼운 산책을 추천합니다.")
