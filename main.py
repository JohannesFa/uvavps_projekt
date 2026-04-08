import ollama
from ollama import chat, ChatResponse
import pandas as pd

models_list = ['falcon3:1b', 'qwen3.5:0.8b']
systemprompt = "\n".join(open("systemprompt.txt", "r").readlines())
questionsdf: pd.DataFrame = pd.read_csv("questions.csv",delimiter=";")

def compare_answers(model_reply:str, expected_answer:str):
    if "Answer:" in model_reply:
        model_answer = model_reply.split("Answer:")[1].strip()[:1].strip()
        print(f"Model answer is {model_answer} expected is {expected_answer}")
        if model_answer == expected_answer.strip():
            return True
    else:
        return False



def check_if_models_exist(model_list: list) :
    ollama_list: list = ollama.list()
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
            

def askQuestion(msg:str, model:str) -> str:
    global systemprompt
    response: ChatResponse = chat(model=model, think='low', messages=[
    {
        'role': 'system',
        'content': systemprompt
    }
    ,
    {
        'role': 'user',
        'content': msg,
    },
    ])
    return response.message.content

def run_model(model: str, df: pd.DataFrame):
    file = open(f"res_{model.replace(":","_")}.csv", "w")
    file.write(f"{model},\n")  

    for row in df.iterrows():
        question = row[1]["Question"]
        available_answers = row[1]["Possible Answers"]
        message = f" Question : {question}, Possible answers: {available_answers}"
        print(message)
        ai_reply = askQuestion(msg=message, model=model)
        file.write(f"res_{model}.csv,\n")
    file.close()




    




if __name__ == "__main__":

    check_if_models_exist(models_list)

    questionsdf: pd.DataFrame = pd.read_csv("questions.csv",delimiter=";")
    
    run_model(models_list[1],questionsdf)
    """
    for row in questionsdf.iterrows():
        #print(row)
        #print("\n")
        question = row[1]["Question"]
        print(f"Question is {question}, expected answer is {""}")
        
        #print(askQuestion("What color is the sky?", models_list[0]))
"""
    ans = askQuestion("Beräkna värdet av (2/3) / (4/9).",models_list[0])
    
    print(ans)