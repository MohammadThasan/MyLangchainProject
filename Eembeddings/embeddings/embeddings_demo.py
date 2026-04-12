import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
llm = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

document = TextLoader("job_listings.txt").load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=250, # we can change the Chunks and try the output
                                               chunk_overlap=15)

chunks=text_splitter.split_documents(document)
db=Chroma.from_documents(chunks,llm)
retriever = db.as_retriever()

text = input("Enter the text: ")

docs = retriever.invoke(text)

for doc in docs:
    print(doc.page_content)