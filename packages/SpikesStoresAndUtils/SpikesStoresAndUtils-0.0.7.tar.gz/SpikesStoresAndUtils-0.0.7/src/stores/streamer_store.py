import requests
import json
import boto3
import os


def loginAndReturnCookies():
    session = requests.Session()
    login_data = {
        "email": f'{os.environ["API_EMAIL"]}',
        "password": f'{os.environ["API_PASSWORD"]}'.strip(),
        "rememberMe": "true"
    }
    res = session.put(f'https://{os.environ["API_SERVER"]}/api/v1/auth/login', login_data)
    if res.status_code != 200:
        raise Exception
    return session.cookies.get_dict()


def logSessionEntry(lambda_name, status, Cookies, session_uuid, stream_uuid, streamer_uuid):
    if status == 'start':
        status_banner = f"{lambda_name}_job_started"
    elif status == 'failed':
        status_banner = f"{lambda_name}_job_failed"
    elif status == 'end':
        status_banner = f"{lambda_name}_job_ended"
    else:
        raise Exception
    create_spike_session_data = {
        "session_id": session_uuid,
        "status": status_banner,
        "stream": stream_uuid,
        "streamer": streamer_uuid
    }
    res = requests.post(f'https://{os.environ["API_SERVER"]}/api/v1/services/spike-session-entry',
                        create_spike_session_data, cookies=Cookies)
    if res.status_code != 200:
        raise Exception


def updateStreamerData(Cookies, streamer_uuid, ccv, threshold, followers):
    upddate_streamer_data = {
        "streamer": streamer_uuid,
        "ccv": ccv,
        "hype_threshold": threshold,
        "ccv_update_date": 1659974374000,
        "avg_viewers": 103.2,
        "followers_count": followers
    }
    res = requests.put(f'https://{os.environ["API_SERVER"]}/api/v1/services/update-streamer-data',
                       upddate_streamer_data, cookies=Cookies)
    if res.status_code != 200:
        raise Exception

def generate_s3_key(streamer_name, stream_id):
    return f'chat-texts/{streamer_name}/{stream_id}.json'


def saveChatDataToS3(streamer_name, stream_id, stream_data):
    session = boto3.Session(aws_access_key_id=os.environ['AWS_ACCESS_ID'].strip(),
                            aws_secret_access_key=os.environ['AWS_ACCESS_SECRET'].strip(),
                            region_name=os.environ['REGION_NAME'].strip())
    s3 = session.resource('s3')
    s3Key = generate_s3_key(streamer_name, stream_id)
    object = s3.Object(os.environ['CHAT_BUCKET'].strip(), s3Key)
    print(f'saving to s3 {os.environ["CHAT_BUCKET"].strip()}, {s3Key}')
    object.put(Body=stream_data)
    print('creating location object')
    location = session.client('s3').get_bucket_location(Bucket=os.environ['CHAT_BUCKET'].strip())['LocationConstraint']
    print(f'location: {location}')
    return "https://s3-%s.amazonaws.com/%s/%s" % (location, os.environ['CHAT_BUCKET'].strip(), s3Key)   # return url


def sendChatDataToQueue(session_uuid, streamer_name, stream_id, streamer_uuid, stream_uuid,
                        chat_file_url, stream_chat_uuid):
    session = boto3.Session(aws_access_key_id=os.environ['AWS_ACCESS_ID'].strip(),
                            aws_secret_access_key=os.environ['AWS_ACCESS_SECRET'].strip(),
                            region_name=os.environ['REGION_NAME'].strip())
    sqs = session.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName=os.environ['CHAT_QUEUE'].strip())
    message = {'session_uuid': session_uuid, 'streamer_name': streamer_name, 'stream_id': stream_id,
               'streamer_uuid': streamer_uuid, 'stream_uuid': stream_uuid, 'chat_file_url': chat_file_url,
               'stream_chat_uuid': stream_chat_uuid}
    queue.send_message(MessageBody=json.dumps(message, default=str))


def createStreamChat(Cookies, session_uuid, stream_uuid, streamer_uuid, s3_url):
    create_stream_chat_data = {
        "stream": stream_uuid,
        "streamer": streamer_uuid,
        "url": s3_url,
        "metadata": "{}",
        "start_time": 0,
        "end_time": 1000,
        "session_id": session_uuid,
    }
    res = requests.post(f'https://{os.environ["API_SERVER"].strip()}/api/v1/services/create-stream-chat',
                        create_stream_chat_data, cookies=Cookies)
    if res.status_code != 200:
        raise Exception
    return res.json()

def get_s3_bucket_content(bucket_name, chat_file_name):
    session = boto3.Session(aws_access_key_id=os.environ['AWS_ACCESS_ID'].strip(),
                            aws_secret_access_key=os.environ['AWS_ACCESS_SECRET'].strip(),
                            region_name=os.environ['REGION_NAME'].strip())
    s3 = session.resource('s3')
    bucket = s3.Bucket(bucket_name)
    for obj in bucket.objects.filter():
        if chat_file_name in obj.key:
            return obj.get()['Body'].read()


def createStreamEvent(Cookies, start_time, end_time, event_type, session_uuid, stream_uuid,
                      streamer_uuid, stream_chat_uuid):
    create_stream_event_data = {
        "start_time": start_time,
        "end_time": end_time,
        "event_type": event_type,
        "stream": stream_uuid,
        "streamer": streamer_uuid,
        "stream_chat": stream_chat_uuid,
        "session_id": session_uuid
    }
    res = requests.post(f'https://{os.environ["API_SERVER"].strip()}/api/v1/services/create-stream-event',
                        create_stream_event_data, cookies=Cookies)
    if res.status_code != 200:
        raise Exception
    return res.json()


def sendSpikesDataToQueue(session_uuid, stream_event_uuid, streamer_uuid, stream_uuid):
    session = boto3.Session(aws_access_key_id=os.environ['AWS_ACCESS_ID'].strip(),
                            aws_secret_access_key=os.environ['AWS_ACCESS_SECRET'].strip(),
                            region_name=os.environ['REGION_NAME'].strip())
    sqs = session.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName=os.environ['SPIKES_QUEUE'])
    message = {'session_uuid': session_uuid, 'stream_event_uuid': stream_event_uuid,
               'streamer_uuid': streamer_uuid, 'stream_uuid': stream_uuid}
    response = queue.send_message(MessageBody=json.dumps(message, default=str))
    print(response.get('MessageId'))
    print(response.get('MD5OfMessageBody'))


def readFromSQS(url):
    sqs = boto3.client('sqs', aws_access_key_id=os.environ['AWS_ACCESS_ID'].strip(),
                       aws_secret_access_key=os.environ['AWS_ACCESS_SECRET'].strip(),
                       region_name=os.environ['REGION_NAME'].strip())
    print(f'queue: {sqs}')
    response = sqs.receive_message(QueueUrl=url, MaxNumberOfMessages=1, WaitTimeSeconds=10)
    print(f'response: {response}')



