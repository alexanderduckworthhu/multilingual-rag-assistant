"""Design tokens and Streamlit CSS shell for the WHO Guidance QA demo."""

from __future__ import annotations

APP_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,650&family=Source+Sans+3:wght@400;500;600;700&display=swap');

:root {
  --color-ink: #0b1f33;
  --color-ink-soft: #122033;
  --color-slate: #334155;
  --color-slate-mid: #3d5a73;
  --color-muted: #5b6b7c;
  --color-mode: #52657a;
  --color-surface: #f4f7fb;
  --color-sidebar: #eef3f9;
  --color-panel: rgba(255, 255, 255, 0.78);
  --color-border: rgba(15, 45, 80, 0.10);
  --color-primary: #005bbb;
  --color-primary-soft: rgba(0, 91, 187, 0.08);
  --color-primary-ring: rgba(0, 91, 187, 0.14);
  --color-glow-a: #d9e6f5;
  --color-glow-b: #e7eef7;
  --color-ok-bg: #e5f3ea;
  --color-ok-fg: #1f6b3a;
  --color-warn-bg: #fff2df;
  --color-warn-fg: #8a5a12;
  --color-muted-bg: #e8eef6;
  --color-muted-fg: #314860;
  --font-sans: "Source Sans 3", "Segoe UI", sans-serif;
  --font-display: "Fraunces", Georgia, serif;
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 24px;
  --space-6: 32px;
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-pill: 999px;
  --shadow-cta: 0 8px 20px rgba(0, 91, 187, 0.22);
  --shadow-cta-hover: 0 10px 24px rgba(0, 91, 187, 0.28);
  --motion-fast: 180ms ease;
  --motion-panel: 450ms ease-out;
}

html, body, [class*="css"] {
  font-family: var(--font-sans);
}

.stApp {
  background:
    radial-gradient(1200px 500px at 10% -10%, var(--color-glow-a) 0%, transparent 55%),
    radial-gradient(900px 420px at 100% 0%, var(--color-glow-b) 0%, transparent 50%),
    var(--color-surface);
}

/* Keep the Streamlit chrome from blocking content while scrolling */
header[data-testid="stHeader"],
.stAppHeader,
div[data-testid="stToolbar"],
.stAppToolbar,
.stDecoration {
  background: transparent !important;
  background-color: transparent !important;
  box-shadow: none !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
}

header[data-testid="stHeader"]::before,
.stAppHeader::before {
  background: transparent !important;
}

h1, h2, h3, .rag-title {
  font-family: var(--font-display) !important;
  letter-spacing: -0.02em;
}

.rag-hero {
  animation: ragFadeUp var(--motion-panel);
  margin-bottom: var(--space-3);
}

.rag-kicker {
  color: var(--color-slate-mid);
  font-size: 0.92rem;
  font-weight: 500;
  margin: 0 0 var(--space-2) 0;
}

.rag-title {
  font-size: clamp(1.9rem, 3vw, 2.45rem);
  font-weight: 650;
  color: var(--color-ink);
  margin: 0 0 var(--space-2) 0;
  line-height: 1.15;
}

.rag-subtitle {
  color: var(--color-slate);
  font-size: 1.05rem;
  line-height: 1.5;
  max-width: 42rem;
  margin: 0;
}

.rag-empty {
  margin-top: var(--space-5);
  padding: var(--space-4) var(--space-5);
  border: 1px dashed var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-panel);
  color: var(--color-slate);
  animation: ragFadeIn var(--motion-panel);
}

.rag-panel {
  background: var(--color-panel);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-4) var(--space-5);
  margin: var(--space-4) 0 var(--space-4);
  animation: ragFadeUp var(--motion-panel);
  backdrop-filter: blur(6px);
}

.rag-status {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  font-size: 0.9rem;
  font-weight: 600;
  padding: 6px 12px;
  border-radius: var(--radius-pill);
  margin-bottom: var(--space-3);
  animation: ragFadeIn var(--motion-panel);
}

.rag-status::before {
  content: "";
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
  flex-shrink: 0;
}

