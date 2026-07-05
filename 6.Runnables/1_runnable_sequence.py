from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence
from dotenv import load_dotenv

load_dotenv()

Model = ChatGoogleGenerativeAI(model="gemini-3.5-flash")
prompt1 = PromptTemplate(
    template = "Write a joke about the {topic}",
    input_variables = ["topic"]
)
prompt2 = PromptTemplate(
    template = "Explain the Following Joke {text}",
    input_variables = ["text"]
)
parser = StrOutputParser()
chain = RunnableSequence(prompt1, Model , parser , prompt2 , Model , parser)
result = chain.invoke({"topic" : "AI and Vibecoders"})
print(result)