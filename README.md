# SRL4E – Semantic Role Labeling for Emotions
This is the official repository for the paper [*SRL4E – Semantic Role Labeling for Emotions: A Unified Evaluation Framework*](), that will be presented at ACL 2022 by [Cesare Campagnano](https://caesar.one), [Simone Conia](https://c-simone.github.io/) and [Roberto Navigli](https://www.diag.uniroma1.it/navigli/). Here you will find the scripts to build the SRL4E dataset and the codebase for our experiments.

## Description
SRL4E (Semantic Role Labeling for Emotions) is an evaluation framework that aggregates and unifies several datasets tagged with emotions and their semantic constituents (namely Cue, Experiencer, Target and Stimulus) using a common labeling scheme. It includes resources that are different in domain, language, style, and annotation scheme.

SRL4E has two main goals:
- to allow researchers to focus on their approaches, without the need to adapt the architectures to multiple resources, each one with its own needs;
- to facilitate model comparisons under a fair setup.

To do this, we leverage [Plutchik](https://en.wikipedia.org/wiki/Robert_Plutchik)'s [wheel of emotions](https://en.wikipedia.org/wiki/Robert_Plutchik#Plutchik's_wheel_of_emotions), and map all the existing resources to 8 basic emotions – anger, anticipation, disgust, fear, joy, sadness, surprise, trust, and other.

## Code and data
Coming soon!

## Abstract
> In the field of sentiment analysis, several studies have highlighted that a single sentence may express multiple, sometimes contrasting, sentiments and emotions, each with its own experiencer, target and/or cause.  
  To this end, over the past few years researchers have started to collect and annotate data manually, in order to investigate the capabilities of automatic systems not only to distinguish between emotions, but also to capture their semantic constituents.  
  However, currently available gold datasets are heterogeneous in size, domain, format, splits, emotion categories and role labels, making comparisons across different works difficult and hampering progress in the area.  
  In this paper, we tackle this issue and present a unified evaluation framework focused on Semantic Role Labeling for Emotions (SRL4E), in which we unify several datasets tagged with emotions and semantic roles by using a common labeling scheme.  
  We use SRL4E as a benchmark to evaluate how modern pretrained language models perform and analyze where we currently stand in this task, hoping to provide the tools to facilitate studies in this complex area.
  
## Cite this work
If you use any part of this work, please consider citing the paper as follows:

```
@inproceedings{campagnano-etal-2022-srl4e,
    title      = "{SRL4E} – {S}emantic {R}ole {L}abeling for {E}motions: {A} Unified Evaluation Framework",
    author     = "Campagnano, Cesare and Conia, Simone and Navigli, Roberto",
    booktitle  = "Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (ACL 2022)",
    month      = may,
    year       = "2022",
    address    = "Dublin, Ireland",
    publisher  = "Association for Computational Linguistics"
}
```

<!-- Todo: add acknowledgements, license, code and data -->
