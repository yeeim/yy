import streamlit as st
from openai import OpenAI

# [1] 시스템 설정 및 보안 인증
# 보안을 위해 API 키는 Secrets에서 관리하며, OpenAI 클라이언트를 초기화합니다.
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# [2] 애플리케이션 데이터 스토리지 (기존 코드와 차별화된 변수명 설계)
# 단순 리스트가 아닌 '사용자 상태 객체'를 정의하여 관리하는 방식을 채택함.
if 'mind_logs' not in st.session_state:
    st.session_state.mind_logs = []  # 마음 습관 기록 (기존 todo_list)
if 'affirmation_phrase' not in st.session_state:
    st.session_state.affirmation_phrase = "나는 내 속도대로 성장하고 있다." # 긍정 문구
if 'update_success_trigger' not in st.session_state:
    st.session_state.update_success_trigger = False # 알림 트리거

# [3] 핵심 비즈니스 로직 함수
def commit_wellness_habit():
    """사용자가 입력한 습관을 데이터 저장소에 기록하는 함수"""
    entry = st.session_state.habit_input_field
    if entry:
        # 데이터 구조화: [내용, 완료여부, 기록시간] 형태로 확장 가능
        st.session_state.mind_logs.append({"task": entry, "done": False})
        st.toast("정서적 자산이 한 줄 추가되었습니다. 🌱")
        st.session_state.habit_input_field = ""

@st.dialog("내면의 문장 재설정")
def show_affirmation_editor():
    """모달 다이얼로그를 통한 데이터 업데이트 로직"""
    new_text = st.text_area("오늘 하루 나를 지켜줄 문장을 작성하세요.", 
                           placeholder=st.session_state.affirmation_phrase)
    if st.button("문장 각인하기"):
        st.session_state.affirmation_phrase = new_text
        st.session_state.update_success_trigger = True
        st.rerun()

# [4] 개별 인터페이스(View) 설계

def view_daily_affirmation():
    """첫 번째 화면: 긍정 확언 및 정서적 지지"""
    st.subheader("📋 오늘의 마인드셋")
    
    # 카드 형태의 UI 구현
    with st.container(border=True):
        st.markdown(f"### \"{st.session_state.affirmation_phrase}\"")
