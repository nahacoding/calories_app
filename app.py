import streamlit as st
import pickle
import numpy as np
import pandas as pd

# 1. 페이지 설정 및 제목 수정
st.set_page_config(page_title="AI 하루", layout="centered") 
st.title("🏃‍♂️ AI 하루(오늘의 활동량은?)")
st.write("오렌지3 인공지능 모델을 활용하여 오늘 당신의 활동 점수를 분석합니다.")

# 모델 파일 불러오기
try:
    with open('Calories_model.pkcls', 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    st.error("모델 파일('Calories_model.pkcls')을 찾을 수 없습니다. 파일명을 확인해 주세요.")
    st.stop()

# 2. 사용자 입력 섹션 (메인 화면)
st.divider()
st.subheader("📊 오늘의 활동량 입력")

col1, col2 = st.columns(2)

with col1:
    steps = st.number_input("총 걸음 수 (TotalSteps)", min_value=0, value=5000)
    very_active = st.number_input("고강도 활동 시간 (분)", min_value=0, value=20)
    fairly_active = st.number_input("중강도 활동 시간 (분)", min_value=0, value=30)

with col2:
    lightly_active = st.number_input("저강도 활동 시간 (분)", min_value=0, value=150)
    sedentary = st.number_input("앉아 있는 시간 (분)", min_value=0, value=600)

# 3. 인공지능 예측 및 결과 출력
st.write("") 
if st.button("🔥 AI 분석 결과 보기", use_container_width=True):
    # 입력 데이터를 모델 형식에 맞게 변환
    input_data = np.array([[steps, very_active, fairly_active, lightly_active, sedentary]]) 
    prediction = model.predict(input_data)
    
    st.divider()
    
    # --- 칼로리 값 빨간색 적용 부분 ---
    st.markdown(
        f"### ✅ 예측 소모 칼로리: <span style='color: #FF4B4B;'>{prediction[0]:.1f} kcal</span>", 
        unsafe_allow_html=True
    )
    # ------------------------------

    # 분석 코멘트
    if prediction[0] > 2500:
        st.success("대단해요! 오늘은 정말 활기찬 하루를 보내셨군요.")
    elif prediction[0] > 1800:
        st.info("평균적인 활동량입니다. 건강을 잘 유지하고 계시네요!")
    else:
        st.warning("오늘은 조금 더 움직여보는 건 어떨까요? 가벼운 산책을 추천합니다.")

    # 4. 하단 그래프 시각화
    st.write("")
    st.subheader("⏱ 활동 시간 비중 분석")
    
    chart_data = pd.DataFrame({
        "활동 유형": ["고강도", "중강도", "저강도", "좌식(비활동)"],
        "시간(분)": [very_active, fairly_active, lightly_active, sedentary]
    })
    
    st.bar_chart(data=chart_data, x="활동 유형", y="시간(분)", color="#ff4b4b")
    
    # 5. 주의 문구 추가
    st.divider()
    st.caption("⚠️ **주의사항**: 본 서비스의 분석 결과는 입력된 데이터를 기반으로 한 AI 예측치이며, 사용자의 기초대사량, 체질, 건강 상태에 따라 실제 소모량과 차이가 있을 수 있습니다. 참고용으로만 활용해 주세요.")
