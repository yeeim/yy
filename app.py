import streamlit as st

with st.sidebar:
    st.header("프로필")
    user_name = st.text-input("닉네임")
   weater = st. selectbox("오늘 날씨", ["맑음", "흐림", '비/눈", "메우 추움"])
    st.markdoowm("---")
    st.info(f"반가워요, {user_name}님! 오늘날씨는 '{weater}'dlspdy.")

                                    st.title("AI코디메이커")
                                    st.write("사이드바에서 날씨를 먼저선택하고 코디를 시작하세요!")   
