from ollama import chat, ChatResponse
import pandas as pd

models_list = ['falcon3:1b', 'qwen3.5:0.8b']

def askQuestion(question:str, model:str) -> str:
    response: ChatResponse = chat(model='falcon3:1b', think=False, messages=[
    {
        'role': 'user',
        'content': question,
    },
    ])
    return response.message.content


questionsdf: pd.DataFrame = pd.read_csv("questions.csv",delimiter=";")

for question in questionsdf["Question"]:
    print(question)
    #print(askQuestion("What color is the sky?", models_list[0]))