.rag-status.ok {
  background: var(--color-ok-bg);
  color: var(--color-ok-fg);
}

.rag-status.warn {
  background: var(--color-warn-bg);
  color: var(--color-warn-fg);
}

.rag-status.muted {
  background: var(--color-muted-bg);
  color: var(--color-muted-fg);
}

.rag-mode {
  color: var(--color-mode);
  font-size: 0.9rem;
  margin: 0 0 var(--space-3) 0;
}

.rag-answer {
  font-size: 1.05rem;
  line-height: 1.65;
  color: var(--color-ink-soft);
  white-space: pre-wrap;
  animation: ragFadeIn var(--motion-panel);
}

.rag-section-label {
  font-family: var(--font-display);
  font-size: 1.2rem;
  font-weight: 650;
  color: var(--color-ink);
  margin: var(--space-5) 0 var(--space-2);
}

div.stButton > button[kind="primary"] {
  background: var(--color-primary) !important;
  border: none !important;
  color: #fff !important;
  font-weight: 700 !important;
  font-size: 1.02rem !important;
  padding: 10px var(--space-5) !important;
  border-radius: var(--radius-md) !important;
  box-shadow: var(--shadow-cta);
  transition: transform var(--motion-fast), box-shadow var(--motion-fast), filter var(--motion-fast);
}

div.stButton > button[kind="primary"]:hover {
  filter: brightness(1.05);
  transform: translateY(-1px);
  box-shadow: var(--shadow-cta-hover);
}

div.stButton > button[kind="primary"]:focus-visible,
div[data-testid="stButton"] > button[kind="secondary"]:focus-visible {
  outline: 3px solid var(--color-primary-ring) !important;
  outline-offset: 2px;
}

div[data-testid="stButton"] > button[kind="secondary"] {
  background: transparent !important;
  border: 1px solid var(--color-border) !important;
  color: var(--color-ink-soft) !important;
  font-weight: 500 !important;
  border-radius: var(--radius-pill) !important;
  transition: background var(--motion-fast), border-color var(--motion-fast), transform var(--motion-fast);
}

div[data-testid="stButton"] > button[kind="secondary"]:hover {
  background: var(--color-primary-soft) !important;
  border-color: rgba(0, 91, 187, 0.35) !important;
  transform: translateY(-1px);
}

textarea {
  border-radius: var(--radius-md) !important;
  border-color: var(--color-border) !important;
  transition: border-color 200ms ease, box-shadow 200ms ease;
}

textarea:focus {
  border-color: rgba(0, 91, 187, 0.55) !important;
  box-shadow: 0 0 0 3px var(--color-primary-ring) !important;
}

section[data-testid="stSidebar"] {
  background: var(--color-sidebar);
}

div[data-testid="stExpander"] {
  background: rgba(255, 255, 255, 0.65);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
  margin-bottom: var(--space-2);
}

@keyframes ragFadeUp {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes ragFadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@media (prefers-reduced-motion: reduce) {
  .rag-hero, .rag-panel, .rag-status, .rag-answer, .rag-empty,
  div.stButton > button[kind="primary"],
  div[data-testid="stButton"] > button[kind="secondary"] {
    animation: none !important;
    transition: none !important;
  }
}
"""

# Applied in addition to APP_CSS when the interface language reads right-to-left.
RTL_CSS = """
.stApp {
  direction: rtl;
}

.stApp .rag-hero,
.stApp .rag-panel,
.stApp .rag-empty,
.stApp .rag-answer,
.stApp .rag-subtitle,
.stApp .rag-mode,
.stApp .rag-kicker,
.stApp .rag-title,
.stApp .rag-section-label,
.stApp [data-testid="stMarkdownContainer"],
.stApp [data-testid="stCaptionContainer"],
.stApp label {
  text-align: right;
}

.stApp textarea,
.stApp input {
  text-align: right;
}

.stApp .rag-status {
  flex-direction: row-reverse;
}

.stApp div[data-testid="stExpander"] summary {
  flex-direction: row-reverse;
  text-align: right;
}

.stApp div[data-testid="stAlert"] {
  text-align: right;
}
"""
