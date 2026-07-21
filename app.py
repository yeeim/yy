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

if 'praise_list' not in st.session_state:
    st.session_state.praise_list = []  

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

def add_praise():
    """칭찬/잘한 점 추가 함수"""
    praise = st.session_state.praise_input
    if praise:
        st.session_state.praise_list.append(praise)
        st.toast("스스로를 향한 칭찬이 저장되었습니다! ⭐")
        st.session_state.praise_input = ""

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
    st.write("오늘 하루 동안 있었던 일이나 느꼈던 감정을 자유롭게 적어보세요.")
    
    journal_text = st.text_area("오늘의 일기 쓰기", 
                                value=st.session_state.daily_journal, 
                                height=150, 
                                placeholder="오늘 있었던 일이나 생각들을 편하게 적어보세요...")
    
    if st.button("일기 저장"):
        st.session_state.daily_journal = journal_text
        st.success("오늘의 일기가 저장되었습니다! 📖")


def page_worries():
    st.header("💭 2. 요즘 나의 고민")
    st.write("마음속에 담아둔 고민들을 자유롭게 털어놓으세요.")
    
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


def page_praise():
    st.header("⭐ 3. 내가 잘한 점 & 칭찬할 점")
    st.write("고민 뒤에는 나의 멋진 점을 찾아볼 차례입니다! 아주 작은 일이라도 좋으니 나를 칭찬해 주세요.")
    
    new_praise = st.text_input("칭찬/잘한 점 입력 (예: 일찍 일어났다, 친구 이야기를 들어주었다)", key="praise_input")
    if st.button("칭찬 추가", on_click=add_praise):
        if not new_praise:
            st.warning("칭찬할 내용을 입력해 주세요!")
            
    st.markdown("---")
    if not st.session_state.praise_list:
        st.info("아직 등록된 칭찬이 없습니다. 나 자신을 격려해 보세요!")
    else:
        for idx, praise_item in enumerate(st.session_state.praise_list):
            c1, c2 = st.columns([5, 1])
            c1.write(f"👏 {praise_item}")
            if c2.button("삭제", key=f"del_praise_{idx}"):
                st.session_state.praise_list.pop(idx)
                st.rerun()

def page_improvement():
    st.header("🎯 4. 내가 개선하고 싶은 점")
    st.info(f"현재 나의 개선 목표:\n\n**\"{st.session_state.improvement_goal}\"**")
    
    if st.button("목표 수정하기"):
        edit_improvement_goal()
        
    if st.session_state.goal_updated:
        st.success("새로운 개선 목표가 저장되었습니다!")
        st.session_state.goal_updated = False
        
    st.markdown("---")
    st.caption("💡 칭찬으로 채운 자존감을 바탕으로, 스스로 변화하고 싶은 목표를 적어보세요.")


