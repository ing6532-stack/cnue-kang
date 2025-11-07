import random
import streamlit as st


st.set_page_config(page_title="끝말잇기 게임", layout="centered")
st.title("끝말잇기 게임 🎯")
st.write("제가 먼저 단어를 제시합니다 — 제시된 단어의 마지막 글자와 같은 글자로 시작하는 단어를 입력해 주세요.")


# --- 단어 목록 (간단한 샘플) ---------------------------------
WORD_LIST = [
    "사과", "학교", "자동차", "나무", "우유", "바나나", "나비", "이름", "먹이", "이사",
    "사랑", "공원", "노트", "트럭", "컵", "피자", "자전거", "게임", "음악", "기차",
    "한국", "국가", "가방", "방울", "울타리", "리본", "본인", "인형", "형광등", "등대"
]


# --- 세션 상태 초기화 -----------------------------------------
if "current_word" not in st.session_state:
    st.session_state.current_word = random.choice(WORD_LIST)
    st.session_state.history = [st.session_state.current_word]
    st.session_state.used_words = set(st.session_state.history)
    st.session_state.feedback = ""


def restart_game():
    st.session_state.current_word = random.choice(WORD_LIST)
    st.session_state.history = [st.session_state.current_word]
    st.session_state.used_words = set(st.session_state.history)
    st.session_state.feedback = ""
    st.experimental_rerun()


def first_char(word: str) -> str:
    return word[0]


def last_char(word: str) -> str:
    return word[-1]


st.markdown(f"### 지금 단어: **{st.session_state.current_word}**")

with st.form(key="word_form"):
    user_word = st.text_input("단어를 입력하세요", value="")
    submitted = st.form_submit_button("제출")

if submitted:
    w = user_word.strip()
    if not w:
        st.session_state.feedback = "단어를 입력해 주세요."
    elif w in st.session_state.used_words:
        st.session_state.feedback = f"'{w}' 는 이미 사용된 단어입니다. 다른 단어를 입력하세요."
    elif first_char(w) != last_char(st.session_state.current_word):
        st.session_state.feedback = (
            f"끝말이 맞지 않습니다. 현재 단어의 마지막 글자 '{last_char(st.session_state.current_word)}' 로 시작해야 합니다."
        )
    else:
        # 사용자의 유효한 단어를 히스토리에 추가
        st.session_state.history.append(w)
        st.session_state.used_words.add(w)

        # 컴퓨터(앱)가 이어갈 수 있는 단어를 WORD_LIST에서 찾음
        needed = last_char(w)
        candidates = [x for x in WORD_LIST if first_char(x) == needed and x not in st.session_state.used_words]
        if candidates:
            comp = random.choice(candidates)
            st.session_state.history.append(comp)
            st.session_state.used_words.add(comp)
            st.session_state.current_word = comp
            st.session_state.feedback = f"올바릅니다 ✅ 제가 '{comp}' 라고 이어갈게요. 다음은 '{last_char(comp)}' 로 시작하는 단어를 입력해 주세요."
        else:
            # 이어갈 단어가 없음 -> 사용자가 승리
            st.session_state.current_word = w
            st.session_state.feedback = f"좋아요! 제가 이어갈 단어를 찾지 못했습니다 — 당신의 승리입니다 🏆"


col1, col2 = st.columns([1, 1])
with col1:
    if st.button("새로 시작"):
        restart_game()
with col2:
    if st.button("초기 단어 재설정"):
        # 현재 게임을 유지하되 시작 단어만 새로 뽑음
        st.session_state.current_word = random.choice(WORD_LIST)
        st.session_state.history = [st.session_state.current_word]
        st.session_state.used_words = set(st.session_state.history)
        st.session_state.feedback = ""
        st.experimental_rerun()


if st.session_state.feedback:
    st.info(st.session_state.feedback)

st.markdown("---")
st.subheader("지금까지의 흐름")
st.write(" → ".join(st.session_state.history))

