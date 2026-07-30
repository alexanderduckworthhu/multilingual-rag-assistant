"""User-facing strings for UI languages and grounded-answer messages."""

from __future__ import annotations

from typing import Any

# Interface + answer languages (queries can be any of these against the EN/FR index).
UI_LANG_CODES: tuple[str, ...] = ("en", "fr", "de", "it", "pt", "es", "ar", "zh", "ru")

# Indexed document languages only (sample corpus).
CORPUS_LANG_CODES: tuple[str, ...] = ("en", "fr")

LANGUAGE_LABELS: dict[str, str] = {
    "en": "English",
    "fr": "Français",
    "de": "Deutsch",
    "it": "Italiano",
    "pt": "Português",
    "es": "Español",
    "ar": "العربية",
    "zh": "中文",
    "ru": "Русский",
}

LLM_LANGUAGE_NAMES: dict[str, str] = {
    "en": "English",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "es": "Spanish",
    "ar": "Arabic",
    "zh": "Simplified Chinese (Mandarin)",
    "ru": "Russian",
}

# Interface languages that read right-to-left.
RTL_LANG_CODES: tuple[str, ...] = ("ar",)

UI: dict[str, dict[str, Any]] = {
    "en": {
        "page_title": "WHO Guidance QA",
        "title": "WHO Guidance QA",
        "subtitle": (
            "Ask about public WHO guidance in your language. "
            "The index holds English and French passages; answers include "
            "citations, or a clear refusal when retrieval is too weak."
        ),
        "portfolio_note": "Portfolio demo · not an official WHO tool",
        "question": "Your question",
        "question_placeholder": "Example: What is universal health coverage?",
        "ask": "Search the guidance",
        "clear_question": "Clear question",
        "try_these": "Start from an example",
        "answer_lang": "Answer language",
        "search_both": "Search English and French documents together",
        "search_both_help": (
            "The corpus is English and French. Multilingual embeddings still "
            "match questions in other languages. Turn off to restrict retrieval "
            "to one document language."
        ),
        "search_lang": "Retrieve from documents in",
        "advanced": "Search options",
        "answer": "Answer",
        "sources": "Supporting passages",
        "sources_hint": "Open a passage to verify wording against the source text.",
        "no_sources": "No passages were retrieved for this question.",
        "empty_question": "Enter a question before searching (at least a few words).",
        "question_too_short": "Add a little more detail so retrieval has something to match.",
        "loading": "Searching indexed WHO guidance…",
        "first_visit": (
            "Type a question above, or pick an example. "
            "You will see a cited answer when retrieval is strong enough, "
            "and a refusal when it is not."
        ),
        "retry": "Search again",
        "status_grounded": "Grounded, supported by indexed passages",
        "status_refused": "Refused, retrieval match too weak to answer safely",
        "status_empty": "Index empty, build the index before searching",
        "mode_llm": "Drafted from retrieved passages (LLM)",
        "mode_extractive": "Showing top matching passages (no API key configured)",
        "mode_refused": "Generation skipped, see explanation below",
        "mode_empty_index": "No documents indexed yet",
        "mode_llm_error": "Model unavailable, showing matching passages instead",
        "sidebar_lang": "Interface language",
        "sidebar_about": "About",
        "sidebar_body": (
            "Multilingual retrieval-augmented QA over public WHO topic guidance. "
            "Ask in English, French, German, Italian, Portuguese, Spanish, Arabic, "
            "Mandarin, or Russian against a shared EN/FR index, with citations and "
            "a distance gate."
        ),
        "sidebar_ready": "{n} passages indexed",
        "index_preparing": "Preparing the search index…",
        "sidebar_empty": (
            "Index is empty. From the project root run:\n"
            "`python -m scripts.build_index`"
        ),
        "distance_label": "relevance",
        "lang_label": "Passage language",
        "open_source": "Open original page",
        "passage_id": "Passage ID",
        "examples": [
            "What is mental health according to WHO?",
            "How should countries strengthen primary health care?",
            "What is universal health coverage?",
        ],
        "msg_empty_index": (
            "The search index is still warming up. Wait a moment, then try again."
        ),
        "msg_refusal": (
            "No passage matched this question closely enough to answer safely. "
            "Ask about mental health, universal health coverage, or primary "
            "health care, or search both English and French documents."
        ),
        "msg_extractive_header": (
            "No LLM API key configured. Top matching passages:"
        ),
        "msg_extractive_same_lang": (
            "Showing passages in your answer language when available."
        ),
        "msg_extractive_other_lang": (
            "No indexed passage in your answer language matched closely enough. "
            "Showing the best English/French source passages (original wording). "
            "Set OPENAI_API_KEY for a drafted answer in your language."
        ),
        "msg_passages_translated": (
            "Source passages were translated into your answer language. "
            "Open “Show original” under each source to verify the indexed wording."
        ),
        "translated_from": "Translated from {source}",
        "show_original": "Show original wording",

    },
    "fr": {
        "page_title": "QA orientations OMS",
        "title": "QA sur les orientations OMS",
        "subtitle": (
            "Posez une question sur des orientations OMS publiques dans votre langue. "
            "L’index contient des passages en anglais et en français, les réponses "
            "sont citées, ou clairement refusées si la récupération est trop faible."
        ),
        "portfolio_note": "Démo portfolio · pas un outil officiel de l’OMS",
        "question": "Votre question",
        "question_placeholder": "Exemple : Qu’est-ce que la couverture sanitaire universelle ?",
        "ask": "Chercher dans les orientations",
        "clear_question": "Effacer la question",
        "try_these": "Partir d’un exemple",
        "answer_lang": "Langue de la réponse",
        "search_both": "Chercher dans les documents anglais et français",
        "search_both_help": (
            "Le corpus est en anglais et en français. Les embeddings multilingues "
            "peuvent aussi matcher d’autres langues. Désactivez pour limiter "
            "à une seule langue de document."
        ),
        "search_lang": "Récupérer depuis les documents en",
        "advanced": "Options de recherche",
        "answer": "Réponse",
        "sources": "Passages sources",
        "sources_hint": "Ouvrez un passage pour vérifier le libellé dans le texte source.",
        "no_sources": "Aucun passage n’a été récupéré pour cette question.",
        "empty_question": "Saisissez une question avant de chercher.",
        "question_too_short": "Ajoutez un peu plus de détail pour améliorer la recherche.",
        "loading": "Recherche dans les orientations OMS indexées…",
        "first_visit": (
            "Saisissez une question ci-dessus, ou choisissez un exemple. "
            "Vous verrez une réponse citée si la récupération est assez solide, "
            "et un refus dans le cas contraire."
        ),
        "retry": "Relancer la recherche",
        "status_grounded": "Fondé, appuyé par des passages indexés",
        "status_refused": "Refusé, correspondance trop faible pour répondre",
        "status_empty": "Index vide, construisez l’index avant de chercher",
        "mode_llm": "Rédigé à partir des passages (LLM)",
        "mode_extractive": "Meilleurs passages (aucune clé API configurée)",
        "mode_refused": "Génération ignorée, voir l’explication ci-dessous",
        "mode_empty_index": "Aucun document indexé",
        "mode_llm_error": "Modèle indisponible, passages affichés à la place",
        "sidebar_lang": "Langue de l’interface",
        "sidebar_about": "À propos",
        "sidebar_body": (
            "QA multilingue augmentée par récupération sur des orientations OMS publiques. "
            "Posez votre question en anglais, français, allemand, italien, portugais, "
            "espagnol, arabe, chinois mandarin ou russe contre un index EN/FR partagé, "
            "avec citations et un seuil de distance."
        ),
        "sidebar_ready": "{n} passages indexés",
        "index_preparing": "Préparation de l’index de recherche…",
        "sidebar_empty": (
            "L’index est vide. Depuis la racine du projet :\n"
            "`python -m scripts.build_index`"
        ),
        "distance_label": "pertinence",
        "lang_label": "Langue du passage",
        "open_source": "Ouvrir la page d’origine",
        "passage_id": "ID du passage",
        "examples": [
            "Qu'est-ce que la santé mentale selon l'OMS ?",
            "Comment renforcer les soins de santé primaires ?",
            "Qu'est-ce que la couverture sanitaire universelle ?",
        ],
        "msg_empty_index": (
            "L’index de recherche est encore en cours de préparation. Réessayez dans un instant."
        ),
        "msg_refusal": (
            "Aucun passage ne correspond assez pour répondre de façon fiable. "
            "Posez une question sur la santé mentale, la couverture sanitaire "
            "universelle ou les soins de santé primaires."
        ),
        "msg_extractive_header": (
            "Aucune clé API LLM configurée. Passages les plus proches :"
        ),
        "msg_extractive_same_lang": (
            "Passages affichés dans la langue de votre réponse lorsqu’ils sont disponibles."
        ),
        "msg_extractive_other_lang": (
            "Aucun passage indexé dans la langue de votre réponse n’a assez bien correspondu. "
            "Voici les meilleurs passages sources en anglais/français (libellé d’origine). "
            "Définissez OPENAI_API_KEY pour une réponse rédigée dans votre langue."
        ),
        "msg_passages_translated": (
            "Les passages sources ont été traduits dans la langue de votre réponse. "
            "Ouvrez « Afficher l’original » sous chaque source pour vérifier le libellé indexé."
        ),
        "translated_from": "Traduit depuis {source}",
        "show_original": "Afficher le libellé d’origine",

    },
    "de": {
        "page_title": "WHO-Leitlinien QA",
        "title": "WHO-Leitlinien QA",
        "subtitle": (
            "Stellen Sie Fragen zu öffentlichen WHO-Leitlinien in Ihrer Sprache. "
            "Der Index enthält englische und französische Passagen; Antworten "
            "sind zitiert, oder klar abgelehnt, wenn die Suche zu schwach ist."
        ),
        "portfolio_note": "Portfolio-Demo · kein offizielles WHO-Tool",
        "question": "Ihre Frage",
        "question_placeholder": "Beispiel: Was ist universelle Gesundheitsversorgung?",
        "ask": "Leitlinien durchsuchen",
        "clear_question": "Frage löschen",
        "try_these": "Mit einem Beispiel starten",
        "answer_lang": "Antwortsprache",
        "search_both": "Englische und französische Dokumente gemeinsam durchsuchen",
        "search_both_help": (
            "Der Korpus ist Englisch und Französisch. Mehrsprachige Embeddings "
            "können auch andere Fragesprachen zuordnen. Deaktivieren, um auf "
            "eine Dokumentsprache zu beschränken."
        ),
        "search_lang": "Abrufen aus Dokumenten in",
        "advanced": "Suchoptionen",
        "answer": "Antwort",
        "sources": "Belegpassagen",
        "sources_hint": "Öffnen Sie eine Passage, um den Wortlaut zu prüfen.",
        "no_sources": "Für diese Frage wurden keine Passagen gefunden.",
        "empty_question": "Geben Sie zuerst eine Frage ein.",
        "question_too_short": "Etwas mehr Detail verbessert die Suche.",
        "loading": "Durchsuche indexierte WHO-Leitlinien…",
        "first_visit": (
            "Geben Sie oben eine Frage ein oder wählen Sie ein Beispiel. "
            "Sie erhalten eine zitierte Antwort bei starker Suche, "
            "sonst eine klare Ablehnung."
        ),
        "retry": "Erneut suchen",
        "status_grounded": "Belegt, gestützt durch indexierte Passagen",
        "status_refused": "Abgelehnt. Treffer zu schwach für eine sichere Antwort",
        "status_empty": "Index leer, zuerst Index aufbauen",
        "mode_llm": "Aus abgerufenen Passagen formuliert (LLM)",
        "mode_extractive": "Beste Passagen (kein API-Schlüssel)",
        "mode_refused": "Keine Generierung, siehe Erklärung unten",
        "mode_empty_index": "Noch keine Dokumente indexiert",
        "mode_llm_error": "Modell nicht verfügbar. Passagen statt Antwort",
        "sidebar_lang": "Oberflächensprache",
        "sidebar_about": "Über diese Demo",
        "sidebar_body": (
            "Mehrsprachige retrieval-augmentierte QA über öffentliche WHO-Themenleitlinien. "
            "Fragen auf Englisch, Französisch, Deutsch, Italienisch, Portugiesisch, "
            "Spanisch, Arabisch, Chinesisch (Mandarin) oder Russisch gegen einen "
            "gemeinsamen EN/FR-Index, mit Zitaten und Distanzschwelle."
        ),
        "sidebar_ready": "{n} Passagen indexiert",
        "index_preparing": "Suchindex wird vorbereitet…",
        "sidebar_empty": (
            "Index ist leer. Im Projektordner ausführen:\n"
            "`python -m scripts.build_index`"
        ),
        "distance_label": "Relevanz",
        "lang_label": "Passagensprache",
        "open_source": "Originalseite öffnen",
        "passage_id": "Passagen-ID",
        "examples": [
            "Was versteht die WHO unter psychischer Gesundheit?",
            "Wie sollten Länder die Primärversorgung stärken?",
            "Was ist universelle Gesundheitsversorgung?",
        ],
        "msg_empty_index": (
            "Der Suchindex wird noch vorbereitet. Bitte versuchen Sie es gleich erneut."
        ),
        "msg_refusal": (
            "Kein Passagen-Treffer war stark genug für eine sichere Antwort. "
            "Fragen Sie zu psychischer Gesundheit, universeller "
            "Gesundheitsversorgung oder Primärversorgung."
        ),
        "msg_extractive_header": (
            "Kein LLM-API-Schlüssel konfiguriert. Beste Passagen:"
        ),
        "msg_extractive_same_lang": (
            "Passagen in Ihrer Antwortsprache werden bevorzugt angezeigt."
        ),
        "msg_extractive_other_lang": (
            "Kein indexierter Treffer in Ihrer Antwortsprache war stark genug. "
            "Es folgen die besten englischen/französischen Quellpassagen (Originalwortlaut). "
            "Setzen Sie OPENAI_API_KEY für eine formulierte Antwort in Ihrer Sprache."
        ),
        "msg_passages_translated": (
            "Quellpassagen wurden in Ihre Antwortsprache übersetzt. "
            "Öffnen Sie „Original anzeigen“, um den indexierten Wortlaut zu prüfen."
        ),
        "translated_from": "Übersetzt aus dem {source}",
        "show_original": "Originalwortlaut anzeigen",

    },
    "it": {
        "page_title": "QA orientamenti OMS",
        "title": "QA sugli orientamenti OMS",
        "subtitle": (
            "Fate domande sugli orientamenti OMS pubblici nella vostra lingua. "
            "L’indice contiene passaggi in inglese e francese; le risposte "
            "sono citate, o rifiutate se il recupero è troppo debole."
        ),
        "portfolio_note": "Demo portfolio · non uno strumento ufficiale OMS",
        "question": "La vostra domanda",
        "question_placeholder": "Esempio: Cos’è la copertura sanitaria universale?",
        "ask": "Cerca negli orientamenti",
        "clear_question": "Cancella domanda",
        "try_these": "Parti da un esempio",
        "answer_lang": "Lingua della risposta",
        "search_both": "Cerca nei documenti inglesi e francesi insieme",
        "search_both_help": (
            "Il corpus è in inglese e francese. Gli embedding multilingue "
            "possono comunque abbinare altre lingue. Disattiva per limitare "
            "a una sola lingua dei documenti."
        ),
        "search_lang": "Recupera dai documenti in",
        "advanced": "Opzioni di ricerca",
        "answer": "Risposta",
        "sources": "Passaggi a supporto",
        "sources_hint": "Aprite un passaggio per verificare il testo sorgente.",
        "no_sources": "Nessun passaggio recuperato per questa domanda.",
        "empty_question": "Inserite una domanda prima di cercare.",
        "question_too_short": "Aggiungete un po’ più di dettaglio per la ricerca.",
        "loading": "Ricerca negli orientamenti OMS indicizzati…",
        "first_visit": (
            "Scrivete una domanda sopra, oppure scegliete un esempio. "
            "Vedrete una risposta citata se il recupero è solido, "
            "altrimenti un rifiuto chiaro."
        ),
        "retry": "Cerca di nuovo",
        "status_grounded": "Fondato, supportato da passaggi indicizzati",
        "status_refused": "Rifiutato, corrispondenza troppo debole",
        "status_empty": "Indice vuoto, costruite prima l’indice",
        "mode_llm": "Redatto dai passaggi recuperati (LLM)",
        "mode_extractive": "Passaggi migliori (nessuna chiave API)",
        "mode_refused": "Generazione saltata, vedi spiegazione sotto",
        "mode_empty_index": "Nessun documento indicizzato",
        "mode_llm_error": "Modello non disponibile, mostro i passaggi",
        "sidebar_lang": "Lingua dell’interfaccia",
        "sidebar_about": "Informazioni",
        "sidebar_body": (
            "QA multilingue con retrieval aumentato sugli orientamenti OMS pubblici. "
            "Domande in inglese, francese, tedesco, italiano, portoghese, spagnolo, "
            "arabo, cinese mandarino o russo contro un indice EN/FR condiviso, con "
            "citazioni e soglia di distanza."
        ),
        "sidebar_ready": "{n} passaggi indicizzati",
        "index_preparing": "Preparazione dell’indice di ricerca…",
        "sidebar_empty": (
            "L’indice è vuoto. Dalla root del progetto:\n"
            "`python -m scripts.build_index`"
        ),
        "distance_label": "rilevanza",
        "lang_label": "Lingua del passaggio",
        "open_source": "Apri pagina originale",
        "passage_id": "ID passaggio",
        "examples": [
            "Cos’è la salute mentale secondo l’OMS?",
            "Come dovrebbero i paesi rafforzare l’assistenza sanitaria primaria?",
            "Cos’è la copertura sanitaria universale?",
        ],
        "msg_empty_index": (
            "L’indice di ricerca è ancora in preparazione. Riprova tra un momento."
        ),
        "msg_refusal": (
            "Nessun passaggio corrisponde abbastanza per rispondere in sicurezza. "
            "Chiedete di salute mentale, copertura sanitaria universale "
            "o assistenza sanitaria primaria."
        ),
        "msg_extractive_header": (
            "Nessuna chiave API LLM configurata. Passaggi più vicini:"
        ),
        "msg_extractive_same_lang": (
            "Vengono mostrati i passaggi nella lingua della risposta quando disponibili."
        ),
        "msg_extractive_other_lang": (
            "Nessun passaggio indicizzato nella lingua della risposta corrisponde abbastanza. "
            "Ecco i migliori passaggi sorgente in inglese/francese (testo originale). "
            "Impostate OPENAI_API_KEY per una risposta redatta nella vostra lingua."
        ),
        "msg_passages_translated": (
            "I passaggi sorgente sono stati tradotti nella lingua della risposta. "
            "Aprite « Mostra originale » sotto ogni fonte per verificare il testo indicizzato."
        ),
        "translated_from": "Tradotto da {source}",
        "show_original": "Mostra testo originale",

    },
    "pt": {
        "page_title": "QA orientações OMS",
        "title": "QA sobre orientações da OMS",
        "subtitle": (
            "Pergunte sobre orientações públicas da OMS no seu idioma. "
            "O índice contém trechos em inglês e francês; as respostas "
            "vêm com citações, ou uma recusa clara quando a recuperação é fraca."
        ),
        "portfolio_note": "Demo de portfólio · não é uma ferramenta oficial da OMS",
        "question": "A sua pergunta",
        "question_placeholder": "Exemplo: O que é cobertura universal de saúde?",
        "ask": "Pesquisar nas orientações",
        "clear_question": "Limpar pergunta",
        "try_these": "Começar com um exemplo",
        "answer_lang": "Idioma da resposta",
        "search_both": "Pesquisar documentos em inglês e francês juntos",
        "search_both_help": (
            "O corpus está em inglês e francês. Embeddings multilíngues ainda "
            "podem corresponder a outras línguas. Desative para restringir "
            "a um idioma de documento."
        ),
        "search_lang": "Recuperar de documentos em",
        "advanced": "Opções de pesquisa",
        "answer": "Resposta",
        "sources": "Trechos de apoio",
        "sources_hint": "Abra um trecho para verificar o texto de origem.",
        "no_sources": "Nenhum trecho foi recuperado para esta pergunta.",
        "empty_question": "Introduza uma pergunta antes de pesquisar.",
        "question_too_short": "Acrescente um pouco mais de detalhe para a pesquisa.",
        "loading": "A pesquisar orientações da OMS indexadas…",
        "first_visit": (
            "Escreva uma pergunta acima ou escolha um exemplo. "
            "Verá uma resposta citada se a recuperação for forte o suficiente, "
            "e uma recusa quando não for."
        ),
        "retry": "Pesquisar novamente",
        "status_grounded": "Fundamentado, apoiado por trechos indexados",
        "status_refused": "Recusado, correspondência demasiado fraca",
        "status_empty": "Índice vazio, construa o índice primeiro",
        "mode_llm": "Redigido a partir dos trechos (LLM)",
        "mode_extractive": "Melhores trechos (sem chave de API)",
        "mode_refused": "Geração omitida, ver explicação abaixo",
        "mode_empty_index": "Ainda sem documentos indexados",
        "mode_llm_error": "Modelo indisponível, a mostrar trechos",
        "sidebar_lang": "Idioma da interface",
        "sidebar_about": "Sobre",
        "sidebar_body": (
            "QA multilíngue com recuperação aumentada sobre orientações públicas da OMS. "
            "Pergunte em inglês, francês, alemão, italiano, português, espanhol, árabe, "
            "chinês mandarim ou russo contra um índice EN/FR partilhado, com citações "
            "e limiar de distância."
        ),
        "sidebar_ready": "{n} trechos indexados",
        "index_preparing": "A preparar o índice de pesquisa…",
        "sidebar_empty": (
            "O índice está vazio. Na raiz do projeto execute:\n"
            "`python -m scripts.build_index`"
        ),
        "distance_label": "relevância",
        "lang_label": "Idioma do trecho",
        "open_source": "Abrir página original",
        "passage_id": "ID do trecho",
        "examples": [
            "O que é saúde mental segundo a OMS?",
            "Como devem os países reforçar os cuidados de saúde primários?",
            "O que é cobertura universal de saúde?",
        ],
        "msg_empty_index": (
            "O índice de pesquisa ainda está a ser preparado. Tente novamente dentro de momentos."
        ),
        "msg_refusal": (
            "Nenhum trecho correspondeu o suficiente para responder com segurança. "
            "Pergunte sobre saúde mental, cobertura universal de saúde "
            "ou cuidados de saúde primários."
        ),
        "msg_extractive_header": (
            "Nenhuma chave de API LLM configurada. Melhores trechos:"
        ),
        "msg_extractive_same_lang": (
            "Quando disponíveis, os trechos são mostrados no idioma da resposta."
        ),
        "msg_extractive_other_lang": (
            "Nenhum trecho indexado no idioma da resposta correspondeu o suficiente. "
            "Seguem os melhores trechos em inglês/francês (redação original). "
            "Defina OPENAI_API_KEY para uma resposta redigida no seu idioma."
        ),
        "msg_passages_translated": (
            "Os trechos de origem foram traduzidos para o idioma da resposta. "
            "Abra « Mostrar original » em cada fonte para verificar o texto indexado."
        ),
        "translated_from": "Traduzido de {source}",
        "show_original": "Mostrar texto original",

    },
    "es": {
        "page_title": "QA orientaciones OMS",
        "title": "QA sobre orientaciones de la OMS",
        "subtitle": (
            "Consulte las orientaciones públicas de la OMS en su idioma. "
            "El índice contiene pasajes en inglés y francés; las respuestas "
            "incluyen citas, o un rechazo claro cuando la recuperación es "
            "demasiado débil."
        ),
        "portfolio_note": "Demo de portafolio · no es una herramienta oficial de la OMS",
        "question": "Su pregunta",
        "question_placeholder": "Ejemplo: ¿Qué es la cobertura sanitaria universal?",
        "ask": "Buscar en las orientaciones",
        "clear_question": "Borrar pregunta",
        "try_these": "Comience con un ejemplo",
        "answer_lang": "Idioma de la respuesta",
        "search_both": "Buscar en documentos en inglés y francés a la vez",
        "search_both_help": (
            "El corpus está en inglés y francés. Las incrustaciones "
            "multilingües igualmente pueden coincidir con preguntas en "
            "otros idiomas. Desactive esta opción para restringir la "
            "búsqueda a un solo idioma de documento."
        ),
        "search_lang": "Recuperar de documentos en",
        "advanced": "Opciones de búsqueda",
        "answer": "Respuesta",
        "sources": "Pasajes de apoyo",
        "sources_hint": "Abra un pasaje para verificar la redacción con el texto fuente.",
        "no_sources": "No se recuperó ningún pasaje para esta pregunta.",
        "empty_question": "Escriba una pregunta antes de buscar (al menos algunas palabras).",
        "question_too_short": "Agregue un poco más de detalle para que la búsqueda tenga algo que comparar.",
        "loading": "Buscando en las orientaciones indexadas de la OMS…",
        "first_visit": (
            "Escriba una pregunta arriba, o elija un ejemplo. "
            "Verá una respuesta citada cuando la recuperación sea "
            "suficientemente sólida, y un rechazo cuando no lo sea."
        ),
        "retry": "Buscar de nuevo",
        "status_grounded": "Fundamentada, respaldada por pasajes indexados",
        "status_refused": "Rechazada, la coincidencia de búsqueda es demasiado débil para responder con seguridad",
        "status_empty": "Índice vacío, construya el índice antes de buscar",
        "mode_llm": "Redactada a partir de los pasajes recuperados (LLM)",
        "mode_extractive": "Mostrando los pasajes más relevantes (no hay clave de API configurada)",
        "mode_refused": "Generación omitida, vea la explicación a continuación",
        "mode_empty_index": "Aún no hay documentos indexados",
        "mode_llm_error": "Modelo no disponible, mostrando pasajes coincidentes en su lugar",
        "sidebar_lang": "Idioma de la interfaz",
        "sidebar_about": "Acerca de",
        "sidebar_body": (
            "QA multilingüe con recuperación aumentada sobre orientaciones "
            "públicas de la OMS. Pregunte en inglés, francés, alemán, italiano, "
            "portugués, español, árabe, chino mandarín o ruso frente a un índice "
            "compartido EN/FR, con citas y un umbral de distancia."
        ),
        "sidebar_ready": "{n} pasajes indexados",
        "index_preparing": "Preparando el índice de búsqueda…",
        "sidebar_empty": (
            "El índice está vacío. Desde la raíz del proyecto, ejecute:\n"
            "`python -m scripts.build_index`"
        ),
        "distance_label": "relevancia",
        "lang_label": "Idioma del pasaje",
        "open_source": "Abrir página original",
        "passage_id": "ID del pasaje",
        "examples": [
            "¿Qué es la salud mental según la OMS?",
            "¿Cómo deben los países fortalecer la atención primaria de salud?",
            "¿Qué es la cobertura sanitaria universal?",
        ],
        "msg_empty_index": (
            "El índice de búsqueda todavía se está preparando. Espere un momento y vuelva a intentarlo."
        ),
        "msg_refusal": (
            "Ningún pasaje coincidió lo suficiente con esta pregunta como "
            "para responder con seguridad. Pregunte sobre salud mental, "
            "cobertura sanitaria universal o atención primaria de salud, o "
            "busque en los documentos en inglés y francés a la vez."
        ),
        "msg_extractive_header": (
            "No hay clave de API de LLM configurada. Pasajes más relevantes:"
        ),
        "msg_extractive_same_lang": (
            "Se muestran los pasajes en su idioma de respuesta cuando están disponibles."
        ),
        "msg_extractive_other_lang": (
            "Ningún pasaje indexado en su idioma de respuesta coincidió lo "
            "suficiente. Se muestran los mejores pasajes fuente en "
            "inglés/francés (redacción original). Configure OPENAI_API_KEY "
            "para obtener una respuesta redactada en su idioma."
        ),
        "msg_passages_translated": (
            "Los pasajes fuente se tradujeron a su idioma de respuesta. "
            "Abra «Mostrar original» debajo de cada fuente para verificar la redacción indexada."
        ),
        "translated_from": "Traducido de {source}",
        "show_original": "Mostrar redacción original",

    },
    "ar": {
        "page_title": "أسئلة وأجوبة: إرشادات منظمة الصحة العالمية",
        "title": "الأسئلة والأجوبة حول إرشادات منظمة الصحة العالمية",
        "subtitle": (
            "اطرح أسئلة حول الإرشادات العامة الصادرة عن منظمة الصحة العالمية "
            "بلغتك. يضم الفهرس مقاطع بالإنجليزية والفرنسية، وتتضمن الإجابات "
            "استشهادات، أو رفضاً واضحاً عندما يكون الاسترجاع ضعيفاً جداً."
        ),
        "portfolio_note": "عرض توضيحي لمحفظة الأعمال، وليس أداة رسمية لمنظمة الصحة العالمية",
        "question": "سؤالك",
        "question_placeholder": "مثال: ما هي التغطية الصحية الشاملة؟",
        "ask": "البحث في الإرشادات",
        "clear_question": "مسح السؤال",
        "try_these": "ابدأ بمثال",
        "answer_lang": "لغة الإجابة",
        "search_both": "البحث في الوثائق الإنجليزية والفرنسية معاً",
        "search_both_help": (
            "تتكون المجموعة النصية من وثائق بالإنجليزية والفرنسية. لا تزال "
            "التضمينات متعددة اللغات قادرة على مطابقة الأسئلة بلغات أخرى. "
            "عطّل هذا الخيار لتقييد الاسترجاع بلغة وثيقة واحدة."
        ),
        "search_lang": "الاسترجاع من الوثائق باللغة",
        "advanced": "خيارات البحث",
        "answer": "الإجابة",
        "sources": "المقاطع الداعمة",
        "sources_hint": "افتح أحد المقاطع للتحقق من الصياغة مقارنة بالنص المصدر.",
        "no_sources": "لم يتم استرجاع أي مقطع لهذا السؤال.",
        "empty_question": "أدخل سؤالاً قبل البحث (بضع كلمات على الأقل).",
        "question_too_short": "أضف مزيداً من التفاصيل حتى يكون لدى عملية الاسترجاع ما تطابقه.",
        "loading": "جارٍ البحث في إرشادات منظمة الصحة العالمية المفهرسة…",
        "first_visit": (
            "اكتب سؤالاً أعلاه، أو اختر أحد الأمثلة. ستظهر لك إجابة مدعومة "
            "بمصادر عندما يكون الاسترجاع قوياً بما يكفي، ورفضاً عندما لا "
            "يكون كذلك."
        ),
        "retry": "البحث مرة أخرى",
        "status_grounded": "مدعومة بمقاطع مفهرسة",
        "status_refused": "مرفوضة، تطابق الاسترجاع ضعيف جداً للإجابة بأمان",
        "status_empty": "الفهرس فارغ، قم ببناء الفهرس قبل البحث",
        "mode_llm": "تمت صياغتها من المقاطع المسترجعة (نموذج لغوي)",
        "mode_extractive": "عرض أفضل المقاطع المطابقة (لم يتم تكوين مفتاح واجهة برمجة التطبيقات)",
        "mode_refused": "تم تخطي التوليد، انظر التوضيح أدناه",
        "mode_empty_index": "لم تتم فهرسة أي وثائق بعد",
        "mode_llm_error": "النموذج غير متاح، يتم عرض المقاطع المطابقة بدلاً من ذلك",
        "sidebar_lang": "لغة الواجهة",
        "sidebar_about": "حول",
        "sidebar_body": (
            "نظام أسئلة وأجوبة متعدد اللغات قائم على الاسترجاع المعزز حول "
            "إرشادات منظمة الصحة العالمية العامة. اطرح أسئلتك بالإنجليزية أو "
            "الفرنسية أو الألمانية أو الإيطالية أو البرتغالية أو الإسبانية أو "
            "العربية أو الصينية الماندرين أو الروسية مقابل فهرس مشترك "
            "بالإنجليزية والفرنسية، مع استشهادات وعتبة مسافة."
        ),
        "sidebar_ready": "تمت فهرسة {n} مقطعاً",
        "index_preparing": "جارٍ تحضير فهرس البحث…",
        "sidebar_empty": (
            "الفهرس فارغ. من جذر المشروع، نفّذ الأمر:\n"
            "`python -m scripts.build_index`"
        ),
        "distance_label": "الصلة",
        "lang_label": "لغة المقطع",
        "open_source": "فتح الصفحة الأصلية",
        "passage_id": "معرّف المقطع",
        "examples": [
            "ما هي الصحة النفسية وفقاً لمنظمة الصحة العالمية؟",
            "كيف ينبغي للبلدان تعزيز الرعاية الصحية الأولية؟",
            "ما هي التغطية الصحية الشاملة؟",
        ],
        "msg_empty_index": (
            "لا يزال فهرس البحث قيد التحضير. انتظر لحظة ثم أعد المحاولة."
        ),
        "msg_refusal": (
            "لم يتطابق أي مقطع مع هذا السؤال بدرجة كافية للإجابة بأمان. "
            "اطرح سؤالاً عن الصحة النفسية، أو التغطية الصحية الشاملة، أو "
            "الرعاية الصحية الأولية، أو ابحث في الوثائق الإنجليزية "
            "والفرنسية معاً."
        ),
        "msg_extractive_header": (
            "لم يتم تكوين مفتاح واجهة برمجة تطبيقات للنموذج اللغوي. أفضل المقاطع المطابقة:"
        ),
        "msg_extractive_same_lang": (
            "تُعرض المقاطع بلغة الإجابة عند توفرها."
        ),
        "msg_extractive_other_lang": (
            "لم يتطابق أي مقطع مفهرس بلغة الإجابة بدرجة كافية. فيما يلي "
            "أفضل المقاطع المصدرية بالإنجليزية والفرنسية (بصياغتها "
            "الأصلية). عيّن OPENAI_API_KEY للحصول على إجابة مصاغة بلغتك."
        ),
        "msg_passages_translated": (
            "تُرجمت المقاطع المصدرية إلى لغة الإجابة. افتح «إظهار النص "
            "الأصلي» أسفل كل مصدر للتحقق من الصياغة المفهرسة."
        ),
        "translated_from": "مُترجم من {source}",
        "show_original": "إظهار النص الأصلي",

    },
    "zh": {
        "page_title": "世卫组织指南问答",
        "title": "世卫组织指南问答",
        "subtitle": (
            "可用您的语言就公开的世卫组织主题指南提问。"
            "索引收录英文与法文段落；回答附带出处引用，, "
            "若检索匹配过弱，则会明确拒绝作答。"
        ),
        "portfolio_note": "作品集演示 · 非世卫组织官方工具",
        "question": "您的问题",
        "question_placeholder": "例如：什么是全民健康覆盖？",
        "ask": "检索指南",
        "clear_question": "清空问题",
        "try_these": "从示例开始",
        "answer_lang": "回答语言",
        "search_both": "同时检索英文与法文文档",
        "search_both_help": (
            "语料为英文与法文。多语言向量仍可匹配其他提问语言。"
            "关闭后可限制为单一文档语言。"
        ),
        "search_lang": "仅从以下语言的文档检索",
        "advanced": "检索选项",
        "answer": "回答",
        "sources": "支持段落",
        "sources_hint": "打开段落以对照原文措辞。",
        "no_sources": "未检索到与此问题相关的段落。",
        "empty_question": "请先输入问题再检索。",
        "question_too_short": "请补充更多细节以提高检索效果。",
        "loading": "正在检索已索引的世卫组织指南…",
        "first_visit": (
            "在上方输入问题，或选择一个示例。"
            "检索足够强时会给出带引用的回答；否则会明确拒绝。"
        ),
        "retry": "重新检索",
        "status_grounded": "有依据, 由索引段落支持",
        "status_refused": "已拒绝, 匹配过弱，无法安全作答",
        "status_empty": "索引为空, 请先构建索引",
        "mode_llm": "根据检索段落起草（大模型）",
        "mode_extractive": "显示最相关段落（未配置 API 密钥）",
        "mode_refused": "已跳过生成, 见下方说明",
        "mode_empty_index": "尚未索引任何文档",
        "mode_llm_error": "模型不可用, 改为显示段落",
        "sidebar_lang": "界面语言",
        "sidebar_about": "关于",
        "sidebar_body": (
            "面向公开世卫组织主题指南的多语言检索增强问答。"
            "可用英语、法语、德语、意大利语、葡萄牙语、西班牙语、阿拉伯语、"
            "普通话或俄语提问，检索共享的英/法索引，并带有引用与距离门控。"
        ),
        "sidebar_ready": "已索引 {n} 个段落",
        "index_preparing": "正在准备检索索引…",
        "sidebar_empty": (
            "索引为空。请在项目根目录运行：\n"
            "`python -m scripts.build_index`"
        ),
        "distance_label": "相关度",
        "lang_label": "段落语言",
        "open_source": "打开原始页面",
        "passage_id": "段落 ID",
        "examples": [
            "根据世卫组织，什么是心理健康？",
            "各国应如何加强初级卫生保健？",
            "什么是全民健康覆盖？",
        ],
        "msg_empty_index": (
            "检索索引仍在准备中，请稍后再试。"
        ),
        "msg_refusal": (
            "没有足够接近的段落可安全作答。"
            "请围绕心理健康、全民健康覆盖或初级卫生保健提问。"
        ),
        "msg_extractive_header": "未配置大模型 API 密钥。最相关段落：",
        "msg_extractive_same_lang": "在可用时优先显示与回答语言相同的段落。",
        "msg_extractive_other_lang": (
            "索引中没有足够接近的回答语言段落。"
            "以下为最相关的英/法原文段落。"
            "设置 OPENAI_API_KEY 可获得用您的语言起草的回答。"
        ),
        "msg_passages_translated": (
            "源段落已翻译为您的回答语言。"
            "可在各来源下打开「显示原文」以核对索引中的措辞。"
        ),
        "translated_from": "译自{source}",
        "show_original": "显示原文",

    },
    "ru": {
        "page_title": "QA по руководствам ВОЗ",
        "title": "QA по руководствам ВОЗ",
        "subtitle": (
            "Задавайте вопросы по открытым тематическим руководствам ВОЗ "
            "на своём языке. В индексе, английские и французские фрагменты; "
            "ответы с цитатами, или явный отказ при слабом поиске."
        ),
        "portfolio_note": "Портфолио-демо · не официальный инструмент ВОЗ",
        "question": "Ваш вопрос",
        "question_placeholder": "Пример: Что такое всеобщий охват услугами здравоохранения?",
        "ask": "Искать в руководствах",
        "clear_question": "Очистить вопрос",
        "try_these": "Начать с примера",
        "answer_lang": "Язык ответа",
        "search_both": "Искать в английских и французских документах вместе",
        "search_both_help": (
            "Корпус, на английском и французском. Многоязычные эмбеддинги "
            "могут сопоставлять и другие языки вопросов. Отключите, чтобы "
            "ограничить язык документов."
        ),
        "search_lang": "Извлекать из документов на",
        "advanced": "Параметры поиска",
        "answer": "Ответ",
        "sources": "Подтверждающие фрагменты",
        "sources_hint": "Откройте фрагмент, чтобы сверить формулировку с источником.",
        "no_sources": "По этому вопросу фрагменты не найдены.",
        "empty_question": "Введите вопрос перед поиском.",
        "question_too_short": "Добавьте чуть больше деталей для лучшего поиска.",
        "loading": "Идёт поиск по индексированным руководствам ВОЗ…",
        "first_visit": (
            "Введите вопрос выше или выберите пример. "
            "При сильном поиске вы увидите ответ с цитатами, "
            "иначе, явный отказ."
        ),
        "retry": "Искать снова",
        "status_grounded": "Обосновано, опирается на индексированные фрагменты",
        "status_refused": "Отказ, совпадение слишком слабое",
        "status_empty": "Индекс пуст, сначала постройте индекс",
        "mode_llm": "Составлено по найденным фрагментам (LLM)",
        "mode_extractive": "Лучшие фрагменты (нет API-ключа)",
        "mode_refused": "Генерация пропущена, см. пояснение ниже",
        "mode_empty_index": "Документы ещё не проиндексированы",
        "mode_llm_error": "Модель недоступна, показаны фрагменты",
        "sidebar_lang": "Язык интерфейса",
        "sidebar_about": "О проекте",
        "sidebar_body": (
            "Многоязычный retrieval-augmented QA по открытым тематическим руководствам ВОЗ. "
            "Вопросы на английском, французском, немецком, итальянском, португальском, "
            "испанском, арабском, китайском (путунхуа) или русском к общему индексу EN/FR, "
            "с цитатами и порогом по расстоянию."
        ),
        "sidebar_ready": "Проиндексировано фрагментов: {n}",
        "index_preparing": "Подготовка поискового индекса…",
        "sidebar_empty": (
            "Индекс пуст. В корне проекта выполните:\n"
            "`python -m scripts.build_index`"
        ),
        "distance_label": "релевантность",
        "lang_label": "Язык фрагмента",
        "open_source": "Открыть исходную страницу",
        "passage_id": "ID фрагмента",
        "examples": [
            "Что ВОЗ понимает под психическим здоровьем?",
            "Как странам укреплять первичную медико-санитарную помощь?",
            "Что такое всеобщий охват услугами здравоохранения?",
        ],
        "msg_empty_index": (
            "Поисковый индекс ещё готовится. Подождите немного и попробуйте снова."
        ),
        "msg_refusal": (
            "Нет достаточно близкого фрагмента для безопасного ответа. "
            "Спросите о психическом здоровье, всеобщем охвате услугами "
            "здравоохранения или первичной помощи."
        ),
        "msg_extractive_header": (
            "API-ключ LLM не настроен. Наиболее близкие фрагменты:"
        ),
        "msg_extractive_same_lang": (
            "По возможности показаны фрагменты на языке ответа."
        ),
        "msg_extractive_other_lang": (
            "В индексе нет достаточно близкого фрагмента на языке ответа. "
            "Ниже лучшие английские/французские исходные фрагменты (оригинальный текст). "
            "Задайте OPENAI_API_KEY для ответа, составленного на вашем языке."
        ),
        "msg_passages_translated": (
            "Исходные фрагменты переведены на язык ответа. "
            "Откройте « Показать оригинал », чтобы сверить индексированный текст."
        ),
        "translated_from": "Переведено с {source}",
        "show_original": "Показать оригинал",

    },
}


