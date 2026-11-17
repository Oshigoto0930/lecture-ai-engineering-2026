"""実SQLiteと固定ベクトルで、索引作成から検索までを確認する。APIは呼ばない。"""

import json
from unittest.mock import Mock

import pytest

from app import retrieval
from scripts.build_rag_index import build_index


@pytest.fixture
def materials(tmp_path):
    source = tmp_path / "lectures.json"
    source.write_text(json.dumps([
        {"id": f"lec{n:02d}-main", "title": f"講義{n}", "content": [
            {"section": "章", "content": [
                {"id": f"lec{n:02d}-main-p001", "title": f"ページ{n}",
                 "page": 1, "content": f"本文{n}"}]}]}
        for n in (1, 2, 5)
    ], ensure_ascii=False), encoding="utf-8")
    return source, tmp_path / "index.sqlite3"


def test_built_index_can_be_searched(materials, monkeypatch):
    source, database = materials
    texts = []

    def embed(text, task):
        assert task == "RETRIEVAL_DOCUMENT"
        texts.append(text)
        return [1, 0] if "本文1" in text else [0, 1]

    result = build_index(source, database, embedder=embed)
    assert result["pages"] == 2  # 第5回の資料は検索対象に含めない
    assert all("章" in text and "ページ" in text for text in texts)
    monkeypatch.setattr(retrieval, "RAG_DB", database)
    monkeypatch.setattr(retrieval, "embed_text", lambda *_: [1, 0])
    hits = retrieval.search("質問")
    assert [h["page_id"] for h in hits] == ["lec01-main-p001", "lec02-main-p001"]
    assert hits[0]["content"] == "本文1"
    assert hits[0]["distance"] == pytest.approx(0)


def test_search_adds_unique_adjacent_pages_without_crossing_documents(tmp_path, monkeypatch):
    source = tmp_path / "lectures.json"
    database = tmp_path / "index.sqlite3"
    pages = [
        {"id": f"lec01-main-p00{n}", "title": f"ページ{n}",
         "page": n, "content": f"本文{n}"}
        for n in (1, 2, 3)
    ]
    other_document_page = {
        "id": "lec02-main-p004", "title": "別資料のページ4",
        "page": 4, "content": "別資料の本文",
    }
    source.write_text(json.dumps([
        {"id": "lec01-main", "title": "講義1", "content": [
            {"section": "章", "content": pages}]},
        {"id": "lec02-main", "title": "講義2", "content": [
            {"section": "章", "content": [other_document_page]}]},
    ], ensure_ascii=False), encoding="utf-8")
    build_index(
        source, database,
        embedder=lambda text, _: [1, 0] if "本文1" in text or "本文3" in text else [0, 1],
    )
    monkeypatch.setattr(retrieval, "RAG_DB", database)
    monkeypatch.setattr(retrieval, "RAG_TOP_K", 2)
    monkeypatch.setattr(retrieval, "embed_text", lambda *_: [1, 0])

    hits = retrieval.search("質問")

    assert [hit["page_id"] for hit in hits] == ["lec01-main-p001", "lec01-main-p003"]
    adjacent_pages = [page for hit in hits for page in hit["adjacent_pages"]]
    assert [page["page_id"] for page in adjacent_pages] == ["lec01-main-p002"]
    assert adjacent_pages[0]["content"] == "本文2"


def test_existing_index_survives_failed_rebuild(materials):
    source, database = materials
    build_index(source, database, embedder=lambda *_: [1, 0])
    before = database.read_bytes()
    embed = Mock(side_effect=RuntimeError("埋め込みに失敗"))
    with pytest.raises(FileExistsError):
        build_index(source, database, embedder=embed)
    embed.assert_not_called()
    with pytest.raises(RuntimeError, match="埋め込みに失敗"):
        build_index(source, database, rebuild=True, embedder=embed)
    assert database.read_bytes() == before
    assert not list(database.parent.glob(".rag-build-*"))
