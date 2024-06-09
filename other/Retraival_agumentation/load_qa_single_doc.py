from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain_anthropic import ChatAnthropic
import warnings

# Ignore all warnings
warnings.filterwarnings("ignore")

# Your code goes here

import os
os.environ['ANTHROPIC_API_KEY']='sk-ant-api03-pDmIPoEA7GXF0JoOUFg17MESh85tgaJJxcAqJzi-bzn39EBjERCIt5yvzpXRDYBUSRaKd1-AtZPjKpfjb-ywGQ-SlsAUQA'
#model = ChatAnthropic(model='claude-3-opus-20240229')
anthropic_llm = ChatAnthropic(model = "claude-3-haiku-20240307")

from langchain.chains.question_answering import load_qa_chain

# load document
loader = PyPDFLoader('samata.pdf')
documents = loader.load()


chain = load_qa_chain(llm=anthropic_llm, chain_type="map_reduce")

query = input("enter you question on resume: ")
response=chain.run(input_documents=documents, question=query)
print(response)