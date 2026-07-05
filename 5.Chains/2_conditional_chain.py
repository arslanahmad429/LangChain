from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnableParallel , RunnableLambda
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Literal
from dotenv import load_dotenv

load_dotenv()

Model = ChatGoogleGenerativeAI(model="gemini-3.5-flash")
class feedback (BaseModel):
    sentiment: Literal["positive", "negative"] = Field(description="Give the Sentiment of the feedback")


parser1 = StrOutputParser()
parser2 = PydanticOutputParser(pydantic_object=feedback)


Prompt1= PromptTemplate(
    template = "Classify the sentiment from the feedback text into positive or negative {format_instructions} \n feedback -> {feedback}",
    input_variables = ["feedback"],
    partial_variables = {'format_instructions': parser2.get_format_instructions()}
)

Prompt2 = PromptTemplate(
    template = "Write an appropriate response to this positive feedback {feedback}",
    input_variables = ["feedback"]

)
 
Prompt3 = PromptTemplate(
    template = "Write an appropriate response to this negative feedback {feedback}",
    input_variables = ["feedback"]

)

Classifier = Prompt1 | Model | parser2

branch_chain = RunnableBranch(
    (lambda x:x.sentiment == "positive", Prompt2 | Model | parser1),
    (lambda x:x.sentiment == "negative", Prompt3 | Model | parser1),
    RunnableLambda(lambda x: "Could not find sentiment"),
)

Main_chain = Classifier | branch_chain
Result = (Main_chain.invoke({"feedback" : "This University seems like heaven"}))
print(Result)

