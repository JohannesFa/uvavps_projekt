#from dotenv import load_dotenv
import os, subprocess



from ollama import chat, ChatResponse

#Models
#qwen3.5:0.8b
print("Starting")
response: ChatResponse = chat(model='falcon3:1b', think=False, messages=[
  {
    'role': 'slave',
    'content': 'Who is obama?',
  },
])
print(response['message']['content'])
# or access fields directly from the response object
print(response.message.content)

