"""Streamlit entry point: ask WHO guidance questions and review cited answers."""

from __future__ import annotations

import html
import logging
import os
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

from src.config import (  # noqa: E402
    QUESTION_MIN_CHARS,
    QUESTION_TEXT_AREA_HEIGHT_PX,
    RETRIEVAL_TOP_K,
)
from src.generate.answer import RagResponse, answer_question  # noqa: E402
from src.i18n import (  # noqa: E402
    CORPUS_LANG_CODES,
    UI_LANG_CODES,
    example_questions,
    language_label,
    mode_label,
    status_label,
    t,
)
from src.retrieve.ensure_index import ensure_index  # noqa: E402
from src.retrieve.store import collection_count  # noqa: E402
from src.styles import APP_CSS  # noqa: E402

logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="WHO Guidance QA",
    page_icon="◎",
    layout="centered",
)

st.markdown(f"<style>{APP_CSS}</style>", unsafe_allow_html=True)


@st.cache_resource(show_spinner=False)
def _cached_ensure_index() -> int:
    """Build the sample index once per container if it is missing."""
    return ensure_index()


def _init_session_state() -> None:
    """Seed Streamlit session keys used by the ask → answer flow."""
    defaults: dict[str, object] = {
        "question": "",
        "last_result": None,
        "answer_lang": "en",
        "search_both": True,
        "search_lang": "en",
        "answer_lang_locked": False,
        "ui_lang": "en",
        "prev_ui_lang": "en",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _set_example_question(example_text: str) -> None:
    """Copy an example into the question box."""
    st.session_state.question = example_text


def _clear_question() -> None:
    """Clear the question box and hide the previous answer panel."""
    st.session_state.question = ""
    st.session_state.last_result = None


def _mark_answer_lang_locked() -> None:
    """Stop auto-syncing answer language with the interface language."""
    st.session_state.answer_lang_locked = True


def _sync_examples_to_ui_language(ui_lang: str) -> None:
    """When the UI language changes, refresh examples into the question box."""
    previous = st.session_state.get("prev_ui_lang")
    if previous == ui_lang:
        return
    examples = example_questions(ui_lang)
    current_question = (st.session_state.get("question") or "").strip()
    previous_examples = set(example_questions(previous)) if previous else set()
    # Replace empty box or a leftover example from the previous language.
    if not current_question or current_question in previous_examples:
        st.session_state.question = examples[0] if examples else ""
    st.session_state.prev_ui_lang = ui_lang
    st.session_state.last_result = None


def _status_css_class(rag_response: RagResponse) -> str:
    """Map response state to a CSS status class name."""
    if rag_response.mode == "empty_index":
        return "muted"
    if rag_response.grounded:
        return "ok"
    return "warn"


def _relevance_pct(cosine_distance: float) -> float:
    """Convert Chroma cosine distance to a 0–1 relevance score for display."""
    return max(0.0, min(1.0, 1.0 - cosine_distance))


def _corpus_language_name(code: str) -> str:
    """Label an indexed passage language (corpus is EN/FR only)."""
    return language_label(code) if code in CORPUS_LANG_CODES else code


def _run_search(ui_lang: str) -> None:
    """Validate input, retrieve, generate, and store the latest RagResponse."""
    question_text = (st.session_state.question or "").strip()
    if not question_text:
        st.warning(t(ui_lang, "empty_question"))
        return
    if len(question_text) < QUESTION_MIN_CHARS:
        st.warning(t(ui_lang, "question_too_short"))
        return

    retrieve_language = (
        None if st.session_state.search_both else st.session_state.search_lang
    )
    answer_language = (
        st.session_state.answer_lang
        if st.session_state.answer_lang_locked
        else ui_lang
    )
    with st.spinner(str(t(ui_lang, "loading"))):
        try:
            st.session_state.last_result = answer_question(
                question=question_text,
                answer_language=answer_language,
                retrieve_language=retrieve_language,
                top_k=RETRIEVAL_TOP_K,
            )
        except Exception:
            logger.exception("Search failed for question=%r", question_text)
            st.error(str(t(ui_lang, "msg_refusal")))


def _render_answer_panel(ui_lang: str, rag_response: RagResponse) -> None:
    """Render status, answer body, and expandable supporting passages."""
    status_text = status_label(ui_lang, rag_response.grounded, rag_response.mode)
    mode_text = mode_label(ui_lang, rag_response.mode)
    status_class = _status_css_class(rag_response)
    answer_html = html.escape(rag_response.answer)

    st.markdown(
        f"""
        <div class="rag-panel" role="region" aria-label="{html.escape(str(t(ui_lang, 'answer')))}">
          <div class="rag-status {status_class}">{html.escape(status_text)}</div>
          <p class="rag-mode">{html.escape(mode_text)}</p>
          <div class="rag-section-label" style="margin-top:0">{t(ui_lang, "answer")}</div>
          <div class="rag-answer">{answer_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="rag-section-label">{t(ui_lang, "sources")}</div>',
        unsafe_allow_html=True,
    )
    st.caption(str(t(ui_lang, "sources_hint")))

    display_passages = rag_response.display_passages or []
    if not display_passages:
        st.info(str(t(ui_lang, "no_sources")))
        return

    for rank, passage in enumerate(display_passages, start=1):
        relevance = _relevance_pct(passage.distance)
        language_name = _corpus_language_name(passage.source_language)
        expander_title = (
            f"#{rank} · {passage.title} · "
            f"{relevance:.0%} {t(ui_lang, 'distance_label')}"
        )
        with st.expander(expander_title, expanded=(rank == 1 and rag_response.grounded)):
            st.caption(
                f"{t(ui_lang, 'lang_label')}: {language_name} · "
                f"{t(ui_lang, 'passage_id')}: `{passage.chunk_id}`"
            )
            if passage.was_translated:
                st.caption(
                    str(
                        t(
                            ui_lang,
                            "translated_from",
                            source=language_name,
                        )
                    )
                )
            st.write(passage.display_text)
            if passage.was_translated:
                with st.expander(str(t(ui_lang, "show_original")), expanded=False):
                    st.write(passage.original_text)
            if passage.source_url:
                st.markdown(f"[{t(ui_lang, 'open_source')}]({passage.source_url})")


def main() -> None:
    """Compose the Streamlit page: sidebar, ask form, and answer panel."""
    _init_session_state()

    with st.sidebar:
        ui_lang = st.selectbox(
            str(t(st.session_state.ui_lang, "sidebar_lang")),
            options=list(UI_LANG_CODES),
            format_func=language_label,
            key="ui_lang",
        )
        _sync_examples_to_ui_language(ui_lang)

        st.markdown("---")
        st.subheader(str(t(ui_lang, "sidebar_about")))
        st.write(str(t(ui_lang, "sidebar_body")))

        try:
            with st.spinner(str(t(ui_lang, "index_preparing"))):
                indexed_passage_count = _cached_ensure_index()
        except Exception:
            logger.exception("Failed to ensure search index")
            try:
                indexed_passage_count = collection_count()
            except Exception:
                indexed_passage_count = 0

        if indexed_passage_count > 0:
            st.caption(str(t(ui_lang, "sidebar_ready", n=indexed_passage_count)))

    st.markdown(
        f"""
        <div class="rag-hero">
          <p class="rag-kicker">{t(ui_lang, "portfolio_note")}</p>
          <h1 class="rag-title">{t(ui_lang, "title")}</h1>
          <p class="rag-subtitle">{t(ui_lang, "subtitle")}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.text_area(
        str(t(ui_lang, "question")),
        key="question",
        height=QUESTION_TEXT_AREA_HEIGHT_PX,
        placeholder=str(t(ui_lang, "question_placeholder")),
    )

    action_cols = st.columns([3, 1])
    search_clicked = action_cols[0].button(
        str(t(ui_lang, "ask")),
        type="primary",
        use_container_width=True,
    )
    action_cols[1].button(
        str(t(ui_lang, "clear_question")),
        type="secondary",
        use_container_width=True,
        on_click=_clear_question,
    )

    st.caption(str(t(ui_lang, "try_these")))
    examples = example_questions(ui_lang)
    example_cols = st.columns(len(examples))
    for index, example_text in enumerate(examples):
        example_cols[index].button(
            example_text,
            key=f"example_{ui_lang}_{index}",
            type="secondary",
            use_container_width=True,
            on_click=_set_example_question,
            args=(example_text,),
        )

    with st.expander(str(t(ui_lang, "advanced")), expanded=False):
        st.selectbox(
            str(t(ui_lang, "answer_lang")),
            options=list(UI_LANG_CODES),
            format_func=language_label,
            key="answer_lang",
            on_change=_mark_answer_lang_locked,
        )
        st.checkbox(
            str(t(ui_lang, "search_both")),
            key="search_both",
            help=str(t(ui_lang, "search_both_help")),
        )
        if not st.session_state.search_both:
            st.radio(
                str(t(ui_lang, "search_lang")),
                options=list(CORPUS_LANG_CODES),
                format_func=language_label,
                horizontal=True,
                key="search_lang",
            )

    if search_clicked:
        _run_search(ui_lang)

    if st.session_state.last_result is not None:
        _render_answer_panel(ui_lang, st.session_state.last_result)
        if st.button(str(t(ui_lang, "retry")), type="secondary", key="retry_search"):
            _run_search(ui_lang)
            st.rerun()
    else:
        st.markdown(
            f'<div class="rag-empty">{t(ui_lang, "first_visit")}</div>',
            unsafe_allow_html=True,
        )


main()
