import os
from dotenv import load_dotenv
from langchain.chat_models import ChatGooglePalm
from langchain.schema import HumanMessage,SystemMessage,AIMessage
from langchain.schema import BaseOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import T


load_dotenv()

os.environ['GOOGLE_API_KEY']=os.getenv('google_api_key')
chat_llm=ChatGooglePalm()
#using this method we cnnot pass the dynamic inputs
#for dynamic input use chatptompt template
messages=[
    SystemMessage(content='Give 2 IMP concepts to learn from user given topic'),
    HumanMessage(content='Cloud Computing')
    ]
print(chat_llm(messages))