import pandas as pd
import os, re

def compare_answers(model_reply:str, expected_answer:str):
        reply = model_reply.lower()
        if "answer:" in reply:
            pattern = re.compile(r"(?i)answer\s*:\s*[*_]*\s*([a-d])\s*[*_]*")
            #last_answer = reply.rsplit("answer:", maxsplit=1)
            #answer = last_answer[1].strip()[:1]
            #tqdm.write(f"Model answer is {model_answer} expected is {expected_answer}")
            answer = pattern.findall(reply)
            if len(answer) > 0:
                return answer[-1] , answer[-1] == expected_answer.strip().lower()
            
        return '' , False


def get_all_models_df():
    files = os.listdir()


    
    
    result_files = []
    for file in files:
        if re.search('res_.*\\.csv',file):
            result_files.append(file)
    
    pd_list: list[pd.DataFrame] = []
    for file in result_files:
        df = pd.read_csv(file,delimiter="|")
        pd_list.append(df)

    return pd_list, result_files
    

if __name__ == "__main__":
    models_df_list, model_names = get_all_models_df()
    
    sat_questions: pd.DataFrame = pd.read_csv("sat_questions.csv")[['question','choice_A','choice_B','choice_C','choice_D','correct_answer','domain']]
    

    dict_list = []

    correct_by_domain_list = []

    
    for model_index, model_df in enumerate(models_df_list):
        #print(model_df)
        model_name: str = model_names[model_index]
        new_model_name = model_name.replace("res_", "res-corrected-")
        print(new_model_name)

        new_df_list = []

        for lineIndex, line in enumerate(sat_questions.iterrows()):
            try:
                model_line = model_df.iloc[lineIndex]
                
            except IndexError as e:
                print(lineIndex)

            model_ans = model_line['Whole Answer']
            if not pd.notna(model_ans):
                model_ans = ""
                print(f"Found empty value at index {lineIndex}")
            #print(model_ans)
            extracted_ans, model_correct = compare_answers(model_ans,line[1]['correct_answer']) # 5 should be correct ans
            if model_correct != model_line['Model Correct']:
                pass
                # print(f"Found new value: {model_correct} at index {lineIndex} with new ans {extracted_ans}")
            
            new_model_line = model_line.copy()
            new_model_line['Model Correct'] = model_correct
            new_model_line['Parsed Answer'] = extracted_ans
            new_df_list.append(new_model_line)

        new_df = pd.DataFrame(new_df_list)
        new_df.to_csv(new_model_name, sep="|", index=False)
        
        

        #print(model_df[])