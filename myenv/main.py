from utils import *
from flask import Flask, render_template, request
import os
import openai

app = Flask(__name__)

# Manually read .env file
with open('../.env', 'r') as file:
    for line in file:
        key, value = line.strip().split('=', 1)
        os.environ[key] = value

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_type = "azure"
openai.api_base = "https://fasgaica-openai-canadaeast.openai.azure.com/"
openai.api_version = "2023-07-01-preview"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def generate_quiz():
    cleaned_quiz = []
    topic = "why AI will pose a threat in the next 10 years"
    num_questions = int(request.form.get('num-questions', 0))
    num_choices = int(request.form.get('num-choices', 0))
    transcript = request.form.get('transcript', topic)
    extra_context = request.form.get('extra-context', '')
    system_message = "You are a multiple choice quiz generator for college students"
    prompt = f"Generate a multiple choice quiz with {num_questions} questions based on the transcript '''{transcript}'''. Each question should have {num_choices} choices. The quiz should have the following requirement:{extra_context}."
    suffix = "Insert '|' BETWEEN each choice and '$' BEFORE every question. Append to the quiz the answer key in parentheses (A,B,C,B,A)"
    message_text = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt + suffix}
    ]
    response_message = prompter(message_text)
    cleaned_quiz = factorQuiz(response_message, num_questions)
    return render_template('index.html', quiz = cleaned_quiz)

@app.route('/questions', methods=['GET', 'POST'])
def show_questions():
    num_questions = int(request.form.get('num-questions', 0))
    student_questions = request.form.get('student-questions', '')
    system_message = "You are a question summarizer that can pinpoint common questions from multiple students"
    prompt = f"Identify {num_questions} questions that are key understanding question from the student questions:'''{student_questions}'''."
    suffix = "Insert '|' BETWEEN each question"
    message_text = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt + suffix}
    ]
    response_message = prompter(message_text)
    cleaned_questions = factorQuestions(response_message, num_questions)
    return render_template('index.html', questions = cleaned_questions)

if __name__ == '__main__':
    app.run(debug=True)


