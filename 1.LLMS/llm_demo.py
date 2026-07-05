from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

# This uses the free Gemini API
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash")

result = llm.invoke("Who is the father of Anas Farooq?")
print(result.content)