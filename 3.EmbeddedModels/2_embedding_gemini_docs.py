from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embedding = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2")
Documents = [
    "Islamabad is the capital of Pakistan",
    "Delhi is the capital of India"
    "Mumbai is the capital of mum",
    "Kolkata is the capital of kol",
    "Chennai is the capital of chen",
    "Bangalore is the capital of ban",
]

result = embedding.embed_documents(Documents)

print(str(result))