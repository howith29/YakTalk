# 💊 약톡(YakTalk)
LangChain + OpenAI 기반 약물 복용 및 부작용 상담 챗봇  
<br/>

## 📌 프로젝트 개요
약톡(YakTalk)은 600개의 의약품 정보를 기반으로 한 RAG (Retrieval-Augmented Generation) 시스템을 구축하여, 사용자가 약물 복용 중 발생하는 의문사항과 부작용에 대해 즉시 신뢰할 수 있는 상담을 받을 수 있는 대화형 헬스케어 AI 서비스입니다.

**🎯 핵심 가치**
- 즉시성: 24시간 언제든 접근 가능한 AI 상담
- 전문성: 500종 의약품 데이터 기반 신뢰할 수 있는 정보
- 안전성: KTAS 기반 5단계 응급도 평가 및 의도분석 기반 응급 키워드 자동 감지
- 편의성: 자연어 대화를 통한 직관적 상담 경험
<br/>

# 👥 팀 소개
**팀명**: 드럭 스토어 (Drug Store)  
| 팀원 | 역할 |
|-----|------|
|👸[슬희](https://github.com/howith29)| [기획 및 시스템 구현] 프로젝트 기획, 시스템 아키텍처 설계 및 구현, 챗봇 파이프라인 설계 및 구현(풀스택) |
|👸[승주](https://github.com/haseungju)| [데이터 엔지니어링 및 AI 모델 최적화] 데이터 수집/전처리, RAG 시스템 및 LLM 성능 최적화 |
<br/>

## 📂 파일 구성

| 파일명 | 설명 |
| ------ | ------ |
| `medical_rag.py` | RAG 검색 시스템 (FAISS 벡터DB, OpenAI 임베딩) |
| `intent_analyzer.py` | GPT-4 기반 의도 분석 및 응급 키워드 감지 모듈 |
| `emergency_evaluator.py` | KTAS 기반 응급도 평가 시스템 (5단계 위험도 판정) |
| `complete_medical_chatbot.py` | 통합 상담 파이프라인: 의도분석 → 응급평가 → RAG 검색 → 최종 응답 생성 |
<br/>

## ⚙️ 기술 스택

- LangChain: RAG 시스템 구축 및 문서 분할, 체인 관리
- OpenAI GPT-4: 의도 분석 및 자연어 응답 생성
- FAISS: 고속 벡터 유사도 검색 엔진
- OpenAI Embedding: text-embedding-3-small 모델 사용
- Pandas: 의약품 CSV 데이터 로드 및 처리
- hashlib, re: 쿼리 캐싱 및 전처리  
<br/>

## 🧱 시스템 아키텍처
```
사용자 질문
↓
의도 분석 (GPT-4 기반)
↓
응급도 평가 (KTAS 기반 5단계)
↓
RAG 검색 (FAISS + OpenAI Embedding)
↓
LLM 응답 생성 (프롬프트 기반 템플릿 답변)
↓
최종 응답 (위험도에 따른 응답 템플릿)
```
<br/>

## 📚 데이터 출처

**의약품 정보 데이터베이스**
- 출처: [식품의약품안전처 의약품개요정보(e약은요) 서비스](https://www.data.go.kr/data/15075057/openapi.do)
- 제공기관: 식품의약품안전처
- 데이터 규모: 500개 의약품 상세 정보 (효능·효과, 사용법, 주의사항, 상호작용, 부작용, 보관법)  
<br/>

## 💡 사용 예시

**🚨 응급상황 감지 예시**
```
👤 사용자: "타이레놀 먹고 호흡곤란이 심하고 의식이 흐려져요"

응답:
🚨응급상황 감지
타이레놀 복용 후 호흡곤란과 의식 장애는 심각한 알레르기 반응일 가능성이 있습니다.

🚨 즉시 119 신고하거나 응급실 방문하세요
• 약물 복용 즉시 중단
• 증상 변화 주의 깊게 관찰
```
<br/>

**📌 일반 부작용 예시**
```
👤 사용자: "타이레놀 먹고 속이 아파요"

응답:
👀 경과 관찰
타이레놀 복용 후 속쓰림은 일반적인 위장관 부작용일 수 있습니다.

👀 2-3일 경과 관찰 후 지속되면 병원 방문하세요
• 대부분 시간이 지나면 호전됩니다
```
<br/>

## 🔬 주요 기능 상세

- **의도 분석 (Intent Analyzer):**  
  - GPT-4 기반 프롬프트 분석 + 사전 정의 응급 키워드 rule 기반 보강
  - 질문 유형을 `side_effect`, `usage`, `efficacy`, `other`로 자동 분류
  - 증상 및 응급 키워드 자동 감지

- **응급도 평가 (Emergency Evaluator):**  
  - KTAS 기반 5단계 응급도 분류  
  - 증상 키워드 매칭을 통해 위험도 자동 판단

- **RAG 시스템 (MedicalRAGSystem):**  
  - CSV 데이터 로드 → 문서 분할 → 임베딩 생성 → FAISS 벡터저장소 구축
  - GPT-4 기반 프롬프트 엔지니어링으로 응답 생성

- **통합 파이프라인 (CompleteMedicalChat):**  
  - 의도분석 → 응급도 평가 → 검색 → 응답 → 위험도 템플릿 반영 → 최종 응답 출력
<br/>

## 📝 테스트 스크립트

- `demo_conversation()`: 샘플 5개 질문 자동 테스트 실행
- `quick_test()`: 단일 질문 빠른 테스트
- `test_emergency_evaluation()`: 응급도 평가 유닛테스트
<br/>

## 📊 발표 자료

- [발표 자료 링크](https://drive.google.com/file/d/1rxvm9Cas3rT-ULSCDUQyVDvHkTmTFsY8/view?usp=sharing)

---

## 🔄 v2 업데이트 (RAG Pipeline Upgrade)

### 개선 배경
기존 시스템의 검색 정확도와 답변 품질을 향상시키기 위해 RAG 파이프라인을 전면 재구성하였습니다.

### 주요 변경사항

#### 🗄️ 벡터 데이터베이스
| 항목 | 기존 (v1) | 개선 (v2) |
|------|-----------|-----------|
| 벡터 DB | FAISS (메모리) | Chroma (영구 저장) |
| 검색 방식 | Similarity | MMR (다양성 고려) |
| 데이터 규모 | 500개 | 4,770개 |

#### 📄 문서 전처리
- **키워드 추출 추가**: LLM이 약품별 핵심 키워드 3~5개 자동 추출
  - 주요 성분, 대상 질환, 약효 분류, 주의 대상 등
- **요약 생성 추가**: 약품 정보를 1문장으로 요약하여 의미 검색 정확도 향상
- **필드별 Document 분리**: 약품당 효능효과/사용법/부작용/주의사항/상호작용/보관법을 개별 Document로 저장

#### 🔍 검색 개선
- **MMR 검색기 도입**: 관련성과 다양성을 동시에 고려한 검색
  - fetch_k=10개 후보 중 다양성 기반으로 k=4개 선별
- **메타데이터 활용**: 약품명, 키워드, 요약, 필드 정보를 메타데이터로 저장

#### 📊 모니터링
- **Langfuse 연동**: 전체 파이프라인 트레이싱 및 프롬프트 버전 관리
  - 키워드 추출 체인 트레이싱
  - 답변 생성 체인 트레이싱
  - 프롬프트 버전 관리 (Langfuse Prompt Management)

### 업데이트된 시스템 아키텍처
```
사용자 질문
↓
의도 분석 (GPT-4 기반)
↓
응급도 평가 (KTAS 기반 5단계)
↓
MMR 검색 (Chroma + OpenAI Embedding)
  └ 키워드/요약 메타데이터 활용
↓
관련성 평가 (LLM-as-Judge)
↓
LLM 응답 생성 (query_type별 프롬프트)
↓
최종 응답 (위험도에 따른 응답 템플릿)
↓
Langfuse 트레이싱
```

### 업데이트된 파일 구성
| 파일명 | 설명 |
| ------ | ------ |
| `get_data.py` | 식품의약품안전처 API 기반 데이터 수집 |
| `rag_pipeline.ipynb` | RAG 파이프라인 구성 노트북 (데이터 전처리 → 벡터 저장소 → 검색기) |
| `medical_rag.py` | RAG 검색 시스템 (Chroma 벡터DB, MMR 검색, 관련성 평가) |
| `intent_analyzer.py` | GPT-4 기반 의도 분석 및 응급 키워드 감지 모듈 |
| `emergency_evaluator.py` | KTAS 기반 응급도 평가 시스템 (5단계 위험도 판정) |
| `complete_medical_chatbot.py` | 통합 상담 파이프라인 |

### 업데이트된 기술 스택
- **LangChain**: RAG 시스템 구축 및 문서 분할, 체인 관리
- **OpenAI GPT-4.1-mini**: 키워드 추출, 의도 분석 및 자연어 응답 생성
- **Chroma**: 영구 저장 벡터 데이터베이스
- **OpenAI Embedding**: text-embedding-3-small 모델 사용
- **Langfuse**: 프롬프트 관리 및 파이프라인 트레이싱
- **Pandas**: 의약품 CSV 데이터 로드 및 처리

### 향후 개선 예정
- [ ] Hybrid Search (BM25 + Embedding) 적용
- [ ] Reranker 도입 (Cross Encoder)
- [ ] 의도 분석 고도화 (약품 성분명 자동 매핑)
- [ ] LLM-as-Judge 답변 품질 평가
- [ ] Pairwise Evaluation (v1 vs v2 성능 비교)