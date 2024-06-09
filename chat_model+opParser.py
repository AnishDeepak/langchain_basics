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
class CommaseparatedOP(BaseOutputParser):
    def parse(self, text: str) -> T:
        return '\n'.join(text.strip().split(','))

template='Provide 3 imp topics to learn from user input'
human="{topic}"

prompt=ChatPromptTemplate.from_messages(
    [
        ('system',template),
        ('human',human)
    ]
)
print('Without output parser')
chain1=prompt|chat_llm
print(chain1.invoke({'topic':'data science'}))
print('with out parser')
chain=prompt | chat_llm | CommaseparatedOP()
print(chain.invoke({'topic':'ML'}))


