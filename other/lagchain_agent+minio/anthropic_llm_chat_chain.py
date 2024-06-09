from langchain.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain.agents import AgentExecutor,create_tool_calling_agent
from langchain.agents import Tool, AgentType, initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain.utilities import DuckDuckGoSearchAPIWrapper
from mnio_connect import upload_file_to_minio,nof_lines
from langchain_anthropic import ChatAnthropic
import os
from langchain.utilities import DuckDuckGoSearchAPIWrapper
from langchain_core.messages import AIMessage, HumanMessage
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser


#define the anthropic model
#os.environ['ANTHROPIC_API_KEY']='sk-ant-api03-XCTRsrZwPwhvjGUyGXl0bxnkW_ZT8_kAib9eocvjdX6mWK9AJUuTonHTJc6YaFfmIEf7wIQR6ABFQp-GbBYRjw-2A3KWwA'
#model = ChatAnthropic(model='claude-3-opus-20240229')
anthropic_llm = ChatAnthropic(model = "claude-3-haiku-20240307")
search=DuckDuckGoSearchAPIWrapper()

tool=Tool(name='search tool',
          func=search.run,
          description='useful when user asks the questions which requires to seach from the internet')

tools = [upload_file_to_minio,nof_lines]
llm_with_tools = anthropic_llm.bind_tools(tools)
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. call nof_lines tool to find number of lines in a file or call  upload_file_to_minio tool for file related tasks are given, otherwise answer to the {input} with just 10 words",
        ),
        MessagesPlaceholder(variable_name='chat_history'),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)


#agent=create_tool_calling_agent(llm=anthropic_llm,prompt=prompt,tools=tools)
agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
        ),
        "chat_history": lambda x: x["chat_history"],
    }
    | prompt
    | llm_with_tools
    | OpenAIToolsAgentOutputParser()
)
agent_executor=AgentExecutor(agent=agent,tools=tools,verbose=True)
next_qs=True
chat_history = []
while next_qs:
    user_input=input('enter your task related for minio : ')

    result=agent_executor.invoke({"input": user_input, "chat_history": chat_history})
    print(result)
    chat_history.extend(
        [
            HumanMessage(content=user_input),
            AIMessage(content=result["output"]),
        ]
    )
    next_qs=input('do you have any qs: (yes or no)').lower()
    if next_qs=='yes':
        next_qs=True
    else:
        next_qs=False


