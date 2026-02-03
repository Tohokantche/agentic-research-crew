# 🔍 Agentic Research Assistant using [CrewAI](https://crewai.com)

A deep agentic research assistant built with CrewAI, Serper, and Streamlit that helps you research any topic.

![Agentic  research assistant ](screenshot.png "")

Link to the <a href="https://github.com/Tohokantche/agentic-research-crew">demo</a> of the application:
```bash

https://github.com/Tohokantche/agentic-research-crew
```

## 🌟 Features

- 🤖 Multiple LLM Support
- 🔍 Advanced answering capabilities using web search
- 📊 Real-time research process visualization
- 📝 Structured downloadable research reports
- 🎯 Topic-focused research and analysis
- 💾 Long, Short, and Entity memory integration
- 🔒 Secure API key management
- 📱 Responsive and modern UI

## 🛠️ Project Structure

```
agentic-research-crew
├── knowledge
│   └── crewai_storage
│       ├── entities
│       │   └── {topic}_expert_Analyst_Academic_writer
│       │       ├── 711b55cb-3a1d-4f9e-9abd-772faaee41b5
│       │       │   ├── data_level0.bin
│       │       │   ├── header.bin
│       │       │   ├── length.bin
│       │       │   └── link_lists.bin
│       │       └── chroma.sqlite3
│       ├── latest_kickoff_task_outputs.db
│       ├── long_term_memory_storage.db
│       └── short_term
│           └── {topic}_expert_Analyst_Academic_writer
│               ├── 8fae73ab-dc24-48e3-b8d9-36ce9ec1a8e2
│               │   ├── data_level0.bin
│               │   ├── header.bin
│               │   ├── length.bin
│               │   └── link_lists.bin
│               └── chroma.sqlite3
├── output
│   └── research_report.md
├── README.md
├── requirements.txt
├── run_app.py
├── screenshot.png
├── src
│   ├── research_crew
│   │   ├── __init__.py
│   │   ├── config
│   │   │   ├── agents.yaml
│   │   │   ├── llms.yaml
│   │   │   └── tasks.yaml
│   │   ├── crew.py
│   │   ├── main.py
│   │   ├── tools
│   │   │   ├── __init__.py
│   │   │   └── custom_tool.py
│   │   └── utils.py
│   ├── tests
│   │   ├── __init__.py
│   │   └── test_research_crew.py
│   ├── ui
│   │   ├── __init__.py
│   │   └── sidebar.py
│   └── utils
│       ├── __init__.py
│       └── output_handler.py
└── streamlit_app.py
```

## 📋 Requirements

- Python >=3.10 and <3.13
- OpenAI API key or GROQ API key
- Serper API key for web search
- Streamlit for UI

## 🚀 Getting Started

1. Clone the repository:
```bash
git clone https://github.com/Tohokantche/agentic-research-crew.git
cd agentic-research-crew
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
streamlit run streamlit_app.py
```

## 🔑 API Keys Setup

The application requires the following API keys:  

1. **OpenAI API Key** or **GROQ API Key**
   - For OpenAI: Get it from [OpenAI Platform](https://platform.openai.com/)
   - For GROQ: Get it from [GROQ Console](https://console.groq.com/)

2. **Serper API Key for web search**
   - Get it from [Serper Dev Dashboard](https://serper.dev/)

Enter these keys in the sidebar of the application when prompted.

## 🎯 Usage

1. Open the application in your web browser
2. Select your preferred LLM provider (OpenAI or GROQ)
3. Enter your API keys in the sidebar
4. Type your research topic and question in the text area
5. Click "Start Research" to begin the research process
6. View the real-time research process, total tokens cost, and final detailed report

## 💡 Features in Detail

### Research Agent
The research agent (`src/research_crew/crew.py`) is powered by CrewAI and configured to:
- Conduct thorough research on given topic and detailed question
- Analyze and summarize information
- Provide structured reports with key findings

### LLMs configuration file
The language models (`src/research_crew/config/llms.yaml`) configurtion file used for the agents:
- Easily access to all hyper-parameters at one place
- Testing different hyper-parameters 

### Process Output
The output handler (`src/utils/output_handler.py`) provides:
- Real-time process visualization
- Clean, formatted output
- Progress tracking

### User Interface
The application features a modern, responsive UI with:
- Intuitive sidebar configuration
- Clear process visualization
- Organized research results
- Professional styling

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [CrewAI](https://crewai.com) for the AI agent framework
- [Serper](https://exa.ai) for advanced search capabilities
- [Streamlit](https://streamlit.io) for the web interface
- [tonykipkemboi](https://github.com/tonykipkemboi/crewai-streamlit-demo.git) for the nice UI inspiration
