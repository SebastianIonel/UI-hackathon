import streamlit as st
import pandas as pd
import json

from graphs import *
from chat import *

# Initialize session state variables
if "companies" not in st.session_state:
    st.session_state["companies"] = []
if "main_option" not in st.session_state:
    st.session_state["main_option"] = None
if "showed_companies" not in st.session_state:
    st.session_state["showed_companies"] = []

# Function to create the slidable menu
def slidable_menu():
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            background-color: yellow;
            border: 1px solid black;
            color: black;
        }
        [data-testid="stSidebar"] img {
            max-width: 150px;
            height: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    with st.sidebar:
        st.image("logo1.png", use_container_width=True)
        st.title("Choose company to inspect")
        
        st.session_state["main_option"] = st.selectbox("Choose a main option", ["Followed", "All"] + 
                                                [elem["Company"] for elem in st.session_state["showed_companies"]])
        
        result = None
        if st.session_state["main_option"] == "Followed":
            query = st.text_input("Enter company name to search:")
            if query:
                for elem in st.session_state["companies"]:
                    if elem['Company'].lower() == query.lower():
                        result = elem['Company']
                        add_company(result)
                        break
                if result:
                    st.write("Search Result:")
                    st.write(f"- {result}")
                else:
                    st.write("No results found.")
            else:
                st.write("Please enter a search query to see results.")

def get_companies_color():
    green, red = 0, 0
    for company in st.session_state["showed_companies"]:
        if company["Score"] > 75:
            green += 1
        elif company["Score"] < 0:
            red += 1
    return green, red

def create_table(show_input):
    sorted_showed = sorted(show_input, key=lambda x: x["Score"], reverse=True)
    data = {
        "Name": [f"<b>{c['Company']}</b>" for c in sorted_showed],
        "Score": [f"{c['Score']}" for c in sorted_showed],
        "Description": [f"{c['Description']}" for c in sorted_showed]
    }
    return pd.DataFrame(data)

def show_table(option):
    st.write("You have selected the Followed option.")
    
    if option == "Followed":
        green, red = get_companies_color()
        df = create_table(st.session_state["showed_companies"])
    else: 
        green, red = 0, 0
        df = create_table(st.session_state["companies"])
    
    css = f"""
    <style>
    .dataframe {{
        border: 2px solid #000;
        border-radius: 10px;
        overflow: hidden;
        width: 100%;
        margin: 50px 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }}
    .dataframe th, .dataframe td {{
        padding: 12px;
        text-align: center;
        border-bottom: 1px solid #ddd;
    }}
    .dataframe th {{
        background-color: yellow;
        color: black;
        font-weight: bold;
    }}
    .dataframe tr:nth-child(-n+{green}) {{
        background-color: #c3e6cb;
        color: black;
    }}
    .dataframe tr:nth-last-child(-n+{red}) {{
        background-color: #f5c6cb;
        color: black;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
    st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)

def get_companies():
    file_path = 'input.json'
    try:
        with open(file_path, 'r') as file:
            st.session_state["companies"] = json.load(file)
    except FileNotFoundError:
        st.error("The 'input.json' file was not found.")

def add_company(company):
    for elem in st.session_state["showed_companies"]:
        if elem["Company"] == company:
            return
    for elem in st.session_state["companies"]:
        if elem["Company"] == company:
            st.session_state["showed_companies"].append(elem)
            break

def main():
    st.title("TITLE")
    get_companies()
    slidable_menu()
    show_chatbox()
    if st.session_state["main_option"] == "Followed" or st.session_state["main_option"] == "All":
        show_table(st.session_state["main_option"])
    
    st.markdown("""
    \n\n# Financial Health Evaluation Report for Company_A\n\n## Executive Summary\n\nCompany_A, a technology firm with 1,500 employees, has demonstrated consistent growth and profitability over the past three years. This report provides a comprehensive analysis of the company's financial health, focusing on profitability, liquidity, efficiency, and leverage. The analysis identifies key strengths and weaknesses and offers recommendations to mitigate potential risks.\n\n## Financial Performance Analysis\n\n### Profitability\n\n#### Revenue Growth\nCompany_A has shown a steady increase in revenue over the past three years:\n- 2021: $5,200,000\n- 2022: $5,900,000 (13.46% growth)\n- 2023: $6,700,000 (13.56% growth)\n\n#### Gross Profit Margin\nThe gross profit margin has remained relatively stable:\n- 2021: 51.92%\n- 2022: 50.85%\n- 2023: 50.75%\n\n#### Operating Margin\nThe operating margin has slightly decreased:\n- 2021: 28.85%\n- 2022: 28.81%\n- 2023: 28.36%\n\n#### Net Profit Margin\nThe net profit margin has also seen a slight decline:\n- 2021: 21.15%\n- 2022: 20.34%\n- 2023: 20.15%\n\n#### EBITDA\nEarnings Before Interest, Taxes, Depreciation, and Amortization (EBITDA) has increased:\n- 2021: $1,626,000\n- 2022: $1,785,000\n- 2023: $2,002,000\n\n### Liquidity\n\n#### Current Ratio\nThe current ratio indicates strong liquidity, although it has slightly decreased:\n- 2021: 4.48\n- 2022: 4.43\n- 2023: 4.32\n\n### Efficiency\n\n#### Return on Assets (ROA)\nROA has shown a positive trend:\n- 2021: 9.05%\n- 2022: 9.20%\n- 2023: 9.54%\n\n#### Return on Equity (ROE)\nROE has also improved:\n- 2021: 13.02%\n- 2022: 13.41%\n- 2023: 13.99%\n\n### Leverage\n\n#### Debt-to-Equity Ratio\nThe debt-to-equity ratio has increased slightly, indicating a higher reliance on debt:\n- 2021: 0.44\n- 2022: 0.46\n- 2023: 0.47\n\n## Key Strengths\n\n1. *Consistent Revenue Growth: Company_A has demonstrated strong revenue growth, with an average annual increase of approximately 13.5% over the past three years. This indicates a robust demand for its products and services.\n\n2. **Strong Liquidity Position: The company maintains a high current ratio, consistently above 4.0, which suggests that it has more than enough current assets to cover its current liabilities. This strong liquidity position reduces the risk of short-term financial distress.\n\n3. **Improving Efficiency: Both ROA and ROE have shown positive trends, indicating that the company is effectively utilizing its assets and equity to generate profits. This improvement in efficiency is a positive indicator of management's ability to enhance operational performance.\n\n## Significant Weaknesses\n\n1. **Declining Profit Margins: Despite revenue growth, both the operating and net profit margins have slightly declined over the past three years. This could indicate rising costs or increased competition, which may pressure profitability.\n\n2. **Increasing Leverage: The debt-to-equity ratio has been gradually increasing, suggesting a higher reliance on debt financing. While the current levels are not alarming, continued increases could pose a risk to financial stability, especially if interest rates rise.\n\n3. **Stagnant Gross Profit Margin: The gross profit margin has remained relatively flat, indicating that the company may not be effectively managing its cost of goods sold (COGS). This stagnation could limit the potential for higher profitability in the future.\n\n## Recommendations\n\n1. **Cost Management Strategies: To address the declining profit margins, Company_A should implement cost management strategies. This could include negotiating better terms with suppliers, optimizing production processes, and reducing operational inefficiencies.\n\n2. **Debt Management: The company should focus on managing its debt levels to prevent further increases in the debt-to-equity ratio. This could involve refinancing existing debt at lower interest rates, reducing discretionary spending, and prioritizing debt repayment.\n\n3. **Enhancing Gross Profit Margin*: Company_A should explore ways to improve its gross profit margin. This could involve introducing higher-margin products, increasing prices where feasible, and improving supply chain efficiencies.\n\n## Conclusion\n\nCompany_A has shown strong financial performance with consistent revenue growth, strong liquidity, and improving efficiency. However, the company faces challenges related to declining profit margins, increasing leverage, and stagnant gross profit margins. By implementing cost management strategies, focusing on debt management, and enhancing its gross profit margin, Company_A can mitigate these risks and continue to strengthen its financial position.\n\n## Charts\n\n### Revenue Growth (2021-2023)
    \n""")

    show_revenue_net_income_chart()
    
    st.markdown("""\n\n### Profit Margins (2021-2023)
    \n""")

    show_profit_margins_chart()
    
    st.markdown("""\n\n### Liquidity and Leverage Ratios (2021-2023)
    \n
    """)

    show_liquidity_leverage_chart()
if __name__ == "__main__":
    main()
