import streamlit as st
from langchain_core.messages import ChatMessage
from rag import naver_news_setup, create_rag_chain

st.title("네이버 뉴스 챗봇")

# 대화 기록이 없다면, chat_history 라는 키로 빈 대화를 저장하는 list 를 생성
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# chain 을 초기화
if "news_chain" not in st.session_state:
    st.session_state["news_chain"] = None


# 대화 기록에 채팅을 추가
def add_history(role, message):
    st.session_state["chat_history"].append(ChatMessage(role=role, content=message))


# 이전 까지의 대화를 출력
def print_history():
    for chat_message in st.session_state["chat_history"]:
        # 메시지 출력(role: 누가 말한 메시지 인가?) .write(content: 메시지 내용)
        st.chat_message(chat_message.role).write(chat_message.content)


# 사이드 바
with st.sidebar:
    naver_news_url = st.text_input("네이버 뉴스 URL을 입력해주세요")

    # 설정이 완료 되었는지 확인하는 버튼
    confirm_btn = st.button("설정 완료")


# 파일을 캐시 저장(시간이 오래 걸리는 작업을 처리할 예정)
@st.cache_resource(show_spinner="URL을 분석 중입니다...")
def embed_file(url):
    retriever = naver_news_setup(url, chunk_size=2000, chunk_overlap=50)
    return retriever


# 파일이 업로드 되었을 때
if confirm_btn:
    retriever = embed_file(naver_news_url)
    st.session_state["news_chain"] = create_rag_chain(retriever)

# 이전 까지의 대화를 출력
print_history()

user_input = st.chat_input("궁금한 내용을 입력해 주세요")

if user_input:
    # 파일이 업로드가 된 이후
    if st.session_state["news_chain"]:
        rag_chain = st.session_state["news_chain"]
        # 사용자의 질문을 출력합니다.
        st.chat_message("user").write(user_input)

        # AI 의 답변을 출력합니다.
        with st.chat_message("ai"):
            # 답변을 출력할 빈 공간을 만든다.
            chat_container = st.empty()

            # 사용자가 질문을 입력하면, 체인에 질문을 넣고 실행합니다.
            answer = rag_chain.stream(user_input)

            # 스트리밍 출력
            ai_answer = ""
            for token in answer:
                ai_answer += token
                chat_container.markdown(ai_answer)

        # 대화 기록에 추가
        add_history("user", user_input)
        add_history("ai", ai_answer)
    else:
        # 파일이 업로드 되지 않았을 때
        st.warning("네이버 뉴스 URL을 입력해주세요")
