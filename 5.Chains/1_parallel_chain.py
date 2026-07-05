from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
from dotenv import load_dotenv

load_dotenv()
parser = StrOutputParser()
Model1 = ChatGoogleGenerativeAI(model="gemini-3.5-flash")

Model2 = ChatGoogleGenerativeAI(model="gemini-3.5-flash")
prompt1 = ChatPromptTemplate.from_template(
    template = "Generate Short and Simple Notes on {topic} in Software Engineering Tone",
)
prompt2 = ChatPromptTemplate.from_template(
    template = "Generate Short and Simple Quiz on {topic} in Software Engineering Tone",
)
prompt3 = ChatPromptTemplate.from_template(
    template = "Merge The provided notes and quiz into a single document \n notes -> {notes} \n quiz -> {quiz}",
)
parallel_chain = RunnableParallel(
    notes = prompt1 | Model1 | parser,
    quiz = prompt2 | Model2 | parser,
)
merge_chain = prompt3 | Model1 | parser
chain = parallel_chain | merge_chain
result = chain.invoke( {"topic" : "Scope and market future of Agentic AI"})
print(result)
chain.get_graph.print_tree()

