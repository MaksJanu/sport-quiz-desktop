import json
from datetime import datetime


#Stworzenie funkcji do zapisu czasu i scorea wraz z sortowaniem
def write_to_json(points, level):
    # Sprawdzanie, czy plik JSON już istnieje
    try:
        with open('score.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        # Jeśli plik nie istnieje, tworzymy nowy pusty słownik
        data = {"rekordy": []}

    # Pobieranie aktualnej daty oraz czasu
    now = datetime.now()
    time = now.strftime("%H:%M:%S")

    # Dodawanie nowego rekordu z czasem i punktacją
    new_record = {
        "czas": time,
        "punktacja": points,
        "poziom trudnosci": level,
    }
    # Dodawanie nowego rekordu do listy rekordów
    data["rekordy"].append(new_record)

    # Zapisywanie danych z powrotem do pliku JSON
    with open('score.json', 'w') as file:
        json.dump(data, file, indent=2)


#Funkcja do sortowania score.json po wynikach malejaca
def sort_records_by_points():
    try:
        with open('score.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("Brak pliku z danymi.")
        return

    # Pobranie listy rekordów
    records = data.get("rekordy", [])

    # Sortowanie bąbelkowe rekordów według punktacji
    n = len(records)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if records[j]["punktacja"] < records[j + 1]["punktacja"]:
                # Zamiana miejscami, jeśli punktacja jest w niewłaściwej kolejności
                records[j], records[j + 1] = records[j + 1], records[j]

    # Aktualizacja danych w słowniku
    data["rekordy"] = records

    # Zapisywanie posortowanych danych z powrotem do pliku JSON
    with open('score.json', 'w') as file:
        json.dump(data, file, indent=2)