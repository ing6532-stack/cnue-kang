import random
import streamlit as st


st.title("� 간단 덧셈/뺄셈 연습")
st.write("3문제를 연속으로 풀고, 몇 문제를 맞혔는지 알려줍니다.")


# --- 초기화 -------------------------------------------------
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.current_question = None
    st.session_state.current_answer = None
    st.session_state.last_feedback = ""


def new_question():
    """새로운 문제를 생성해 세션에 저장한다."""
    a = random.randint(0, 20)
    b = random.randint(0, 20)
    op = random.choice(["+", "-"])
    # 뺄셈일 때 음수가 되지 않도록 순서 조정
    if op == "-" and a < b:
        a, b = b, a
    q_text = f"{a} {op} {b}"
    ans = a + b if op == "+" else a - b
    st.session_state.current_question = q_text
    st.session_state.current_answer = ans


# 문제 시작 조건
if st.session_state.current_question is None:
    new_question()


st.write(f"문제 {st.session_state.q_index + 1} / 3")
st.markdown(f"### {st.session_state.current_question} = ?")

with st.form(key="answer_form"):
    user_answer = st.number_input("정답을 입력하세요", step=1, value=0)
    submitted = st.form_submit_button("제출")

if submitted:
    try:
        ua = int(user_answer)
    except Exception:
        ua = None

    if ua == st.session_state.current_answer:
        st.session_state.score += 1
        st.session_state.last_feedback = "정답입니다 ✅"
    else:
        st.session_state.last_feedback = (
            f"틀렸습니다 ❌ 정답은 {st.session_state.current_answer} 입니다."
        )

    st.session_state.q_index += 1

    if st.session_state.q_index < 3:
        # 다음 문제 준비
        new_question()
        # 페이지가 다시 렌더링되며 다음 문제가 보입니다.
        st.experimental_rerun()
    else:
        # 3문제 완료
        st.success(f"완료! 총 {st.session_state.score} / 3 문제 정답")
        st.info(st.session_state.last_feedback)

        if st.button("다시하기"):
            # 상태 초기화 후 새 문제 생성
            st.session_state.q_index = 0
            st.session_state.score = 0
            st.session_state.current_question = None
            st.session_state.current_answer = None
            st.session_state.last_feedback = ""
            new_question()
            st.experimental_rerun()

        # 이후 아래의 입력 폼이나 안내는 보이지 않도록 중단
        st.stop()


if st.session_state.last_feedback:
    st.write(st.session_state.last_feedback)

