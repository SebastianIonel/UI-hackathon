import streamlit as st

# Function to create the slidable menu
def slidable_menu():
    # Inject custom CSS to style the sidebar and selectbox
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
        
        main_option = st.selectbox("Choose a main option", ["A", "B", "C", "D"])
        
        if main_option == "A":
            sub_option = st.selectbox("Choose a sub-option for A", ["A1", "A2", "A3"])
        elif main_option == "B":
            sub_option = st.selectbox("Choose a sub-option for B", ["B1", "B2"])
        elif main_option == "C":
            sub_option = st.selectbox("Choose a sub-option for C", ["C1", "C2", "C3", "C4"])
        elif main_option == "D":
            sub_option = st.selectbox("Choose a sub-option for D", ["D1", "D2", "D3", "D4", "D5"])
        
        st.button("Click me")

# Main function to run the Streamlit app
def main():
    st.title("Main Page")
    st.write("This is the main content of the page.")
    slidable_menu()

if __name__ == "__main__":
    main()