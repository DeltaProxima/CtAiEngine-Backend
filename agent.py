from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
import os
from  dotenv import load_dotenv

load_dotenv()
model = ChatOpenAI(model="gpt-4o", openai_api_key=os.getenv("OPENAI_API_KEY"))

