import os
from dotenv import load_dotenv
from langchain.chat_models import ChatGooglePalm
from langchain.schema import BaseOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import T
import streamlit as st

load_dotenv()

os.environ['GOOGLE_API_KEY']=os.getenv('google_api_key')
llm=ChatGooglePalm(temperature=.45)

class CustomOpParser(BaseOutputParser):
    def parse(self, text: str) -> T:
        return '\n'.join(text.strip().split(','))

sys_template='Answer for the user query just with 10 words'
human='{query}'
chat_prompt = ChatPromptTemplate.from_messages(
        [
            ('system', sys_template),
            ('human', human)
        ]
    )

def get_llm_response(user_query):

    chain=chat_prompt | llm | CustomOpParser()
    response=chain.invoke({'query':user_query})
    return response

st.set_page_config(page_title='Simple QA')
st.header('Google Palm')
user_input=st.text_input('Input',key='Input')
response=get_llm_response(user_input)



submit=st.button('Enter your query')

if submit:
    st.subheader('The response is')
    st.write(response)