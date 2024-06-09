import os
from dotenv import load_dotenv
from langchain.llms import GooglePalm
from langchain.prompts import PromptTemplate
from langchain.chains import SimpleSequentialChain,LLMChain
load_dotenv()
os.environ['GOOGLE_API_KEY']=os.getenv('google_api_key')
llm=GooglePalm()

capital_prompt=PromptTemplate(
    input_variables=['country'],
    template='tell me the capital of {country}'
)
capital_chain=LLMChain(llm=llm,prompt=capital_prompt)

famous_place_prompt=PromptTemplate(
    input_variables=['capital'],
    template='tell me 5 best places to visit in {capital}'
)
famous_chain=LLMChain(llm=llm,prompt=famous_place_prompt)

seq_chain=SimpleSequentialChain(
    chains=[capital_chain,famous_chain]
)
print(seq_chain.run('india'))