import time
import threading
import rospy
from qt_robot_interface.srv import *
from qt_gesture_controller.srv import *

class QTRobotClass():

    def __init__(self):
        self.liveLoopCheck=False
        self.liveLoopRunning=False
        self.faceLoopCheck=False

        self.facelessTalker= rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        self.animator=  rospy.ServiceProxy('/qt_robot/gesture/play', gesture_play)
        self.talker=  rospy.ServiceProxy('/qt_robot/behavior/talkText', behavior_talk_text)
        self.listener= None
        self.player=  rospy.ServiceProxy('/qt_robot/audio/play', audio_play)
        self.face= rospy.ServiceProxy('/qt_robot/emotion/show', emotion_show)
        toTurkish= rospy.ServiceProxy('/qt_robot/speech/config', speech_config)
        
        rospy.wait_for_service('/qt_robot/emotion/show')

        toTurkish.call("tr_TR",0,0)
        
    def ListenRobot(self,options):
        print("Robot Listen called:")
        self.player('siri','/home/developer')
        if False:
            text= self.speech.main()
            return text
        else:
            text = self.listener({'language':'en_US','options':options,'timeout':10})['transcript']
            return text

    def GestureRobot(self, message):
        self.animator(message, 0)
    def GestureRobotWithSpeed(self, message, speed):
        self.animator(message,speed)
    def TalkRobot(self, message):
        self.talker(message)
    def TalkWithoutFace(self, message):
        self.facelessTalker(message)
    def EndRobot(self):
        # self.client.close()
        pass



    def liveLoop(self):
        print("Live loop started")
        while self.liveLoopCheck:   
            self.liveLoopRunning=True
            self.GestureRobot('ozyegin.edu/liveloop')
            self.liveLoopRunning=False
            time.sleep(1)

    def faceLoop(self):
        print("Face loop started")
        while self.faceLoopCheck:
            self.showFace('QT/talking')
            time.sleep(1)

    def showFace(self,faceName):
        self.face(faceName)


    def first_recipe_aSyncRobotController(self, talkText, GestureName,GestureName2 ,speed, delay):
        talkThread = threading.Thread(target=self.TalkRobot, args=(talkText,))
        gestureThread = threading.Thread(
            target=self.GestureRobotWithSpeed, args=(GestureName, speed,))
        gestureThread2 = threading.Thread(
            target=self.GestureRobotWithSpeed, args=(GestureName2, speed,))
        gestureThread.start()
        time.sleep(delay)
        talkThread.start()

        gestureThread.join()
        gestureThread2.start()
        talkThread.join()
        gestureThread2.join()

    def aSyncRobotController(self, talkText, GestureName, speed, delay):
        talkThread = threading.Thread(target=self.TalkRobot, args=(talkText,))
        gestureThread = threading.Thread(
            target=self.GestureRobotWithSpeed, args=(GestureName, speed,))
        gestureThread.start()
        time.sleep(delay)
        talkThread.start()
        talkThread.join()
        gestureThread.join()
    
    def aSyncRobotControllerWithFace(self, talkText, GestureName,faceName):
        talkThread = threading.Thread(target=self.TalkWithoutFace, args=(talkText,))
        gestureThread = threading.Thread(
            target=self.GestureRobot, args=(GestureName,))
        faceThread = threading.Thread(
            target=self.showFace, args=(faceName,))
        
        faceloopThread = threading.Thread(target=self.faceLoop)
        faceThread.start()

        gestureThread.start()
        talkThread.start()

        faceThread.join()
        self.faceLoopCheck=True
        faceloopThread.start()
        talkThread.join()
        self.faceLoopCheck=False
        gestureThread.join()


def main():
    robot = QTRobotClass()

    robot.aSyncRobotControllerWithFace("türkçe test","ozyegin.edu/startrecoring4","QT/happy")
    print("talk end")


if __name__ == "__main__":

    main()
