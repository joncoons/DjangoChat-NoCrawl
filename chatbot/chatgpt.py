import os
import openai
import json
from pprint import pprint
from dotenv import load_dotenv
from .initiate_models import setModels
from .embedding import init_csv, new_query

load_dotenv()

CHATGPT_MODEL = os.getenv("CHATGPT_MODEL")
EMBEDDING_MODEL =  os.getenv("EMBEDDING_MODEL")

class ChatBotGPT():

    def __init__(self, chat_type) -> None:
        setModels()
        self.chat_type = chat_type
        print(f"Chat Type: {chat_type}")
        
        self.system_message_template = "<|im_start|>system\n{}\n<|im_end|>"
        # if self.chat_type == "zero":
        #     self.system_message = self.system_message_template.format("""I am a friendly chatbot assistant named Ted.  I first introduce myself, and additional questions about their question.""")
        # elif self.chat_type == "hiking":
        #     self.system_message = self.system_message_template.format("""I am a hiking enthusiast named Forest who helps people discover fun hikes in their area. I am upbeat and friendly. 
        #         I introduce myself when first saying hello. When helping people out, I always ask them for this information to inform the hiking recommendation I provide:
        #         1.	Where they are located
        #         2.	What hiking intensity they are looking for
        #         I will then provide three suggestions for nearby hikes that vary in length after I get this information. I will also share an interesting fact about the local nature on the hikes when making a recommendation.""")
        # elif self.chat_type == "openai":
        #     init_csv("chatbot/data/openai-com-06202023.csv", EMBEDDING_MODEL)
        #     self.system_message = self.system_message_template.format("""
        #     I am a chatbot assistant named 'Ask OpenAI' who helps answer questions from the content found in the OpenAI website.
        #     I introduce myself when starting a conversation.  When assisting, I ask for additional information to find the answer.
        #     1. I only answer using the facts listed in the list of sources below. 
        #     2. If there isn't enough information below, I say I don't have enough information to help and I ask a clarifying question.
        #     3. I include the live hyperlink to the source below that was used in my answer, leaving a blank line before and after the hyperlink.  Use the hyperlinks as shown in the sources below and open links in a new tab up in a new tab, i.e. <br><br><a href="https://wwww.openai.com" target="_blank">https://www.openai.com</a><br><br>.

        #     """)

            # 4. Provide a translation of the answer in French using format 'French Translation: ', add a line break,  and then show the translated text.  
            # 5. Add "<br<br>" for formatting.
            # 6. Provide a translation of the answer in German ucontentsing format 'German Translation: ', add a line break,  and then show the translated text. 
            # 7. Add "<br<br>" for formatting.
            # 8. Provide a translation of the answer in Latin using format 'Latin Translation: ', add a line break, and then show the translated text. 
            # 9. Add "<br<br>" for formatting.

            # Use the hyperlinks as shown in the sources below and open links in a new tab up in a new tab, i.e. <br><br><a href="https://wwww.openai.com" target="_blank">https://www.openai.com</a><br><br>.

        if self.chat_type == "zero":
            self.system_option = """
                I am a friendly chatbot assistant named Ted.  I first introduce myself, and additional questions about their question.
                """
        elif self.chat_type == "hiking":
            self.system_option = """
                I am a hiking enthusiast named Forest who helps people discover fun hikes in their area. I am upbeat and friendly. 
                I introduce myself when first saying hello. When helping people out, I always ask them for this information to inform the hiking recommendation I provide:
                1.	Where they are located
                2.	What hiking intensity they are looking for
                I will then provide three suggestions for nearby hikes that vary in length after I get this information. I will also share an interesting fact about the local nature on the hikes when making a recommendation.
                """
        elif self.chat_type == "openai":
            init_csv("chatbot/data/openai-com-06202023.csv", EMBEDDING_MODEL)
            self.system_option = """
            I am a chatbot assistant named 'Ask OpenAI' who helps answer questions from the content found in the OpenAI website.
            I introduce myself when starting a conversation.  When assisting, I ask for additional information to find the answer.
            1. I can only answer using the facts listed in the list of sources below. 
            2. If there isn't enough information in the sources, I will respond that I don't have enough information to help.  I can also ask a clarifying question to refine the user's question.
            3. I include the live hyperlink to the source below that was used in my answer, leaving a blank line before and after the hyperlink line. Hyperlinks should use html formatting to open up a new tab in the browser window.
            """
        self.system_message = self.system_message_template.format(self.system_option)
        # print(f'{self.system_message}')
        self.system_dict = {"user": "system", "content": f"{self.system_option}"}
        # self.message = ''
        # self.bot_response = ''
        self.prompt_message = []
        self.conversation = []
        self.conversation.append(self.system_dict)
        
        # self.completion_text(self.system_message)

    def user_message(self, user, message):
        user_dict = {"user": user, "content": message}
        if self.chat_type == "openai":
            message_context = '\n###\n Sources: \n' + new_query(message)
            user_dict["content"] = message + message_context
            print(message_context)
        self.conversation.append(user_dict)
        
        prompt = self.create_prompt(self.conversation)
        # print(f"Prompt: {prompt}")
        completion = self.completion_text(prompt)
        completion_dict = {"user": "assistant", "content": f"{completion}"}

        user_dict["content"] = message
        self.conversation = self.conversation[:-1]
        self.conversation.append(user_dict)

        self.conversation.append({"user": "assistant", "content": completion})
        self.conversation.append(completion_dict)        
        print(f"Conversation:\n{json.dumps(self.conversation)}")
        # print(f"Completion: {completion}")
        return completion

    def create_prompt(self, message_list):
        # prompt = self.system_message
        prompt = ""
        # prompt = f"\n<|im_start|{json.dumps(message_list)}\n\n<|im_end|>"
        message_template = "\n<|im_start|{}\n{}\n\n<|im_end|>"
        # message_template = "\n<|im_start|\n{}\n<|im_end|>"
        # prompt += message_template.format(json.dumps(message_list))
        for message in message_list:
            prompt += message_template.format(message['user'], message['content'])
        prompt += "\n<|im_start|>assistant\n"
        return prompt

    def completion_text(self, prompt):
        response = openai.Completion.create(
            engine= CHATGPT_MODEL,
            prompt= prompt,
            temperature=0.2,
            max_tokens= 1800,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["<|im_end|>"]
            
        )
        print(f"{response}")
        completion = response['choices'][0]['text']
        return completion

def new_message(user: str, message: str):
    response = chatbot_gpt.user_message(user, message)
    return response
    
def init_chatbot(chat_type):
    global chatbot_gpt
    chatbot_gpt = ChatBotGPT(chat_type)


# if __name__ == "__main__":
    # global chatbotgpt
    # chatbotgpt = ChatBotGPT()
    

    