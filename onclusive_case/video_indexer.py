# Original source code: https://github.com/bklim5/python_video_indexer_lib

import os
import re
import time
import datetime
from io import BytesIO
from PIL import Image

import requests


def get_retry_after_from_message(message):
    match = re.search(r'Try again in (\d+) second', message or '')
    if match:
        return int(match.group(1))

    return 30  # default to retry in 30 seconds


class VideoIndexer:
    def __init__(self, vi_api_key, vi_location, vi_account_id):
        self.vi_api_key = vi_api_key
        self.vi_location = vi_location
        self.vi_account_id = vi_account_id
        self.access_token = None
        self.access_token_timestamp = None
        self.video_name_to_id_dict = None
        self.get_access_token()

    def del_video(self, video_id):
        self.check_access_token()

        params = {
            'accessToken': self.access_token
        }

        delete_video = requests.delete(
            'https://api.videoindexer.ai/{loc}/Accounts/{acc_id}/Videos/{videoId}?{access_token}'.format(  # NOQA E501
                loc=self.vi_location,
                acc_id=self.vi_account_id,
                videoId=video_id,
                access_token=self.access_token
            ),
            params=params
        )
        try:
            print(delete_video.json())
        except Exception as ex:
            print("Response:", delete_video)
        return delete_video

    def get_access_token(self):
        print('Getting video indexer access token...')
        headers = {
            'Ocp-Apim-Subscription-Key': self.vi_api_key
        }

        params = {
            'allowEdit': 'true'
        }
        access_token_req = requests.get(
            'https://api.videoindexer.ai/auth/{loc}/Accounts/{acc_id}/AccessToken'.format(  # NOQA E501
                loc=self.vi_location,
                acc_id=self.vi_account_id
            ),
            params=params,
            headers=headers
        )

        access_token = access_token_req.text[1:-1]
        print('Access Token: {}'.format(access_token))
        self.access_token = access_token
        self.access_token_timestamp = datetime.datetime.now()
        return access_token

    def get_all_videos_list(self):
        all_videos_list = []
        done = False
        skip = 0
        page_size = 200
        while (not done):
            response = self.get_videos_list(page_size=page_size, skip=skip)
            all_videos_list.extend(response['results'])
            next_page = response['nextPage']
            skip = next_page['skip']
            page_size = next_page['pageSize']
            done = next_page['done']
        return all_videos_list

    def get_videos_list(self, page_size=25, skip=0):
        self.check_access_token()

        params = {
            'accessToken': self.access_token,
            'pageSize': page_size,
            'skip': skip
        }
        print('Getting videos list..')

        get_videos_list = requests.get(
            'https://api.videoindexer.ai/{loc}/Accounts/{acc_id}/Videos'.format(  # NOQA E501
                loc=self.vi_location,
                acc_id=self.vi_account_id
            ),
            params=params
        )
        response = get_videos_list.json()

        return response

    def check_access_token(self):
        delta = datetime.datetime.now() - self.access_token_timestamp
        if delta > datetime.timedelta(minutes=50):
            self.get_access_token()

    def upload_to_video_indexer(
            self, video_url, name,
            force_upload_if_exists=False,
            video_language='English', streaming_preset='Default',
            indexing_preset='Default',
            verbose=False
    ):
        self.check_access_token()

        # file_name = os.path.basename(os.path.splitext(video_url)[0])
        if self.video_name_to_id_dict is None:
            self.get_video_name_to_id_dict()
        if name in self.video_name_to_id_dict.keys():
            if verbose:
                print("Video with the same name already exists in current Video Indexer account.")  # NOQA E501
            if not force_upload_if_exists:
                return self.video_name_to_id_dict[name]
            if verbose:
                print("'force_upload_if_exists' set to 'True' so uploading the file anyway.")
        if verbose:
            print('Uploading video to video indexer...')
        params = {
            'streamingPreset': streaming_preset,
            'indexingPreset': indexing_preset,
            'language': video_language,
            'name': name,
            'accessToken': self.access_token
        }
        files = {}
        if "http" in video_url.lower():
            params['videoUrl'] = video_url
        else:
            files = {
                'file': open(video_url, 'rb')
            }

        retry = True
        while retry:
            upload_video_req = requests.post(
                'https://api.videoindexer.ai/{loc}/Accounts/{acc_id}/Videos'.format(  # NOQA E501
                    loc=self.vi_location,
                    acc_id=self.vi_account_id
                ),
                params=params,
                files=files
            )

            if upload_video_req.status_code == 200:
                retry = False
                break
            # hit throttling limit, sleep and retry
            if upload_video_req.status_code == 429:
                error_resp = upload_video_req.json()
                if verbose:
                    print('Throttling limit hit. Error message: {}'.format(
                        error_resp.get('message')))
                retry_after = get_retry_after_from_message(
                    error_resp.get('message'))
                time.sleep(retry_after + 1)
                continue

            if verbose:
                print('Error uploading video to video indexer: {}'.format(
                    upload_video_req.json()))
            raise Exception('Error uploading video to video indexer')

        response = upload_video_req.json()
        return response['id']

    def get_video_info(self, video_id, video_language='English', verbose=False):
        self.check_access_token()

        params = {
            'accessToken': self.access_token,
            'language': video_language
        }
        if verbose:
            print('Getting video info for: {}'.format(video_id))

        get_video_info_req = requests.get(
            'https://api.videoindexer.ai/{loc}/Accounts/{acc_id}/Videos/{video_id}/Index'.format(  # NOQA E501
                loc=self.vi_location,
                acc_id=self.vi_account_id,
                video_id=video_id
            ),
            params=params
        )
        response = get_video_info_req.json()
        if response['state'] == 'Processing':
            if verbose:
                print('Video still processing, current status: {}'.format(
                    response['videos'][0]['processingProgress'],
                ))

        return response

    def get_video_insights(self, video_id, video_language='English', verbose=False):
        self.check_access_token()

        if verbose:
            print('Getting video insights for: {}'.format(video_id))

        insights_url = f"https://api.videoindexer.ai/{self.vi_location}/Accounts/{self.vi_account_id}/Videos/{video_id}/Index?accessToken={self.access_token}&language={video_language}"  # NOQA E501
        insights_response = requests.get(insights_url)
        insights_data = insights_response.json()

        return insights_data

    def get_frame(self, video_id, thumbnailId, video_language='English', verbose=False):
        self.check_access_token()

        if verbose:
            print('Getting video insights for: {}'.format(video_id))

        # insights_url = f"https://api.videoindexer.ai/{self.vi_location}/Accounts/{self.vi_account_id}/Videos/{video_id}/Index?accessToken={self.access_token}&language={video_language}"
        frame_url = f"https://api.videoindexer.ai/{self.vi_location}/Accounts/{self.vi_account_id}/Videos/{video_id}/Thumbnails/{thumbnailId}?accessToken={self.access_token}"
        frame_response = requests.get(frame_url)
        image = Image.open(BytesIO(frame_response.content))
        # image.save(str(x)+'.jpg', 'JPEG')
        image.show()

        return

    def get_video_name_to_id_dict(self):
        all_videos = self.get_all_videos_list()
        names = [video['name'] for video in all_videos]
        ids = [video['id'] for video in all_videos]
        self.video_name_to_id_dict = dict(zip(names, ids))
        return self.video_name_to_id_dict

    def get_transcript_text_from_insights(self, insights_data):
        if insights_data['state'] != "Processed":
            return None
        if len(insights_data['videos']) > 1:
            print("more than 1 videos, name: ", insights_data['name'], "VI ID: ", insights_data['id'])
        transcript = insights_data['videos'][0]['insights']['transcript']

        formatted_transcript = []
        raw_text = ''
        for v in transcript:
            # Extract start time and remove milliseconds
            start_time = v['instances'][0]['start']
            # Splitting the time and discarding milliseconds
            start_time_components = start_time.split('.')
            formatted_time = start_time_components[0]  # This will have the format h:mm:ss
            # Append formatted time and text to the new list
            formatted_transcript.append({'time': formatted_time, 'text': v['text']})
            raw_text += v['text'] + ' '

        # Return a list of dictionaries with 'time' and 'text'
        return formatted_transcript, raw_text


