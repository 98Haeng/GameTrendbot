from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import BedrockChat
import boto3
import json
import pandas as pd
import glob
import os
def summary():
    session = boto3.Session()
    save_dir = 'Dataset/summarytext' 
    bedrock = session.client(
        service_name='bedrock-runtime',
        region_name='us-east-1',
        endpoint_url="https://bedrock-runtime.us-east-1.amazonaws.com"
    )
    ## 전체 txt파일 불러오기
    directory_path = '/Users/leeshinhaeng/Desktop/aws-bedrock-tutorial-main/NDC_Project/Dataset/fulltext'
    # 해당 폴더 내 모든 .txt 파일에 대한 패턴 생성
    file_pattern = os.path.join(directory_path, '*.txt')

    for i, file_path in enumerate(glob.glob(file_pattern), start=1):
        with open(file_path, 'r', encoding='utf-8') as file:
            script = file.read()
            print(f"파일: {file_path}")

            # 언어모델 설정
            llm = BedrockChat(model_kwargs={"temperature": 0, 'max_tokens_to_sample':1000},
                                    model_id="anthropic.claude-v2",
                                    client=bedrock,

                                )
            # 프롬프트 설정
            prompt = PromptTemplate(
                template="""백틱으로 둘러싸인 전사본을 이용해 해당 유튜브 비디오를 요약해주세요. \
                ```{text}```
                """, input_variables=["text"]
            )
            combine_prompt = PromptTemplate(
                template="""백틱(`) 안에 제공된 모든 유튜브 비디오 대본을 결합하세요 \
                ```{text}```
                10문장 이상 30문장 사이의 정리본을 제공해주세요.
                """, input_variables=["text"]
            )
            # LangChain을 활용하여 긴 글 요약하기
            # 글 쪼개기
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=0)
            texts = text_splitter.create_documents([script])
            # 요약하기
            chain = load_summarize_chain(llm, chain_type="map_reduce", verbose=False,
                                        map_prompt=prompt, combine_prompt=combine_prompt )
            summerize = chain.run(texts)
            # 최종 출력
            print(summerize)
            filename = f"{i}.txt"
            file_path = os.path.join(save_dir, filename)

            # 파일 저장
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(f"{summerize}")
