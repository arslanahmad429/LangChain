from langchain_google_genai import ChatGoogleGenerativeAI 
from openai import vector_stores
from youtube_transcript_api import YouTubeTranscriptApi , TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
load_dotenv()
video_id= "_CRIPwLLATg"
try:
    yt = YouTubeTranscriptApi()
    transcript_list = yt.fetch(video_id , languages = ["en"])
    transcript = " ".join(chunk.text for chunk in transcript_list)
    splitter = RecursiveCharacterTextSplitter(chunk_size = 1000 , chunk_overlap = 100)
    chunks = splitter.split_text(transcript)
    print(chunks)
except TranscriptsDisabled:
    print("No captions Available for this video")
    retriever = vector_stores.as_retriever(search_type="similarity",search_kwargs = { "k": 4 })
    retriever.invoke(" WHat is this ebay")