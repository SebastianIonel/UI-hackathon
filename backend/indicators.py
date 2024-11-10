DEFAULT_INDICATORS = [
    "Revenue Growth", 
    "Gross Profit Margin", 
    "Operating Margin", 
    "Net Profit Margin", 
    "Earnings Before Interest, Taxes, Depreciation, and Amortization (EBITDA)", 
    "Return on Assets (ROA)", 
    "Return on Equity (ROE)", 
    "Current Ratio", 
    "Debt-to-Equity Ratio"
]

class Indicators:
    def __init__(self, indicators: list[str] = DEFAULT_INDICATORS):
        self.indicators = indicators

    def calc_indicators(self, company: dict) -> dict:
        result = {
            "Company": company["Company"],
            "Indicators": {}
        }

        for year, data in company["Financials"].items():
            year_result = {}
            
            if "Revenue Growth" in self.indicators:
                if str(int(year) - 1) in company["Financials"]:
                    prev_year = str(int(year) - 1)
                    curr_revenue = data["Revenue"]
                    prev_revenue = company["Financials"][prev_year]["Revenue"]
                    year_result["Revenue Growth"] = ((curr_revenue - prev_revenue) / prev_revenue) * 100
                else:
                    year_result["Revenue Growth"] = None  # No previous year for 2021

            if "Gross Profit Margin" in self.indicators:
                year_result["Gross Profit Margin"] = ((data["Revenue"] - data["COGS"]) / data["Revenue"]) * 100

            if "Operating Margin" in self.indicators:
                year_result["Operating Margin"] = (data["Operating_Income"] / data["Revenue"]) * 100

            if "Net Profit Margin" in self.indicators:
                year_result["Net Profit Margin"] = (data["Net_Income"] / data["Revenue"]) * 100

            if "Earnings Before Interest, Taxes, Depreciation, and Amortization (EBITDA)" in self.indicators:
                year_result["EBITDA"] = (data["Net_Income"] + data["Interest_Expense"] + data["Taxes"] +
                                         data["Depreciation"] + data["Amortization"])

            if "Return on Assets (ROA)" in self.indicators:
                year_result["Return on Assets (ROA)"] = (data["Net_Income"] / data["Total_Assets"]) * 100

            if "Return on Equity (ROE)" in self.indicators:
                year_result["Return on Equity (ROE)"] = (data["Net_Income"] / data["Shareholders_Equity"]) * 100

            if "Current Ratio" in self.indicators:
                year_result["Current Ratio"] = data["Current_Assets"] / data["Current_Liabilities"]

            if "Debt-to-Equity Ratio" in self.indicators:
                year_result["Debt-to-Equity Ratio"] = data["Total_Liabilities"] / data["Shareholders_Equity"]

            result["Indicators"][year] = year_result

        return result

import json

companies = json.loads(open("company_stats.json", "r").read())
indicators = Indicators(["Revenue Growth"])

with open("out.json", "w") as f:
	f.write(json.dumps([indicators.calc_indicators(company) for company in companies], indent=4))