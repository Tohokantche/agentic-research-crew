import streamlit as st
import os
from pathlib import Path
from src.ui.sidebar import render_sidebar
from src.research_crew.main import run
from src.utils.output_handler import capture_output, get_cost
from datetime import datetime
import shutil

project_root = Path(__file__).parent
storage_dir = project_root / "knowledge" / "crewai_storage"

# Set the environment variables from streamlit default configuration file
# These environment variables are overide by the ones provided by the user via the UI 
os.environ["CREWAI_STORAGE_DIR"] = str(storage_dir)
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
os.environ["SERPER_API_KEY"] = st.secrets["SERPER_API_KEY"]

# Initialize session state
if 'completed_task' not in st.session_state:
    st.session_state.completed_task = False

if 'task_count' not in st.session_state:
    st.session_state.task_count = 0

# Define a callback function to run when the button is clicked
def on_button_click():
    if not topic or not detailed_questions:
        st.error("Please fill all the fields.")

    if st.session_state.task_count >1:
        st.error("Sorry! You can only perfrom two research.")

def on_text_change():
    st.session_state.completed_task = False


#--------------------------------#
#         Streamlit App          #
#--------------------------------#
# Configure the page
st.set_page_config(
    page_title="Agentic Research Assistant",
    page_icon="🕵️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main layout
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.title("🔍 :red[Agentic] Research Assistant", anchor=False)

# Render sidebar and get selection (provider and model)
selection = render_sidebar()

# Check if API keys are set based on provider
if selection["provider"] == "OpenAI":
    if not os.environ.get("OPENAI_API_KEY"):
        st.warning("⚠️ Please enter your OpenAI API key in the sidebar to get started")
        st.stop()
elif selection["provider"] == "GROQ":
    if not os.environ.get("GROQ_API_KEY"):
        st.warning("⚠️ Please enter your GROQ API key in the sidebar to get started")
        st.stop()

# Add Ollama check
if selection["provider"] == "Ollama" and not selection["model"]:
    st.warning("⚠️ No Ollama models found. Please make sure Ollama is running and you have models loaded.")
    st.stop()

# Set provider and model name
os.environ["PROVIDER"] = f"{selection['provider'].lower()}_llm"
os.environ["MODEL_NAME"] =  f"{selection['provider'].lower()}/{selection['model']}"


# Create two columns for the input section
input_col1, input_col2, input_col3 = st.columns([1, 3, 1])
with input_col2:
    topic = st.text_input("Main topic of your research: ", placeholder="LLM", on_change=on_text_change)
    detailed_questions = st.text_area(
        "Specific questions or subtopics you are interested in exploring: ",
        placeholder="How to evaluate LLMs model ?",
        on_change=on_text_change,
        height=68
    )

col1, col2, col3 = st.columns([1, 0.5, 1])
with col2:
    start_research = st.button("🚀 Start Research", use_container_width=False,
                                type="primary", on_click=on_button_click)

proceed_condition = topic and detailed_questions and not st.session_state.completed_task and st.session_state.task_count<2
if start_research and proceed_condition:
    with st.status("🤖 Researching...", expanded=True) as status:
        try:
            # Create persistent container for process output with fixed height.
            process_container = st.container(height=300, border=True)
            output_container = process_container.container()
            
            # Single output capture context.
            with capture_output(output_container):

                inputs = {"topic": str(topic), "detailed_questions": str(detailed_questions),
                       "current_year": str(datetime.now().year)}
                crew, result = run(inputs)
                status.update(label="✅ Research completed!", state="complete", expanded=False)

        except Exception as e:
            status.update(label="❌ Error occurred", state="error")
            st.error(f"An error occurred: {str(e)}")
            st.stop()
    
    st.subheader("Detailed cost of the search")
    st.dataframe(get_cost(crew))
    st.divider()
    # Display the final result
    st.markdown(result)
    st.session_state.task_count+=1
    # Create download buttons
    st.divider()
    
    download_col1, download_col2, download_col3 = st.columns([1, 2, 1])
    with download_col2:
        st.markdown("### 📥 Download Research Report")
        
        # Download as Markdown
        report_col1, memory_col2, = st.columns(2)
        with report_col1:
            st.download_button(
                label="Download Report",
                data=str(result),
                file_name="research_report.md",
                mime="text/markdown",
                help="Download the research report in Markdown format"
            )
        with memory_col2:
            shutil.make_archive('agent_memory', 'zip', storage_dir)
            with open('agent_memory.zip', 'rb') as f:
                st.download_button('Download Agent Memory', 
                                   f, file_name='agent_memory.zip',
                                   help="Download the agent memory in zip format") 
     
# Add footer
st.divider()
footer_col1, footer_col2, footer_col3 = st.columns([1, 1, 1])
with footer_col2:
    st.caption("Made with ❤️ using [CrewAI](https://crewai.com), and [Streamlit](https://streamlit.io)",
               text_alignment="center")
    
