import streamlit as st
from conversation_chain import EnglishConversationChain, SummaryChain, BlogChain
from langchain_core.messages import ChatMessage
import os


# 사이트의 제목 입력
st.title("우리 모두의 챗GPT")

if "OPENAI_API_KEY" in os.environ:
    st.write("API 키가 설정되었습니다.")
else:
    st.error("API 키가 설정되지 않았습니다.")

# 대화 기록이 없다면, chat_history 라는 키로 빈 대화를 저장하는 list 를 생성
if "conversation_chat_history" not in st.session_state:
    st.session_state["conversation_chat_history"] = []


def add_history(tab, role, message):
    st.session_state["conversation_chat_history"].append(
        (tab, ChatMessage(role=role, content=message))
    )


with st.sidebar:
    selected_model = st.selectbox("모델 선택", ["gpt-4o-mini", "gpt-4o"], index=0)


def generate_answer(mychain, question, answer_container):
    # 답변을 요청(스트리밍 출력)
    answer = mychain.stream({"question": question})

    final_answer = ""
    for token in answer:
        # final_answer 에 토큰을 추가
        final_answer += token
        # 답변을 출력
        answer_container.markdown(final_answer)

    return final_answer


# 사용자가 입력할 상황
question = st.chat_input("영어회화에 주어질 상황을 입력해 보세요.")

tab1, tab2, tab3 = st.tabs(["요약", "블로그", "영어회화"])


def print_history():
    for tab, chat_message in st.session_state["conversation_chat_history"]:
        # 메시지 출력(role: 누가 말한 메시지 인가?) .write(content: 메시지 내용)
        if tab == "tab1":
            tab1.chat_message(chat_message.role).write(chat_message.content)
        elif tab == "tab2":
            tab2.chat_message(chat_message.role).write(chat_message.content)
        elif tab == "tab3":
            tab3.chat_message(chat_message.role).write(chat_message.content)


# request_btn 클릭이 된다면...
if question:
    # 1) 사용자가 입력한 상황을 먼저 출력

    add_history("tab1", "user", question)
    add_history("tab2", "user", question)
    add_history("tab3", "user", question)

    summary_chain = SummaryChain(model_name=selected_model).create()
    blog_chain = BlogChain(model_name=selected_model).create()
    english_chain = EnglishConversationChain(model_name=selected_model).create()
    
    for tab in [tab1, tab2, tab3]:
        with tab.chat_message("user"):
            st.write(question)
    
    with tab1.chat_message("ai"):
        tab1_answer = st.empty()
        answer1 = generate_answer(summary_chain, question, tab1_answer)

    with tab2.chat_message("ai"):
        tab2_answer = st.empty()
        answer2 = generate_answer(blog_chain, question, tab2_answer)

    with tab3.chat_message("ai"):
        tab3_answer = st.empty()
        answer3 = generate_answer(english_chain, question, tab3_answer)

    # answer2 = generate_answer(blog_chain, question, tab2_answer)
    # answer3 = generate_answer(english_chain, question, tab3_answer)

    add_history("tab1", "ai", answer1)
    add_history("tab2", "ai", answer2)
    add_history("tab3", "ai", answer3)
