import openai
# break up string output into questions and answers
def factorQuiz(response_message, num_questions=0):
    questions = []
    choices = []
    arr = response_message.split("$")
    arr = arr[1:]
    for question in arr:
        temp = question.split("|")
        qmark_index= temp[0].find("?")
        questions.append(temp[0][:qmark_index + 1])
        temp[0] = temp[0][qmark_index + 1:]
        choices.append(temp)
    # print("Questions:", questions)
    # print("Choices: ", choices)
    return zip(range(1, num_questions + 1), questions, choices)

# gpt prompter
def prompter(message_text):
    completion = openai.ChatCompletion.create(
            engine="gpt-4",
            messages=message_text,
            temperature=0.7,
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
    )
    return completion.choices[0].message["content"]

# used for showQuestions
def factorQuestions(response_message, num_questions = 0):
    questions = response_message.split('|')
    return zip(range(1, num_questions + 1), questions)