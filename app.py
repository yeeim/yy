import streamlit as st
from openai import OpenAI

# 1. API 클라이언트 설정 (상단 선언)
ai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 2. 세션 상태 초기화
if 'todo_list' not in st.session_state:
    st.session_state.todo_list = []
if 'user_motto' not in st.session_state:
    st.session_state.user_motto = "오늘도 화이팅!"
if 'motto_updated' not in st.session_state:
    st.session_state.motto_updated = False

# 3. 할 일 추가 함수
def add_todo():
    task = st.session_state.todo_input
    if task:
        st.session_state.todo_list.append([task, False])
        st.toast("할 일이 추가되었습니다!")
        st.session_state.todo_input = ""

# 4. 다짐 수정 팝업 다이얼로그
@st.dialog("오늘의 다짐 수정")
def edit_motto():
    motto = st.text_input("나의 한 줄 좌우명을 적어주세요.")
    if st.button("다짐 저장"):
        st.session_state.user_motto = motto
        st.session_state.motto_updated = True
        st.rerun()

# --- 1페이지: 오늘의 다짐 ---
def page_motto():
    st.header("📣 1. 오늘의 다짐")
    st.info(f"현재 다짐: {st.session_state.user_motto}")
    if st.button("다짐 수정하기"):
        edit_motto()
    if st.session_state.motto_updated:
        st.success("새로운 좌우명이 등록되었습니다!")
        st.session_state.motto_updated = False
    st.markdown("---")

# --- 2페이지: 오늘의 할 일 ---
def page_todo():
    st.header("✅ 2. 오늘의 할 일")
    st.write(f"현재 다짐: **{st.session_state.user_motto}**")
    new_todo = st.text_input("추가할 할 일을 입력하세요", key="todo_input")
    if st.button("추가하기", on_click=add_todo):
        if new_todo == "":
            st.warning("할 일을 입력하고 버튼을 눌러주세요!")
    
    st.markdown("---")
    for i in range(len(st.session_state.todo_list)):
        col_task, col_btn, col_status = st.columns([4, 1, 1])
        with col_task:
            st.write(f"{i+1}. {st.session_state.todo_list[i][0]}")
        with col_btn:
            if st.button("완료", key=f"btn_{i}"):
                st.session_state.todo_list[i][1] = True
                st.rerun()
        with col_status:
            if st.session_state.todo_list[i][1]:
                st.write("✅ **달성!**")
    st.markdown("---")

# --- 3페이지: 나의 갓생 지수 ---
def page_report():
    st.header("📈 3. 나의 갓생 지수")
    if not st.session_state.todo_list:
        st.write("아직 등록된 할 일이 없습니다.")
    else:
        total = len(st.session_state.todo_list)
        count = 0
        for item in st.session_state.todo_list:
            if item[1] == True:
                count += 1
        progress = (count / total) * 100
        st.metric("오늘의 달성률", f"{progress:.1f}%")
        st.progress(progress / 100)
        
        # 들여쓰기(Indentation) 문제 해결 부분
        if progress == 100:
            st.balloons()
            st.success("모든 목표를 달성하셨습니다! 🏆")
            
        if st.button("기록 전체 초기화"):
            st.session_state.todo_list = []
            st.rerun()

# --- 4페이지: AI 코치와 대화하기 ---
def page_ai_coach():
    st.header("🤖 AI 코치와 대화하기")
    prompt = st.text_input("질문을 입력하세요")
    if st.button("보내기
