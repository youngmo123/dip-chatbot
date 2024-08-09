import streamlit as st
import os

st.title("API 설정")

st.markdown(
    """
OpenAI API 키 발급 방법은 아래 링크를 참고해 주세요!
* [발급방법](https://wikidocs.net/233342)
"""
)


# API 키 입력
api_key = st.text_input("API 키 입력", type="password")

# 설정 확인 버튼
confirm_btn = st.button("설정하기", key="api_key")

if confirm_btn:
    os.environ["OPENAI_API_KEY"] = api_key
    st.write(f"API 키가 설정되었습니다: `{api_key[:15]}************`")
