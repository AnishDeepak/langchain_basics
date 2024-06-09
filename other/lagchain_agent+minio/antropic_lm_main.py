from langchain.schema import HumanMessage,SystemMessage
from langchain.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor,create_tool_calling_agent
from mnio_connect import upload_file_to_minio,nof_lines
from langchain_anthropic import ChatAnthropic
import os

#define the anthropic model
#os.environ['ANTHROPIC_API_KEY']='sk-ant-api03-XCTRsrZwPwhvjGUyGXl0bxnkW_ZT8_kAib9eocvjdX6mWK9AJUuTonHTJc6YaFfmIEf7wIQR6ABFQp-GbBYRjw-2A3KWwA'
#model = ChatAnthropic(model='claude-3-opus-20240229')
anthropic_llm = ChatAnthropic(model = "claude-3-haiku-20240307")

tools = [upload_file_to_minio, nof_lines]

# llm with tools
llm_with_tools = anthropic_llm.bind_tools(tools)
user_input=input('enter you question: ')

#print(llm_with_tools.invoke(messages).tool_calls)
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. call tools if file related tasks are given, otherwise answer to the {input}",
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)
# Construct the Tool Calling Agent
agent = create_tool_calling_agent(anthropic_llm, tools, prompt)

# Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Run Agent

agent_executor.invoke({"input": user_input})