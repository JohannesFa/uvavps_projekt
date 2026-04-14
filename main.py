from email import message

import ollama
from ollama import Client
import pandas as pd
from pandas.core import missing
from tqdm import tqdm

client = Client(host="127.0.0.1:11434")

models_list = ['falcon3:1b', 'qwen3.5:0.8b', 'gemma4:e2b']
systemprompt = "\n".join(open("systemprompt.txt", "r").readlines())

def compare_answers(model_reply:str, expected_answer:str):
    if "answer:" in model_reply.lower():
        model_answer = model_reply.split("Answer:")[1].strip()[:1].strip()
        #tqdm.write(f"Model answer is {model_answer} expected is {expected_answer}")
        return model_answer == expected_answer.strip()
    else:
        return False



def check_if_models_exist(model_list: list) :
    ollama_list = client.list()
    installed_models = []
    for x in ollama_list['models'] :
        installed_models.append(x['model'])
    found_not_installed_model = False
    missing_models = []
    for model in model_list:
        if model not in installed_models:
            print(f"Model {model} not installed or misspelled")
            missing_models.append(model)
            found_not_installed_model = True

    if found_not_installed_model:
        print(f"Exiting because all models not installed \n The following models weren't found: \n {missing_models}")
        exit()
            

def ask_question(msg:str, model:str) -> str:
    global systemprompt
    response = client.chat(model=model, think=False, options={'num_ctx': 8192, 'num_predict': 2048}, messages=[
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
    return getattr(response.message,'content',"")

def test_all_models(models: list, df : pd.DataFrame) :
    for model in tqdm(models):
        run_model(model, df)

def run_model(model: str, df: pd.DataFrame):
    with open(f"res_{model.replace(":","_")}.csv", "w+", encoding='utf-8-sig') as file:
        file.write(f"sep=;\nModel_correct;Model_answer\n")

        for row in tqdm(df.iterrows(),total=len(df), desc=model):
            question = row[1]["Question"]
            available_answers = row[1]["Possible Answers"]
            correct_answer = row[1]["Answer"]
            message = f" Question : {question}, Possible answers: {available_answers}"
            #tqdm.write(message)
            ai_reply = ask_question(msg=message, model=model).replace("\n", " ").replace(";",",").strip()
            #tqdm.write(f"{ai_reply=}")
            compared = str(compare_answers(ai_reply,correct_answer))
            file.write(f"{compared};")
            file.write(f"{ai_reply}")
            file.write("\n")
            file.flush()




    




if __name__ == "__main__":

    #check_if_models_exist(models_list)

   #questions_df: pd.DataFrame = pd.read_csv("questions.csv",delimiter=";")

    sat_questions: pd.DataFrame = pd.read_csv("sat_questions.csv")[['question','choice_A','choice_B','choice_C','correct_answer','domain']]

    
    #test_all_models(models_list,questions_df)
    #run_model(models_list[2],questions_df)
    """
    for row in questionsdf.iterrows():
        #print(row)
        #print("\n")
        question = row[1]["Question"]
        print(f"Question is {question}, expected answer is {""}")
        
        #print(askQuestion("What color is the sky?", models_list[0]))
"""