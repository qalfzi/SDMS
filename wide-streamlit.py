import streamlit as st

# Set page configuration to wide layout
st.set_page_config(layout="wide")

# Create a Streamlit app
st.title("Left Sidebar Streamlit App")

# Create a container to center the image
col1, col2, col3 = st.sidebar.columns([1, 1, 2])

# Add the logo image within the centered column
with col2: st.image("ai.png", width=100)

# Add "About" section in the left sidebar
st.sidebar.header("About")
st.sidebar.markdown("Lorem ipsum dolor sit amet, consectetur adipiscing elit.")

user_input = st.sidebar.text_input("Enter some text in left sidebar:")

# Add content to the main area
st.header("Main Area")
button_clicked = st.button("Click me in main area!")

# Check if the button is clicked
if button_clicked:
    # Display the entered text from the left sidebar
    st.write("You entered in left sidebar:", user_input)
