from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel , RunnableSequence , RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()


Model = ChatGoogleGenerativeAI(model="gemini-3.5-flash")
prompt1 = PromptTemplate(
    template = "Write a tweet about the {topic} with no emojies and in short and concise well formatted professional manner",
    input_variables = ["topic"]
)
prompt2 = PromptTemplate(
    template = "Write a Linkedln post about the {topic} with no emojies and in short and concise  well formatted professional manner",
    input_variables = ["topic"]
)
parser = StrOutputParser()
joke_gen_chain = RunnableSequence(prompt1 , Model , parser)
parallel_chain = RunnableParallel({
    'joke': RunnablePassthrough(),
    'explanation' : RunnableSequence(prompt2 | Model | parser),
})
final_chain = RunnableSequence(joke_gen_chain , parallel_chain)
result = final_chain.invoke({"topic" : "AI and Vibecoders"})
print(result)
