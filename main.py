from ollama import chat, ChatResponse
import pandas as pd

models_list = ['falcon3:1b', 'qwen3.5:0.8b']

def run_model(model: str) :

    ollama_list = ollama.list()
    installed_models_list = []
    for x in ollama_list['models'] :
        installed_models_list.append(x['model'])
    if model not in installed_models_list:
        print(f"Model {model} not installed or misspelled")
        return
    file_out = open("results.csv", "w")
    file_out.write(f"{model},")
    file_out.close()

def askQuestion(question:str, model:str) -> str:
    response: ChatResponse = chat(model=model, think=False, messages=[
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