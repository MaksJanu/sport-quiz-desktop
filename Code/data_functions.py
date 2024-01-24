import random
import html
import requests
import pandas as pd


#Pobieranie z API bazy pytan i odpowiedzi o sportach
def get_question_sets(difficulty):
    response = requests.get(url=f"https://opentdb.com/api.php?amount=15&category=21&difficulty={difficulty}&type=multiple")
    print("API Response:", response.text)
    if response.status_code == 200:
        data = response.json()
        if data["response_code"] == 0 and data["results"] != []:
            df = pd.DataFrame(data["results"])
            return df
        else:
            return 0
    elif response.status_code != 200:
        return 0


#Przygotowanie odpowiedzi i pytan
def preload_data(question_index, question_set, parameters):
    question = html.unescape(question_set["question"][question_index])
    correct_answer = html.unescape(question_set["correct_answer"][question_index])
    wrong_answers = question_set["incorrect_answers"][question_index]

    print("Question:", question)
    print("Correct Answer:", correct_answer)
    print("Wrong Answers:", wrong_answers)
    #Zastapienie formatowania dla znakow z uzyciem krotek, ale niestety czasami zle zastepuje i zastapilem to html.unescape
    # formatting = [
    #     ("#039", "'"),
    #     ("&", "'"),
    #     ("&quot;", '"'),
    #     ("&lt;", "<"),
    #     ("&gt;", ">"),
    # ]

    # #Zastapienie zlych znakow w stringach
    # for tuple in formatting:
    #     question = question.replace(tuple[0], tuple[1])
    #     correct_answer = correct_answer.replace(tuple[0], tuple[1])
    # #Zastapienia zlych znakow w listach
    #     for tuple in formatting:
    #         wrong_answers = [char.replace(tuple[0], tuple[1]) for char in wrong_answers]

    parameters["question"].append(question)
    parameters["correct"].append(correct_answer)
    #Scalenie wszystkich odpowiedzi i przetasowanie
    all_answers = wrong_answers + [correct_answer]
    random.shuffle(all_answers)
    #Dodawanie odpowiedzi do parameters
    for i in range(0, 4):
        parameters[f"answer{i+1}"].append(all_answers[i])

    return all_answers



#_________Testy_________

def test_get_question_sets():
    difficulty = "easy"
    result = get_question_sets(difficulty)
    assert isinstance(result, pd.DataFrame) or result == 0


def test_preload_data():
    question_index = 0
    question_set = {
        "question": ["What is the capital of France?"],
        "correct_answer": ["Paris"],
        "incorrect_answers": [["Berlin", "London", "Madrid"]]
    }
    parameters = {"question": [], "correct": [], "answer1": [], "answer2": [], "answer3": [], "answer4": []}
    
    all_answers = preload_data(question_index, question_set, parameters)

    assert len(all_answers) == 4
    assert len(parameters["question"]) == 1
    assert len(parameters["correct"]) == 1
    assert len(parameters["answer1"]) == 1
    assert len(parameters["answer2"]) == 1
    assert len(parameters["answer3"]) == 1
    assert len(parameters["answer4"]) == 1
    assert parameters["question"] == ["What is the capital of France?"]
    assert parameters["correct"] == ["Paris"]
    assert all_answers.count("Paris") == 1

