import customtkinter as ctk
import tkinter as tk
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import random
from datetime import datetime 
import re


# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize lemmatizer and stopwords
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Function to preprocess user input
def preprocess(sentence):
    tokens = word_tokenize(sentence)
    tokens = [word.lower() for word in tokens if word.isalpha() and word not in stop_words]
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return tokens

class ChatBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Responsive Chatbot")
        self.root.geometry("800x600")
        self.root.configure(bg='#ffffff')

        # Header
        self.header = ctk.CTkLabel(self.root, text="Chatbot", font=("Montserrat", 24, "bold"), text_color="#ffffff", anchor="center")
        self.header.grid(row=0, column=0, columnspan=2, pady=(20, 10))

        # Sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self.root, width=200, corner_radius=10, fg_color="#2F365B")
        self.sidebar_frame.grid(row=1, column=0, rowspan=2, sticky="nswe", padx=(20, 10), pady=20)
        self.sidebar_frame.grid_rowconfigure(0, weight=1)
        self.sidebar_frame.grid_rowconfigure(1, weight=1)
        self.sidebar_frame.grid_rowconfigure(2, weight=1)
        self.sidebar_frame.grid_rowconfigure(3, weight=1)
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        # Clear Chat button at the bottom
        self.clear_button = ctk.CTkButton(self.sidebar_frame, text="Delete Chat", command=self.clear_chat, fg_color="#ff6666", hover_color="#ff4d4d")
        self.clear_button.grid(row=6, column=0, padx=20, pady=(10, 20), sticky="s")

        # Chat display area
        self.chat_display = ctk.CTkTextbox(self.root, width=560, height=400, wrap="word", corner_radius=10, fg_color="#ffffff", text_color="#050505", font=("Montserrat", 14,"bold"))
        self.chat_display.grid(row=1, column=1, padx=(10, 20), pady=20, sticky="nsew")
        self.chat_display.configure(state=tk.DISABLED)

        # User input frame
        self.input_frame = ctk.CTkFrame(self.root, fg_color="#2c2c2c")
        self.input_frame.grid(row=2, column=1, padx=(10, 20), pady=(0, 20), sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.user_input = ctk.CTkEntry(self.input_frame, width=400, corner_radius=10, fg_color="#4e4e4e", text_color="#ffffff")
        self.user_input.grid(row=0, column=0, padx=(20, 10), pady=10, sticky="ew")

        self.send_button = ctk.CTkButton(self.input_frame, text="Chat", command=self.send_message, fg_color="#4caf50", hover_color="#45a049")
        self.send_button.grid(row=0, column=1, padx=10, pady=10)

        self.user_input.bind("<Return>", lambda event: self.send_message())

    def send_message(self):
        user_message = self.user_input.get().strip()
        if user_message:
            self.display_message("User", user_message)
            bot_response = self.get_bot_response(user_message)
            self.display_message("Bot", bot_response)
            self.user_input.delete(0, tk.END)

    def display_message(self, sender, message):
        self.chat_display.configure(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{sender}: {message}\n\n", ("user" if sender == "User" else "bot"))
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.yview(tk.END)

    def get_bot_response(self, message):
        processed_input = preprocess(message)
        if 'hello' in processed_input or 'hi' in processed_input:
            return "Hello! How can I help you today?"
        elif 'bye' in processed_input or 'goodbye' in processed_input:
            return "Goodbye! Have a great day!"
        elif 'name' in processed_input:
            return "I am a simple chatbot created using Python and NLTK."
        elif 'favorite' in processed_input and 'color' in processed_input:
            return "My favorite color is blue. What's yours?"
        elif 'hobby' in processed_input or 'hobbies' in processed_input:
            return "I enjoy chatting with people like you!"
        elif 'thank' in processed_input or 'thank you' in processed_input:
            return "You're welcome! If you have any other questions, feel free to ask."
        elif 'help' in processed_input:
            return "I can assist you with simple queries. Ask me anything!"
        elif 'time' in processed_input:
            current_time = datetime.now().strftime("%H:%M:%S")
            return f"The current time is {current_time}."
        elif 'ability' in processed_input or 'abilities' in processed_input:
            return "I can chat with you, tell jokes, and perform simple arithmetic. How can I assist you today?"
        elif 'joke' in processed_input:
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Why was the math book sad? Because it had too many problems."
            ]
            return random.choice(jokes)
        elif 'fact' in processed_input:
            facts = [
                "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still edible.",
                "Bananas are berries, but strawberries aren't.",
                "An octopus has three hearts."
            ]
            return random.choice(facts)
        elif 'arithmetic' in processed_input or 'math' in processed_input:
            return "Sure! I can help with simple arithmetic. Try asking me to add, subtract, multiply, or divide two numbers."
        elif any(op in processed_input for op in ['add', 'subtract', 'multiply', 'divide']):
            try:
                result = self.perform_arithmetic(message)
                return f"The result is {result}."
            except Exception as e:
                return "Sorry, I couldn't perform the calculation. Please check your input and try again."
        else:
            return "I'm sorry, I don't understand that. Could you please rephrase?"

    def perform_arithmetic(self, message):
        message = message.lower()
        if 'add' in message:
            numbers = list(map(float, re.findall(r'\d+', message)))
            return sum(numbers)
        elif 'subtract' in message:
            numbers = list(map(float, re.findall(r'\d+', message)))
            return numbers[0] - sum(numbers[1:])
        elif 'multiply' in message:
            numbers = list(map(float, re.findall(r'\d+', message)))
            result = 1
            for num in numbers:
                result *= num
            return result
        elif 'divide' in message:
            numbers = list(map(float, re.findall(r'\d+', message)))
            if len(numbers) != 2:
                raise ValueError("Division requires exactly two numbers.")
            return numbers[0] / numbers[1]
        else:
            raise ValueError("Unknown arithmetic operation.")
    
    def change_theme(self, theme):
        ctk.set_appearance_mode(theme)

    def clear_chat(self):
        self.chat_display.configure(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.configure(state=tk.DISABLED)

if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")  # Modes: "System" (default), "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

    root = ctk.CTk()
    app = ChatBotApp(root)
    root.mainloop()
