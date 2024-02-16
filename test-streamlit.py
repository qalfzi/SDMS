import streamlit as st

# Set page configuration to wide layout
st.set_page_config(layout="wide")

# Create a CSS file named "style.css" in the same directory as your app
with open("style.css", "w") as f:
    f.write(".stSidebar { background-color: #90EE90; }")

# Include the CSS file in your Streamlit app
st.markdown("<style>@import url('style.css');</style>", unsafe_allow_html=True)

# Title and header
st.title("My Streamlit App with Sidebar")
st.header("Explore different options")

# Select button
# Refer: https://discuss.streamlit.io/t/new-component-st-btn-select-selectbox-alternative-with-buttons/18466
from st_btn_select import st_btn_select
selection_btn = st_btn_select(('Financial', 'Resources', 'Technology', 'Ownership', 'Data', 'Infra', 'Security', 'Agility', 'People', 'Process'))
st.write("You selected:", selection_btn)

# Sidebar content
with st.sidebar:
    # Text input
    name = st.text_input("Enter your name:")
    
    # Radio buttons
    choice = st.radio(
        "Choose an option:",
        ("Option 1", "Option 2", "Option 3"),
    )
    
    # Checkbox
    show_data = st.checkbox("Show some data")

# Main content based on sidebar selections
if show_data:
    # Display some data based on user choices
    if choice == "Option 1":
        st.write("Data for Option 1")
    elif choice == "Option 2":
        st.write("Data for Option 2")
    else:
        st.write("Data for Option 3")

# Display user name
st.write(f"Hello, {name}!")

