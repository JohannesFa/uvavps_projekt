import ollama
from ollama import chat, ChatResponse
import pandas as pd
from pandas import DataFrame

models_list = ['falcon3:1b', 'qwen3.5:0.8b']
systemprompt = "\n".join(open("systemprompt.txt", "r").readlines())
questionsdf: DataFrame = pd.read_csv("questions.csv",delimiter=";")

def compare_answers(model_reply:str, expected_answer:str):
    if "answer:" in model_reply.lower():
        model_answer = model_reply.split("Answer:")[1].strip()[:1].strip()
        print(f"Model answer is {model_answer} expected is {expected_answer}")
        if model_answer == expected_answer.strip():
            return True
        else:
            return False
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
    response: ChatResponse = chat(model=model, messages=[
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

def test_all_models(models_list: list, df : DataFrame) :
    for model in models_list:
        run_model(model, df)

def run_model(model: str, df: DataFrame):
    with open(f"res_{model.replace(":","_")}.csv", "w+") as file:
        file.write(f"{model},\n")

        for row in df.iterrows():
            question = row[1]["Question"]
            available_answers = row[1]["Possible Answers"]
            correct_answer = row[1]["Answer"]
            message = f" Question : {question}, Possible answers: {available_answers}"
            print(message)
            ai_reply = askQuestion(msg=message, model=model).replace("\n", " ")
            print(ai_reply)
            file.write(f"{ai_reply},")
            file.write(str(compare_answers(ai_reply,correct_answer)))
            file.write("\n")
            file.flush()




    




if __name__ == "__main__":

    check_if_models_exist(models_list)

    questionsdf: DataFrame = pd.read_csv("questions.csv",delimiter=";")
    
    run_model(models_list[0],questionsdf)
    """
    for row in questionsdf.iterrows():
        #print(row)
        #print("\n")
        question = row[1]["Question"]
        print(f"Question is {question}, expected answer is {""}")
        
        #print(askQuestion("What color is the sky?", models_list[0]))
"""