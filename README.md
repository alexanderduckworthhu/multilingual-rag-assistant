# WHO Guidance QA

A multilingual document question-answering assistant over public WHO topic guidance (English/French index; UI and answers in EN, FR, DE, IT, PT, ZH, RU), built for analysts in bilingual international workflows who need cited answers they can verify.

| | |
|---|---|
| **Project page** | https://alexanderduckworthhu.github.io/multilingual-rag-assistant/ |
| **Live demo** | https://multilingual-rag-assistant.streamlit.app/ |
| **Status** | Portfolio demo, **not** an official WHO product |
| **Latest retrieval eval** | Precision@5 **0.65** · MRR **0.938** (n=8 golden queries) |

---

## Why it exists

Policy and health analysts often need a short answer grounded in WHO wording, not a fluent paraphrase from a general-purpose chat model. Generic assistants invent citations; monolingual search fails in bilingual international workflows. This project indexes English and French guidance in one vector space, answers with passage IDs, and refuses when retrieval is weak.

---

## Technical decisions

- **Corpus. WHO topic guidance (mental health, UHC, primary health care), EN+FR**  
  Considered UNGA resolutions. Chose WHO for denser prose, natural bilingual pairs, and WHO HQ relevance. UNGA remains a v2 corpus once metrics are stable.

- **Chunking, recursive character split, 800 chars / 120 overlap**  
  Considered semantic/LLM chunking. Chose recursive split for deterministic, debuggable boundaries; overlap reduces answers split across chunks.

- **Embeddings, `intfloat/multilingual-e5-small`**  
  Considered OpenAI `text-embedding-3-small`. Chose E5 for a shared EN/FR space, offline demos, and explicit `query:` / `passage:` prefixes that are easy to defend.

- **Vector store. Chroma (cosine, local persist)**  
  Considered FAISS and Pinecone. Chose Chroma for metadata filters, zero Docker/cloud cost, and inspectable on-disk indexes.

- **Generator, `gpt-4o-mini` (temperature 0) + extractive fallback**  
  Considered local Ollama-only. Chose a citation-capable cloud model with a no-key extractive path so retrieval quality stays visible without paid credentials.

- **Trust stack, distance gate → closed-context prompt → `[chunk_id]` citations → UI passages**  
  Evaluates retrieval (Precision@k, MRR) as the engineering claim; does not assert “zero hallucinations.”

---

## Results & metrics

From `python -m scripts.run_eval` on `data/eval/golden_queries.json` (8 labeled queries, top-k=5):

| Metric | Value |
|---|---|
| Precision@5 | **0.65** |
| Mean Reciprocal Rank (MRR) | **0.938** |
| Indexed documents / passages | 6 docs · 18 passages (sample corpus) |

Reproduce: rebuild the index, then re-run eval (commands below). Report file: `data/processed/eval_report.json`.

---

## Data

| Field | Detail |
|---|---|
| **Source** | Educational WHO-topic excerpts in `data/sample/` (EN/FR), plus optional HTML extracts via `scripts/download_corpus.py` from public WHO health-topic pages |
| **License / use** | Public web content for a **portfolio demo only**, not redistributed as official WHO publications; not for clinical or operational decisions |
| **Languages** | Indexed corpus: English + French. UI / questions / answers: EN, FR, DE, IT, PT, ES, AR, ZH (Mandarin), RU via multilingual-e5 + i18n |
| **Provenance** | Each passage keeps `doc_id`, `title`, `source_url`, `chunk_id` for citation and audit |
| **Production gap** | Replace samples with WHO IRIS / licensed corpora, add access logging, retention policy, and human review for high-stakes answers |

---

## Setup & usage

```bash
cd multilingual-rag-assistant
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Build local index (downloads embedding model on first run)
python -m scripts.build_index

# Optional: drafted answers (without this key, UI shows matching passages)
export OPENAI_API_KEY=sk-...

# Launch demo
streamlit run app.py

# Retrieval metrics for the writeup
python -m scripts.run_eval
```

Optional larger corpus (best-effort WHO topic page download):

```bash
python -m scripts.download_corpus
python -m scripts.build_index
python -m scripts.run_eval
```

Tests: `pytest -q`

---

## What I'd improve next

1. **Hybrid retrieval (BM25 + dense) + cross-encoder rerank**. Precision@5 is diluted when several chunks from the right doc crowd the top-k; a reranker would lift passage-level precision without abandoning multilingual dense search.
2. **Faithfulness check (NLI / entailment) as a second gate**, the distance threshold blocks weak retrieval; it does not catch a fluent model that overstates a retrieved sentence.
3. **WHO IRIS PDF pipeline with page-level provenance**, sample texts prove the architecture; production needs licensed PDFs, cleaner extraction, and page anchors in citations.

---

## Project layout

```
app.py                 Streamlit ask → answer → sources UI
src/config.py          Architectural constants + rationale
src/i18n.py            All user-facing UI strings (9 languages)
src/styles.py          CSS design tokens + motion
src/ingest/            load, chunk, embed
src/retrieve/          Chroma store + search
src/generate/          prompts + answer orchestration
src/eval/              Precision@k, MRR
data/sample/           Offline EN/FR WHO-style excerpts
data/eval/             Golden queries
scripts/               build_index, run_eval, download_corpus
docs/                  Architecture + interview talking points
REVERSE_ENGINEERING.txt
```

Deep dive: [`REVERSE_ENGINEERING.txt`](REVERSE_ENGINEERING.txt) · architecture table: [`docs/architecture.md`](docs/architecture.md)
