# Core automatic prompt optimization papers

The reference set that defines this repository's scope. Each paper is a method
for automatically searching for or rewriting natural-language prompts.

## Sources

- Ramnath et al., *A Systematic Survey of Automatic Prompt Optimization
  Techniques* (arXiv:2502.16923v2). Section 2 defines the scope: black-box APO
  techniques that "systematically search through the prompt solution space" and
  "retain human interpretability of prompt improvements". Its Figure 1 taxonomy
  (seed prompts, inference evaluation and feedback, candidate generation,
  filtering, iteration depth) and Tables 2-4 list the methods below.
- Added beyond the survey: AutoPrompt and RLPrompt (earlier discrete prompt
  search the survey builds on) and GEPA, SPO, CAPO, AutoPDL and MASS (2025
  methods published after it).
- Not included: GATE (Joko et al., 2024), cited by the survey, which could not
  be matched to an arXiv paper.

## Use in the topic rule

`core_papers.json` holds the title and abstract of 52 of these papers. The
topic rule's similarity gate accepts a paper only if it is close to at least
one of them, and the tests require every one to pass the keyword rule and to
clear the similarity threshold against the others. Two listed papers are not
used: LMEA treats the LLM as an optimizer for combinatorial problems and never
mentions prompts, and DSP is a retrieval pipeline framework (DSPy's
predecessor) rather than a prompt optimizer.

