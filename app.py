import streamlit as st

st.markdown("# 앱UI만들기")
이름=st.text_input("이름", placeholder="example_user")
학년= st.number_input("학년", [1,2,3], horizontal=True)
반= st.number_input("반")
난이도=st.selct_slider("난이도, [쉬움, 보통, 어려움]")
점수=st.select_slider("점수", [0, 50, 100])
소감=st.text_area("소감")
