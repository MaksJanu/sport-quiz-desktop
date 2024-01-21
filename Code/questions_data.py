import random
import requests
import html


def get_question_sets():
    response = requests.get(url="https://opentdb.com/api.php?amount=30&category=21&difficulty=easy&type=multiple")
    if response.status_code == 200:
        data = response.json()
        return data["results"]
    elif response.status_code == 404:
        return False


def get_question_with_answers(array):
    random_quest_index = random.randint(0,29)
    temp_index = random_quest_index
    question = html.unescape(array[temp_index]['question'])
    incorrect_answers = array[temp_index]["incorrect_answers"]
    correct_answer = html.unescape(array[temp_index]["correct_answer"])
    all_answers = [correct_answer] + incorrect_answers
    return {
        "question": question,
        "all_answers": all_answers,
        "correct_answer": correct_answer,
    }
sets = get_question_sets()
data = get_question_with_answers(sets)
print(data)
