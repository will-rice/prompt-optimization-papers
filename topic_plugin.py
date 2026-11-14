"""Automatic prompt optimization relevance rule.

Automatic prompt optimization searches for or rewrites natural-language
prompts with an optimizer, usually an LLM: AutoPrompt, APE, ProTeGi, OPRO,
PromptBreeder, DSPy, TextGrad, GEPA and their successors. Learned continuous
prompts (soft prompts, prompt tuning, prefix tuning), point and box prompts
for Segment Anything, and adversarial prompt search (jailbreaks, attacks) are
out of scope.

A title that names the task or a known method decides on its own, unless it
names an excluded topic: discrete methods often contrast themselves with soft
prompts, or evaluate on jailbreak detection, in their abstracts. A paper whose
title does not name the task needs more: its abstract must avoid attack and
continuous-prompt terms and name the task or a method at least twice, and its
title must still be about prompts or optimization. Papers that only use DSPy
or compare against OPRO mention them once, in passing.
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

# Phrases that name the task, counted in an abstract.
TASK_PATTERN = re.compile(
    r"(automatic|automated) prompt (optimi[sz]|engineer)|textual gradients?"
    r"|prompt evolution|evolutionary prompt|prompt optimi[sz]"
    r"|instruction optimi[sz]|instruction induction|" + METHODS
)
ABSTRACT_MENTIONS = 2

# A title names the task with these, or with an optimization verb applied to
# prompts or instructions ("Optimizing Instructions and Demonstrations",
# "Evolving LLM Instructions"), or calls a system a prompt engineer (APE).
TITLE_PATTERN = re.compile(
    TASK_PATTERN.pattern
    + r"|automatic(ally)? prompt|automated prompt|prompt engineers?\b"
    r"|(prompt|instruction) search|discrete prompt|prompt (refinement|rewriting)"
    r"|\b(optimi[sz]\w*|evolv\w*|search\w*|refin\w*|rewrit\w*|train\w*"
    r"|tun(e|es|ing)) ([\w-]+ ){0,3}(prompts?|instructions)\b"
)

# Without a task phrase in its title, a paper must at least be about prompts
# or optimization.
TOPICAL_TITLE = re.compile(r"prompt|instruction|optimi[sz]|evolv|textual|self-improv")


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
    if len(TASK_PATTERN.findall(text)) < ABSTRACT_MENTIONS:
        return TopicDecision(False, "missing prompt optimization signal")
    if not TOPICAL_TITLE.search(title):
        return TopicDecision(False, "title not about prompts or optimization")
    return TopicDecision(True, "accepted by abstract")
