from flask import Flask, request
from flask_cors import CORS, cross_origin
from endpoints import bulk, company, converse
from agents import ConversationAgent
from indicators import Indicators

import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


HOST = "192.168.0.131"
PORT = 5000

conversation_agents = {}

with open("company_stats.json", "r") as f:
	companies = json.loads(f.read())

indicators = Indicators()

conversation_agents = {
	c["id"]: ConversationAgent(company_info=c, company_indicators=indicators.calc_indicators(c)) for c in companies
}

conversation_agents["general"] = ConversationAgent(company_info={}, company_indicators={})

@app.get("/")
@cross_origin()
def home():
	return {"text": "text"}, 201

@app.get("/bulk")
@cross_origin()
def get_bulk():
	return bulk()

@app.get("/company/<id>")
@cross_origin()
def get_company(id:str):
	return company(int(id))

@app.post("/company/<id>/converse")
@cross_origin()
def conversation(id:str):
	question = request.json["question"]
	return converse(id, question, conversation_agents)

if __name__ == "__main__":
	app.run(HOST, PORT, debug=True)
