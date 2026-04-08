import ollama

ollama_list = ollama.list()
installed_models_list = []

for model in ollama_list['models']:
    installed_models_list.append(model['model'])
print(installed_models_list)