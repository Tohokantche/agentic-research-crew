from crewai import Agent, Crew, Process, Task, LLM
from crewai_tools import  SerperDevTool, WebsiteSearchTool, ScrapeWebsiteTool 
from src.research_crew.tools.custom_tool import SendEmailTool
import yaml, os

class ResearchCrewAgents:
    """ResearchCrewAgents crew"""

    def __init__(self):

        config = {}
        files = {
            "agents" : 'src/research_crew/config/agents.yaml',
            "tasks" : 'src/research_crew/config/tasks.yaml',
            "llms": 'src/research_crew/config/llms.yaml'
            }
        
        for config_type, file_path in files.items():
            try:
                with open(file_path, 'r') as file:
                    config[config_type] = yaml.safe_load(file)
            except Exception as e:
                raise Exception(e)
        
        self.agents_config = config['agents']
        self.tasks_config = config['tasks']  
        llm_provider = os.getenv("PROVIDER", None) if os.getenv("PROVIDER", None) else 'openai_llm'
        model_name = os.getenv("MODEL_NAME", None) if os.getenv("MODEL_NAME", None) else 'openai/gpt-4o-mini'
        self.llms_config = config['llms'][llm_provider] 
        self.llms_config.update({"model": model_name})

        # Declaring tools
        self.serper = SerperDevTool()
        self.web = WebsiteSearchTool()
        self.web_scrape=ScrapeWebsiteTool()  

        self.researcher_agent = self.researcher()
        self.analyst_agent = self.analyst()
        self.writer_agent = self.writer()
        self.researcher_task = self.research_task()
        self.analyst_task = self.analysis_task()
        self.writer_task = self.writing_task()
   
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher_agent'],
            allow_delegation=False,
            tools=[self.serper, self.web, self.web_scrape],
            llm = LLM(**self.llms_config),
            max_iter=2,
            verbose=True
        )

    def analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['analyst_agent'],
            allow_delegation=False,
            llm = LLM(**self.llms_config),
            max_iter=2,
            verbose=True
        )
    
    def writer(self) -> Agent:
        self.llms_config.update({"temperature": 1.0})
        return Agent(
            config=self.agents_config['writer_agent'],
            allow_delegation=False,
            llm = LLM(**self.llms_config),
            max_iter=2,
            verbose=True
        )

    def research_task(self) -> Task:
        return Task(
             config= self.tasks_config['researcher_task'],
             agent= self.researcher_agent
        )

    def analysis_task(self) -> Task:
        return Task(
            config = self.tasks_config['analyst_task'],
            agent= self.analyst_agent,
            context = [self.researcher_task],
        )
    
    def writing_task(self) -> Task:
        return Task(
            config=self.tasks_config['writer_task'],
            agent = self.writer_agent,
            context = [self.analyst_task],
            output_file='output/research_report.md'
        )
    
    def crew(self) -> Crew:
        """Creates the ResearcherAgent crew"""
        return Crew(
            agents=[self.researcher_agent, self.analyst_agent, self.writer_agent],
            tasks=[self.researcher_task, self.analyst_task, self.writer_task],
            process=Process.sequential,
            # memory=True,
            verbose=True
        )
