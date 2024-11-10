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
        "Description": [f"{c['Description']}" for c in sorted_showed],
        "RiskClass": [f"{c['RiskClass']}" for c in sorted_showed],
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

    # Create columns for buttons
    if len(st.session_state["showed_companies"]) != 0:
        st.write("Select a company:")
        cols = st.columns(len(st.session_state["showed_companies"]))
        for idx, company in enumerate(st.session_state["showed_companies"]):
            if cols[idx].button(company["Company"]):
                st.session_state["main_option"] = company['Company']
                st.write(f"{company['Company']} selected!")  # Action for the selected company

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
    if st.session_state["main_option"] != "Followed" and st.session_state["main_option"] != "All":
        # call api for st.session_state["main_option"]
        # write answer in info.json 
        show_all_info()
    
if __name__ == "__main__":
    main()
