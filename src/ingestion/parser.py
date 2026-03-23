import json
import ast
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from src.config import Config


class DocumentParser:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=Config.MODEL_NAME,
            google_api_key=Config.GEMINI_API_KEY,
            temperature=0
        )

    def extract_graph_from_text(self, text: str, filename: str):
        #  SAFETY CHECK: Did the PDF reader actually find words?
        if not text or len(text.strip()) < 10:
            print(f"      ⚠️ WARNING: No text was extracted from {filename}. The PDF reader failed to read the file.")
            return {"nodes": [], "edges": []}

        print(f"       Success: Extracted {len(text)} characters from document. Analyzing...")

        prompt_template = """
        You are a Data Extraction Assistant. Extract a Knowledge Graph from the text below.

        GOAL: Map organizational structures, ownership, and financial transactions.

        RULES:
        1. Extract entities: 'Person', 'Company', 'BankAccount', 'Email'.
        2. Extract relationships: 'OWNS', 'DIRECTOR_OF', 'TRANSFERRED_MONEY', 'SENT_EMAIL_TO'.

        CRITICAL: Your response MUST be valid JSON. Double-quote all property names.

        OUTPUT FORMAT:
        {{
            "nodes": [
                {{"id": "Exact Name", "type": "Person", "properties": {{"role": "CEO"}}}}
            ],
            "edges": [
                {{"source": "Name1", "target": "Name2", "type": "TRANSFERRED_MONEY", "properties": {{"amount": "10000"}}}}
            ]
        }}

        TEXT TO ANALYZE:
        {text}
        """

        prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
        chain = prompt | self.llm

        try:
            response = chain.invoke({"text": text[:30000]})

            #  FORMAT FIX: Safely pull the text out of Gemini's new list format
            raw_output = response.content
            if isinstance(raw_output, list):
                raw_text = "".join([block.get("text", "") for block in raw_output if isinstance(block, dict)])
            else:
                raw_text = str(raw_output)

            parsed_dict = self._parse_to_dict(raw_text)
            return parsed_dict

        except Exception as e:
            print(f"       Parser Error on {filename}: {e}")
            return {"nodes": [], "edges": []}

    def _parse_to_dict(self, text):
        text = str(text).strip()
        start = text.find('{')
        end = text.rfind('}')

        if start != -1 and end != -1:
            clean_text = text[start:end + 1]
        else:
            return {"nodes": [], "edges": []}

        try:
            return json.loads(clean_text)
        except:
            pass

        try:
            return ast.literal_eval(clean_text)
        except:
            pass

        return {"nodes": [], "edges": []}