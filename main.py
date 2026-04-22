from urllib import response
from openai import OpenAI

import ollama
from ollama import Client
import pandas as pd
from tqdm import tqdm
import time
import csv

useOpenAiApi = True

if useOpenAiApi:
    client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="lm-studio")
    installed_models = client.models.list()
    def ask_question(msg:str, model:str, sys_prompt:str) -> None | str:
        #max_tokens=2048,
        response = client.chat.completions.create(
            model=model,
            reasoning_effort=None,
            messages=[
                {
                    'role': 'system',
                    'content': sys_prompt
                }
                ,
                {
                    'role': 'user',
                    'content': msg,
                },
            ]
        )
        return response.choices[0].message.content
else:
    client = Client(host="127.0.0.1:11434")
    installed_models_client = client.list()
    
        
    def ask_question(msg:str, model:str, sys_prompt:str) -> str:
        response = client.chat(model=model, think=False, options={'num_ctx': 8192, 'num_predict': 2048}, messages=[
            {
                'role': 'system',
                'content': sys_prompt
            }
            ,
            {
                'role': 'user',
                'content': msg,
            },
            ])
        return getattr(response.message,'content',"")




#models_list = ['falcon3:1b', 'qwen3.5:0.8b', 'gemma4:e2b']
models_list = ['google/gemma-4-e4b']
system_prompt = "\n".join(open("systemprompt.txt", "r").readlines())


def compare_answers(model_reply:str, expected_answer:str):
        reply = model_reply.lower()
        if "answer:" in reply:
            last_answer = reply.rsplit("answer:", maxsplit=1)
            answer = last_answer[1].strip()[:1]
            #tqdm.write(f"Model answer is {model_answer} expected is {expected_answer}")
            return answer , answer == expected_answer.strip().lower()
        else:
            return '' , False


def check_if_models_exist(model_list: list) :
    global installed_models_client
    installed_models = []
    if useOpenAiApi:
        for x in installed_models_client.data:
            installed_models.append(x.id)
    else:
        for x in installed_models_client['models']:
            installed_models.append(x['model'])
    found_not_installed_model = False
    missing_models = []
    for model in model_list:
        if model not in installed_models:
            missing_models.append(model)
            found_not_installed_model = True

    if found_not_installed_model:
        print(f"Exiting because all models not installed \n The following models weren't found: \n {missing_models}")
        exit()
            


def test_all_models(models: list, df : pd.DataFrame) :
    for model in tqdm(models):
        run_model(model, df)

def run_model(model: str, df: pd.DataFrame):
    with open(f"res_{model.replace(":","_").replace("/","_")}.csv", "w+", encoding='utf-8-sig', newline='') as file:
        headers = ['Model Correct','Parsed Answer', 'Whole Answer','Domain','Time taken']
        writer = csv.writer(file, delimiter='|')
        writer.writerow(headers)

        for row in tqdm(df.iterrows(),total=len(df), desc=model):
            question = row[1]["question"]
            available_answers = f"A: {row[1]["choice_A"]} B: {row[1]["choice_B"]} C: {row[1]["choice_C"]} D: {row[1]["choice_D"]}"
            correct_answer = row[1]["correct_answer"]
            domain = row[1]["domain"]
            message = f" Question : {question}, Possible answers: {available_answers}"
            tqdm.write(message)
            start_time = time.perf_counter()
            ai_reply = ask_question(msg=message, model=model, sys_prompt=system_prompt).replace("\n", " ").replace(";",",").replace('|', ':').strip()
            end_time = time.perf_counter()
            tqdm.write(f"{ai_reply=}")
            extracted_answer, correct = compare_answers(ai_reply,correct_answer)
            next_line = [
                str(correct),
                extracted_answer,
                ai_reply,
                domain,
                end_time - start_time
            ]
            writer.writerow(next_line)
            file.flush()




    




if __name__ == "__main__":

    #check_if_models_exist(models_list)

    hp_questions: pd.DataFrame = pd.read_csv("questions.csv",delimiter=";")

    sat_questions: pd.DataFrame = pd.read_csv("sat_questions.csv")[['question','choice_A','choice_B','choice_C','choice_D','correct_answer','domain']]
    
    #test_all_models(models_list,hp_questions)
    run_model(models_list[0],sat_questions)
    """
    for row in questionsdf.iterrows():
        #print(row)
        #print("\n")
        question = row[1]["Question"]
        print(f"Question is {question}, expected answer is {""}")
        
        #print(askQuestion("What color is the sky?", models_list[0]))
"""
