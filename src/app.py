# server.py
# will handle ros too 
from flask import Flask, request
import requests
import json
from llmManager import initHistory, initPrompt, generatemessage
from RobotController import QTRobotClass
from easygoogletranslate import EasyGoogleTranslate
from time import sleep,time
import os 

AnythingtoTR = EasyGoogleTranslate(
source_language="auto",
target_language="tr")

#Custom defined gestures by the Ozyegin staff for the QT robot
gesturelist = {"annoyed" : "ozyegin.edu/Annoyed-1-1", 
               "annoyedShakingHead" : "ozyegin.edu/Annoyed-1-2", 
               "shortExplainWithHand" : "ozyegin.edu/content-1", 
               "shortExplainWithTwoHands" : "ozyegin.edu/content-2",
                "convincedlong" : "ozyegin.edu/convinced-1", 
                "convincedshort" : "ozyegin.edu/convinced-4", 
                "greeting" : "QT/show_QT", 
                "deny" : "ozyegin.edu/denyTest", 
                "dissatisfied" : "ozyegin.edu/dissatisfied-1", 
                "dissatisfiedstrict" : "ozyegin.edu/dissatisfied-2",
                "excitement" : "ozyegin.edu/excitement-1", 
                "frustrated" : "ozyegin.edu/frustrated-1", 
                "waitingForNewQuestion" : "ozyegin.edu/listen", 
                "headnode" : "ozyegin.edu/nodding", 
                "headnope" : "ozyegin.edu/nope",
                "neutral" : "ozyegin.edu/neutral"} 

global robot
global prompt
app = Flask(__name__)


NEON_GREEN = "\033[92m"
RESET_COLOR = "\033[0m"

# Corrects the incorrect translations from the google translate API
# Ceviriler={
#     "destekçisiyim":"tanıtımcısıyım",
#     "organizatörüyüm":"tanıtımcısıyım",
#     "destekçisi":"tanıtımcısı",
#     "organizatörü": "tanıtımcısı",
#     "organizatör": "tanıtımcı",
#     "destekçi": "tanıtımcı"}

@app.route('/conversation', methods=['POST'])
def receive_data():

    data = request.json

    print("whispher sent: " + data["context"] )
    
    response_data = {"message": "Data received", "data": data}

    response = generatemessage(data["context"], prompt)

    jsonResponse = response

    jsonResponse["answer"] = AnythingtoTR.translate(jsonResponse["answer"])
    jsonResponse["answer"]=jsonResponse["answer"].replace("tanıtımcısısın","tanıtımcısıyım")

    print(Fore.BLACK + "Translated: " + Fore.GREEN+ jsonResponse["answer"]+Fore.WHITE)

    jsonResponse["gesture"] = jsonResponse["gesture"].lower()

    if jsonResponse["gesture"]  not in gesturelist.keys():
        jsonResponse["gesture"] = "neutral"
    robot.aSyncRobotControllerWithFace(jsonResponse["answer"], gesturelist[jsonResponse["gesture"]], jsonResponse["emotion"])
    robot.GestureRobot("ozyegin.edu/neutral")

    with open("logs/log.log", "a",encoding='utf-8') as file:
        file.write(f'Time:{str(time())}\nQuestion:\t{data["context"]}\nAnswer:\t{jsonResponse["answer"]}\n\n')

    return 

if __name__ == '__main__':
    while True:
        try:
                
            robot = QTRobotClass()
            prompt = initPrompt()

            app.run(debug=True, port=3000, use_reloader=True)
        except:
            print("whoops error")

