from src.ingest.chunk import DocumentRecord, chunk_documents


def test_chunk_documents_assigns_stable_ids():
    docs = [
        DocumentRecord(
            doc_id="doc_a",
            title="A",
            language="en",
            source_url="",
            text=("Paragraph one. " * 40) + "\n\n" + ("Paragraph two. " * 40),
        )
    ]
    chunks = chunk_documents(docs)
    assert len(chunks) >= 1
    assert chunks[0].chunk_id.startswith("doc_a::c")
    assert chunks[0].language == "en"
