import tkinter as tk
from tkinter import scrolledtext
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')
faq_data = {
    "hello": "Hello! How can I help you with your CodeAlpha internship today?",
    "hi": "Hi there! Feel free to ask any questions about your internship.",
    "hey": "Hey! Need help with your CodeAlpha internship?",
    "how to submit tasks": "You need to upload your source code to GitHub and fill out the official Google Form shared in your WhatsApp group.",
    "what is the deadline": "The final submission deadline for this batch is 10th August 2026 at 11:59 PM.",
    "will i get a certificate": "Yes, you will get a QR-verified Completion Certificate and LOR if you complete at least 2 or 3 tasks before the deadline.",
    "how many tasks to complete": "You must complete a minimum of 2 or 3 tasks from your domain to be eligible for certificates.",
    "what if i miss the deadline": "If you miss the deadline, no extension will be provided, and you will NOT receive your Certificate or LOR.",
    "contact support": "You can message support on WhatsApp at +91 9555054118 or email services@codealpha.tech.",
    "bye": "Goodbye! All the best for your internship tasks!"
}

questions = list(faq_data.keys())
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    cleaned_tokens = [
        lemmatizer.lemmatize(token) for token in tokens 
        if token.isalnum() and token not in stop_words
    ]
    if not cleaned_tokens:
        return text.lower()
    return " ".join(cleaned_tokens)

preprocessed_questions = [preprocess_text(q) for q in questions]
def get_bot_response(user_query):
    user_query = user_query.strip().lower()
    if user_query in faq_data:
        return faq_data[user_query]
        
    processed_query = preprocess_text(user_query)
    
    vectorizer = TfidfVectorizer()
    all_texts = preprocessed_questions + [processed_query]
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    
    sim_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])[0]
    
    best_match_idx = sim_scores.argmax()
    highest_score = sim_scores[best_match_idx]
    
    if highest_score > 0.2:
        matched_question = questions[best_match_idx]
        return faq_data[matched_question]
    else:
        return "I am sorry, I don't have information on that. Please contact support at +91 9555054118."

# 4. Tkinter GUI
def send_message():
    user_text = user_entry.get()
    if user_text.strip() == "":
        return
    
    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, "You: " + user_text + "\n", "user")
    user_entry.delete(0, tk.END)
    
    bot_reply = get_bot_response(user_text)
    chat_box.insert(tk.END, "Bot: " + bot_reply + "\n\n", "bot")
    chat_box.config(state=tk.DISABLED)
    chat_box.yview(tk.END)

root = tk.Tk()
root.title("CodeAlpha AI - FAQ Chatbot")
root.geometry("450x500")
root.resizable(False, False)

chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, width=50, height=22, bg="#f4f6f9", font=("Arial", 10))
chat_box.pack(padx=10, pady=10)

chat_box.tag_config("user", foreground="#1a73e8", font=("Arial", 10, "bold"))
chat_box.tag_config("bot", foreground="#202124")

input_frame = tk.Frame(root)
input_frame.pack(fill=tk.X, padx=10, pady=5)

user_entry = tk.Entry(input_frame, font=("Arial", 11), width=35)
user_entry.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)
user_entry.bind("<Return>", lambda event: send_message())

send_button = tk.Button(input_frame, text="Send", bg="#1a73e8", fg="white", font=("Arial", 10, "bold"), command=send_message)
send_button.pack(side=tk.RIGHT, padx=5, pady=5)

chat_box.config(state=tk.NORMAL)
chat_box.insert(tk.END, "Bot: Hello! Welcome to CodeAlpha FAQ Chatbot. Ask me anything about deadlines, certificates, or submissions!\n\n", "bot")
chat_box.config(state=tk.DISABLED)

root.mainloop()
