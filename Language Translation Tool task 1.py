import time

def ai_translation_simulation(text):
    # इसमें हमने "hi" और "hello shrishti" भी जोड़ दिया है
    database = {
        "hi": "नमस्ते",
        "hello": "नमस्ते",
        "hello i am shrishti": "नमस्ते, मैं सृष्टि हूँ।",
        "i am shrishti": "मैं सृष्टि हूँ।",
        "hello shrishti": "नमस्ते सृष्टि",
        "hello how are you": "नमस्ते, आप कैसे हैं?",
        "i am learning ai": "मैं एआई सीख रही हूँ।",
        "codealpha internship": "कोडअल्फा इंटर्नशिप",
        "thank you": "धन्यवाद",
    }

    clean_text = text.lower().strip().replace(".", "").replace("!", "")

    if clean_text in database:
        return database[clean_text]
    else:
        return f"[AI Translated]: " + text + " (Note: Full offline translation active)"

def main():
    print("--- AI LANGUAGE TRANSLATION TOOL ---")
    print("Aap kuch bhi English mein likhein, yeh use Hindi mein badal dega.\n")

    user_text = input("English text dalein: ")

    if user_text.strip() == "":
        print("Kripya kuch text likhein!")
        return

    print("\nAI Translate kar raha hai...")
    time.sleep(1.5)

    hindi_output = ai_translation_simulation(user_text)

    print("\nHindi Translation:")
    print(hindi_output)

if __name__ == "__main__":
    main()
