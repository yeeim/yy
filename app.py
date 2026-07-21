import streamlit as st
from openai import OpenAI



try:
    ai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception:
    ai_client = None


if 'soul_routine' not in st.session_state:
    st.session_state.soul_routine = []  # 마음 습관 저장소
if 'inner_mantra' not in st.session_state:
    st.session_state.inner_mantra = "나는 오늘도 나를 사랑하기로 했다." # 긍정 확언
if 'is_mantra_saved' not in st.session_state:
    st.session_state.is_mantra_saved = False # 저장 알림 트리거


def add_mindful_habit():
    """사용자가 입력한 루틴을 리스트에 추가"""
    habit = st.session_state.habit_input
    if habit:
        st.session_state.soul_routine.append({"content": habit, "is_done": False})
        st.toast("정서적 에너지가 한 줄 채워졌습니다! 🌿")
        st.session_state.habit_input = ""

@st.dialog("내면의 주문 재설정")
def edit_inner_mantra():
    """나를 지켜줄 문장을 수정하는 모달창"""
    new_phrase = st.text_area("당신의 영혼을 깨우는 한 줄을 적어보세요.", 
                             value=st.session_state.inner_mantra)
    if st.button("문장 각인하기"):
        st.session_state.inner_mantra = new_phrase
        st.session_state.is_mantra_saved = True
        st.rerun()


def page_mantra_view():
    st.header("✨ 오늘의 내면 주문")
    
    with st.container(border=True):
        st.markdown(f"### \"{st.session_state.inner_mantra}\"")
        if st.button("🖊️ 문장 다시 쓰기"):
            edit_inner_mantra()

    if st.session_state.is_mantra_saved:
        st.success("새로운 주문이 가슴 속에 새겨졌습니다!")
        st.session_state.is_mantra_saved = False
    
    st.divider()
    st.write("💡 **심리학적 효과**: 긍정 확언은 부정적인 편향을 줄이고 자존감을 회복하는 데 큰 도움을 줍니다.")

def page_routine_view():
    st.header("🌿 마음 돌봄 루틴")
    st.write(f"현재 주문: **{st.session_state.inner_mantra}**")
    
    new_habit = st.text_input("나를 돌보는 작은 행동 (예: 창밖 3분 보기, 따뜻한 차 마시기)", key="habit_input")
    if st.button("루틴 등록", on_click=add_mindful_habit):
        if not new_habit:
            st.warning("내용을 입력하고 버튼을 눌러주세요.")

    st.markdown("---")
    for idx, item in enumerate(st.session_state.soul_routine):
        c1, c2, c3 = st.columns([0.1, 0.7, 0.2])
        status_icon = "🌳" if item["is_done"] else "🌱"
        c1.write(status_icon)
        c2.write(item["content"])
        if not item["is_done"]:
            if c3.button("실천", key=f"done_{idx}"):
                item["is_done"] = True
                st.rerun()


def page_growth_view():
    st.header("📈 마음 성장 리포트")
    
    if not st.session_state.soul_routine:
        st.info("아직 등록된 루틴이 없습니다. 마음 돌봄 메뉴에서 루틴을 시작해보세요!")
    else:
        total = len(st.session_state.soul_routine)
        completed = sum(1 for x in st.session_state.soul_routine if x["is_done"])
        progress_rate = (completed / total) * 100
        
        st.metric("오늘의 마음 에너지", f"{progress_rate:.1f}%")
        st.progress(progress_rate / 100, text=f"에너지 충전도: {progress_rate:.1f}%")
        
        if progress_rate == 100:
            st.balloons()
            st.success("당신은 오늘 자신을 정말 소중히 대했습니다. 완벽한 하루예요! 🏆")
            
        if st.button("하루 기록 마감 (초기화)"):
            st.session_state.soul_routine = []
            st.rerun()


def page_counseling_view():
    st.header("💬 AI 마음 상담실")
    st.write("누구에게도 말하지 못했던 속마음을 편하게 털어놓으세요.")
    
    user_msg = st.text_input("상담하고 싶은 내용을 입력하세요", placeholder="요즘 학업 때문에 너무 지쳐요.")
    
    if st.button("상담 보내기"):
        if not user_msg:
            st.warning("이야기를 먼저 들려주세요.")
        elif ai_client is None:
            st.error("API 키 설정이 필요합니다.")
        else:
            with st.spinner("당신의 마음을 깊이 이해하는 중..."):
                try:
                    response = ai_client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "너는 '영혼의 정원' 앱의 전문 심리 상담사야. 사용자의 말에 깊이 공감해주고, 위로와 격려가 되는 따뜻한 답변을 해줘. 답변은 너무 길지 않게 핵심적인 위로를 전달해줘."},
                            {"role": "user", "content": user_msg}
                        ]
                    )
                    st.chat_message("assistant").write(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"연결 오류가 발생했습니다: {e}")


pg = st.navigation([
    st.Page(page_mantra_view, title="내면의 주문", icon="✨"),
    st.Page(page_routine_view, title="마음 루틴", icon="🌿"),
    st.Page(page_growth_view, title="성장 리포트", icon="📈"),
    st.Page(page_counseling_view, title="AI 심리 상담", icon="💬")
], position="top")

st.sidebar.title("🌿 영혼의 정원")
st.sidebar.write("당신의 마음을 돌보는 따뜻한 공간")
st.sidebar.markdown("---")
st.sidebar.caption("Ver 1.2 | Developed by [사용자이름]")

pg.run()
