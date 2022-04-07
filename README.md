# SRL4E – Semantic Role Labeling for Emotions
This is the official repository for the paper [*SRL4E – Semantic Role Labeling for Emotions: A Unified Evaluation Framework*](), which will be presented at ACL 2022 by [Cesare Campagnano](https://caesar.one), [Simone Conia](https://c-simone.github.io/) and [Roberto Navigli](https://www.diag.uniroma1.it/navigli/). Here you will find the scripts to build the SRL4E dataset and the codebase for our experiments.

## Paper Abstract
> In the field of sentiment analysis, several studies have highlighted that a single sentence may express multiple, sometimes contrasting, sentiments and emotions, each with its own experiencer, target and/or cause. 
To this end, over the past few years researchers have started to collect and annotate data manually, in order to investigate the capabilities of automatic systems not only to distinguish between emotions, but also to capture their semantic constituents. 
However, currently available gold datasets are heterogeneous in size, domain, format, splits, emotion categories and role labels, making comparisons across different works difficult and hampering progress in the area. 
In this paper, we tackle this issue and present a unified evaluation framework focused on Semantic Role Labeling for Emotions (SRL4E), in which we unify several datasets tagged with emotions and semantic roles by using a common labeling scheme. 
We use SRL4E as a benchmark to evaluate how modern pretrained language models perform and analyze where we currently stand in this task, hoping to provide the tools to facilitate studies in this complex area.

## Description
SRL4E (Semantic Role Labeling for Emotions) is an evaluation framework that aggregates and unifies several datasets tagged with emotions and their semantic constituents (namely Cue, Experiencer, Target and Stimulus) using a common labeling scheme. It includes resources that are different in domain, language, style, and annotation scheme.

SRL4E has two main goals:
- to allow researchers to focus on their approaches, without the need to adapt the architectures to multiple resources, each one with its own needs;
- to facilitate model comparisons under a fair setup.

To do this, we leverage [Plutchik](https://en.wikipedia.org/wiki/Robert_Plutchik)'s [wheel of emotions](https://en.wikipedia.org/wiki/Robert_Plutchik#Plutchik's_wheel_of_emotions), and map all the existing resources to 8 basic emotions – anger, anticipation, disgust, fear, joy, sadness, surprise, trust, and other.
We refer to our paper for more details.

## Data
Instructions to build up SRL4E and more detailed information about the resources are reported in the [data](DATA.md) page.

## Code
Coming soon!
  
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

### Other references
If you evaluate your work on this benchmark, please also cite the original datasets.

```
@inproceedings{aman-szpakowicz-2007-identifying,
    author = "Aman, Saima and
        Szpakowicz, Stan",
    editor = "Matou{\v{s}}ek, V{\'a}clav
    and Mautner, Pavel",
    title = "Identifying Expressions of Emotion in Text",
    booktitle = "Text, Speech and Dialogue",
    year = "2007",
    publisher = "Springer Berlin Heidelberg",
    address = "Berlin, Heidelberg",
    pages = "196--205",
}

@inproceedings{mohammad-etal-2014-semantic,
    title = "Semantic Role Labeling of Emotions in Tweets",
    author = "Mohammad, Saif  and
        Zhu, Xiaodan  and
        Martin, Joel",
    booktitle = "Proceedings of the 5th Workshop on Computational Approaches to Subjectivity, Sentiment and Social Media Analysis",
    month = jun,
    year = "2014",
    address = "Baltimore, Maryland",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/W14-2607",
    doi = "10.3115/v1/W14-2607",
    pages = "32--41",
}

@inproceedings{liew-etal-2016-emotweet,
    title = "{E}mo{T}weet-28: A Fine-Grained Emotion Corpus for Sentiment Analysis",
    author = "Liew, Jasy Suet Yan  and
        Turtle, Howard R.  and
        Liddy, Elizabeth D.",
    booktitle = "Proceedings of the Tenth International Conference on Language Resources and Evaluation ({LREC}'16)",
    month = may,
    year = "2016",
    address = "Portoro{\v{z}}, Slovenia",
    publisher = "European Language Resources Association (ELRA)",
    url = "https://aclanthology.org/L16-1183",
    pages = "1149--1156",
}

@inproceedings{bostan-etal-2020-goodnewseveryone,
    title = "{G}ood{N}ews{E}veryone: A Corpus of News Headlines Annotated with Emotions, Semantic Roles, and Reader Perception",
    author = "Bostan, Laura Ana Maria  and
        Kim, Evgeny  and
        Klinger, Roman",
    booktitle = "Proceedings of the 12th Language Resources and Evaluation Conference",
    month = may,
    year = "2020",
    address = "Marseille, France",
    publisher = "European Language Resources Association",
    url = "https://aclanthology.org/2020.lrec-1.194",
    pages = "1554--1566",
    ISBN = "979-10-95546-34-4",
}

@article{gao_overview_2017,
    title = {Overview of {NTCIR}-13 {ECA} {Task}},
    language = {en},
    author = {Gao, Qinghong 
        and Hu, Jiannan and
        Xu, Ruifeng and
        Lin, Gui and
        He, Yulan and
        Lu, Qin and
        Wong, Kam-Fai},
    year = {2017},
    pages = {6},
}

@inproceedings{kim-klinger-2018-feels,
    title = "Who Feels What and Why? Annotation of a Literature Corpus with Semantic Roles of Emotions",
    author = "Kim, Evgeny  and
        Klinger, Roman",
    booktitle = "Proceedings of the 27th International Conference on Computational Linguistics",
    month = aug,
    year = "2018",
    address = "Santa Fe, New Mexico, USA",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/C18-1114",
    pages = "1345--1359",
}
```

## Acknowledgements

The authors gratefully acknowledge the support of the [ERC Consolidator Grant MOUSSE No. 726487](http://mousse-project.org/) and the [European Language Grid
project No. 825627 (Universal Semantic Annotator, USeA)](https://live.european-language-grid.eu/catalogue/project/5334/) under the European Union’s Horizon 2020 research and innovation programme.

This work was supported in part by the MIUR under grant “Dipartimenti di eccellenza 2018-2022” of the Department of Computer Science of the Sapienza University of Rome.


## License
This work is under the Attribution-NonCommercial 4.0 International (CC BY-NC 4.0) license.
