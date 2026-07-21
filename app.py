import streamlit as st
from openai import OpenAI


try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception:
    client = None


if 'mind_logs' not in st.session_state:
    st.session_state.mind_logs = []  # 습관 목록
if 'affirmation_phrase' not in st.session_state:
    st.session_state.affirmation_phrase = "나는 내 속도대로 성장하고 있다." # 확언
if 'update_success_trigger' not in st.session_state:
    st.session_state.update_success_trigger = False


def commit_wellness_habit():
    """입력된 마음 습관을 저장하는 함수"""
    entry = st.session_state.habit_input_field
    if entry:
        st.session_state.mind_logs.append({"task": entry, "done": False})
        st.toast("정서적 자산이 추가되었습니다! 🌱")
        st.session_state.habit_input_field = ""

@st.dialog("내면의 문장 재설정")
def show_affirmation_editor():
    """모달 팝업으로 확언 문구 수정"""
    new_text = st.text_area("오늘 하루 나를 지켜줄 문장을 작성하세요.", 
                           value=st.session_state.affirmation_phrase)
    if st.button("문장 저장하기"):
        st.session_state.affirmation_phrase = new_text
        st.session_state.update_success_trigger = True
        st.rerun()



def view_daily_affirmation():
    """오늘의 확언 화면"""
    st.subheader("📋 오늘의 마인드셋")
    
    with st.container(border=True):
        st.markdown(f"### \"{st.session_state.affirmation_phrase}\"")
        if st.button("🖊️ 문장 수정"):
            show_affirmation_editor()

    if st.session_state.update_success_trigger:
        st.success("내면의 문장이 성공적으로 업데이트되었습니다.")
        st.session_state.update_success_trigger = False
    
    st.divider()
    st.caption("작은 확언이 모여 단단한 자아를 만듭니다.")

def view_habit_tracker():
    """마음 실천 습관 화면"""
    st.subheader("🌿 웰니스 루틴 관리")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.text_input("추가할 습관 (예: 명상 5분, 산책하기)", key="habit_input_field")
    with col2:
        st.write("##")
        st.button("등록", on_click=commit_wellness_habit, use_container_width=True)

    st.write("---")
    
    for idx, item in enumerate(st.session_state.mind_logs):
        c1, c2, c3 = st.columns([0.1, 0.7, 0.2])
        status = "✅" if item["done"] else "⏳"
        c1.write(status)
        c2.write(item["task"])
        if not item["done"]:
            if c3.button("달성", key=f"complete_{idx}"):
                item["done"] = True
                st.rerun()

def view_analytics_report():
    """성장 리포트 화면"""
    st.subheader("📈 정서 성장 리포트")
    
    if not st.session_state.mind_logs:
        st.info("기록된 데이터가 아직 없습니다. 웰니스 루틴에서 습관을 등록해 보세요!")
    else:
        total = len(st.session_state.mind_logs)
        completed = sum(1 for x in st.session_state.mind_logs if x["done"])
        ratio = completed / total if total > 0 else 0
        
        m1, m2 = st.columns(2)
        m1.metric("총 실천 시도", f"{total}회")
        m2.metric("달성한 루틴", f"{completed}회", delta=f"{ratio*100:.1f}%")
        
        st.progress(ratio, text=f"마음 성장
