import os
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 1. 한글 폰트 등록 (Windows 맑은 고딕)
FONT_REGULAR = "Malgun"
FONT_BOLD = "Malgun-Bold"

malgun_path = "C:/Windows/Fonts/malgun.ttf"
malgun_bd_path = "C:/Windows/Fonts/malgunbd.ttf"

if os.path.exists(malgun_path):
    pdfmetrics.registerFont(TTFont(FONT_REGULAR, malgun_path))
else:
    FONT_REGULAR = "Helvetica"

if os.path.exists(malgun_bd_path):
    pdfmetrics.registerFont(TTFont(FONT_BOLD, malgun_bd_path))
else:
    FONT_BOLD = FONT_REGULAR

def create_manual_pdf(filename: str = "Deepwoken_Build_Analyzer_Guide.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # 커스텀 스타일 정의
    title_style = ParagraphStyle(
        "DocTitle",
        fontName=FONT_BOLD,
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#1A365D"),
        alignment=1, # Center
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        fontName=FONT_REGULAR,
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#4A5568"),
        alignment=1,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        "Heading1_Custom",
        fontName=FONT_BOLD,
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#2B6CB0"),
        spaceBefore=8,
        spaceAfter=5
    )

    body_style = ParagraphStyle(
        "Body_Custom",
        fontName=FONT_REGULAR,
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#2D3748"),
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        "Code_Custom",
        fontName=FONT_REGULAR,
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#C53030"),
        backColor=colors.HexColor("#EDF2F7"),
        spaceAfter=3
    )

    table_header_style = ParagraphStyle(
        "TableHeader",
        fontName=FONT_BOLD,
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=1
    )

    table_cell_style = ParagraphStyle(
        "TableCell",
        fontName=FONT_REGULAR,
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#2D3748")
    )

    table_cell_bold = ParagraphStyle(
        "TableCellBold",
        fontName=FONT_BOLD,
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#1A202C")
    )

    box_title_style = ParagraphStyle(
        "BoxTitle",
        fontName=FONT_BOLD,
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#2C5282")
    )

    elements = []

    # =========================================================================
    # [PAGE 1] 시스템 매뉴얼 및 CLI 명령어 총정리
    # =========================================================================
    elements.append(Paragraph("⚔️ Deepwoken Build Analyzer — 사용자 매뉴얼", title_style))
    elements.append(Paragraph("멀티모달 AI(Gemini 2.5) & 서브 에이전트 기반 빌드 분석 및 RAG 추천 시스템", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#3182CE"), spaceAfter=8))

    # Section 1: 시스템 개요
    elements.append(Paragraph("1. 시스템 개요 (System Overview)", h1_style))
    elements.append(Paragraph(
        "<b>Deepwoken Build Analyzer</b>는 Roblox의 하드코어 액션 RPG <i>Deepwoken</i>의 방대한 빌드 데이터를 "
        "유튜브 영상(화면 UI + 음성 해설) 및 웹사이트(위키/빌드 플래너/포럼)로부터 자동 추출하여 "
        "정형 JSON 및 고가독성 Markdown 문서로 구조화하고, <b>ChromaDB 벡터 데이터베이스(RAG)</b>를 통해 "
        "사용자 맞춤형 빌드를 실시간으로 추천해주는 AI 솔루션입니다.",
        body_style
    ))

    # Section 2: 설치 및 환경 설정
    elements.append(Paragraph("2. 빠른 시작 & 환경 설정 (Setup Guide)", h1_style))
    
    setup_data = [
        [
            Paragraph("<b>단계</b>", table_header_style),
            Paragraph("<b>실행 명령어 및 작업 내용</b>", table_header_style),
            Paragraph("<b>설명</b>", table_header_style)
        ],
        [
            Paragraph("1. 의존성 설치", table_cell_bold),
            Paragraph("<code>pip install -r requirements.txt</code>", code_style),
            Paragraph("yt-dlp, google-generativeai, chromadb, rich 등 설치", table_cell_style)
        ],
        [
            Paragraph("2. API 키 등록", table_cell_bold),
            Paragraph("<code>.env</code> 파일 생성 후 <code>GEMINI_API_KEY=AIzaSy...</code> 입력", code_style),
            Paragraph("Google AI Studio 발급 키 등록", table_cell_style)
        ],
        [
            Paragraph("3. 설정 커스텀", table_cell_bold),
            Paragraph("<code>config/settings.yaml</code> (모델, 경로 등 설정)", code_style),
            Paragraph("Gemini 모델(Pro/Flash), ChromaDB 경로 지정", table_cell_style)
        ]
    ]

    setup_table = Table(setup_data, colWidths=[80, 240, 200])
    setup_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2B6CB0")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(setup_table)
    elements.append(Spacer(1, 8))

    # Section 3: CLI 명령어 총정리
    elements.append(Paragraph("3. 핵심 CLI 명령어 가이드 (CLI Reference)", h1_style))

    cli_data = [
        [
            Paragraph("<b>모드 (Command)</b>", table_header_style),
            Paragraph("<b>사용 예시 (Example)</b>", table_header_style),
            Paragraph("<b>핵심 기능 및 동작</b>", table_header_style)
        ],
        [
            Paragraph("<b>analyze</b><br/>(단일 영상 분석)", table_cell_bold),
            Paragraph("<code>python main.py analyze \"https://youtu.be/...\"</code>", code_style),
            Paragraph("유튜브 고화질 영상 다운로드 → Gemini Files API 멀티모달 분석 → JSON/MD 생성 → ChromaDB 자동 인덱싱", table_cell_style)
        ],
        [
            Paragraph("<b>web</b><br/>(웹 서브에이전트)", table_cell_bold),
            Paragraph("<code>python main.py web \"https://deepwoken.co/...\"</code>", code_style),
            Paragraph("웹페이지 스크래핑 → 2개 서브 에이전트(Build/Context) 병렬 파싱 → 교차 검증 → RAG 자동 등록", table_cell_style)
        ],
        [
            Paragraph("<b>batch</b><br/>(대량 일괄 분석)", table_cell_bold),
            Paragraph("<code>python main.py batch \"PLAYLIST_URL\" --playlist</code>", code_style),
            Paragraph("재생목록 내 모든 영상 순차 분석 (Rate Limit 대응 딜레이 및 오류 복구 내장)", table_cell_style)
        ],
        [
            Paragraph("<b>index</b><br/>(RAG 재인덱싱)", table_cell_bold),
            Paragraph("<code>python main.py index</code>", code_style),
            Paragraph("<code>data/analysis</code> 및 <code>knowledge_base</code>의 모든 빌드를 ChromaDB에 일괄 재색인", table_cell_style)
        ],
        [
            Paragraph("<b>chat</b><br/>(AI 빌드 추천)", table_cell_bold),
            Paragraph("<code>python main.py chat</code>", code_style),
            Paragraph("RAG 벡터 검색 기반 대화형 어드바이저 실행 (스탯, 무기, 탤런트, 콤보 추천)", table_cell_style)
        ]
    ]

    cli_table = Table(cli_data, colWidths=[90, 210, 220])
    cli_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2B6CB0")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(cli_table)
    elements.append(Spacer(1, 8))

    # Footer note for page 1
    elements.append(Paragraph(
        "💡 <b>Tip</b>: 영상 파일은 2GB 초과 시 자동으로 720p/480p로 다운스케일링되며, 분석 완료 후 로컬 디스크 절약을 위해 임시 영상이 자동 삭제됩니다.",
        body_style
    ))

    # =========================================================================
    # [PAGE 2] 작동 예시 및 내부 동작 원리 상세 설명
    # =========================================================================
    elements.append(PageBreak())

    elements.append(Paragraph("🔍 Deepwoken Build Analyzer — 실전 작동 예시 및 동작 원리", title_style))
    elements.append(Paragraph("서브 에이전트 협업 메커니즘 & RAG 기반 AI 빌드 추천 시나리오", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#3182CE"), spaceAfter=8))

    # Section 1: 내부 동작 원리
    elements.append(Paragraph("1. 멀티 서브 에이전트 동작 원리 (Internal Architecture)", h1_style))
    
    flow_data = [
        [
            Paragraph("<b>단계</b>", table_header_style),
            Paragraph("<b>담당 서브 에이전트</b>", table_header_style),
            Paragraph("<b>상세 동작 원리 및 역할</b>", table_header_style)
        ],
        [
            Paragraph("1단계: 수집", table_cell_bold),
            Paragraph("<b>WebScraperAgent</b><br/>(웹) / <b>VideoCollector</b>(영상)", table_cell_style),
            Paragraph("HTML 파싱(태그/표/메타 추출) 또는 yt-dlp 최고화질 다운로드 및 메타데이터 추출", table_cell_style)
        ],
        [
            Paragraph("2단계: 분석", table_cell_bold),
            Paragraph("<b>BuildParser</b> &<br/><b>ContextParser</b> (병렬)", table_cell_style),
            Paragraph("• BuildParser: 스탯(STR/FORT/AGI 등), 속성, Oath, 탤런트, 만트라, SoO 추출<br/>• ContextParser: PvP/PvE 분류, 난이도, 제작자 의도, 장단점, 콤보 사이클 추출", table_cell_style)
        ],
        [
            Paragraph("3단계: 검증", table_cell_bold),
            Paragraph("<b>CrossValidatorAgent</b>", table_cell_style),
            Paragraph("서브 에이전트 추출 결과 병합, Deepwoken 인게임 룰셋 검증(스탯 범위, Oath 정규화) 및 정제", table_cell_style)
        ],
        [
            Paragraph("4단계: 지식화", table_cell_bold),
            Paragraph("<b>BuildStructurer</b> &<br/><b>KnowledgeBuilder</b>", table_cell_style),
            Paragraph("<code>data/analysis/ID.json</code> 및 <code>data/knowledge_base/ID.md</code> 생성 후 ChromaDB 벡터 DB 임베딩", table_cell_style)
        ],
        [
            Paragraph("5단계: 추천", table_cell_bold),
            Paragraph("<b>BuildAdvisor</b> (챗봇)", table_cell_style),
            Paragraph("사용자 자연어 쿼리 벡터 검색 → 관련 상위 빌드 컨텍스트 결합 → Gemini 맞춤형 조언 생성", table_cell_style)
        ]
    ]

    flow_table = Table(flow_data, colWidths=[70, 140, 310])
    flow_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2B6CB0")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    elements.append(flow_table)
    elements.append(Spacer(1, 8))

    # Section 2: 실전 작동 예시 (Step-by-Step Scenario)
    elements.append(Paragraph("2. 실전 작동 예시 (Step-by-Step Walkthrough)", h1_style))

    scenario_box_data = [
        [
            Paragraph("<b>[시나리오 1] 웹사이트 빌드 분석 실행</b>", box_title_style)
        ],
        [
            Paragraph(
                "<code>> python main.py web \"https://deepwoken.co/builder?id=sample_build\"</code><br/>"
                "<font color='#276749'><b>[1/5]</b> WebScraper: HTML 및 테이블 파싱 완료</font><br/>"
                "<font color='#276749'><b>[2/5]</b> BuildParser & ContextParser: 병렬 AI 분석 수행 완료</font><br/>"
                "<font color='#276749'><b>[3/5]</b> CrossValidator: JSON 스키마 및 Oath('Jetstriker') 정규화 완료</font><br/>"
                "<font color='#276749'><b>[4/5]</b> ChromaDB: 'Thundercall Speedster' 벡터 인덱싱 완료 (소요: 3.2초)</font>",
                code_style
            )
        ],
        [
            Paragraph("<b>[시나리오 2] RAG 기반 AI 빌드 추천 챗봇 대화</b>", box_title_style)
        ],
        [
            Paragraph(
                "<code>> python main.py chat</code><br/>"
                "<b>질문:</b> <font color='#B7791F'>\"포티튜드 50 이상이고 빠른 기동성을 가진 Thundercall PvP 빌드 추천해줘\"</font><br/>"
                "<b>어드바이저 응답:</b><br/>"
                "💡 <b>추천 빌드: ⚔️ Thundercall Jetstriker Speedster (PvP / Advanced)</b><br/>"
                "• <b>스탯 분배</b>: STR 80, FORT 50 (Exoskeleton 확보), AGI 40, WIL 25, Thundercall 80<br/>"
                "• <b>핵심 Oath & 탤런트</b>: Jetstriker / Showstopper, Exoskeleton, Lightning Cloak<br/>"
                "• <b>추천 콤보</b>: Slide 대시 진입 → M1 평타 2타 → Lightning Cloak 발동 후 Mantra 연계<br/>"
                "• <b>출처</b>: deepwoken.co / 영상 링크 제공",
                body_style
            )
        ]
    ]

    scenario_table = Table(scenario_box_data, colWidths=[520])
    scenario_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor("#EBF8FF")),
        ('BACKGROUND', (0, 1), (0, 1), colors.HexColor("#F7FAFC")),
        ('BACKGROUND', (0, 2), (0, 2), colors.HexColor("#EBF8FF")),
        ('BACKGROUND', (0, 3), (0, 3), colors.HexColor("#F7FAFC")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#BEE3F8")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(scenario_table)
    elements.append(Spacer(1, 8))

    # Section 3: 주요 팁
    elements.append(Paragraph("3. 운영 및 최적화 팁 (Pro Tips)", h1_style))
    elements.append(Paragraph(
        "• <b>비용 최적화</b>: <code>config/settings.yaml</code>에서 <code>gemini.model</code>을 <code>gemini-2.5-flash</code>로 설정하면 비용과 속도를 극대화할 수 있습니다.<br/>"
        "• <b>데이터 수정</b>: <code>data/knowledge_base/*.md</code> 파일을 직접 편집한 후 <code>python main.py index</code>를 실행하면 즉시 지식 베이스에 반영됩니다.",
        body_style
    ))

    # PDF 빌드
    doc.build(elements)
    print(f"✅ Successfully generated PDF manual: {filename}")

if __name__ == "__main__":
    out_pdf = sys.argv[1] if len(sys.argv) > 1 else "Deepwoken_Build_Analyzer_Guide.pdf"
    create_manual_pdf(out_pdf)
