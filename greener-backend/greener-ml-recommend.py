import sys
import random
import pprint
import numpy as np
import requests
import json 
from collections import defaultdict

class BanditModel:
    def __init__(self, eventPool, userPreference, userEventScoreMatrix):
        self.eventPool = eventPool
        self.userPreference = userPreference
        self.userEventScoreMatrix = userEventScoreMatrix
        for event in eventPool:
            if(event not in userEventScoreMatrix):
                self.userEventScoreMatrix[event] = dict()
                self.userEventScoreMatrix[event]["userScore"] = self.eventMatchingScore(self.userPreference, eventPool[event]["attributes"])
                self.userEventScoreMatrix[event]["userRecommendCount"] = 0
            
    def recommend(self, n, offset):
        totalGet = n + offset
        randomTopEventCount = random.randint(0, totalGet)
        
        sortedEventScores = sorted(self.userEventScoreMatrix.items(), key=lambda x: x[1]["userScore"], reverse=True)
        
        result = []
        
        result.extend(sortedEventScores[:randomTopEventCount])
        result.extend(random.sample(sortedEventScores[randomTopEventCount:], totalGet - randomTopEventCount))

        result = result[offset:]

        for selectedEvent in result:
            self.userEventScoreMatrix[selectedEvent[0]]["userRecommendCount"] += 1
            
        return result       
    
    def eventMatchingScore(self, userPreference, event):
        score = 0
        for attr in userPreference:
            score = score + (userPreference[attr] * event[attr])
        return score
    
    def updateUserActionOnEvent(self, event, userAction):
        targetEventScoreMatrix = self.userEventScoreMatrix[event]
        
        if userAction == "LIKE":
            addScore = 2
        elif userAction == "ATTEND":
            addScore = 5
        
        n = targetEventScoreMatrix["userRecommendCount"]
        
        targetEventScoreMatrix["userScore"] += ( (1 / n) * (addScore - targetEventScoreMatrix["userScore"]))
        
        return targetEventScoreMatrix["userScore"]
        
    def getUserEventScoreMatrix(self):
        return self.userEventScoreMatrix
    
    def __repr__(self):
        return pprint.pformat(self.getUserEventScoreMatrix())
    
class GreenerRLModel:
    def __init__(self):
        self.user = {}
        self.events = dict()
        self.userScore = {}
        
    def initialize(self, eventPool, user):
        self.events = eventPool
        self.user = user
        self.userScore = BanditModel(self.events, user["attributes"], user["eventScores"])
    
    def recommend(self, n, offset):        
        recommendations = self.userScore.recommend(n, offset)
        
        for recommendation in recommendations:
            if("recommendCount" in self.events[recommendation[0]]):
                self.events[recommendation[0]]["recommendCount"] += 1
            else:
                self.events[recommendation[0]]["recommendCount"] = 1

        self.user["eventScores"] = self.userScore.getUserEventScoreMatrix()
        
        return list(map(lambda eventRev: self.events[eventRev[0]], recommendations))
    
    def updateUserFeedback(self, eventFeedbackMap):
        bandit = self.userScore
        
        for eventFeedback in eventFeedbackMap:
            userOldEventScore = bandit.getUserEventScoreMatrix()[eventFeedback]
            
            userNewEventScore = bandit.updateUserActionOnEvent(eventFeedback, eventFeedbackMap[eventFeedback])
            
            self.events[eventFeedback]["score"] += userNewEventScore
            self.events[eventFeedback]["score"] += userOldEventScore
            
            if eventFeedbackMap[eventFeedback] == "LIKE":
                self.user["likedEvents"][eventFeedback] = self.events[eventFeedback]
            elif eventFeedbackMap[eventFeedback] == "ATTEND":
                self.user["attendedEvents"][eventFeedback] = self.events[eventFeedback]

        self.user["eventScores"] = self.getUserEventScoreMatrix()
            
    def getEvents(self):
        return self.events
    
    def getUser(self):
        return self.user
        
    def getUserScore(self):
        return self.userScore

def updateItems(itemList):
    for item in itemList:
        putDict = {
            "doc": itemList[item]
        }        
        putParam = json.dumps(putDict)
        headers = {"Content-Type": "application/json"}
        resp = requests.put("https://fcd54591.us-south.apigw.appdomain.cloud/update-event", data=putParam, headers=headers)

def updateUser(user):
    putDict = {
        "doc": user
    }
    putParam = json.dumps(putDict)
    headers = {"Content-Type": "application/json"}
    resp = requests.put("https://us-south.functions.appdomain.cloud/api/v1/web/6715ac50-fa50-4b71-bde4-975607b56165/greener-ml/update-user", data=putParam, headers=headers)

def main(param):
    
    response = requests.get("https://fcd54591.us-south.apigw.appdomain.cloud/list")
    
    baseParam = response.json()
    
    userPostDict = {
        "id": param["userid"]
    }        
    userPostParam = json.dumps(userPostDict)
    headers = {"Content-Type": "application/json"}
    resp = requests.post("https://us-south.functions.appdomain.cloud/api/v1/web/6715ac50-fa50-4b71-bde4-975607b56165/greener-ml/get-user-details", data=userPostParam, headers=headers)

    baseUser = resp.json()
    
    eventPool = {}
    
    for item in baseParam["rows"]:
        eventPool[item["doc"]["_id"]] = item["doc"]
        
    model = GreenerRLModel()

    model.initialize(eventPool, baseUser)

    offset = int(param["offset"])
    numberOfEvent = int(param["numEvent"])

    recommendation = model.recommend(numberOfEvent, offset)
    
    updateUser(model.getUser())
    updateItems(model.getEvents())
    
    result = {
        "recommendations": recommendation,
        "updatedUsers": model.getUser(),
        "updatedEvents": model.getEvents(),
        "numEvents": len(model.getEvents())
    }
        
    return result
