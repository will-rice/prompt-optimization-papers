import pytest

from papers_pipeline.config import TopicConfig
from papers_pipeline.models import Paper
from papers_pipeline.topics import TopicDecision, build_topic_gate
from topic_plugin import accept_topic


@pytest.mark.parametrize(
    ("title", "abstract", "decision"),
    [
        (
            'Automatic Prompt Optimization with "Gradient Descent" and Beam Search',
            "Natural language gradients edit the prompt. Tasks include jailbreak"
            " detection.",
            TopicDecision(True, "accepted by title"),
        ),
        (
            "RLPrompt: Optimizing Discrete Text Prompts with Reinforcement Learning",
            "Unlike soft prompt tuning, the optimized prompts are discrete tokens.",
            TopicDecision(True, "accepted by title"),
        ),
        (
            "GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning",
            "A reflective optimizer evolves the prompts of compound AI systems.",
            TopicDecision(True, "accepted by title"),
        ),
        (
            "Large Language Models Are Human-Level Prompt Engineers",
            "We propose Automatic Prompt Engineer (APE) for instruction generation.",
            TopicDecision(True, "accepted by abstract"),
        ),
        (
            "Large Language Models as Optimizers",
            "We propose OPRO, which describes the optimization task in natural"
            " language.",
            TopicDecision(True, "accepted by abstract"),
        ),
        (
            "Query-Dependent Prompt Evaluation and Optimization with Offline Inverse RL",
            "Prompt optimization is costly online; offline prompt optimization"
            " learns a reward model from existing data.",
            TopicDecision(True, "accepted by repeated abstract mentions"),
        ),
        (
            "In-context Examples Selection for Machine Translation",
            "Unlike prompt optimization, we select demonstrations by similarity.",
            TopicDecision(False, "missing prompt optimization signal"),
        ),
        (
            "Learning to Prompt for Continual Learning",
            "Learnable prompt vectors are optimized; we optimize the prompts to"
            " instruct the model.",
            TopicDecision(False, "matched excluded term: learnable prompt"),
        ),
        (
            "Be a Multitude to Itself: A Prompt Evolution Framework for Red Teaming",
            "Prompt evolution finds prompts that elicit unsafe outputs.",
            TopicDecision(False, "title matched excluded term: red team"),
        ),
        (
            "Self-Prompt SAM: Medical Image Segmentation via Automatic Prompt SAM"
            " Adaptation",
            "Point and box prompts are generated automatically.",
            TopicDecision(False, "title matched excluded term: sam"),
        ),
        (
            "GePA*SE: Generalized Edge-Based Parallel A* for Slow Evaluations",
            "A parallel search algorithm for planning.",
            TopicDecision(False, "missing prompt optimization signal"),
        ),
        (
            "Constraining new physics with SModelS version 2",
            "Prompt search strategies for long-lived particles.",
            TopicDecision(False, "missing prompt optimization signal"),
        ),
    ],
)
def test_accept_topic_applies_prompt_optimization_rule(
    paper: Paper, title: str, abstract: str, decision: TopicDecision
) -> None:
    candidate = paper.model_copy(update={"title": title, "abstract": abstract})

    assert accept_topic(candidate) == decision


def test_papers_yml_plugin_reference_builds_repository_gate(paper: Paper) -> None:
    gate = build_topic_gate(TopicConfig(plugin="topic_plugin:accept_topic"))
    candidate = paper.model_copy(
        update={"title": "Self-Supervised Prompt Optimization", "abstract": ""}
    )

    assert gate(candidate) == TopicDecision(True, "accepted by title")
