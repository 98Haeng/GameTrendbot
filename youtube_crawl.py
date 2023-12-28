## youtube_crawl.py
import pandas as pd
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from datetime import datetime, timezone
from googleapiclient.discovery import build
import urllib.parse
from dateutil.parser import parse

def crawling():
    # API 키 입력
    DEVELOPER_KEY = 'your_api' #여기 사용자의 api키를 입력하면 됩니다.
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'

    # 유튜브 API 인증 및 연결
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    # 동영상 검색
    search_response = youtube.search().list(
        q='넥슨 개발자 컨퍼런스',  #여기에 검색어 넣으시면 됩니당
        part='snippet',
        maxResults=500,
        channelId = 'UC3ZjKSQX9JJRCjw3aSrBXSg'
    ).execute()

    videos = []

    # 검색 결과에서 영상 정보 추출
    for item in search_response['items']:
        if item['id']['kind'] == 'youtube#video':
            video_id = item['id']['videoId']
            video_title = item['snippet']['title']
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            published_at = item['snippet']['publishedAt']
            upload_year = parse(published_at).year  # 업로드 년도 추출

            # 영상 정보를 리스트에 추가
            videos.append({
                'Title': video_title,
                'URL': video_url,
                'Year': upload_year
            })

    # 데이터프레임 생성
    df_videos = pd.DataFrame(videos)

    # 데이터프레임 출력 (또는 저장)
    print(df_videos.head())

    # Data폴더에 저장
    df_videos.to_excel('Dataset/video_list.xlsx', index=False)
    return df_videos