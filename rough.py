import os
from dotenv import load_dotenv
from langchain.chat_models import ChatGooglePalm
from langchain.schema import BaseOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import T
import streamlit as st

load_dotenv()

os.environ['GOOGLE_API_KEY']=os.getenv('google_api_key')
chat_llm=ChatGooglePalm()

class CustomOpParser(BaseOutputParser):
    def parse(self, text: str) -> T:
        return '\n'.join(text.strip().split(','))

sys_template='Answer for the user query just with 10 words'
human="{query}"
chat_prompt = ChatPromptTemplate.from_messages(
        [
            ('system', sys_template),
            ('human', human)
        ]
    )

#def get_llm_response(user_query):
llm=ChatGooglePalm(temperature=.45)

chain=llm | chat_llm | CustomOpParser()
print(chain.invoke({'topic':'ML'}))
#return response
