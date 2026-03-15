from google import genai # pip install google-genai
from rich.console import Console # pip install rich
from rich.markdown import Markdown
from rules import rules_list

client = genai.Client()
console = Console()
print("Асистента запущено!\n")

while True:
    user_prompt = input(" >")
    if user_prompt.lower() == "exit": break

    prompt = (f"Виконай запит користувача: {user_prompt}.\n"
              f"При формулюванні відповіді виконуй наступні правила:\n{'\n'.join(rules_list)}")
    print(f"-----\n{prompt}\n-----")
    # Доступні моделі:
    # — gemini-3-flash-preview
    # — gemini-2.5-flash
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    # print(response.text)
    console.print(Markdown(str(response.text)))

'''
    Змінити програму таким чином, щоб після надання відповіді на запит
    у користувача була можливість ввести ще один запит.
   
    Зупиняти програму при введені ключового слова exit (або іншого на
    свій вибір).
'''