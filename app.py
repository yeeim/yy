import streamlit as st
from openai import OpenAI

# 1. AI 클라이언트 설정 (OpenAI API 키 필요)
ai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 2. 세션 상태 초기화 (심리 상담 컨셉에 맞게 초기값 변경)
if 'todo_list' not in st.session_state:
    st.session_state.todo_list = []
if 'user_motto' not in st.session_state:
    st.session_state.user_motto = "나는 충분히 잘하고 있어."
if 'motto_updated' not in st.session_state:
    st.session_state.motto_updated = False

# 3. 마음 습관 추가 함수
def add_todo():
    task = st.session_state.todo_input
    if task:
        st.session_state.todo_list.append([task, False])
        st.toast("마음 건강 습관이 추가되었습니다! ✨")
        st.session_state.todo_input = ""

# 4. 긍정 확언 수정 팝업창 (st.dialog 활용)
@st.dialog("나를 위한 긍정 확언 수정")
def edit_motto():
    motto = st.text_input("나에게 해주고 싶은 따뜻한 한마디를 적어주세요.")
    if st.button("확언 저장"):
        st.session_state.user_motto = motto
        st.session_state.motto_updated = True
        st.rerun()

# --- 페이지 1: 오늘의 확언 ---
def page_motto():
    st.header("✨ 1. 오늘의 긍정 확언")
    st.info(f"오늘의 나에게: **\"{st.session_state.user_motto}\"**")
    if st.button("확언 수정하기"):
        edit_motto()
    if st.session_state.motto_updated:
        st.success("새로운 확언이 가슴 속에 저장되었습니다! ❤️")
        st.session_state.motto_updated = False
    
    st.markdown("---")
    st.write("💡 **팁**: 긍정적인 확언은 뇌의 보상 체계를 활성화하여 스트레스 완화에 도움을 줍니다.")

# --- 페이지 2: 마음 건강 습관 ---
def page_todo():
    st.header("🌿 2. 마음 건강 실천")
    st.write(f"현재 다짐: **{st.session_state.user_motto}**")
    
    new_todo = st.text_input("실천할 마음 습관을 입력하세요 (예: 명상 5분, 산책하기)", key="todo_input")
    if st.button("추가하기", on_click=add_todo):
        if new_todo == "":
            st.warning("내용을 입력하고 버튼을 눌러주세요!")
    
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
                st.write("✅ **실천함**")

# --- 페이지 3: 마음 성장 지수 ---
def page_report():
    st.header("📈 3. 나의 마음 성장 지수")
    if not st.session_state.todo_list:
        st.write("아직 등록된 습관이 없습니다.")
    else:
        total = len(st.session_state.todo_list)
        count = sum(1 for item in st.session_state.todo_list if item[1])
        progress = (count / total) * 100
        
        st.metric("오늘의 마음 성장도", f"{progress:.1f}%")
        st.progress(progress / 100)
        
        if progress == 100:
            st.balloons()
            st.success("오늘 하루, 자신을 정말 잘 돌봐주셨네요! 당신은 소중한 사람입니다. 🏆")
        
        if st.button("기록 전체 초기화"):
            st.session_state.todo_list = []
            st.rerun()

# --- 페이지 4: AI 마음 상담사 ---
def page_ai_coach():
    st.header("💬 4. AI 마음 상담사")
    st.write("말 못 할 고민이나 오늘 힘들었던 점을 털어놓아 보세요. 제가 들어드릴게요.")
    
    prompt = st.text_input("상담하고 싶은 내용을 입력하세요", placeholder="오늘 학교에서 좀 힘들었어...")
    
    if st.button("대화하기"):
        if prompt:
            with st.spinner("당신의 이야기에 귀를 기울이는 중..."):
                # 상담사 역할을 부여하는 시스템 프롬프트 포함
                response = ai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "너는 다정하고 공감 능력이 뛰어난 청소년 심리 상담사야. 사용자의 고민에 공감해주고, 위로가 되는 따뜻한 말을 해줘. 너무 딱딱한 조언보다는 마음을 어루만지는 말을 해줘."},
                        {"role": "user", "content": prompt}
                    ]
                )
                answer = response.choices[0].message.content
                st.chat_message("assistant").write(answer)
        else:
            st.warning("상담 내용을 입력해 주세요.")

# 5. 내비게이션 설정
pg = st.navigation([
    st.Page(page_motto, title="오늘의 확언", icon="✨"),
    st.Page(page_todo, title="마음 건강 실천", icon="🌿"),
    st.Page(page_report, title="마음 성장 지수", icon="📈"),
    st.Page(page_ai_coach, title="AI 마음 상담", icon="💬")
], position="top")

st.title("🌿 마음 쉼터 플래너")
pg.run()
