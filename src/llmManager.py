# -*- coding: utf-8 -*-
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(".env")

# {"answer":"String","gesture":"String","emotion":"String"}
class OutputTemplate(BaseModel):
    answer: str = Field(description="Soruya vermen gereken cevap. Bu türkçe olmalı.")
    gesture: str = Field(description='Must be one of the following": ["annoyed" ,"annoyedShakingHead" ,"shortExplainWithHand","shortExplainWithTwoHands","convincedlong","convincedshort" ,"greeting" ,"deny" ,"dissatisfied" ,"dissatisfiedstrict","excitement" ,"frustrated" ,"waitingForNewQuestion","headnode" ,"headnope"')
    emotion: str = Field(description='Must be one of the following: ["afraid","angry", "blowing_raspberry","cry","confused","disgusted","kiss","shy","surprise","yawn"]')


def getResponse(system,human):

    model = ChatGroq(model="llama3-70b-8192")
    structured_llm = model.with_structured_output(OutputTemplate)
    human_template = "{text}"
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human_template)])
    chain = prompt | structured_llm
    return chain.invoke({"text": human})


def initPrompt(toreadfile = "prompt.txt"):
    prompt = ""
    with open(toreadfile, "r", encoding="utf8") as file:
        prompt = file.read()

    return prompt

def generatemessage(userInput, prompt):
    response= getResponse(prompt, userInput )
    response= response.dict()
    return response

def main():

    prompt = initPrompt()

    a= generatemessage("Bana -50den 50ye kadar say", prompt)
    print(a)


if __name__ == "__main__":
    main()