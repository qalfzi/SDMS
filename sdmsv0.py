from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain.chains import LLMChain, SequentialChain
from langchain.prompts import PromptTemplate
import google.generativeai as genai 

from dotenv import load_dotenv
import streamlit as st 
import os 

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    temperature=0.1,
    convert_system_message_to_human=True
)

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

template1 = """
I have a problem for you to solve, the problem is {input}
Provide {number} distinct solutions and I want you to take into consideration, factors such as {factors}
"""

prompt1 = PromptTemplate(
    input_variables=["input", "factors", "number"],
    template=template1
)

chain1= LLMChain(
    llm=llm,
    prompt=prompt1,
    output_key="prop_soln"
)


template2 = """
For each of the proposed solution, evaluate their potential.
Consider their pros and cons, initial effort required, implementation, difficulty, potential callenges, and the expected outcomes.
Assign a probability of success and a confidence level to each option based on their factors
{prop_soln}
"""

prompt2 = PromptTemplate(
    input_variables=["prop_soln"],
    template=template2
)

chain2 = LLMChain(
    llm = llm,
    prompt=prompt2,
    output_key="solns"
)


template3 = """
For each solution, elaborate on the thought process by generating potential scenarios, outlining strategies for implementation,
identifying necessary partnership or resources, and proposing solutions to potential obstacles.
Additionally, consider any unexpected outcomes and outline contingency plans for their management.
{solns}
"""

prompt3 = PromptTemplate(
    input_variables=["solns"],
    template=template3
)

chain3 = LLMChain(
    llm=llm,
    prompt=prompt3,
    output_key="proc_output"
)


template4 = """
Rank the solutions based on evaluations and scenarios, assigning a probability of success in percentage for each.
Provide justification and final thought for each ranking.
Each ranking should be broken down into 4 points, Probability of success, justification, modes of failure and final thoughts.
Rank according to the highest probability of success.
{proc_output}
"""

prompt4 = PromptTemplate(
    input_variables=["proc_output"],
    template=template4
)

chain4 = LLMChain(
    llm=llm,
    prompt=prompt3,
    output_key="result"
)

chain = SequentialChain(
    chains=[chain1, chain2, chain3, chain4],
    input_variables=["input", "factors", "number"],
    output_variables=["result"]
)

# Set page configuration to wide layout
st.set_page_config(layout="wide")

#--------------------------------------------------------------------------------------
# Theme Dark or Light
# https://discuss.streamlit.io/t/changing-the-streamlit-theme-with-a-toggle-button-solution/56842/2
ms = st.session_state
if "themes" not in ms: 
  ms.themes = {"current_theme": "light",
                    "refreshed": True,
                    
                    "light": {"theme.base": "dark",
                              "theme.backgroundColor": "black",
                              "theme.primaryColor": "#c98bdb",
                              "theme.secondaryBackgroundColor": "#5591f5",
                              "theme.textColor": "white",
                              "theme.textColor": "white",
                              #"button_face": "🌜"},
                              "button_face": "Dark"},

                    "dark":  {"theme.base": "light",
                              "theme.backgroundColor": "white",
                              "theme.primaryColor": "#5591f5",
                              "theme.secondaryBackgroundColor": "#82E1D7",
                              "theme.textColor": "#0a1464",
                              #"button_face": "🌞"},
                              "button_face": "Light"},
                    }
def ChangeTheme():
  previous_theme = ms.themes["current_theme"]
  tdict = ms.themes["light"] if ms.themes["current_theme"] == "light" else ms.themes["dark"]
  for vkey, vval in tdict.items(): 
    if vkey.startswith("theme"): st._config.set_option(vkey, vval)

  ms.themes["refreshed"] = False
  if previous_theme == "dark": ms.themes["current_theme"] = "light"
  elif previous_theme == "light": ms.themes["current_theme"] = "dark"


btn_face = ms.themes["light"]["button_face"] if ms.themes["current_theme"] == "light" else ms.themes["dark"]["button_face"]
# st.button(btn_face, on_click=ChangeTheme)

# Align the button to the right
st.write("")  # Add an empty space to push the button to the right
col1, col2 = st.columns([20, 3])  # Adjust column widths as needed
with col2:
    st.button(btn_face, on_click=ChangeTheme)

if ms.themes["refreshed"] == False:
  ms.themes["refreshed"] = True
  st.rerun()
#--------------------------------------------------------------------------------------
# Sidebar
# Create a container to center the image
col1, col2, col3 = st.sidebar.columns([1, 1, 2])

# Add the logo image within the centered column
with col2: st.image("ai.png", width=100)

# Add "About" section in the left sidebar
st.sidebar.header("About")
st.sidebar.markdown("DECISIO is your premier strategic decision-making companion designed to elevate your organizational prowess to new heights. In the dynamic landscape of today's business world, informed decisions are the cornerstone of success, and DECISIO is here to empower you with the tools and insights you need to navigate with confidence.")

st.sidebar.header("Distinct Solution")
num     = st.sidebar.slider("How many distinct solutions do you want ?", 1, 3, step=1)

#user_input = st.sidebar.text_input("Enter some text in left sidebar:")
#--------------------------------------------------------------------------------------
# Main
st.header("Strategic Decision Making v0")

# Select button
# Refer: https://discuss.streamlit.io/t/new-component-st-btn-select-selectbox-alternative-with-buttons/18466
from st_btn_select import st_btn_select
st.write("Select one element")
selection_btn = st_btn_select(('Financial', 'Resources', 'Technology', 'Ownership', 'Data', 'Infra', 'Security', 'Agility', 'People', 'Process'))
# st.write("You selected:", selection_btn)

st.subheader("Problem description, Goals and Constraints/Limitation")
inp     = st.text_input("The current [process/procedure/system] at [Organization/Department] is inefficient, leading to delays in [desired outcome]. This problem is significant as it hampers [impact on stakeholders or goals], impacting the organization's ability to [relevant organizational objectives], (Copy, paste and change accordingly)", placeholder="Input", label_visibility='visible')

st.subheader("Stakeholders & Decision Criteria")
factors = st.text_input("Addressing this problem is crucial for the organization as it aims to [desired improvement], ultimately [benefit to the organization or stakeholders] (Copy, paste and change accordingly).", placeholder="Factors", label_visibility='visible')

# st.subheader("Distinct Solution")
# num     = st.slider("How many distinct solutions do you want ?", 1, 3, step=1)

if st.button("THINK", use_container_width=True):
    res = chain({"input" : inp, "factors" : factors, "number" : num})

    st.write("")
    st.subheader(":red[Response]")
    # st.write("")

    st.markdown(res['result'])