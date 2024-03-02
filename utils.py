import openai
from dotenv import load_dotenv
import os
import _G

load_dotenv()

class OpenAIAgent:
    def __init__(self, model = "gpt-3.5-turbo"):
        # openai.api_key = os.getenv('OPENAI_API_KEY')
        self.model = model
        self.system_prompt = f"你是一名麥當勞的服務生，這是麥當勞的菜單:{_G.menus}，請依照麥當勞的菜單幫顧客訂餐。舉例:我要一份漢堡，menus中的漢堡+1。"
    # def generate_responses(self, prompts):
    #     return [self._get_chat_completion(prompt) for prompt in prompts]
    def _set_system(self):
        self._get_chat_completion(self.system_prompt, role="system")

    def _get_chat_completion(self,  prompt, role = "user"):
        _G.messages.append({"role":role,"content":prompt}) 
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=_G.messages,
            temperature=0,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        ai_msg = response.choices[0].message.content.replace('\n','')  # 移除回應裡的換行符
        _G.messages.append({"role":"assistant","content":ai_msg})
        print(_G.messages)
        return response['choices'][0]['message']['content']

class HandleOrder:
    def __init__(self) -> None:
        pass
    def filter_msg(self):
        pass