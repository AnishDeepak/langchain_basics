from langchain.llms import GooglePalm
from langchain import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv
load_dotenv()

#using HF
# HF_api_key=os.getenv('hugging_face_api')
# os.environ['HUGGINGFACEHUB_API_TOKEN']=hugging_face_key
# HF_llm=HuggingFaceHub(repo_id='google/flan-t5-large',model_kwargs={'temperature':0,'max_length':64})
# print(HF_llm('capital of china'))

#using google
google_api_key=os.getenv('google_api_key')
google_llm=GooglePalm(google_api_key=google_api_key,temperature=.4)
template='''Tell me the capital of {country}
            and give the answer as the capital of india is your answer'''
prompt=PromptTemplate.from_template(
    input_variable=['country'],
    template=template
)
print(prompt.format(country='india'))
chain=LLMChain(llm=google_llm,prompt=prompt)
print(chain.run('india'))
