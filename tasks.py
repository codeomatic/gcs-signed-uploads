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


@task
def mb(c):
    """Create bucket based on .env and assign proper CORS"""
    bucket = env("BUCKET")
    c.run(f'gsutil mb gs://{bucket}')
    c.run(f'gsutil cors set cors.json gs://{bucket}')


@task
def service_account(c, name):
    """Create service account, json key, and proper permissions to the bucket"""

    # check bucket access before we create service account
    c.run(f'gsutil ls {env("BUCKET")}', hide=True)

    project = project_name(c)
    c.run(f'gcloud iam service-accounts create {name} --display-name="GCS URL Signer {name}" --project={project}')
    c.run('mkdir -p auth')
    c.run(f'gcloud iam service-accounts keys create auth/service_account.json '
          f'--iam-account={name}@{project}.iam.gserviceaccount.com')
    c.run(f'gsutil iam ch '
          f'serviceAccount:{name}@{project}.iam.gserviceaccount.com:roles/storage.admin '
          f'gs://{env("BUCKET")}')
