"""
1. job_listings.txt → [TextLoader] → Full Document
                                          ↓
2. Full Document → [TextSplitter] → Chunk 1, Chunk 2, Chunk 3...
                                          ↓
3. Each Chunk → [OpenAIEmbeddings] → Vector [0.1, 0.8, ...]
                                          ↓
4. Vectors → [Chroma Database] → Stored for searching
                                          ↓
5. Your Query → [Embeddings] → Query Vector
                                          ↓
6. Query Vector → [Similarity Search] → Matching Chunks
                                          ↓
7. Results Displayed

This code creates a simple semantic search system that can find relevant job listings based on your query. Let me break it down piece by piece:
PART 1: IMPORTS AND SETUP

What's happening here?
import os: Gives access to environment variables (where API keys are safely stored)
OpenAIEmbeddings: Converts text into numerical vectors (embeddings) that capture semantic meaning
TextLoader: Reads text files from your computer
RecursiveCharacterTextSplitter: Breaks long documents into smaller, manageable pieces
Chroma: A vector database that stores and searches these embeddings
"""
import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

# PART 2: INITIALIZING THE EMBEDDINGS MODEL
"""
What's happening?
Getting the API Key: Your OpenAI API key is stored as an environment variable (a secure way to handle secrets)
Creating the Embeddings Model: This is the "brain" that will understand the meaning of text
Despite being called llm, it's actually an embedding model, not a language model
It converts text like "software engineer" into a list of 1536 numbers that represent its meaning
"""
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
llm = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

# PART 3: LOADING AND SPLITTING DOCUMENTS
"""
What's happening?
Loading: Reads job_listings.txt from your current directory
Creating a Splitter:
chunk_size=200: Each piece will be about 200 characters long
chunk_overlap=10: Each chunk shares 10 characters with the next chunk (prevents cutting sentences in awkward places)
Splitting: Breaks the document into smaller chunks

Example: If your file has:
"Senior Python Developer needed. Must know Django and FastAPI. Remote position with competitive salary."
It becomes chunks like:

Chunk 1: "Senior Python Developer needed. Must know Django and..."
Chunk 2: "...and FastAPI. Remote position with competitive salary."
"""
document = TextLoader("job_listings.txt").load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=10)
chunks = text_splitter.split_documents(document)

# PART 4: CREATING THE VECTOR DATABASE
"""
What's happening?
Creating the Database:
    - Takes all chunks
    - Converts each chunk to embeddings using the llm model
    - Stores them in Chroma (a vector database)
Creating a Retriever:
    - This is like a search engine interface
    - When you ask a question, it finds the most similar chunks

Visual Analogy:

Chunks → Embeddings → Vector Space
"Python job" → [0.1, 0.8, -0.3, ...] → Plotted in 1536-dimensional space
Similar queries find nearby points in this space
"""
db = Chroma.from_documents(chunks, llm)
retriever = db.as_retriever()

# PART 5: SEMANTIC SEARCH
"""
What's happening?
1. User Input: Prompts you to type a search query (e.g., "remote python jobs")
2. Semantic Search:
    - Converts your query to an embedding
    - Finds chunks with similar embeddings (using cosine similarity)
    - Returns the most relevant chunks
3. Display Results: Prints the content of matching chunks

Example Query: "remote python jobs"
    - The system understands this means "Python positions that are remote"
    - It doesn't just match keywords - it understands the meaning
"""

text = input("Enter the text: ")
docs = retriever.invoke(text)

for doc in docs:
    print(doc.page_content)

# PART 6: VIEWING ALL STORED DATA
"""
What's happening?
1. db.get(): Retrieves everything stored in the database
2. docs.keys(): Shows the structure - typically ['ids', 'embeddings', 'documents', 'metadatas']
3. Looping through: Displays each document with:
    - ID: Unique identifier
    - Text: The actual content
    - Metadata: Source information (file name, chunk position, etc.)
"""
# Display all stored documents
docs = db.get()
print(docs.keys())

for i in range(len(docs['documents'])):
    print(("ID:", docs["ids"][i]))
    print(("text:", docs['documents'][i]))
    print("Metadata:", docs["metadatas"][i])
    print("--------")

# PART 7: VIEWING RAW CHUNKS
"""
What's happening?
    - Shows exactly how the document was split before being stored
    - Useful for debugging and understanding why certain results appear
"""
print("\n===== CHUNKS CREATED =====\n")
for i, chunk in enumerate(chunks):
    print(f"\nChunk {i + 1}")
    print(chunk.page_content)
    print("Metadata:", chunk.metadata)
    print("--------")