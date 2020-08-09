from invoke import task
from dotenv import load_dotenv
load_dotenv()


def get_project_name(c):
    result = c.run('gcloud config list --format="value(core.project)"', hide=True)
    return result.stdout.strip()


@task
def build(c):
    project_name = get_project_name(c)
    print(project_name)
