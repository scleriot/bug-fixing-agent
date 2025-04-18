from dotenv import load_dotenv
from smolagents import CodeAgent, LiteLLMModel, List, tool
import subprocess
import os

load_dotenv()

model = LiteLLMModel(
    model_id=os.getenv("MODEL_ID"),
    api_key=os.getenv("API_KEY"),
    temperature=0,
)

@tool
def get_codebase() -> str:
    """
    Gets the whole codebase in order to analyze the request.
    """

    import os

    codebase_content = ""
    for root, dirs, files in os.walk(os.getenv("CODEBASE_PATH", "")):
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']

        for file in files:
            with open(os.path.join(root, file), 'r') as f:
                codebase_content += f"Filename: {os.path.join(root, file)}\n"
                codebase_content += f.read()
                codebase_content += "\n\n"

    return codebase_content

@tool
def pull_code() -> str:
    """
    Pulls the latest code from the remote repository.
    """

    result = subprocess.check_output(f"cd {os.getenv('CODEBASE_PATH', '')} && git pull", shell=True)
    return result.decode('utf-8')

@tool
def commit_code(commit_message: str) -> str:
    """
    Commits the latest code to the remote repository.

    Args:
        commit_message (str): The commit message.
    """

    result = subprocess.check_output(f"cd {os.getenv('CODEBASE_PATH', '')} && git add . && git commit -am '{commit_message.replace("'", "\\'")}'", shell=True)

    return result.decode('utf-8')

@tool
def push_code() -> str:
    """
    Pushes the latest code to the remote repository.
    """

    result = subprocess.check_output(f"cd {os.getenv('CODEBASE_PATH', '')} && git push", shell=True)
    return result.decode('utf-8')

@tool
def get_file_contents(file_path: str) -> str:
    """
    Retrieves the contents of a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The contents of the file.
    """

    with open(file_path, 'r') as file:
        return file.read()

@tool
def write_file(file_path: str, content: str) -> str:
    """
    Writes content to a file.

    Args:
        file_path (str): The path to the file.
        content (str): The content to write.

    Returns:
        str: The path to the file.
    """

    with open(file_path, 'w') as file:
        file.write(content)
    return file_path

@tool
def list_all_files() -> List[str]:
    """
    Lists all files.

    Returns:
        List[str]: A list of file paths.
    """
    import os

    file_list = []
    for path, subdirs, files in os.walk(os.getenv('CODEBASE_PATH', '')):
        files = [f for f in files if not f[0] == '.']
        subdirs[:] = [d for d in subdirs if not d[0] == '.']

        for name in files:
            file_list.append(os.path.join(path, name))

    return file_list

agent = CodeAgent(tools=[
    pull_code,
    list_all_files,
    write_file,
    get_file_contents,
    # commit_code,
    # push_code,
],
model=model)

agent.prompt_templates["system_prompt"] = agent.prompt_templates["system_prompt"] + """
You are a bug fixing agent.
Your role is to help non-technical users fix functional bugs and typos.
Always pull latest code first.
Always commit and push the code at the end as a last action.

Your main task is to make changes to the codebase.
`replace` python method must always have the third parameter set to 1.
You can change multiple parts of the codebase.

After you've made the changes, check the files to make sure they are correct.

Final answer: return JSON in the format { "result": "" }."""

def run_agent(query, context):
    return agent.run(f"""
Web application context:
---
{context}
---

User query that is describing the required changes:
{query}
""")

if __name__ == "__main__":
    import sys
    agent.run(" ".join(sys.argv[1:]))
