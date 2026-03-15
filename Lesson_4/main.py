import tkinter as tk
from tkinter import scrolledtext
from google import genai # pip install google-genai
from PIL import Image, ImageTk # pip install pillow
from rules import rules_list

client = genai.Client()

# Словник для зберігання емоцій
emotionImages = {}

# Завантаження емоцій з папки images
def load_emotions():
    # Емоція normal
    img = Image.open("images/normal.png")
    img = img.resize((75, 75), Image.LANCZOS)
    emotionImages['normal'] = ImageTk.PhotoImage(img)

    # Емоція thinking
    img = Image.open("images/thinking.png")
    img = img.resize((75, 75), Image.LANCZOS)
    emotionImages['thinking'] = ImageTk.PhotoImage(img)

# Встановити емоцію за назвою
def change_emotion(emotion):
    response_label.config(image=emotionImages.get(emotion))

# Виведення повідомлення з відповідним тегом у textbox
def print_message(text, tag="response"):
    response_textbox.configure(state=tk.NORMAL)
    response_textbox.insert("end", text + "\n", tag)
    response_textbox.configure(state=tk.DISABLED)
    response_textbox.see("end")

# Функція для виконання запиту
def onclick(event=None):
    try:
        user_prompt = prompt_entry.get()
        print_message(user_prompt + "\n", "prompt")
        prompt_entry.delete(0, tk.END)

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

        print_message(str(response.text) + "\n")
    except Exception as error:
        print(str(error))

# Створення та налаштування вікна
window = tk.Tk()
window.title("Візуальний асистент")
window.geometry("300x500")
window.resizable(True, True)
window.maxsize(600, 0)
window.minsize(300, 500)

# ПІДКЛЮЧЕННЯ ЕМОЦІЙ
load_emotions()
response_label = tk.Label()
change_emotion("normal")
response_label.pack(side="top", fill="x")

response_textbox = scrolledtext.ScrolledText(state=tk.DISABLED, wrap=tk.WORD)
response_textbox.pack(side="top", fill="both", expand=True)
response_textbox.tag_configure("response", foreground="gray", font=("Arial", 14, "italic"))
response_textbox.tag_configure("prompt", foreground="green", font=("Arial", 18, "bold"))

# Кнопка для відправки запиту
send_button = tk.Button(text="Відправити", command=onclick)
send_button.pack(side="bottom", fill="x")

# Поле для введення запиту
prompt_entry = tk.Entry()
prompt_entry.pack(side="bottom", fill="x")
prompt_entry.bind("<Return>", onclick)

window.mainloop()

