import streamlit as st
import pandas as pd

def create_table_with_styling(show_input):
    # Sort data
    sorted_showed = sorted(show_input, key=lambda x: x["Score"], reverse=True)
    
    # Create CSS style for each row
    row_styles = []
    for i, row in enumerate(sorted_showed):
        color = "#d1e7dd" if i % 2 == 0 else "#f8d7da"  # Alternating row colors
        row_styles.append(
            f"""
            <style>
            .row-{i} {{
                background-color: {color};
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 5px;
            }}
            </style>
            """
        )
    
    # Render each row with custom HTML and CSS
    for i, row in enumerate(sorted_showed):
        st.markdown(row_styles[i], unsafe_allow_html=True)  # Inject CSS for each row
        st.markdown(
            f"""
            <div class="row-{i}">
                <strong>Name:</strong> {row['Company']} <br>
                <strong>Score:</strong> {row['Score']} <br>
                <strong>Description:</strong> {row['Description']} <br>
                <strong>Risk Class:</strong> {row['RiskClass']} <br>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Display button
        if st.button("Select", key=f"btn_{i}"):
            st.write(f"Selected {row['Company']}")  # Your action here

# Sample data
show_input = [
    {"Company": "Company A", "Score": 90, "Description": "High performance", "RiskClass": "Low"},
    {"Company": "Company B", "Score": 75, "Description": "Moderate performance", "RiskClass": "Medium"},
    {"Company": "Company C", "Score": 65, "Description": "Low performance", "RiskClass": "High"},
]

# Call the function
create_table_with_styling(show_input)
