import streamlit as st

st.markdown("# 앱UI만들기")
name = st.text_input("이름", placeholder="example_user")
grade = st.radio("학년", [1,2,3], horizontal=True)
clas = st.number_input("반")
level =st.selct_slider("난이도, [쉬움, 보통, 어려움]")
score = st.select_slider("점수", [0, 50, 100])
소감 =st.text_area("소감")
