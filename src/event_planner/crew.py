from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List



@CrewBase
class EventPlanner():
    """EventPlanner crew"""

    agents: List[BaseAgent]
    tasks: List[Task]


    @agent
    def event_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['event_researcher'],
            verbose=True
        )

    @agent
    def event_coordinator(self) -> Agent:
        return Agent(
            config=self.agents_config['event_coordinator'],
            verbose=True
        )

    @agent
    def event_reporter(self) -> Agent:
        return Agent(
            config=self.agents_config['event_reporter'],
            verbose=True
        )

    @agent
    def creative_designer(self) -> Agent:
        return Agent(
            config=self.agents_config['creative_designer'],
            verbose=True
        )

    @agent
    def budget_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['budget_planner'],
            verbose=True
        )


    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task']
        )

    @task
    def design_task(self) -> Task:
        return Task(
            config=self.tasks_config['design_task']
        )

    @task
    def coordination_task(self) -> Task:
        return Task(
            config=self.tasks_config['coordination_task']
        )

    @task
    def budget_task(self) -> Task:
        return Task(
            config=self.tasks_config['budget_task']
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'],
            output_file='event_plan.md'
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
