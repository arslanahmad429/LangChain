from langchain_huggingface import HuggingFaceEmbeddings
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
Documents = [
    "Islamabad is the capital of Pakistan",
    "Delhi is the capital of India"
    "Mumbai is the capital of mum",
    "Kolkata is the capital of kol",
    "Chennai is the capital of chen",
    "Bangalore is the capital of ban",
]

result = embedding.embed_documents(Documents)

# printtext)
print(str(result))
