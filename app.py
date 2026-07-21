import streamlit as st
from openai import OpenAI


try:
    ai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception:
    ai_client = None


if 'daily_journal' not in st.session_state:
    st.session_state.daily_journal = ""  

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
        st.toast("고민이 추가되었습니다. 💭")
        st.session_state.worry_input = ""

def add_habit():
    """습관 추가 함수"""
    habit = st.session_state.habit_input
    if habit:
        st.session_state.self_care_habits.append([habit, False])
        st.toast("나를 위한 습관이 등록되었습니다! 🌿")
        st.session_state.habit_input = ""

@st.dialog("개선 점 수정")
def edit_improvement_goal():
    """개선 점 수정 팝업"""
    new_goal = st.text_area("스스로 개선하고 싶은 점을 적어주세요.", 
                            value=st.session_state.improvement_goal)
    if st.button("저장하기"):
        st.session_state.improvement_goal = new_goal
        st.session_state.goal_updated = True
        st.rerun()


def page_journal():
    st.header("📝 1. 오늘의 일기")
    st.write("오늘 하루 동안 있었던 일이나 느꼈던 감정을 간단히 자유롭게 적어보세요.")
    
    journal_text = st.text_area("오늘의 일기 쓰기", 
                                value=st.session_state.daily_journal, 
                                height=150, 
                                placeholder="오늘 있었던 일이나 생각들을 편하게 적어보세요...")
    
    if st.button("일기 저장"):
        st.session_state.daily_journal = journal_text
        st.success("오늘의 일기가 저장되었습니다! 📖")


def page_worries():
    st.header("💭 2. 요즘 나의 고민")
    st.write("마음속에 담아둔 고민들을 여러 개 등록해 보세요.")
    
    new_worry = st.text_input("고민 입력", key="worry_input")
    if st.button("고민 추가", on_click=add_worry):
        if not new_worry:
            st.warning("고민 내용을 입력해 주세요!")
            
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
    st.header("🎯 3. 내가 개선하고 싶은 점")
    st.info(f"현재 나의 개선 목표:\n\n**\"{st.session_state.improvement_goal}\"**")
    
    if st.button("목표 수정하기"):
        edit_improvement_goal()
        
    if st.session_state.goal_updated:
        st.success("새로운 개선 목표가 저장되었습니다!")
        st.session_state.goal_updated = False
        
    st.markdown("---")
    st.caption("💡 스스로 변화하고 싶은 목표를 정하면 심리적 성장에 도움을 줍니다.")


def page_habits():
    st.header("🌿 4. 나를 돌보는 습관")
    st.write("나를 위해 실천할 습관들을 등록하고 달성해 보세요.")
    
    new_habit = st.text_input("습관 입력 (예: 10분 산책, 따뜻한 물 마시기)", key="habit_input")
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
    st.header("🤖 5. AI 심리 상담실")
    st.write("작성하신 **일기, 고민, 개선 점, 돌봄 습관** 정보를 종합하여 맞춤 상담을 제공합니다.")
    
    # 세션에 기록된 1~4번 데이터 취합
    journal_text = st.session_state.daily_journal if st.session_state.daily_journal else "작성된 일기 없음"
    worry_text = ", ".join(st.session_state.worry_list) if st.session_state.worry_list else "등록된 고민 없음"
    habit_text = ", ".join([h[0] for h in st.session_state.self_care_habits]) if st.session_state.self_care_habits else "등록된 습관 없음"
    
    st.markdown(f"""
    > **기록 요약**
    > * **오늘의 일기:** {journal_text}
    > * **요즘 고민:** {worry_text}
    > * **개선하고 싶은 점:** {st.session_state.improvement_goal}
    > * **나를 돌보는 습관:** {habit_text}
    """)
    
    user_prompt = st.text_input("AI 상담사에게 물어보고 싶은 내용을 적어주세요")
    
    if st.button("상담 받기"):
        if ai_client is None:
            st.error("OpenAI API 키가 바르게 설정되지 않았습니다.")
        else:
            with st.spinner("작성하신 기록들을 다정하게 살펴보고 상담을 구성 중..."):
                try:
                    system_content = f"""
                    너는 따뜻하고 공감 능력이 뛰어난 심리 상담사야. 
                    사용자가 입력한 아래 일기와 고민, 목표, 습관 데이터를 참고하여 깊이 공감하고 조언해 줘.
                    
                    [사용자 데이터]
                    - 오늘의 일기: {journal_text}
                    - 요즘 고민들: {worry_text}
                    - 개선 점: {st.session_state.improvement_goal}
                    - 나를 돌보는 습관들: {habit_text}
                    
                    조언을 해줄 때는 사용자의 마음을 충분히 위로해 주고, 긍정적인 방향을 제시해 줘.
                    """
                    
                    response = ai_client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": system_content},
                            {"role": "user", "content": user_prompt if user_prompt else "제 기록들을 바탕으로 상담과 조언 부탁드립니다."}
                        ]
                    )
                    st.chat_message("assistant").write(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"상담 연결 중 오류가 발생했습니다: {e}")


def page_cheering_message():
    st.header("💌 6. 나를 위한 힘이 되는 한마디")
    st.write("작성하신 일기와 고민, 습관 데이터를 토대로 AI가 오늘 나에게 힘이 되는 따뜻한 메시지를 전해줍니다.")
    
    journal_text = st.session_state.daily_journal if st.session_state.daily_journal else "없음"
    worry_text = ", ".join(st.session_state.worry_list) if st.session_state.worry_list else "없음"
    
    if st.button("응원 메시지 받기"):
        if ai_client is None:
            st.error("OpenAI API 키가 바르게 설정되지 않았습니다.")
        else:
            with st.spinner("당신만을 위한 따뜻한 응원의 한마디를 작성 중..."):
                try:
                    system_content = f"""
                    너는 사용자의 일기({journal_text})와 고민({worry_text})을 알고 있는 따뜻한 멘토야. 
                    사용자가 힘을 얻을 수 있도록 마음을 울리는 짧고 명확하며 따뜻한 격려의 한마디(3~4문장)를 적어줘.
                    """
                    
                    response = ai_client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": system_content},
                            {"role": "user", "content": "지금 나에게 힘이 될 만한 짧고 따뜻한 한마디를 해줘."}
                        ]
                    )
                    
                    message = response.choices[0].message.content
                    st.success("❤️ 당신을 위한 응원 카드")
                    st.markdown(f"### \"{message}\"")
                except Exception as e:
                    st.error(f"메시지 생성 중 오류가 발생했습니다: {e}")


pg = st.navigation([
    st.Page(page_journal, title="오늘의 일기", icon="📝"),
    st.Page(page_worries, title="요즘 나의 고민", icon="💭"),
    st.Page(page_improvement, title="내가 개선하고 싶은 점", icon="🎯"),
    st.Page(page_habits, title="나를 돌보는 습관", icon="🌿"),
    st.Page(page_ai_counselor, title="AI 심리 상담", icon="🤖"),
    st.Page(page_cheering_message, title="힘이 되는 한마디", icon="💌")
], position="top")

st.title("🌱 멘탈 웰니스 & AI 심리케어 플래너")
pg.run()

