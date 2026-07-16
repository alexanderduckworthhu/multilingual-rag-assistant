# Architecture — WHO Guidance QA

## One sentence

Answer grounded questions over public WHO guidance in English and French, with citations — and refuse when retrieval is weak.

## Pipeline

```
data/sample + data/raw
        │
        ▼
 load_docs → chunk (recursive, overlap)
        │
        ▼
 embed (multilingual-e5-small, query:/passage: prefixes)
        │
        ▼
 Chroma (cosine, metadata: language, doc_id, title, url)
        │
        ▼
 retrieve top-k ──► distance gate ──► refuse OR generate
                                      │
                          OpenAI gpt-4o-mini (temp=0)
                          OR extractive fallback (no API key)
                                      │
                                      ▼
                         Streamlit: answer + expandable sources
```

## Decision table

| Choice | Decision | Alternative considered | Why this one |
|---|---|---|---|
| Corpus | WHO guidance EN+FR | UNGA resolutions | Geneva-relevant, bilingual, denser for laptop eval |
| Chunking | Recursive, 800 / 120 | Semantic/LLM chunking | Deterministic and debuggable |
| Embeddings | multilingual-e5-small | OpenAI embeddings | Shared EN/FR space, offline, free |
| Vector store | Chroma | FAISS, Pinecone | Local metadata filters, no cloud |
| LLM | gpt-4o-mini + extractive | Ollama-only | Citation quality + no-key demo path |
| Multilingual | One index + language metadata | Dual indexes | Cross-lingual retrieval is intentional |
| Anti-hallucination | Distance gate + closed context + citations + temp 0 | “Trust the model” | Independent, measurable controls |

## Multilingual indexing

1. Embed every passage with the same multilingual model.  
2. Store `language` in metadata — do not create separate collections unless hard isolation is required.  
3. At query time, optionally filter `where={"language": "fr"}`; default searches both.  
4. Answer language is independent of retrieve language.

## Hallucination-reduction stack

1. Refuse if best cosine distance exceeds threshold.  
2. Closed context — prompt forbids outside knowledge.  
3. Citations required — each claim ends with `[chunk_id]`.  
4. Temperature 0.  
5. UI shows raw passages for human verification.  
6. Publish Precision@k and MRR — do not claim “no hallucinations.”

## Evaluation

```bash
python -m scripts.build_index
python -m scripts.run_eval
```

Reports land in `data/processed/eval_report.json`.
