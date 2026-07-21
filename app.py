import streamlit as st
from openai import OpenAI


try:
    ai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception:
    ai_client = None


if 'worry_list' not in st.session_state:
    st.session_state.worry_list = []  

if 'improvement_goal' not in st.session_state:
    st.session_state.improvement_goal = "작은 일에 너무 흔들리지 않는 마음 갖기" 

if 'self_care_habits' not in st.session_state:
    st.session_state.self_care_habits = []  

if 'goal_updated' not in st.session_state:
    st.session_state.goal_updated = False


def add_worry():
    """고민 추가 함수"""
    worry = st.session_state.worry_input
    if worry:
        st.session_state.worry_list.append(worry)
        st.toast("고민이 털어놓아졌습니다. 💭")
        st.session_state.worry_input = ""

def add_habit():
    """나를 돌보는 습관 추가 함수"""
    habit = st.session_state.habit_input
    if habit:
        st.session_state.self_care_habits.append([habit, False])
        st.toast("나를 위한 습관이 등록되었습니다! 🌿")
        st.session_state.habit_input = ""

@st.dialog("개선 목표 수정")
def edit_improvement_goal():
    """개선하고 싶은 점 수정 팝업"""
    new_goal = st.text_area("내가 스스로 개선하고 싶은 점을 적어주세요.", 
                            value=st.session_state.improvement_goal)
    if st.button("목표 저장"):
        st.session_state.improvement_goal = new_goal
        st.session_state.goal_updated = True
        st.rerun()


def page_worries():
    st.header("💭 1. 요즘 나의 고민")
    st.write("마음속에 담아둔 고민들을 자유롭게 적어보세요.")
    
    new_worry = st.text_input("새로운 고민을 적어주세요", key="worry_input")
    if st.button("고민 등록", on_click=add_worry):
        if not new_worry:
            st.warning("고민 내용을 입력하고 버튼을 눌러주세요!")
            
    st.markdown("---")
    if not st.session_state.worry_list:
        st.info("아직 등록된 고민이 없습니다.")
    else:
        for idx, worry_item in enumerate(st.session_state.worry_list):
            c1, c2 = st.columns([5, 1])
            c1.write(f"• {worry_item}")
            if c2.button("삭제", key=f"del_worry_{idx}"):
                st.session_state.worry_list.pop(idx)
                st.rerun()


def page_improvement():
    st.header("🎯 2. 내가 개선하고 싶은 점")
    st.info(f"현재 나의 개선 목표:\n\n**\"{st.session_state.improvement_goal}\"**")
    
    if st.button("목표 수정하기"):
        edit_improvement_goal()
        
    if st.session_state.goal_updated:
        st.success("새로운 개선 목표가 반영되었습니다!")
        st.session_state.goal_updated = False
        
    st.markdown("---")
    st.caption("💡 스스로 변화하고 싶은 목표를 명확히 정의하면 성장의 계기가 됩니다.")
def page_habits():
    st.header("🌿 3. 나를 돌보는 습관")
    st.write("지친 나를 위해 실천할 작은 습관들을 등록하고 달성해 보세요.")
    
    new_habit = st.text_input("나를 돌보는 습관 (예: 10분 산책, 따뜻한 물 마시기)", key="habit_input")
    if st.button("습관 추가", on_click=add_habit):
        if not new_habit:
            st.warning("습관을 입력하고 버튼을 눌러주세요!")
            
    st.markdown("---")
    if not st.session_state.self_care_habits:
        st.info("등록된 습관이 없습니다.")
    else:
        for idx in range(len(st.session_state.self_care_habits)):
            col_task, col_btn, col_status = st.columns([4, 1, 1])
            with col_task:
                st.write(f"{idx+1}. {st.session_state.self_care_habits[idx][0]}")
            with col_btn:
                if st.button("실천", key=f"btn_habit_{idx}"):
                    st.session_state.self_care_habits[idx][1] = True
                    st.rerun()
            with col_status:
                if st.session_state.self_care_habits[idx][1]:
                    st.write("✅ **완료**")


def page_ai_counselor():
    st.header("🤖 4. AI 심리 상담실")
    st.write("앞서 적은 **고민, 개선 목표, 돌봄 습관** 데이터를 토대로 AI가 맞춤 상담을 제공합니다.")
    
    # 세션에 기록된 정보를 요약하여 AI에게 함께 전달
    worry_text = ", ".join(st.session_state.worry_list) if st.session_state.worry_list else "없음"
    habit_text = ", ".join([h[0] for h in st.session_state.self_care_habits]) if st.session_state.self_care_habits else "없음"
    
    st.markdown(f"""
    > **내 기록 요약**
    > * **요즘 고민:** {worry_text}
    > * **개선하고 싶은 점:** {st.session_state.improvement_goal}
    > * **나를 돌보는 습관:** {habit_text}
    """)
    
    user_prompt = st.text_input("AI 상담사에게 추가로 하고 싶은 질문이나 이야기를 적어주세요")
    
    if st.button("상담 받기"):
        if ai_client is None:
            st.error("OpenAI API 키가 바르게 설정되지 않았습니다.")
        else:
            with st.spinner("작성하신 기록들을 바탕으로 따뜻한 조언을 구성 중..."):
                try:
                    # 사용자 데이터가 녹아든 시스템 프롬프트 구성
                    system_content = f"""
                    너는 따뜻하고 공감 능력이 뛰어난 심리 상담사야. 
                    사용자가 작성한 아래 정보를 바탕으로 따뜻한 위로와 구체적인 조언을 해줘.
                    
                    [사용자 정보]
                    - 요즘 고민들: {worry_text}
                    - 개선하고 싶은 점: {st.session_state.improvement_goal}
                    - 나를 돌보는 습관들: {habit_text}
                    
                    지나치게 딱딱한 조언보다는 공감을 먼저 해주고, 사용자의 고민을 완화하고 개선 목표를 달성할 수 있도록 다정하게 격려해줘.
                    """
                    
                    response = ai_client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": system_content},
                            {"role": "user", "content": user_prompt if user_prompt else "제 고민과 목표를 보고 조언 한마디 해주세요."}
                        ]
                    )
                    st.chat_message("assistant").write(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"상담 연결 중 오류가 발생했습니다: {e}")


pg = st.navigation([
    st.Page(page_worries, title="요즘 나의 고민", icon="💭"),
    st.Page(page_improvement, title="개선하고 싶은 점", icon="🎯"),
    st.Page(page_habits, title="나를 돌보는 습관", icon="🌿"),
    st.Page(page_ai_counselor, title="AI 심리 상담", icon="🤖")
], position="top")

st.title("🧠 멘탈 웰니스 & AI 케어 플래너")
pg.run()
