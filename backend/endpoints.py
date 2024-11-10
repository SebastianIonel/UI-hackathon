
import json
import time
from agents import ConversationAgent
from mock_data import *

MAX_TRIES = 15

# Mocked response data with previously returned responses
# For fast presentation

def bulk():
    time.sleep(2)
    return mock_bulk_data, 201
    # describer = DescribeAgent()

    # for _ in range(MAX_TRIES):
    #     response = describer.send_request("")
    #     try:
    #         content:str = response["content"]

    #         if content.startswith("```"):
    #             return json.loads(content[7: -4]), 201
            
    #         return json.loads(content), 201
    #     except:
    #         print("Retrying")
    #         print(response)
    #         time.sleep(0.5)
    
    # return {"error": "Couldn't reach OpenAI"}, 404

def company(id: int):
    time.sleep(1.5)
    
    try:
        return mock_data_companies[id], 201
    except:
        return {"error": "Invalid id"}, 404
    # analysis_agent = AnalysisAgent()

    # with open("company_stats.json", "r") as f:
    #     companies = json.loads(f.read())

    # for c in companies:
    #     if c["id"] == id:
    #         for _ in range(MAX_TRIES):
    #             response = analysis_agent.send_request(c["Company"])
    #             try:
    #                 company_indicators = Indicators().calc_indicators(c)
    #                 return {"text": response["content"], "companyInfo": c, "companyIndicators": company_indicators}, 201
    #             except:
    #                 print("Retrying")
    #                 time.sleep(0.5)            
        
    # return {"error": "No company with that id found"}, 404

def converse(id:str, question:str, conversation_agents: list[ConversationAgent]):
    if id == "general":
        response = conversation_agents[id].send_request(question)
        for _ in range(MAX_TRIES):
            response = conversation_agents[id].send_request(question)
            if "error" not in response:
                return {"response": response["content"]}, 201
            else:
                print("Retrying")
                time.sleep(0.5)

        return {"error": "Max tries exceeded"}, 404

    id = int(id)

    with open("company_stats.json", "r") as f:
        companies = json.loads(f.read())

    for c in companies:
        if c["id"] == id:
            for _ in range(MAX_TRIES):
                response = conversation_agents[id].send_request(question)
                if "error" not in response:
                    return {"response": response["content"]}, 201
                else:
                    print("Retrying")
                    time.sleep(0.5)
    
    return {"error": "Couldn't reach OpenAI"}, 404