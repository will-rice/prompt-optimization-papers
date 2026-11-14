"""Automatic prompt optimization relevance rule.

Automatic prompt optimization searches for or rewrites the natural-language
prompts of language models with an optimizer, usually an LLM: AutoPrompt, APE,
ProTeGi, OPRO, PromptBreeder, DSPy, TextGrad, GEPA and their successors.
Learned continuous prompts (soft prompts, prefix tuning), prompts for image,
video, audio and vision models, and adversarial prompt search (jailbreaks,
attacks) are out of scope.

A paper must pass two checks. The keyword rule: a title that names the task or
a known method is enough; otherwise the abstract must avoid attack and
continuous-prompt terms and name the task or a method at least twice, and the
title must still be about prompts or optimization. The similarity gate: the
paper's title and abstract must be close to at least one paper in
core_papers.json, the core methods listed in docs/research/core-papers.md. The
gate removes papers that only use prompt optimization as a tool in an
unrelated field.
"""

import functools
import json
import re
from pathlib import Path

import numpy as np
from fastembed import TextEmbedding

from papers_pipeline.models import Paper
from papers_pipeline.topics import TopicDecision

ATTACK_PHRASES = (
    "jailbreak",
    "red team",
    "red-team",
    "adversarial suffix",
    "prompt injection",
)

CONTINUOUS_PHRASES = (
    "soft prompt",
    "continuous prompt",
    "prefix tuning",
    "prefix-tuning",
    "learnable prompt",
    "visual prompt",
)

# Titles naming these are out of scope whatever else they say: attacks,
# continuous prompts, and prompts for models other than language models.
TITLE_EXCLUSION = re.compile(
    "|".join(ATTACK_PHRASES)
    + r"|attack|soft prompt|soft and hard prompt|continuous prompt|prefix[ -]tuning"
    r"|segment anything|\bsam\b|text-to-(image|video|3d|music|speech)|\bt2[iv]\b"
    r"|\b(image|video|audio|diffusion|vision|visual)\b|(?<!prompt )segmentation"
    r"|anomaly detection|\bclip\b"
)

# Method names, as whole words. GEPA is left out: the name collides with a
# search algorithm, and its paper's title says "prompt evolution".
METHODS = (
    r"\b(dspy|textgrad|opro|promptbreeder|evoprompt|protegi|autoprompt(ing)?"
    r"|rlprompt|promptagent|mipro(v2)?|promptboosting)\b"
)

# Phrases that name the task, counted in an abstract.
TASK_PATTERN = re.compile(
    r"(automatic|automated) prompt (optimi[sz]|engineer)|textual gradients?"
    r"|prompt evolution|evolutionary prompt|prompt optimi[sz]"
    r"|instruction optimi[sz]|instruction induction|" + METHODS
)
ABSTRACT_MENTIONS = 2

# A title names the task with these, or with a verb applied to prompts or
# instructions ("Optimizing Instructions and Demonstrations", "Automated
# Construction of a Mixture-of-Expert Prompts"), or calls a system a prompt
# engineer (APE).
TITLE_PATTERN = re.compile(
    TASK_PATTERN.pattern
    + r"|automatic(ally)? prompt|automated prompt|prompt engineers?\b"
    r"|(prompt|instruction) search|discrete prompt|hard prompts?"
    r"|black-box (discrete )?prompt (learning|optimi[sz]|search)"
    r"|prompt (refinement|rewriting|ensembles?)|boosted prompt"
    r"|\b(optimi[sz]\w*|evolv\w*|search\w*|refin\w*|rewrit\w*|train\w*|improv\w*"
    r"|engineer\w*|construct\w*|tun(e|es|ing)) ([\w-]+ ){0,3}(prompts?|instructions)\b"
)

# Without a task phrase in its title, a paper must at least be about prompts
# or optimization.
TOPICAL_TITLE = re.compile(r"prompt|instruction|optimi[sz]|evolv|textual|self-improv")

CORE_PAPERS = Path(__file__).with_name("core_papers.json")
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
# Every core paper scores at least 0.63 against the other core papers; papers
# below 0.55 apply prompt optimization to unrelated fields (privacy, trading,
# exploit generation) or only mention it.
SIMILARITY_THRESHOLD = 0.55


def accept_topic(paper: Paper) -> TopicDecision:
    """Apply the prompt optimization relevance rule to a paper's title and abstract.

    Args:
        paper: Normalized paper to classify.

    Returns:
        Acceptance decision with the rule that decided it.
    """
    decision = keyword_decision(paper)
    if not decision.accepted:
        return decision
    similarity = float(
        (embed([f"{paper.title}. {paper.abstract}"]) @ core_embeddings().T).max()
    )
    if similarity < SIMILARITY_THRESHOLD:
        return TopicDecision(
            False, f"similarity to core papers {similarity:.2f} below threshold"
        )
    return decision


def keyword_decision(paper: Paper) -> TopicDecision:
    """Apply the keyword part of the rule.

    Args:
        paper: Normalized paper to classify.

    Returns:
        Acceptance decision with the rule that decided it.
    """
    title = paper.title.lower()
    text = f"{title} {paper.abstract.lower()}"
    excluded_title = TITLE_EXCLUSION.search(title)
    if excluded_title is not None:
        return TopicDecision(False, f"title matched excluded term: {excluded_title[0]}")
    if TITLE_PATTERN.search(title):
        return TopicDecision(True, "accepted by title")
    excluded = next(
        (phrase for phrase in ATTACK_PHRASES + CONTINUOUS_PHRASES if phrase in text),
        None,
    )
    if excluded is not None:
        return TopicDecision(False, f"matched excluded term: {excluded}")
    if len(TASK_PATTERN.findall(text)) < ABSTRACT_MENTIONS:
        return TopicDecision(False, "missing prompt optimization signal")
    if not TOPICAL_TITLE.search(title):
        return TopicDecision(False, "title not about prompts or optimization")
    return TopicDecision(True, "accepted by abstract")


@functools.cache
def core_embeddings() -> np.ndarray:
    """Embed the core papers once per process.

    Returns:
        Unit-normalized embeddings, one row per core paper.
    """
    core = json.loads(CORE_PAPERS.read_text(encoding="utf-8"))
    return embed([f"{entry['title']}. {entry['abstract']}" for entry in core])


def embed(texts: list[str]) -> np.ndarray:
    """Embed texts with the shared model.

    fastembed runs the model with ONNX Runtime and returns NumPy arrays; torch
    is only installed with the conversion extra, so the gate stays in NumPy.

    Args:
        texts: Texts to embed.

    Returns:
        Unit-normalized embeddings, one row per text.
    """
    vectors = np.stack(list(embedding_model().embed(texts)))
    return vectors / np.linalg.norm(vectors, axis=1, keepdims=True)


@functools.cache
def embedding_model() -> TextEmbedding:
    """Load the embedding model once per process.

    Returns:
        The sentence embedding model.
    """
    return TextEmbedding(EMBEDDING_MODEL)
