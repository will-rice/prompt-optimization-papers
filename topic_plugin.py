"""Automatic prompt optimization relevance rule.

Automatic prompt optimization searches for or rewrites natural-language
prompts with an optimizer, usually an LLM: AutoPrompt, APE, ProTeGi, OPRO,
PromptBreeder, DSPy, TextGrad, GEPA and their successors. Learned continuous
prompts (soft prompts, prompt tuning, prefix tuning), point and box prompts
for Segment Anything, and adversarial prompt search (jailbreaks, attacks) are
out of scope.

A title that names the task or a known method decides on its own, unless it
names an excluded topic: discrete methods often contrast themselves with soft
prompts, or evaluate on jailbreak detection, in their abstracts. Otherwise the
abstract must avoid attack and continuous-prompt terms and either use a phrase
specific to the task or a method name, or name the task with a generic phrase
at least twice.
"""

import re

from papers_pipeline.models import Paper
from papers_pipeline.topics import TopicDecision

# Adversarial prompt search.
ATTACK_PHRASES = (
    "jailbreak",
    "red team",
    "red-team",
    "adversarial suffix",
    "prompt injection",
    "attack",
)

# Learned continuous prompts.
CONTINUOUS_PHRASES = (
    "soft prompt",
    "continuous prompt",
    "prefix tuning",
    "prefix-tuning",
    "prompt tuning",
    "prompt learning",
    "learnable prompt",
    "visual prompt",
)

# Titles naming these are out of scope whatever else they say. Discrete
# methods' titles may say "prompt tuning", so only unambiguous continuous
# terms are listed. Segment Anything takes point and box prompts.
TITLE_EXCLUSION = re.compile(
    "|".join(ATTACK_PHRASES)
    + r"|soft prompt|continuous prompt|prefix[ -]tuning|segment anything|\bsam\b"
)

# Method names, as whole words. GEPA is left out: the name collides with a
# search algorithm, and its paper's title says "prompt evolution".
METHODS = (
    r"\b(dspy|textgrad|opro|promptbreeder|evoprompt|protegi|autoprompt(ing)?"
    r"|rlprompt|promptagent|mipro(v2)?)\b"
)

# Phrases specific enough that one mention in an abstract makes the paper
# about prompt optimization.
SPECIFIC_PATTERN = re.compile(
    r"(automatic|automated) prompt (optimi[sz]|engineer)|textual gradients?"
    r"|prompt evolution|evolutionary prompt|" + METHODS
)

# Generic phrases that abstracts also use in passing (and "instruction
# induction" is a benchmark other papers evaluate on); they count only when
# the abstract names the task at least twice.
GENERIC_PATTERN = re.compile(
    r"prompt optimi[sz]|instruction optimi[sz]|instruction induction"
)
GENERIC_MENTIONS = 2

# A title is a stronger signal, so it may also use these broader phrases.
TITLE_PATTERN = re.compile(
    SPECIFIC_PATTERN.pattern
    + "|"
    + GENERIC_PATTERN.pattern
    + r"|automatic(ally)? prompt|automated prompt"
    r"|optimi[sz](e|es|ing) (the )?prompts?\b|(prompt|instruction) search"
    r"|discrete prompt|hard prompt|prompt (refinement|rewriting)"
)


def accept_topic(paper: Paper) -> TopicDecision:
    """Apply the prompt optimization relevance rule to a paper's title and abstract.

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
    if SPECIFIC_PATTERN.search(text):
        return TopicDecision(True, "accepted by abstract")
    if len(GENERIC_PATTERN.findall(text)) >= GENERIC_MENTIONS:
        return TopicDecision(True, "accepted by repeated abstract mentions")
    return TopicDecision(False, "missing prompt optimization signal")
