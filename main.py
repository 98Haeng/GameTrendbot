from youtube_crawl import crawling
from script_extract import extractor
import pandas as pd
from script_summary import summary

# 새로운 데이터를 집어넣는 경우에만 사용합니다.
def main():
    df_videos = crawling()
    print('Phase 1 : Crawling Complete')

    extractor(df_videos)
    print('Phase 2 : Extractor Complete')

    summary()
    print('Phase 3 : Summary Complete')

if __name__ == "__main__":
    main()

