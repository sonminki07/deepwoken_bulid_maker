import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings
import chromadb.utils.embedding_functions as ef

logger = logging.getLogger(__name__)

class KnowledgeBuilder:
    """4단계: ChromaDB 벡터 DB 인덱싱 및 RAG 지식 베이스 구축기"""

    def __init__(
        self,
        db_path: str = "data/chromadb",
        collection_name: str = "deepwoken_builds",
        api_key: Optional[str] = None,
        use_gemini_embedding: bool = False
    ):
        self.db_path = Path(db_path)
        self.db_path.mkdir(parents=True, exist_ok=True)
        self.collection_name = collection_name
        self.client = chromadb.PersistentClient(path=str(self.db_path))

        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        embedding_fn = None
        if use_gemini_embedding and self.api_key:
            try:
                embedding_fn = GeminiEmbeddingFunction(api_key=self.api_key)
                logger.info("Using Gemini text-embedding for vector search.")
            except Exception as e:
                logger.warning(f"Failed to init Gemini embedding function: {e}. Falling back to default.")

        if embedding_fn is None:
            embedding_fn = ef.DefaultEmbeddingFunction()

        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=embedding_fn
        )

    def ingest_build(self, video_id: str, json_path: Path, md_path: Path) -> None:
        """단일 빌드 데이터(JSON + MD)를 벡터 DB에 인덱싱"""
        if not json_path.exists() or not md_path.exists():
            logger.error(f"Cannot ingest: files not found ({json_path}, {md_path})")
            return

        build_data = json.loads(json_path.read_text(encoding="utf-8"))
        md_content = md_path.read_text(encoding="utf-8")

        summary = build_data.get("build_summary", {})
        meta = build_data.get("video_meta", {})
        stats = build_data.get("stats", {})
        attunements = build_data.get("attunements", {})

        # ChromaDB 메타데이터 (string/int/float/bool 만 허용)
        flat_metadata = {
            "video_id": str(video_id),
            "build_name": str(summary.get("build_name", "Unknown")),
            "build_type": str(summary.get("build_type", "Hybrid")),
            "difficulty": str(summary.get("difficulty", "Intermediate")),
            "oath": str(build_data.get("oath", "None")),
            "channel": str(meta.get("channel", "Unknown")),
            "url": str(meta.get("url", "")),
            "strength": int(stats.get("strength", 0) or 0),
            "fortitude": int(stats.get("fortitude", 0) or 0),
            "agility": int(stats.get("agility", 0) or 0),
            "intelligence": int(stats.get("intelligence", 0) or 0),
            "willpower": int(stats.get("willpower", 0) or 0),
            "charisma": int(stats.get("charisma", 0) or 0),
        }

        # 속성 투자 여부 추가
        for att_name, val in attunements.items():
            if val and val > 0:
                flat_metadata[f"attunement_{att_name}"] = int(val)

        # 문서 upsert
        self.collection.upsert(
            ids=[video_id],
            documents=[md_content],
            metadatas=[flat_metadata]
        )
        logger.info(f"Indexed build '{flat_metadata['build_name']}' (ID: {video_id}) into ChromaDB.")

    def ingest_all(self, analysis_dir: str = "data/analysis", kb_dir: str = "data/knowledge_base") -> int:
        """분석 디렉토리 및 지식 베이스 내의 모든 빌드와 위키/티어리스트 문서를 일괄 인덱싱"""
        a_dir = Path(analysis_dir)
        k_dir = Path(kb_dir)
        count = 0

        # 1. 빌드 JSON + MD 인덱싱
        for json_file in a_dir.glob("*.json"):
            video_id = json_file.stem
            md_file = k_dir / f"{video_id}.md"
            if md_file.exists():
                self.ingest_build(video_id, json_file, md_file)
                count += 1

        # 2. 독립형 지식 문서 (tier_lists.md, wiki/*.md 등) 인덱싱
        for md_file in k_dir.rglob("*.md"):
            doc_id = f"doc_{md_file.stem}"
            # 이미 인덱싱된 빌드 MD는 스킵
            if (a_dir / f"{md_file.stem}.json").exists():
                continue
            
            content = md_file.read_text(encoding="utf-8")
            self.collection.upsert(
                ids=[doc_id],
                documents=[content],
                metadatas=[{
                    "video_id": doc_id,
                    "build_name": md_file.stem,
                    "build_type": "KnowledgeBase",
                    "difficulty": "All",
                    "oath": "All",
                    "channel": "DeepwokenWiki",
                    "url": "https://deepwoken.co"
                }]
            )
            count += 1
                
        logger.info(f"Successfully ingested {count} documents into ChromaDB.")
        return count

    def query(self, query_text: str, n_results: int = 5, where: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """자연어 쿼리로 유사 빌드 검색"""
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where=where
        )

        formatted = []
        if results and "documents" in results and results["documents"]:
            docs = results["documents"][0]
            metas = results["metadatas"][0] if "metadatas" in results else [{}] * len(docs)
            ids = results["ids"][0] if "ids" in results else [""] * len(docs)
            distances = results["distances"][0] if "distances" in results and results["distances"] else [0.0] * len(docs)

            for doc_id, doc, meta, dist in zip(ids, docs, metas, distances):
                formatted.append({
                    "id": doc_id,
                    "document": doc,
                    "metadata": meta,
                    "distance": dist
                })

        return formatted
