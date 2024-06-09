from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate,PromptTemplate
from langchain.agents import AgentExecutor,AgentType,Tool,initialize_agent,load_tools
from langchain_core.messages import HumanMessage,AIMessage
from langchain import LLMChain

import os
os.environ['ANTHROPIC_API_KEY']='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'
anthropic_llm = ChatAnthropic(model = "claude-3-haiku-20240307")
from langchain.prompts import PromptTemplate,FewShotPromptTemplate
from langchain.prompts.example_selector import LengthBasedExampleSelector
exmples=[
    {'input':'who is the CM of andhra pradesh',
    'answer':'sorry I dont answer for the political questions'
     },
    {'input':'Who is the PM of india',
    'answer':' I have assigned to answer for technical doubts'},
    {'input':'who won the state elections in 2019',
     'answer':'Dont ask me such questions instead ask me minio related questions'},
    {'input':'what is minio',
     'answer':'MinIO\'s High Performance Object Storage is Open Source, Amazon S3 compatible'}
    ]

template='''
user:{input}
AI:{answer}'''
prefix=''' Answer for the user questions with only 10 words maximum.And answer for minio related questions only'''

suffix='''
user:{input}'
AI:'''
sample_prompt=PromptTemplate(
    input_variables=['input','answer'],
    template=template
)

selector=LengthBasedExampleSelector(
    examples=exmples,
    example_prompt=sample_prompt,
    max_length=50
)
prompt=FewShotPromptTemplate(
    example_selector=selector,  # use example_selector instead of examples
    example_prompt=sample_prompt,
    prefix=prefix,
    suffix=suffix,
    input_variables=["input"],
    example_separator="\n"

)
llm_chian=LLMChain(prompt=prompt,llm=anthropic_llm)

user_qs=input('enter you qs: ')
print(prompt.format(input=user_qs))
response=llm_chian.invoke(user_qs)
print(response)