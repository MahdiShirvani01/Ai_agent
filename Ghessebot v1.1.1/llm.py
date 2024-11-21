from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

def llm_setup(api_key, topic):

    # llm setup
    llm = ChatOpenAI(
        openai_api_base="https://api.groq.com/openai/v1",
        api_key= api_key,
        model_name="groq/llama3-70b-8192",
        max_tokens=8000
    )

    # defining agents
    story_outliner = Agent(
    role='Story Outliner',
    goal='Develop an ethical outline for a children\'s storybook about {topic}, including chapter titles and characters for 5 chapters.',
    backstory="An imaginative creator who lays the foundation of captivating stories for children.",
    verbose=True,
    llm=llm,
    allow_delegation=False
    )

    story_writer = Agent(
    role='Story Writer',
    goal='Write the full content of the story for all 5 chapters, each chapter 1000 words, weaving together the narratives and characters outlined.',
    backstory="A talented storyteller who brings to life the world and characters outlined, crafting engaging and imaginative tales for children.",
    verbose=True,
    llm=llm,
    allow_delegation=False
    )

    # defining tasks
    task_outline = Task(
        description='Create an ethical outline for the children\'s storybook about {topic}, detailing chapter titles and character descriptions for 5 chapters.',
        agent=story_outliner,
        expected_output='A structured outline document containing 5 chapter titles, with detailed character descriptions.'
    )

    task_write = Task(
        description='Using the outline provided, write the full story content for all chapters, ensuring a cohesive and engaging narrative for children. Each Chapter 1000 words. Include Title of the story at the top.',
        agent=story_writer,
        expected_output='A complete manuscript of the children\'s storybook about {topic} with 5 chapters. Each chapter should contain approximately 1000 words, following the provided outline and integrating the characters.'
    )

    # crewai
    crew = Crew(
        agents=[story_outliner, story_writer],
        tasks=[task_outline, task_write],
        verbose=True
    )
    
    result = crew.kickoff(inputs={"topic": topic})
    return result