def language_label(code: str) -> str:
    """Return the native display label for a language code."""
    return LANGUAGE_LABELS.get(code, code)


def llm_language_name(code: str) -> str:
    """Return the English language name used in LLM system prompts."""
    return LLM_LANGUAGE_NAMES.get(code, "English")


def example_questions(lang: str) -> list[str]:
    """Return example questions for the active interface language."""
    examples = t(lang, "examples")
    if isinstance(examples, list):
        return [str(item) for item in examples]
    return example_questions("en")


def t(lang: str, key: str, **kwargs: Any) -> Any:
    """Return a localized string or list for `key`, with optional format kwargs."""
    bundle = UI.get(lang, UI["en"])
    value = bundle.get(key, UI["en"].get(key, key))
    if isinstance(value, str) and kwargs:
        return value.format(**kwargs)
    return value


def mode_label(lang: str, mode: str) -> str:
    """Return a localized label for a generation mode code."""
    key = f"mode_{mode}"
    bundle = UI.get(lang, UI["en"])
    if key in bundle:
        return str(bundle[key])
    return mode.replace("_", " ")


def status_label(lang: str, grounded: bool, mode: str) -> str:
    """Return a localized status line for the answer panel."""
    if mode == "empty_index":
        return str(t(lang, "status_empty"))
    if grounded:
        return str(t(lang, "status_grounded"))
    return str(t(lang, "status_refused"))