| Method | arXiv | Year | First discussed in survey | Title |
|---|---|---|---|---|
| AutoPrompt | [2010.15980](https://arxiv.org/abs/2010.15980) | 2020 | added (not in survey) | AutoPrompt: Eliciting Knowledge from Language Models with Automatically Generated Prompts |
| BDPL | [2201.08531](https://arxiv.org/abs/2201.08531) | 2022 | §5.1.4 Vocabulary Pruning | Black-box Prompt Learning for Pre-trained Language Models |
| GrIPS | [2203.07281](https://arxiv.org/abs/2203.07281) | 2022 | §4.1.3 Entropy-based Scores | GrIPS: Gradient-free, Edit-based Instruction Search for Prompting Large Language Models |
| Instruction Induction | [2205.10782](https://arxiv.org/abs/2205.10782) | 2022 | §3.2 Instruction Induction via LLMs | Instruction Induction: From Few Examples to Natural Language Task Descriptions |
| RLPrompt | [2205.12548](https://arxiv.org/abs/2205.12548) | 2022 | added (not in survey) | RLPrompt: Optimizing Discrete Text Prompts with Reinforcement Learning |
| GPS | [2210.17041](https://arxiv.org/abs/2210.17041) | 2022 | §3.1 Manual Instructions | GPS: Genetic Prompt Search for Efficient Few-shot Learning |
| APE | [2211.01910](https://arxiv.org/abs/2211.01910) | 2022 | §3.1 Manual Instructions | Large Language Models Are Human-Level Prompt Engineers |
| TEMPERA | [2211.11890](https://arxiv.org/abs/2211.11890) | 2022 | §11 Limitations | TEMPERA: Test-Time Prompting via Reinforcement Learning |
| PromptBoosting | [2212.09257](https://arxiv.org/abs/2212.09257) | 2022 | §5.4.3 Ensemble Methods | PromptBoosting: Black-Box Text Classification with Ten Forward Passes |
| DSP | [2212.14024](https://arxiv.org/abs/2212.14024) | 2022 | §5.5 Program Synthesis | Demonstrate-Search-Predict: Composing retrieval and language models for knowledge-intensive NLP |
| Boosted Prompting | [2304.05970](https://arxiv.org/abs/2304.05970) | 2023 | §5.4.3 Ensemble Methods | Boosted Prompt Ensembles for Large Language Models |
| ProTeGi | [2305.03495](https://arxiv.org/abs/2305.03495) | 2023 | §3.1 Manual Instructions | Automatic Prompt Optimization with "Gradient Descent" and Beam Search |
| GPO | [2305.13954](https://arxiv.org/abs/2305.13954) | 2023 | §3.2 Instruction Induction via LLMs | Robust Prompt Optimization for Large Language Models Against Distribution Shifts |
| DLN | [2306.12509](https://arxiv.org/abs/2306.12509) | 2023 | §5.5 Program Synthesis | Joint Prompt Optimization of Stacked LLMs using Variational Inference |
| AutoHint | [2307.07415](https://arxiv.org/abs/2307.07415) | 2023 | §4.2.1 Improving Single Candidate | AutoHint: Automatic Prompt Optimization with Hint Generation |
| PACE | [2308.10088](https://arxiv.org/abs/2308.10088) | 2023 | §4.1.4 Negative Log-likelihood of Output | PACE: Improving Prompt with Actor-Critic Editing for Large Language Model |
| PREFER | [2308.12033](https://arxiv.org/abs/2308.12033) | 2023 | §4.2.2 Improving Multiple Candidates | PREFER: Prompt Ensemble Learning via Feedback-Reflect-Refine |
| OPRO | [2309.03409](https://arxiv.org/abs/2309.03409) | 2023 | §4.2 LLM Feedback | Large Language Models as Optimizers |
| Prompt-OIRL | [2309.06553](https://arxiv.org/abs/2309.06553) | 2023 | §5.2.1 Reinforcement-learning | Query-Dependent Prompt Evaluation and Optimization with Offline Inverse RL |
| EvoPrompt | [2309.08532](https://arxiv.org/abs/2309.08532) | 2023 | §5.1.2 Genetic Algorithm | EvoPrompt: Connecting LLMs with Evolutionary Algorithms Yields Powerful Prompt Optimizers |
| Promptbreeder | [2309.16797](https://arxiv.org/abs/2309.16797) | 2023 | Table 2 | Promptbreeder: Self-Referential Self-Improvement Via Prompt Evolution |
| DSPy | [2310.03714](https://arxiv.org/abs/2310.03714) | 2023 | §4.2 LLM Feedback | DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines |
| CLAPS | [2310.12774](https://arxiv.org/abs/2310.12774) | 2023 | §4.1.3 Entropy-based Scores | Survival of the Most Influential Prompts: Efficient Black-Box Prompt Search via Clustering and Pruning |
| PromptAgent | [2310.16427](https://arxiv.org/abs/2310.16427) | 2023 | §4.2.2 Improving Multiple Candidates | PromptAgent: Strategic Planning with Language Models Enables Expert-level Prompt Optimization |
| LMEA | [2310.19046](https://arxiv.org/abs/2310.19046) | 2023 | §5.1.2 Genetic Algorithm | Large Language Models as Evolutionary Optimizers |
| BPO | [2311.04155](https://arxiv.org/abs/2311.04155) | 2023 | §5.2.2 Finetuning LLMs | Black-Box Prompt Optimization: Aligning Large Language Models without Model Training |
| PE2 | [2311.05661](https://arxiv.org/abs/2311.05661) | 2023 | §5.3 Metaprompt Design | Prompt Engineering a Prompt Engineer |
| PLUM | [2311.08364](https://arxiv.org/abs/2311.08364) | 2023 | §6.4 Metaheuristic Ensemble | Plum: Prompt Learning using Metaheuristic |
| AELP | [2311.10117](https://arxiv.org/abs/2311.10117) | 2023 | §5.1.2 Genetic Algorithm | Automatic Engineering of Long Prompts |
| PROMST | [2402.08702](https://arxiv.org/abs/2402.08702) | 2024 | §4.3 Human-feedback | PRompt Optimization in Multi-Step Tasks (PROMST): Integrating Human Feedback and Heuristic-based Sampling |
| FIPO | [2402.11811](https://arxiv.org/abs/2402.11811) | 2024 | §5.2.2 Finetuning LLMs | FIPO: Free-form Instruction-oriented Prompt Optimization with Preference Dataset and Modular Fine-tuning Schema |
| SAMMO | [2404.02319](https://arxiv.org/abs/2404.02319) | 2024 | §5.5 Program Synthesis | Symbolic Prompt Program Search: A Structure-Aware Approach to Efficient Compile-Time Prompt Optimization |
| APOHF | [2405.17346](https://arxiv.org/abs/2405.17346) | 2024 | §4.3 Human-feedback | Prompt Optimization with Human Feedback |
| PromptWizard | [2405.18369](https://arxiv.org/abs/2405.18369) | 2024 | §5.1.2 Genetic Algorithm | PromptWizard: Task-Aware Prompt Optimization Framework |
| COPLE | [2405.20701](https://arxiv.org/abs/2405.20701) | 2024 | §5.1.3 Word / Phrase Level Edits | Unveiling the Lexical Sensitivity of LLMs: Combinatorial Optimization for Prompt Enhancement |
| TextGrad | [2406.07496](https://arxiv.org/abs/2406.07496) | 2024 | §4.2.2 Improving Multiple Candidates | TextGrad: Automatic "Differentiation" via Text |
| UniPrompt | [2406.10504](https://arxiv.org/abs/2406.10504) | 2024 | §3.2 Instruction Induction via LLMs | Task Facet Learning: A Structured Approach to Prompt Optimization |
| MIPRO | [2406.11695](https://arxiv.org/abs/2406.11695) | 2024 | §5.5 Program Synthesis | Optimizing Instructions and Demonstrations for Multi-Stage Language Model Programs |
| DAPO | [2406.13443](https://arxiv.org/abs/2406.13443) | 2024 | §3.2 Instruction Induction via LLMs | Dual-Phase Accelerated Prompt Optimization |
| MOP | [2407.00256](https://arxiv.org/abs/2407.00256) | 2024 | §3.2 Instruction Induction via LLMs | One Prompt is not Enough: Automated Construction of a Mixture-of-Expert Prompts |
| PIN | [2407.14733](https://arxiv.org/abs/2407.14733) | 2024 | §5.1.4 Vocabulary Pruning | Hard Prompts Made Interpretable: Sparse Entropy Regularization for Prompt Tuning with RL |
| CriSPO | [2410.02748](https://arxiv.org/abs/2410.02748) | 2024 | §4.2 LLM Feedback | CriSPO: Multi-Aspect Critique-Suggestion-guided Automatic Prompt Optimization for Text Generation |
| StraGo | [2410.08601](https://arxiv.org/abs/2410.08601) | 2024 | §4.2.2 Improving Multiple Candidates | StraGo: Harnessing Strategic Guidance for Prompt Optimization |
| AMPO | [2410.08696](https://arxiv.org/abs/2410.08696) | 2024 | §5.4.1 Single Prompt-expansion | AMPO: Automatic Multi-Branched Prompt Optimization |
| SOS | [2410.09652](https://arxiv.org/abs/2410.09652) | 2024 | §4.2.2 Improving Multiple Candidates | Survival of the Safest: Towards Secure Prompt Optimization through Interleaved Multi-Objective Evolution |
| SPRIG | [2410.14826](https://arxiv.org/abs/2410.14826) | 2024 | §3.1 Manual Instructions | SPRIG: Improving Large Language Model Performance by System Prompt Optimization |
| SCULPT | [2410.20788](https://arxiv.org/abs/2410.20788) | 2024 | §3.2 Instruction Induction via LLMs | SCULPT: Systematic Tuning of Long Prompts |
| DRPO | [2411.08733](https://arxiv.org/abs/2411.08733) | 2024 | §4.1.2 Reward-model Scores | Dynamic Rewarding with Prompt Optimization Enables Tuning-free Self-Alignment of Language Models |
| Align-Pro | [2501.03486](https://arxiv.org/abs/2501.03486) | 2025 | §8.1 Upper Bound of Improvement from APO | Align-Pro: A Principled Approach to Prompt Optimization for LLM Alignment |
| MASS | [2502.02533](https://arxiv.org/abs/2502.02533) | 2025 | added (not in survey) | Multi-Agent Design: Optimizing Agents with Better Prompts and Topologies |
| SPO | [2502.06855](https://arxiv.org/abs/2502.06855) | 2025 | added (not in survey) | Self-Supervised Prompt Optimization |
| AutoPDL | [2504.04365](https://arxiv.org/abs/2504.04365) | 2025 | added (not in survey) | AutoPDL: Automatic Prompt Optimization for LLM Agents |
| CAPO | [2504.16005](https://arxiv.org/abs/2504.16005) | 2025 | added (not in survey) | CAPO: Cost-Aware Prompt Optimization |
| GEPA | [2507.19457](https://arxiv.org/abs/2507.19457) | 2025 | added (not in survey) | GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning |
