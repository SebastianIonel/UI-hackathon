import streamlit as st
import pandas as pd
import json

global companies
global main_option
global number_of_companies
global showed_companies
global number_of_showed_companies


# Function to create the slidable menu
def slidable_menu():
    # Inject custom CSS to style the sidebar and selectbox
    global main_option
    global companies
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
        # st.write("This is a slidable right-hand menu.")
        
        main_option = st.selectbox("Choose a main option", ["Overall", "A", "B", "C", "D"])

        result = None
        if main_option == "Overall":
            query = st.text_input("Enter company name to search:")
            # Filter companies based on search query
            if query:
                # Case-insensitive search
                for elem in companies:
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


        elif main_option == "A":
            sub_option = st.selectbox("Choose a sub-option for A", ["A1", "A2", "A3"])
        elif main_option == "B":
            sub_option = st.selectbox("Choose a sub-option for B", ["B1", "B2"])
        elif main_option == "C":
            sub_option = st.selectbox("Choose a sub-option for C", ["C1", "C2", "C3", "C4"])
        elif main_option == "D":
            sub_option = st.selectbox("Choose a sub-option for D", ["D1", "D2", "D3", "D4", "D5"])
        
        st.button("Click me")

def get_companies_color():
    green = 0
    red = 0
    for i in range(number_of_companies):
        if companies[i]["Score"] > 75:
            green += 1
        elif companies[i]["Score"] < 0:
            red += 1
    
    return (green, red)

def create_table(n):
    global companies
    global showed_companies

    showed_companies.sort(key=lambda x: x["Score"], reverse=True)
    data = {
        "Name": [f"<b>{showed_companies[i]['Company']}</b>" for i in range(n)],
        "Score": [f"{showed_companies[i]['Score']}" for i in range(n)],
        "Description": [f"{showed_companies[i]['Description']}" for i in range(n)]
    }
    df = pd.DataFrame(data)
    return df


def show_table():
    global number_of_showed_companies
    st.write("You have selected the Overall option.")
          
    df = create_table(number_of_showed_companies)

    number_of_green, number_of_read = get_companies_color();

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

    .dataframe tr:nth-child(-n+{number_of_green}) {{
        background-color: #c3e6cb;
        color: black;
    }}

    .dataframe tr:nth-last-child(-n+{number_of_read}) {{
        background-color: #f5c6cb;
        color: black;
    }}
    </style>
    """

    # Apply the CSS to the Streamlit app
    st.markdown(css, unsafe_allow_html=True)

    # Display the table with HTML rendering
    st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)

def get_companies():

    global companies
    global number_of_companies

    # populate file
    # TODO

    # Path to your JSON file
    file_path = 'input.json'

    # Open and load the JSON file
    with open(file_path, 'r') as file:
        companies = json.load(file)
        number_of_companies = companies.__len__()

def send_message():
    user_input = st.session_state["text_input_for_chat"]
    if user_input:
        st.session_state["chat_history"].append(f"You: {user_input}")
        st.session_state["chat_history"].append(f"ChatGPT: Your message '{user_input}' was received!")
        st.session_state["input"] = ""  # Clear the input field after sending

def show_chatbox():
    # Initialize session state for storing chat messages if not already initialized
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    
    # Display chat box title
    st.markdown("<h3 style='text-align: center;'>Chat Box</h3>", unsafe_allow_html=True)

    # Placeholder for chat history, placed above the input box
    chat_history_placeholder = st.empty()    

    # User input and send button
    user_input = st.text_input("Start conversation", key="text_input_for_chat", on_change=send_message, autocomplete="off")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("Send"):
            send_message()

    with col2:
        if st.button("Clear History"):
            # Clear the chat history after the animation
            st.session_state["chat_history"] = []

    # Render the chat history in the placeholder
    with chat_history_placeholder.container():
        for message in st.session_state["chat_history"]:
            st.markdown(f"<div style='text-align: left; color: black;'>{message}</div>", unsafe_allow_html=True)

def add_company(company):
    global showed_companies
    global number_of_showed_companies
    for i in range(number_of_showed_companies):
        if companies[i]["Company"] == company:
            showed_companies.append(companies[i])
            show_table()
            break


# Main function to run the Streamlit app
def main():
    st.title("TITLE")
    global number_of_companies
    global showed_companies
    global number_of_showed_companies

    showed_companies = []
    number_of_showed_companies = showed_companies.__len__()
    get_companies()



    slidable_menu()
    show_chatbox()
    if main_option == "Overall":
        show_table()



if __name__ == "__main__":
    main()