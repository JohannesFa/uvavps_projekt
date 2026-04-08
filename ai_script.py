import os.path
import ollama
import pandas as pd

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
    file_out.close

