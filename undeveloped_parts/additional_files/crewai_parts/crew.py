from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import BaseTool
from tools.job_scraper import scrape_jobs_from_web
from crewai_tools import FileReadTool, CSVSearchTool
from dotenv import load_dotenv
from pathlib import Path
import yaml
import os
csv_reader = CSVSearchTool()

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent

@CrewBase
class MatchToProposalCrew:
    """MatchToProposal crew"""

    agents_config = BASE_DIR / "config" / "agents.yaml"
    tasks_config = BASE_DIR / "config" / "tasks.yaml"

    # Define agents
    @agent
    def cv_reader(self) -> Agent:
        return Agent(
            config=self.agents_config['cv_reader'],
            tools=[FileReadTool()],  # Tools passed as a list
            verbose=True,
            allow_delegation=False
        )

    @agent
    def matcher(self) -> Agent:
        return Agent(
            config=self.agents_config['matcher'],
            tools=[FileReadTool(), CSVSearchTool()],  # Tools for the matcher
            verbose=True,
            allow_delegation=False
        )

    # Define tasks
    @task
    def read_cv_task(self) -> Task:
        """
        Task to read and process a CV file.
        """
        def execute_reader(cv_file):
            cv_data = self.cv_reader().execute(cv_file)
            return {
                "professional_summary": cv_data.get("professional_summary", ""),
                "technical_skills": cv_data.get("technical_skills", []),
                "work_history": cv_data.get("work_history", []),
                "education": cv_data.get("education", []),
                "key_achievements": cv_data.get("key_achievements", []),
                "desired_position": cv_data.get("desired_position", "general job"),
                "preferred_location": cv_data.get("preferred_location", "remote"),
            }

        return Task(
            config=self.tasks_config['read_cv_task'],
            agent=self.cv_reader(),
            execute=execute_reader
        )

    @task
    def scrape_jobs_task(self) -> Task:
        """
        Task to scrape job postings based on CV data.
        """
        def execute_scraper(cv_data):
            if not isinstance(cv_data, dict):
                raise ValueError("cv_data must be a dictionary.")
            query = cv_data.get("desired_position", "general job")
            location = cv_data.get("preferred_location", "remote")
            output_csv = f"src/match_to_proposal/data/jobs_{query.replace(' ', '_')}.csv"
            return scrape_jobs_from_web(query, location, output_file=output_csv)

        return Task(
            config=self.tasks_config.get('scrape_jobs_task'),
            agent=None,  # No agent for this task
            execute=execute_scraper
        )

    @task
    def match_cv_task(self) -> Task:
        """
        Task to match CV data with scraped job opportunities.
        """
        def execute_matcher(cv_file, jobs_csv):
            return self.matcher().execute(cv_file=cv_file, jobs_csv=jobs_csv)

        return Task(
            config=self.tasks_config['match_cv_task'],
            agent=self.matcher(),
            execute=execute_matcher
        )

    # Define the crew
    @crew
    def crew(self) -> Crew:
        """
        Crew definition to orchestrate tasks.
        """
        return Crew(
            agents=['cv_reader', 'matcher'],  # Explicitly define agent names
            tasks=[
                self.read_cv_task(),
                self.scrape_jobs_task(),
                self.match_cv_task()
            ],
            process=Process.sequential,  # Tasks are executed sequentially
            verbose=True
        )
