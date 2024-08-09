from langchain_core.prompts import PromptTemplate
from base_chain import BaseConversationChain


class EnglishConversationChain(BaseConversationChain):
    def create_prompt(self):
        template = """당신은 영어를 가르치는 10년차 영어 선생님입니다. 주어진 상황에 맞는 영어 회화를 작성해 주세요.
        양식은 Example을 참고하여 작성해 주세요.

        #상황:
        {question}

        #Example:
        **영어 회화**
        - Customer: Hi there! I would like to order a pizza, please.
        - Staff: Sure! What size would you like?
        - Customer: I’ll have a large pizza, please.
        - Staff: Great! What toppings do you want?
        ...

        **한글 해석**
        - 고객: 안녕하세요! 피자를 주문하고 싶어요.
        - 직원: 물론입니다! 어떤 사이즈로 주문하시겠어요?
        - 고객: 대형 피자로 주세요.
        - 직원: 좋습니다! 어떤 토핑을 원하시나요?
        ...
        """

        # 프롬프트 템플릿을 이용하여 프롬프트를 생성합니다.
        prompt = PromptTemplate.from_template(template)
        return prompt


class SummaryChain(BaseConversationChain):
    def create_prompt(self):
        template = """당신은 요약을 잘하는 요약 AI 입니다. 주어진 글을 요약해 주세요.
        요약은 bullet point로 작성해 주세요.
        문장의 시작은 적절한 emoji 로 시작해 주세요.
        
        #Context:
        {question}
        """

        # 프롬프트 템플릿을 이용하여 프롬프트를 생성합니다.
        prompt = PromptTemplate.from_template(template)
        return prompt


class BlogChain(BaseConversationChain):
    def create_prompt(self):
        template = """당신은 블로그 글 작성 AI 입니다.
        주어진 글은 뉴스 기사입니다. 뉴스 기사의 내용을 블로그 글로 작성하세요.
        블로그 글의 끝에는 hashtag를 추가해 주세요.
        블로그는 3-5 문단으로 작성해 주세요.
        
        #Context:
        {question}
        """

        # 프롬프트 템플릿을 이용하여 프롬프트를 생성합니다.
        prompt = PromptTemplate.from_template(template)
        return prompt
