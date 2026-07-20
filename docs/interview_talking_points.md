# Interview talking points (90 seconds)

## Opening (15s)

I built a bilingual RAG assistant over public WHO guidance so an analyst can ask in English or French and get answers with citations, the trust pattern international organizations need when policy wording matters.

## Architecture (30s)

I use recursive chunking with overlap for debuggable boundaries, multilingual-e5 so English and French share one vector space, and Chroma so the demo runs locally. Generation uses gpt-4o-mini with a closed-context citation prompt, plus an extractive fallback when there is no API key, so retrieval quality stays visible.

## Trust / hallucination (25s)

I refuse when retrieval distance is weak, constrain the prompt to retrieved passages, require chunk IDs on claims, set temperature to zero, and show raw sources in the UI. I measure retrieval with Precision@k and MRR on a golden set rather than claiming the model never invents.

## Why this role (20s)

This matches knowledge-tool workflows at WHO/UN agencies and advisory firms: grounded answers, bilingual corpora, and measurable retrieval, not chat for its own sake.
