from langchain.chains import RetrievalQA


from langchain_community.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.text_splitter import CharacterTextSplitter

from langchain_community.vectorstores import Chroma
from langchain_anthropic import ChatAnthropic
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
import warnings

# Ignore all warnings
warnings.filterwarnings("ignore")

# Your code goes here

import os
os.environ['ANTHROPIC_API_KEY']='sk-ant-api03-pDmIPoEA7GXF0JoOUFg17MESh85tgaJJxcAqJzi-bzn39EBjERCIt5yvzpXRDYBUSRaKd1-AtZPjKpfjb-ywGQ-SlsAUQA'
#model = ChatAnthropic(model='claude-3-opus-20240229')
anthropic_llm = ChatAnthropic(model = "claude-3-haiku-20240307")



# load document
loader = PyPDFLoader('anish.pdf')
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
texts = text_splitter.split_documents(documents)
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

db = Chroma.from_documents(texts, embedding_function)
retriever = db.as_retriever(search_type="similarity", search_kwargs={"k":2})

qa = RetrievalQA.from_chain_type(
    llm=anthropic_llm, chain_type="stuff", retriever=retriever, return_source_documents=True)

query = input('enter you query: ')
result = qa({"query": query})
print(result)