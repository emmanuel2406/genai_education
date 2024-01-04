import os
import openai

openai.api_type = "azure"
openai.api_base = "https://fasgaica-openai-canadaeast.openai.azure.com/"
openai.api_version = "2023-07-01-preview"

# Manually read .env file
with open('../.env', 'r') as file:
    for line in file:
        key, value = line.strip().split('=', 1)
        os.environ[key] = value

openai.api_key = os.getenv("OPENAI_API_KEY")


system_message = "You are a multiple choice quiz generator for college students"
topic = "why AI will pose a threat in the next 10 years"
extra_context = "None"
prompt = f"Generate a multiple choice quiz with 2 questions on {topic}. Each question should have 4 choices. The quiz should have the following requirement:{extra_context}"
message_text = [{"role":"system","content":system_message},{"role":"user","content":prompt}]

completion = openai.ChatCompletion.create(
  engine="gpt-4",
  messages = message_text,
  temperature=0.7,
  max_tokens=800,
  top_p=0.95,
  frequency_penalty=0,
  presence_penalty=0,
  stop=None
)

print(completion.choices[0].message["content"])