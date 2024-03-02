from utils import OpenAIAgent
from firebase_connect import FirebaseConnect
import _G
if __name__=="__main__":
    firebaseconnect = FirebaseConnect()
    firebaseconnect.firebase_init()
    firebaseconnect.get_menus()
    openai_agent = OpenAIAgent()
    openai_agent._set_system()  
    while True:
        q = input("User: ")
        msg = openai_agent._get_chat_completion(q)
        print("msg", msg)
    