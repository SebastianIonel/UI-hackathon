import streamlit as st
import pandas as pd

global companies
global main_option


# Function to create the slidable menu
def slidable_menu():
    # Inject custom CSS to style the sidebar and selectbox
    global main_option
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
        st.title("Right-Hand Menu")
        st.write("This is a slidable right-hand menu.")
        
        main_option = st.selectbox("Choose a main option", ["Overall", "A", "B", "C", "D"])
        
        if main_option == "A":
            sub_option = st.selectbox("Choose a sub-option for A", ["A1", "A2", "A3"])
        elif main_option == "B":
            sub_option = st.selectbox("Choose a sub-option for B", ["B1", "B2"])
        elif main_option == "C":
            sub_option = st.selectbox("Choose a sub-option for C", ["C1", "C2", "C3", "C4"])
        elif main_option == "D":
            sub_option = st.selectbox("Choose a sub-option for D", ["D1", "D2", "D3", "D4", "D5"])
        
        st.button("Click me")


def create_table(n):
    global companies
    companies = [("A", 5, "Compania A este cea mai buna"), ("B", 3, "Compania e cea s"), ("C", 7, "Compania e cea s"), ("D", 4, "Compania e cea ssdadsa")]
    companies.sort(key=lambda x: x[1], reverse=True)
    data = {
        "Name": [f"<b>{companies[i][0]}</b>" for i in range(n)],
        "Score": [f"{companies[i][1]}" for i in range(n)],
        "Description": [f"{companies[i][2]}" for i in range(n)]
    }
    df = pd.DataFrame(data)
    return df

# Main function to run the Streamlit app
def main():
    st.title("Main Page")
    st.write("This is the main content of the page.")
    slidable_menu()
    
    if main_option == "Overall":
        st.write("You have selected the Overall option.")
        n = 4  # Replace with the desired number of lines
        
        df = create_table(n)

        # Apply custom CSS to style the table
        st.markdown(
            """
            <style>
            .dataframe {
                border: 2px solid #000;
                border-radius: 10px;
                overflow: hidden;
                width: 100%;
                margin: 50px 0;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
            .dataframe th, .dataframe td {
                padding: 12px;
                text-align: center;
                border-bottom: 1px solid #ddd;
            }
            .dataframe th {
                background-color: yellow;
                color: white;
                font-weight: bold;
            }
            .dataframe tr:nth-child(even) {
                background-color: #f2f2f2;
            }
            .dataframe tr:hover {
                background-color: #ddd;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        # Display the table with HTML rendering
        st.markdown(df.to_html(escape=False), unsafe_allow_html=True)

        

if __name__ == "__main__":
    main()