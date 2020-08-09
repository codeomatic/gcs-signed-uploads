import os
from invoke import task
from dotenv import load_dotenv
load_dotenv()


def project_name(c):
    result = c.run("gcloud config list --format='value(core.project)'", hide=True)
    return result.stdout.strip()


def commit_sha(c):
    result = c.run('git rev-parse --short HEAD')
    return result.stdout.strip()


def env(name):
    return os.getenv(name)


@task
def deploy(c, git_hash_tag=False):
    tag = git_hash_tag and commit_sha(c) or 'latest'
    image = f'gcr.io/{project_name(c)}/{env("SERVICE_NAME")}:{tag}'

    c.run(f'docker build -t {image} ./')
    c.run(f'docker push {image}')

    c.run(
        f'gcloud run deploy {env("SERVICE_NAME")} '
        f'--image {image} --region {env("REGION")} '
        f'--allow-unauthenticated --platform managed '
        f'--update-env-vars '
        f'BUCKET={env("BUCKET")}'
    )

