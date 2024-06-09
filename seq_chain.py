import os
from dotenv import load_dotenv
from langchain.llms import GooglePalm
from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain,LLMChain
load_dotenv()
os.environ['GOOGLE_API_KEY']=os.getenv('google_api_key')
llm=GooglePalm()

capital_prompt=PromptTemplate(
    input_variables=['country'],
    template='tell me the capital of {country}'
)
capital_chain=LLMChain(llm=llm,prompt=capital_prompt,output_key='capital')

famous_place_prompt=PromptTemplate(
    input_variables=['capital'],
    template='tell me 5 best places to visit in {capital}'
)
famous_chain=LLMChain(llm=llm,prompt=famous_place_prompt,output_key='places')

seq_chain=SequentialChain(
    chains=[capital_chain,famous_chain],
    input_variables=['country'],
    output_variables=['capital','places']
)
print(seq_chain({'country':'india'}))