from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import  CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_anthropic import ChatAnthropic
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.chains import ConversationalRetrievalChain

import warnings

# Ignore all warnings
warnings.filterwarnings("ignore")

# Your code goes here

import os
os.environ['ANTHROPIC_API_KEY']='sk-ant-api03-pDmIPoEA7GXF0JoOUFg17MESh85tgaJJxcAqJzi-bzn39EBjERCIt5yvzpXRDYBUSRaKd1-AtZPjKpfjb-ywGQ-SlsAUQA'
#model = ChatAnthropic(model='claude-3-opus-20240229')
anthropic_llm = ChatAnthropic(model = "claude-3-haiku-20240307")

loader=PyPDFLoader('anish.pdf')
doc_text=loader.load()

text_splitter=CharacterTextSplitter(chunk_size=100,chunk_overlap=0)
splitted_text=text_splitter.split_documents(doc_text)

embedding_function=SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
db=Chroma.from_documents(doc_text,embedding_function)

retriver_type=db.as_retriever(type='similarity',search_kwargs={'k':1})

conversation_chain=ConversationalRetrievalChain.from_llm(anthropic_llm,retriver_type)
chat_history=[]
next_qs=True
while next_qs:
    query=input('user: ')
    result=conversation_chain({'question':query,'chat_history':chat_history})
    print(f"AI:{result['answer']}")
    chat_history=[(query,result['answer'])]
    next_qs=input('do you have next qs (yes or no): ').lower()
    if next_qs=='yes':
        next_qs=True
    else:next_qs=False