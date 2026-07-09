from langchain_core.tools import StructuredTool
from pydantic import BaseModel , Field

class MultiplyInput(BaseModel):
    a: int = Field(description = "First number")
    b: int = Field(description = "Second number")

def Multiply_func(a : int , b : int) -> int:
    return a * b

multiply_tool = StructuredTool.from_function(
    func = Multiply_func,
    name = "Multiply",
    description = "Multiply two numbers",
    args_schema = MultiplyInput
)
Result = multiply_tool.invoke({'a':3 , 'b':4})
print(Result)
print(multiply_tool.name)
print(multiply_tool.description)
print(multiply_tool.args_schema)