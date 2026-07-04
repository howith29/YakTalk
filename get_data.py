from urllib.request import urlopen
from urllib.parse import urlencode
import xml.etree.ElementTree as ET
import pandas as pd
import time
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("DRUG_API_KEY")
base_url = "https://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList"

all_data = []
page = 1
num_of_rows = 100

while True:
    params = urlencode({
        "serviceKey": api_key,
        "pageNo": page,
        "numOfRows": num_of_rows,
        "type": "xml"
    })

    url = f"{base_url}?{params}"
    response = urlopen(url)
    root = ET.fromstring(response.read())

    body = root.find('body')
    items = body.find('items')

    if items is None or len(items) == 0:
        break

    for item in items:
        all_data.append({
            "제품명": item.findtext('itemName'),
            "업체명": item.findtext('entpName'),
            "품목기준코드": item.findtext('itemSeq'),
            "효능효과": item.findtext('efcyQesitm'),
            "사용법": item.findtext('useMethodQesitm'),
            "부작용": item.findtext('seQesitm'),
            "주의사항": item.findtext('atpnQesitm'),
            "주의사항_경고": item.findtext('atpnWarnQesitm'),
            "상호작용": item.findtext('intrcQesitm'),
            "보관법": item.findtext('depositMethodQesitm'),
        })

    total_count = int(body.findtext('totalCount', 0))
    print(f"페이지 {page} 완료 - 누적 {len(all_data)}개 / 전체 {total_count}개")

    if page * num_of_rows >= total_count:
        break

    page += 1
    time.sleep(0.3)

df = pd.DataFrame(all_data)
print(f"\n총 {len(df)}개 약품 데이터 수집 완료")
df.to_csv("drug_info.csv", index=False, encoding='utf-8-sig')
print("drug_info.csv 저장 완료!")