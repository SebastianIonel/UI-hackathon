from pydantic import BaseModel
from indicators import Indicators
import requests
import json

API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
API_KEY = "INSERT_API_KEY" 

class Agent(BaseModel):
	name: str = "Agent"
	model: str = "gpt-4o"
	instructions: str = "You are a helpful Agent"
	tools: list = []

	def build_question(self, question: str):
		return question

	def send_request(self, question: str):
		endpoint = API_ENDPOINT
		api_key = API_KEY

		# Header-ul pentru request
		headers = {
			"Content-Type": "application/json",
			"api-key": api_key,
		}

		# Datele pentru request
		data = {
			"temperature": 0.1,
			"messages": [
				{"role": "system", "content": self.instructions},
				{"role": "user", "content": self.build_question(question)}
			]
		}

		# Trimitere request
		response = requests.post(endpoint, headers=headers, json=data)

		# Afisare raspuns
		result = response.json()
		try:
			return result["choices"][0]["message"]
		except:
			return result

class ConversationAgent(Agent):
	name:str="Analysis agent"
	instructions:str="""You are a senior Financial Analyst /at a bank. If you are given 2 json objects, you are tasked with evaluating a company’s financial health. Considering
	the financial data I gave you, answer my questions or any misunderstanding in a
	friendly and professional manner. Your goal is to help me as a financial analyst. Also, do it in plaintext, not markdown and between 50 to 100 words.
	If you receive two empty json objects, behave like a Financial Analyst. And try to find a good loan plan for this customer and what would you recommend him to do ? Try to give exact numbers, like for example a loan for 1 year with 4% interest rate."""
	messages:str = []
	company_info:dict = {}
	company_indicators:dict = {}

	def build_question(self, question):
		return f"{self.company_info} {self.company_indicators} {question}"

	def send_request(self, question: str):
		endpoint = API_ENDPOINT # insert the provided endpoint here
		api_key = API_KEY # insert the provided api key here
		
		# Header-ul pentru request
		headers = {
			"Content-Type": "application/json",
			"Authorization": f"Bearer {api_key}"
		}

		self.messages.append(self.build_question(question))

		# Datele pentru request
		data = {
			"model": "gpt-4o",
			"temperature": 0.1,
			"messages": [
				{"role": "system", "content": self.instructions},
				*[{"role": "user", "content": question} for question in self.messages]
			]
		}

		# Trimitere request
		response = requests.post(endpoint, headers=headers, json=data)

		# Afisare raspuns
		result = response.json()
		try:
			return result["choices"][0]["message"]
		except:
			return result

class AnalysisAgent(Agent):
	name:str="Analysis agent"
	instructions:str="""You are a senior Financial Analyst at a bank, tasked with evaluating a company’s financial health. Using the provided
	financial indicators, Income Statement, and Balance Sheet, prepare a comprehensive, detailed report of approximately 1000 words. 
	Your analysis should include an in-depth assessment of the company’s performance, covering profitability, liquidity, efficiency, and leverage.
	Identify and explain three key strengths and three significant weaknesses that highlight the company’s overall financial position and potential 
	risks. Additionally, include recommendations for improvement or strategies to mitigate any identified risks. The tone should be professional and
	analytical, suitable for presentation to senior bank management. Also, where you think it is good, put 3 placeholder for graphs in format
	INSERT_GRAPH(name) where name needs to be one of these: ["pmt", "rniot", "llrot"], they derive from "Profit Margin Type", "Revenue and Net 
	Income Over Time" and "Liquidity and Leverage Ratios Over Time"]. Also instead of '$' write '\$' every time.
	I will give you 2 JSON objects. The first is a company's name and their info (number of employees and industry) and their financials. 
	In the second one, the same company is there, but with some financial indicators calculated."""

	def build_question(self, question: str):
		with open("company_stats.json", "r") as f:
			in_companies = f.read()
		
		companies_json = json.loads(in_companies)

		for c in companies_json:
			if c["Company"] == question:
				indicators = Indicators()
				company_indicator = indicators.calc_indicators(c)
				return f"{json.dumps(c)} {json.dumps(company_indicator)}"

class DescribeAgent(Agent):
    name:str="Description agent"
    instructions:str="""You are a senior Financial Analyst that works at a bank. Based on these [financial indicators / Income Statement and Balance
	Sheet], assign to each company a score depending on how high is the bank's risk / oportunity in mitigating losses / increasing profits.
	Also, suggest me whether this company needs support for avoiding crediting issues and which actions are more suitable. If the company is
	doing well, please suggest what kind of banking products and services could we provide to it. The number of employees of a company is not important.
	Also add new lines with '\\n' characters and other markdown formats where needed to make it prettier. Also instead of '$' write '\$' every time.
	I will give you 2 JSON objects. The first is a list of companies and their info (number of employees and industry) and their financials. 
	In the second one, the same companies are there, but with some financial indicators calculated. I need you to give me just the JSON list, 
	not in markdown format, just plain json, with every object having the following fields: 'id', 'Company': the name of the company, 'Description': a short 
	description of the company's financial stability and future forecasting between 50 and 100 words, 'NEmployees': the number of employees, 'Score', which will be a score you will give
	the company from -100 to 100 depending on how urgent the actions need to be. Also return them in sorted order of how urgent the actions are 
	(I mean -90 and 90 have the same priority), "Industry" which is the industry of the company and "RiskClass" which is determined by the score of the company. Possible values are
	"High Risk", "Medium Risk", "Low Risk", "High Opportunity", "Medium Opportunity", "Low Opportunity\". I need your response with plain json"""

    def build_question(self, question):
        with open("company_stats.json", "r") as f:
            in_companies = f.read()
        
        companies_json = json.loads(in_companies)
        indicators = Indicators()
        company_indicators = [indicators.calc_indicators(company) for company in companies_json]
        return f"{json.dumps(in_companies)} {json.dumps(company_indicators)}"
	