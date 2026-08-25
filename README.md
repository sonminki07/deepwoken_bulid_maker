# ⚔️ Deepwoken Build Analyzer

> 유튜브 Deepwoken 빌드 가이드 영상을 멀티모달 AI(Gemini 2.5)로 자동 분석하여 JSON 및 지식 문서로 구조화하고, RAG(ChromaDB) 기반으로 최적의 빌드를 추천해주는 파이프라인 시스템

---

## 🌟 주요 기능

1. **자동 수집 (Collector)**: `yt-dlp`를 통해 고화질 비디오 및 상세 메타데이터(제목, 채널, 업로드일)를 자동 추출. 2GB 초과 시 자동 해상도 다운스케일링.
2. **멀티모달 시각+음성 분석 (Analyzer)**: Gemini Files API를 통해 인게임 UI 화면(스탯, 탤런트 목록, 장비)과 유튜버 음성 해설(운용법, 콤보, 필수 탤런트 강조)을 동시 분석하여 구조화된 JSON 추출.
3. **구조화 & 지식 문서화 (Structurer)**: JSON Schema 정밀 검증 후 사람이 읽기 쉬운 표준 Markdown 지식 문서 자동 생성.
4. **벡터 인덱싱 & RAG (Knowledge Builder)**: `text-embedding-004` 모델을 활용하여 ChromaDB에 임베딩 및 다차원 메타데이터(스탯, Oath, 속성 등) 인덱싱.
5. **빌드 어드바이저 챗봇 (Build Advisor)**: 사용자의 선호 스타일, 속성, PvP/PvE 목적에 맞는 최적의 빌드를 찾아 분석 및 추천해주는 대화형 CLI.

---

## 📁 프로젝트 구조

```
deepwoken-build-analyzer/
├── config/
│   ├── settings.yaml          # 전역 설정 파일 (모델, 경로, 파라미터)
│   └── build_schema.json      # Deepwoken 빌드 JSON Schema 정의
├── agents/
│   ├── collector.py           # 1단계: yt-dlp 영상 다운로드 수집기
│   ├── analyzer.py            # 2단계: Gemini 멀티모달 분석기
│   ├── structurer.py          # 3단계: JSON 검증 & Markdown 변환기
│   └── knowledge_builder.py   # 4단계: ChromaDB 벡터 인덱싱 & RAG
├── chatbot/
│   └── build_advisor.py       # 5단계: 대화형 빌드 어드바이저 챗봇
├── pipeline/
│   ├── orchestrator.py        # E2E 파이프라인 오케스트레이터
│   └── batch_processor.py     # 대량 영상 / 재생목록 배치 처리기
├── prompts/
│   └── analysis_prompt.txt    # Gemini 멀티모달 분석 프롬프트
├── data/
│   ├── videos/                # 다운로드된 비디오 임시 보관함
│   ├── analysis/              # 분석 결과 JSON 저장소
│   ├── knowledge_base/        # 변환된 Markdown 지식 저장소
│   └── chromadb/              # ChromaDB 벡터 임베딩 저장소
├── main.py                    # 통합 CLI 엔트리포인트
├── requirements.txt           # Python 의존성 패키지
└── .env.example               # 환경 변수 예시 템플릿
```

---

## 🚀 빠른 시작 가이드 (Quickstart)

### 1. 의존성 설치
```bash
cd C:\Users\minki\.gemini\antigravity\scratch\deepwoken-build-analyzer
pip install -r requirements.txt
```

### 2. API 키 설정
`.env.example` 파일을 복사하여 `.env` 파일을 생성하고 Gemini API 키를 입력합니다.
```env
GEMINI_API_KEY=AIzaSy...
```

### 3. 단일 영상 분석
```bash
python main.py analyze "https://www.youtube.com/watch?v=VIDEO_ID"
```

### 4. 재생목록 일괄 분석
```bash
python main.py batch "https://www.youtube.com/playlist?list=PLAYLIST_ID" --playlist
```

### 5. 빌드 추천 챗봇 대화
```bash
python main.py chat
```

---

## 🛠️ CLI 옵션 가이드

| 명령어 | 옵션 | 설명 |
| :--- | :--- | :--- |
| `analyze` | `URL` | 단일 영상 다운로드 → 분석 → JSON/MD 변환 → RAG 등록 |
| `batch` | `TARGET` | 재생목록 또는 여러 URL 일괄 분석 (`--playlist` 플래그 지원) |
| `index` | | 기존 `data/analysis` 및 `data/knowledge_base` 파일을 ChromaDB에 재등록 |
| `chat` | `--model`, `--top-k` | RAG 기반 빌드 추천 대화형 터미널 인터페이스 실행 |
