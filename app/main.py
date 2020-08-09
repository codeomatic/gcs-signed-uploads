from flask import Flask, request, jsonify
from collections import OrderedDict
from google.cloud import storage
import logging
import datetime

try:
    import settings
except ImportError:
    from . import settings

logging.basicConfig(level=logging.INFO)
client = storage.Client()

app = Flask(__name__)


def bucket():
    return client.bucket(settings.bucket_name)


def file_exists(filename):
    return bucket().blob(filename).exists()


@app.route('/', methods=['GET'])
def health_check():
    if not settings.bucket_name:
        return 'BUCKET environment variable is not defined.', 500

    return f'URL to GCS service version {settings.version}', 200


@app.route('/api/upload-url/', methods=['POST'])
def signed_upload_url():
    content = request.json
    filename = content.get('filename', '')
    response = OrderedDict()
    if not filename:
        response['status'] = 'failed'
        response['error'] = 'Valid filename is required.'
        return jsonify(response), 400

    prefixed_filename = settings.signed_prefix + filename.strip('/')
    if file_exists(prefixed_filename):
        response['status'] = 'failed'
        response['error'] = f'{filename} already exists.'
        return jsonify(response), 400

    blob = bucket().blob(prefixed_filename)
    url = blob.generate_signed_url(
        expiration=datetime.timedelta(minutes=60),
        method='POST', version="v4")

    response['status'] = 'ok'
    response['result'] = url
    return jsonify(response), 201


if __name__ == "__main__":
    app.run(host='localhost', debug=True)
