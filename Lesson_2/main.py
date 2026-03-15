import requests # pip install requests
import os
import json

PARAMS_FILE_PATH = "params.json"
params = { "lang": "", "count": 0 }

def getParamsFromFile():
    global params
    if os.path.exists(PARAMS_FILE_PATH):
        with open(PARAMS_FILE_PATH, "r") as file:
            params = json.loads(file.read())

def getParamsFromConsole():
    global params
    params["count"] = int(input("Скільки фактів вивести? "))
    params["lang"] = input("Оберіть мову (ukr, eng, ger):")
    with open(PARAMS_FILE_PATH, "w") as file:
        file.write(json.dumps(params))


if os.path.exists(PARAMS_FILE_PATH):
    getParamsFromFile()
    if input(f"Отримати {params['count']} фактів мовою {params['lang']}? (y / n):").lower() == "n":
        getParamsFromConsole()
else:
    getParamsFromConsole()

response = requests.get(f"https://meowfacts.herokuapp.com/", params)

if response.ok:
    json = response.json()
    facts = json["data"]

    print("Цікаві факти про котів: ")
    for fact in facts:
        print(f' — {fact}')
else:
    response.raise_for_status()

'''
    Зробити так, щоб програма не брала мову з файлу автоматично, а пропонувала користувачу використати
    цю мову або обрати іншу. Наприклад:
    
    Отримати факти мовою ukr? (так / ні): ні
    Оберіть мову (ukr, eng, ger): ...
'''