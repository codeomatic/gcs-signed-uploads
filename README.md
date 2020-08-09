# Generate signed upload urls for GCS bucket
This project is inspired by [gcs-file-uploader](https://github.com/mcowger/gcs-file-uploader)

## What does is solve?
Scripts can get timed permission to upload files to some intermediate bucket and they don't need to
store permissions or know anything about supporting infrastructure. One example is backup uploads. 


## Why gcs service account key is built into the container?
A better way would be to mount it when container starts but managed cloud run
doesn't support mounting secrets. If you try, you'll get the following error:
```
ERROR: (gcloud.run.deploy) The `--[update|set|remove|clear]-secrets` flag is not supported 
on the fully managed version of Cloud Run. Specify `--platform gke` or run `gcloud config 
set run/platform gke` to work with Cloud Run for Anthos deployed on Google Cloud.
```
I guess it's possible to add it as clear text variable to triggers but it also feels wrong.