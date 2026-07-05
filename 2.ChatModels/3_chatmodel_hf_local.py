from langchain_huggingface import ChatHuggingFace , HuggingFacePipeline
llm = HuggingFacePipeline.from_model_id(
    model_id = "TinyLlama/TinyLlama-1.18-Chat-v1.0",
    task = "text-generation",
    pipeline_kwargs = dict(
        temperature = 0.7,
    ),
)

model = ChatHuggingFace( llm = llm )
result = model.invoke("What is the Capitl of Pakistan")
print(result.content)