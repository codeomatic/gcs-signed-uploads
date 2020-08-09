# Generate signed upload urls for GCS bucket
This project is inspired by [gcs-file-uploader](https://github.com/mcowger/gcs-file-uploader)

## What does is solve?
Scripts can get timed permission to upload files to some intermediate bucket and they don't need to
store permissions or know anything about supporting infrastructure. One example is backup uploads. 

## Environment variables
To run locally or deploy to Cloud Run define environment variables or create `.env` file.
```
PORT=8080
BUCKET=put-bucket-name-here
SERVICE_NAME=signed-upload
REGION=us-central1
```

## Running locally
`docker.compose up --build`

## Useful helper script
It's possible to do everything using `gcloud` cli but `task.py` contains some useful
shortcuts for common tasks. 

```
pip install -U python-dotenv invoke
```

`invoke deploy` - Deploy the latest version to managed Google Cloud Run.


## Why gcs service account key is built into the container?
A better way would be to mount it when container starts but managed cloud run
doesn't support mounting secrets. If you try, you'll get the following error:
```
ERROR: (gcloud.run.deploy) The `--[update|set|remove|clear]-secrets` flag is not supported 
on the fully managed version of Cloud Run. Specify `--platform gke` or run `gcloud config 
set run/platform gke` to work with Cloud Run for Anthos deployed on Google Cloud.
```
I guess it's possible to add it as clear text variable to triggers but it also feels wrong.