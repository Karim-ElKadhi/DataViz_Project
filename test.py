import pandas as pd
import json
import os
from utils.analyse import DataAnalyzer
from utils.prompt import GeminiService
from dotenv import load_dotenv
load_dotenv()
data_analyzer = DataAnalyzer()
gemini_service = GeminiService(api_key=os.getenv("GROQ_API_KEY"))
df = pd.read_csv('Housing.csv')
current_dataset = df
analysis = data_analyzer.analyze_dataset(df)

proposals = gemini_service.generate_visualization_proposals(
            question="donne moi la répartition des maisons par nombre de chambres",
            dataset_info=analysis,
            columns=list(current_dataset.columns)
        )
print("Proposals from Gemini API:", proposals)