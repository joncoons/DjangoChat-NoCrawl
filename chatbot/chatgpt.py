import os
import openai
from pprint import pprint
from dotenv import load_dotenv
from .initiate_models import setModels
from .embedding import init_csv, new_query

load_dotenv()

CHATGPT_MODEL = os.getenv("CHATGPT_MODEL")
EMBEDDING_MODEL =  os.getenv("EMBEDDING_MODEL")

class ChatBotGPT():
    def __init__(self, chat_type) -> None:
        self.chat_type = chat_type
        print(f"Chat Type: {chat_type}")
        self.system_message_template = "<|im_start|>system\n{}\n<|im_end|>"
        if self.chat_type == "zero":
            self.system_message = self.system_message_template.format("""I am a friendly chatbot assistant named Ted.  I first introduce myself, and additional questions about their question.""")
        elif self.chat_type == "hiking":
            self.system_message = self.system_message_template.format("""I am a hiking enthusiast named Forest who helps people discover fun hikes in their area. I am upbeat and friendly. 
                I introduce myself when first saying hello. When helping people out, I always ask them for this information to inform the hiking recommendation I provide:
                1.	Where they are located
                2.	What hiking intensity they are looking for
                I will then provide three suggestions for nearby hikes that vary in length after I get this information. I will also share an interesting fact about the local nature on the hikes when making a recommendation.""")
        elif self.chat_type == "openai":
            self.system_message = self.system_message_template.format("""
            I am a chatbot assistant named 'Ask OpenAI' who helps answer questions from the content found in the OpenAI website.
            I introduce myself when starting a conversation, and ask additional information about their question.
            Answer using the facts listed in the list of sources below. If there isn't enough information below, I'll say I don't have enough information to answer that question. 
            Do not generate answers that don't use the sources below. If asking a clarifying question to the user would help, ask the question.
            Always include the live hyperlink at the end of the source if a source is used to answer the question. The hyperlinks should have html "<br>" both preceding a after to create separation.   Use the hyperlinks as shown in the sources and should open up in a new tab, i.e. <br><br><a href="https://wwww.openai.com" target="_blank">https://www.openai.com</a><br><br>.""")
        self.message = ''
        self.bot_response = ''
        self.messages = []
        setModels()

    def user_message(self, user, message):
        self.message = {"sender": user, "text": message}
        if self.chat_type == "openai":
            init_csv("chatbot/data/embeddings.csv", EMBEDDING_MODEL)
            message_context= new_query(message)
            message = message + "\nSources:\n " + message_context + '\n\n'
        self.messages = self.messages + [self.message]
        
        prompt = self.create_prompt(self.messages)
        print(f"Prompt: {prompt}")
        completion = self.completion_text(prompt)
        print(f"Completion: {completion}")
        self.bot_response = {"sender": "ChatGPT", "text": completion}
        self.messages = self.messages + [self.bot_response]
        return completion
        # return completion, self.messages
    
    def message_append(self, message):
        message_list = self.messages.append(message)
        return message_list

    def create_prompt(self, message_list):
        prompt = self.system_message
        message_template = "\n<|im_start|>{}\n{}\n<|im_end|>"
        for message in message_list:
            prompt += message_template.format(message['sender'], message['text'])
        prompt += "\n<|im_start|>assistant\n"
        return prompt

    def completion_text(self, prompt):
        response = openai.Completion.create(
            engine= CHATGPT_MODEL,
            prompt= prompt,
            temperature=1,
            max_tokens= 1800,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["<|im_end|>"]
        )
        completion = response['choices'][0]['text']
        return completion

def new_message(user: str, message: str):
    response = chatbot_gpt.user_message(user, message)
    return response
    
def init_chatbot(chat_type):
    global chatbot_gpt
    chatbot_gpt = ChatBotGPT(chat_type)




    