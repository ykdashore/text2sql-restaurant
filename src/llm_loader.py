from langchain_google_genai import ChatGoogleGenerativeAI
import os

class LLMLoader:
    def __init__(self, model_provider):
        self.model_provider = model_provider

    def get_model(self):
        if self.model_provider.lower() == "google-gemini":

            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash-preview-09-2025",
                temperature=0,
                max_tokens=None,
                timeout=None,
                max_retries=2,
            )
            return llm
        
# TODO
# 1. add more llm providers and make the llm loader more flaxible