import json
from typing import Dict
from tempfile import TemporaryDirectory
import os
import boto3
import base64
from datetime import datetime
from music_function import create_music


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    querystring: Dict = event.get('queryStringParameters', event)
    text = querystring.get('text')
    task = querystring.get('task', "music-generation")
    tempo = int(querystring.get('tempo', 60))
    sr = int(querystring.get('sr', 44100))

    print(f"event: {event}")

    with TemporaryDirectory() as tmp_dir:
        os.chdir(tmp_dir)

        if not (text and task):
            return {
                "statusCode": 400,
                "headers": {
                    "Access-Control-Allow-Origin": "*",  # Change this to your specific allowed origins
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                },
                "body": json.dumps({
                    "error": "Must provide valid text and task",
                }),
            }

        if task=='music-generation':
            # save the text to a temporary text file
            txt_path = 'temporary.txt'

            with open(txt_path, 'w') as f:
                f.write(text)

            music_path = 'temporarymp3.mp3'

            create_music(txt_path, music_path, tempo, sr)

            with open(music_path, 'rb') as audio_file:
                base64_audio = base64.b64encode(audio_file.read()).decode()

            # give each mp3 file a unique name based on time stamp
            s3_key = f"{datetime.now().strftime('%Y%m%d_%H%M%S%f')}.mp3"
            s3 = boto3.client('s3')
            s3.upload_file(music_path, "s3bucketforfiles", s3_key)

            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",  # Change this to your specific allowed origins
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                },
                "body": json.dumps({
                    "Result Mp3": f"{base64_audio}"
                }),
            }

        else:
            raise NotImplemented(f"Unknown task: {task}")
