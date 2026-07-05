from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

load_dotenv()
Documents = [
    "Islamabad is the capital of Pakistan",
    "Delhi is the capital of India"
    "Mumbai is the capital of mum",
    "Kolkata is the capital of kol",
    "Chennai is the capital of chen",
    "Bangalore is the capital of ban",
    "Arslan Ahmad is a S Software Engineering student at PUCIT combining strong technical skills in Android and Web Development with proven experience in UK customersupport. Fluent in English and skilled at translating user requirements intosolutions, with a track record of managing international client deals,resolving complaints, and maintaining customer trust on digital platforms.Highly adaptable to fast-paced workflows, utilizing an analytical approachto handle technical support tools, manage high-volume customer queries,and deliver consistent service quality." 
]
query = "Who is Arslan Ahmad"
embedding = GoogleGenerativeAIEmbeddings(model = "gemini-embedding-2", dimensions = 300)
doc_embeddings = embedding.embed_documents(Documents)
query_embedding = embedding.embed_query(query)
result =cosine_similarity([query_embedding],doc_embeddings)[0]
index , score = sorted(list(enumerate(result)), key=lambda x: x[1])[-1]
print(f"Score is {score}")
print(Documents[index])

