import ollama
from ollama import chat, ChatResponse
import pandas as pd

models_list = ['falcon3:1b', 'qwen3.5:0.8b']

def check_if_models_exist(model_list: list) :
    ollama_list = ollama.list()
    installed_models = []
    for x in ollama_list['models'] :
        installed_models.append(x['model'])


    found_not_installed_model = False
    for model in model_list:
        if model not in installed_models:
            print(f"Model {model} not installed or misspelled")
            found_not_installed_model = True
    if found_not_installed_model:
        print("Exiting beacuse all models not installed")
        exit()
            

def askQuestion(question:str, model:str) -> str:
    response: ChatResponse = chat(model=model, think=False, messages=[
    {
        'role': 'user',
        'content': question,
    },
    ])
    return response.message.content



if __name__ == "__main__":

    check_if_models_exist(models_list)

    questionsdf: pd.DataFrame = pd.read_csv("questions.csv",delimiter=";")

    for question in questionsdf["Question"]:
        print(f"Question is {question}, expected answer is {""}")
        
        #print(askQuestion("What color is the sky?", models_list[0]))
