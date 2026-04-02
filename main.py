from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()    # Daten aus .env Datei werden geladen
my_api_key = os.getenv("GROQ_API_KEY")

client = OpenAI(
    api_key= my_api_key,
    base_url= "https://api.groq.com/openai/v1")    # Muss NUR bei groq etc angegeben werden, nicht bei ChatGPT

MODEL_NAME = "llama-3.3-70b-versatile"    # Groß schreiben, weil es eine konstante ist (also eine Variable, die man nicht verändert)

# Kontext mit Systemprompt wird erstellt
system_anweisungen = {"role": "system", "content": "Du bist ein sarkastischer Roboter."}
nachrichten_verlauf = [system_anweisungen]

print("Bot gestartet!\nSchreibe 'ende' zum beenden.")
print("Bitte 'neu' eingeben, um einen neuen Chat zu starten.")

while True:
    user_input = input("Du: ")    # Unser Prompt

    if user_input.lower() == "ende":
        # print("Du hast die Unterhaltung beendet!")
        break
    # Kontext (Gedächtnis) löschen
    elif user_input.lower() == "neu":
        nachrichten_verlauf = [system_anweisungen]
        print("___ Gedächtnis gelöscht, alles zurück auf Anfang! ___")
        continue

    nachrichten_verlauf.append({"role": "user", "content": user_input})    # User-Antwort wird dem Verlauf hinzugefügt

    completion = client.chat.completions.create(
        model= MODEL_NAME,
        messages=nachrichten_verlauf
    )

    antwort = completion.choices[0].message.content

    print(f"Bot: {antwort}")
    nachrichten_verlauf.append({"role": "assistant", "content": antwort})    # Bot-Antwort wird dem Verlauf hinzugefügt

client.close()
print("Bot beendet! Bis zum nächsten Mal!")