def page_habits():
    st.header("🌿 5. 나를 돌보는 습관")
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
    st.header("🤖 6. AI 심리 상담실")
    st.write("작성하신 **일기, 고민, 잘한 점, 개선 점, 습관** 데이터를 종합하여 맞춤 상담을 제공합니다.")
    
    journal_text = st.session_state.daily_journal if st.session_state.daily_journal else "작성된 일기 없음"
    worry_text = ", ".join(st.session_state.worry_list) if st.session_state.worry_list else "등록된 고민 없음"
    praise_text = ", ".join(st.session_state.praise_list) if st.session_state.praise_list else "등록된 칭찬 없음"
    habit_text = ", ".join([h[0] for h in st.session_state.self_care_habits]) if st.session_state.self_care_habits else "등록된 습관 없음"
    
    st.markdown(f"""
    > **기록 요약**
    > * **오늘의 일기:** {journal_text}
    > * **요즘 고민:** {worry_text}
    > * **잘한 점/칭찬:** {praise_text}
    > * **개선하고 싶은 점:** {st.session_state.improvement_goal}
    > * **나를 돌보는 습관:** {habit_text}
    """)
    
    user_prompt = st.text_input("AI 상담사에게 물어보고 싶은 내용을 적어주세요")
    
    if st.button("상담 받기"):
        if ai_client is None:
            st.error("OpenAI API 키가 설정되지 않았습니다.")
        else:
            with st.spinner("모든 기록을 깊이 이해하며 상담을 구성하는 중..."):
                try:
                    system_content = f"""
                    너는 따뜻하고 공감 능력이 뛰어난 심리 상담사야. 
                    사용자가 입력한 아래 일기, 고민, 칭찬, 목표, 습관 데이터를 참고하여 깊이 공감하고 조언해 줘.
                    
                    [사용자 데이터]
                    - 오늘의 일기: {journal_text}
                    - 요즘 고민들: {worry_text}
                    - 잘한 점/칭찬: {praise_text}
                    - 개선 점: {st.session_state.improvement_goal}
                    - 나를 돌보는 습관들: {habit_text}
                    
                    사용자의 고민을 경청하면서도, 사용자가 직접 적은 '잘한 점'을 적극 활용하여 자존감을 높여주는 따뜻한 상담을 제공해 줘.
                    """
                    
                    response = ai_client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": system_content},
                            {"role": "user", "content": user_prompt if user_prompt else "제 종합 데이터들을 바탕으로 조언과 상담 부탁드립니다."}
                        ]
                    )
                    st.chat_message("assistant").write(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"상담 연결 중 오류가 발생했습니다: {e}")


def page_cheering_message():
    st.header("💌 7. AI의 맞춤 칭찬 & 응원")
    st.write("내가 적은 잘한 점과 고민을 토대로, AI가 특급 칭찬과 따뜻한 격려 메시지를 전해줍니다.")
    
    praise_text = ", ".join(st.session_state.praise_list) if st.session_state.praise_list else "특별히 작성된 칭찬이 없음"
    worry_text = ", ".join(st.session_state.worry_list) if st.session_state.worry_list else "고민 없음"
    
    if st.button("AI 칭찬 & 응원 받기"):
        if ai_client is None:
            st.error("OpenAI API 키가 설정되지 않았습니다.")
        else:
            with st.spinner("당신만을 위한 진심 어린 칭찬 카드를 작성 중..."):
                try:
                    system_content = f"""
                    너는 사용자의 고민({worry_text})을 다정하게 감싸안고, 사용자가 칭찬한 점({praise_text})을 극찬해 주는 칭찬 전문 멘토야. 
                    사용자가 스스로 적은 칭찬 거리를 바탕으로 "정말 대단하다"고 열렬히 칭찬해 주고, 힘을 얻을 수 있는 응원의 한마디(4~5문장)를 다정하게 작성해 줘.
                    """
                    
                    response = ai_client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": system_content},
                            {"role": "user", "content": "나를 위한 AI 맞춤 칭찬과 응원의 글을 보여줘."}
                        ]
                    )
                    
                    message = response.choices[0].message.content
                    
                    
                    st.balloons()
                    
                    st.success("🎉 AI 칭찬 & 응원 카드")
                    st.markdown(f"### \"{message}\"")
                except Exception as e:
                    st.error(f"메시지 생성 중 오류가 발생했습니다: {e}")


pg = st.navigation([
    st.Page(page_journal, title="오늘의 일기", icon="📝"),
    st.Page(page_worries, title="요즘 나의 고민", icon="💭"),
    st.Page(page_praise, title="내가 잘한 점 & 칭찬", icon="⭐"),
    st.Page(page_improvement, title="내가 개선하고 싶은 점", icon="🎯"),
    st.Page(page_habits, title="나를 돌보는 습관", icon="🌿"),
    st.Page(page_ai_counselor, title="AI 심리 상담", icon="🤖"),
    st.Page(page_cheering_message, title="AI 맞춤 칭찬 & 응원", icon="💌")
], position="top")

st.title("🌱 멘탈 웰니스 & AI 심리케어 플래너")
pg.run()
