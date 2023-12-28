# 패키지 불러오기
from langchain.document_loaders import YoutubeLoader
import pandas as pd
import os
from tqdm import tqdm
def extractor(df):
    # fulltext 저장 디렉토리 지정
    save_dir = 'Dataset/fulltext'  # 저장할 경로 지정
    os.makedirs(save_dir, exist_ok=True)

    #URL 주소
    # df = pd.read_excel('/Users/leeshinhaeng/Desktop/aws-bedrock-tutorial-main/NDC_Project/Dataset/video_list.xlsx')

    full_extract = []
    titles = []
    for i in tqdm(range(len(df))):
        url = df['URL'][i]
        title = df['Title'][i]
        youtube_video_url= url
        loader = YoutubeLoader.from_youtube_url(youtube_video_url, language='ko')
        transcript = loader.load()
        try:
            script = transcript[0].page_content
            if len(script) > 6000:
                # 파일 이름 설정 (순번을 포함)
                filename = f"{i}.txt"
                file_path = os.path.join(save_dir, filename)
                # 파일 저장
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(f"제목: {title}\n\n{script}")
        except:
            print(f'{title}에서 오류 발생!')
            continue

