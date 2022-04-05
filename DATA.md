# SRL4E - Data
In this page you will find important informations about the resources included in SRL4E and the instructions to reproduce the benchmark.

## Annotation
SRL4E is composed of several resources, but they share a similar argument structure. In the following table we formalize this structure, according to the scheme adopted in SRL4E:
| Role | Definition |
| :----- | :----- |
|Cue| Trigger word or expression that describes (even implicitly) an emotion. |
|Experiencer| Person or entity that feels or experiences the emotion identified by the cue. |
|Target| Person or entity towards whom/which the emotion identified by the cue is directed. | 
|Stimulus| Entity, action or event that causes the emotion identified by the cue. |

This argument structure should be interpreted as in the example below.
![Example of argumental structure](assets/images/example.png)
The Cue expression is “stand by”, and its associated emotion is Trust. 
The participants to the emotion are “I” (Experiencer of Trust), “Obama” (Target of Trust), and “he deserves another 4yrs in office” (Stimulus of Trust).

Each dataset uses different categories of emotions. In SRL4E we set up a set that is valid in most cases, and map all resources to it. 
This schema is based on [Plutchik](https://en.wikipedia.org/wiki/Robert_Plutchik)'s [wheel of emotions](https://en.wikipedia.org/wiki/Robert_Plutchik#Plutchik's_wheel_of_emotions). 
It provides clearly distinct and well-defined coarse-grained categories: anger, anticipation, disgust, fear, joy, sadness, surprise and trust. 
These categories can be compounded into dyads to virtually describe all other fine-grained sets, and to form even more complex feelings, as in the image below.
![Plutchik's wheel of emotions with dyads](assets/images/wheel_of_emotions.png)
The following table summarizes which annotations form part of the original corpora and, therefore, which ones are also part of SRL4E.
|Resource| Cue | Stimulus | Experiencer | Target|
| ------ | :------: | :------: | :------: | :------: |
|Blogs | :heavy_check_mark:  | – | – | – |
|Elections  | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
|EmoTweet   | :heavy_check_mark: | – | – | – |
|GNE        | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
|NTCIR      | :heavy_check_mark: | :heavy_check_mark: | – | – |
|REMAN      | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |

## Instructions
Coming soon!

## Resource Licenses and Links
The following table summarizes license information, availability and link for each dataset that is part of SRL4E. 

| Resource        | Source       | License     | Link |
| ----------- | ----------- | :-----------: | ------------- |
| Blogs      | [Aman and Szpakowicz (2007)](https://doi.org/10.1007/978-3-540-74628-7_27) |**R-R**| Contact authors (as described [here](http://saimacs.github.io/)) | 
| Elections   | [Mohammad et al. (2014)](https://aclanthology.org/W14-2607/) |**D-R**|[Link](http://saifmohammad.com/WebPages/SentimentEmotionLabeledData.html)|
| EmoTweet      | [Liew et al. (2016)](https://www.aclweb.org/anthology/L16-1183)       |**R-R**| Email authors | 
| GNE      |  [Bostan et al. (2020)](https://www.aclweb.org/anthology/2020.lrec-1.194)       |**D-C**| [Link](https://www.ims.uni-stuttgart.de/en/research/resources/corpora/goodnewseveryone/) | 
| NTCIR      | [Gao et al. (2017)](https://research.nii.ac.jp/ntcir/workshop/OnlineProceedings13/pdf/ntcir/01-NTCIR13-OV-ECA-GaoQ.pdf)       |**D-U**| [Original link (broken)](http://hlt.hitsz.edu.cn/ECA.html) and [Archive.org link](https://web.archive.org/web/20170913034355/http://hlt.hitsz.edu.cn/ECA.html) | 
| REMAN      | [Kim and Klinger (2018)](https://aclanthology.org/C18-1114/)       |**D-C**| [Link](https://www.ims.uni-stuttgart.de/en/research/resources/corpora/reman/) | 

Where:
- **R-R**: available upon **R**equest for **R**esearch only purposes; 
- **D-R**: available online for **D**ownload for **R**esearch only purposes; 
- **D-U**: available online for **D**ownload with **U**nknown license;
- **D-C**: available online for **D**ownload under **C**C-BY 4.0 license.

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
## Other references
If you evaluate your work on this benchmark, please also cite the original datasets.

```
@InProceedings{10.1007/978-3-540-74628-7_27,
    author="Aman, Saima
    and Szpakowicz, Stan",
    editor="Matou{\v{s}}ek, V{\'a}clav
    and Mautner, Pavel",
    title="Identifying Expressions of Emotion in Text",
    booktitle="Text, Speech and Dialogue",
    year="2007",
    publisher="Springer Berlin Heidelberg",
    address="Berlin, Heidelberg",
    pages="196--205",
    abstract="Finding emotions in text is an area of research with wide-ranging applications. We describe an emotion annotation task of identifying emotion category, emotion intensity and the words/phrases that indicate emotion in text. We introduce the annotation scheme and present results of an annotation agreement study on a corpus of blog posts. The average inter-annotator agreement on labeling a sentence as emotion or non-emotion was 0.76. The agreement on emotion categories was in the range 0.6 to 0.79; for emotion indicators, it was 0.66. Preliminary results of emotion classification experiments show the accuracy of 73.89{\%}, significantly above the baseline.",
    isbn="978-3-540-74628-7"
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
    abstract = "This paper describes EmoTweet-28, a carefully curated corpus of 15,553 tweets annotated with 28 emotion categories for the purpose of training and evaluating machine learning models for emotion classification. EmoTweet-28 is, to date, the largest tweet corpus annotated with fine-grained emotion categories. The corpus contains annotations for four facets of emotion: valence, arousal, emotion category and emotion cues. We first used small-scale content analysis to inductively identify a set of emotion categories that characterize the emotions expressed in microblog text. We then expanded the size of the corpus using crowdsourcing. The corpus encompasses a variety of examples including explicit and implicit expressions of emotions as well as tweets containing multiple emotions. EmoTweet-28 represents an important resource to advance the development and evaluation of more emotion-sensitive systems.",
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
    abstract = "Most research on emotion analysis from text focuses on the task of emotion classification or emotion intensity regression. Fewer works address emotions as a phenomenon to be tackled with structured learning, which can be explained by the lack of relevant datasets. We fill this gap by releasing a dataset of 5000 English news headlines annotated via crowdsourcing with their associated emotions, the corresponding emotion experiencers and textual cues, related emotion causes and targets, as well as the reader{'}s perception of the emotion of the headline. This annotation task is comparably challenging, given the large number of classes and roles to be identified. We therefore propose a multiphase annotation procedure in which we first find relevant instances with emotional content and then annotate the more fine-grained aspects. Finally, we develop a baseline for the task of automatic prediction of semantic role structures and discuss the results. The corpus we release enables further research on emotion classification, emotion intensity prediction, emotion cause detection, and supports further qualitative studies.",
    language = "English",
    ISBN = "979-10-95546-34-4",
}

@article{gao_overview_2017,
	title = {Overview of {NTCIR}-13 {ECA} {Task}},
	language = {en},
	author = {Gao, Qinghong and Hu, Jiannan and Xu, Ruifeng and Lin, Gui and He, Yulan and Lu, Qin and Wong, Kam-Fai},
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
    abstract = "Most approaches to emotion analysis in fictional texts focus on detecting the emotion expressed in text. We argue that this is a simplification which leads to an overgeneralized interpretation of the results, as it does not take into account who experiences an emotion and why. Emotions play a crucial role in the interaction between characters and the events they are involved in. Until today, no specific corpora that capture such an interaction were available for literature. We aim at filling this gap and present a publicly available corpus based on Project Gutenberg, REMAN (Relational EMotion ANnotation), manually annotated for spans which correspond to emotion trigger phrases and entities/events in the roles of experiencers, targets, and causes of the emotion. We provide baseline results for the automatic prediction of these relational structures and show that emotion lexicons are not able to encompass the high variability of emotion expressions and demonstrate that statistical models benefit from joint modeling of emotions with its roles in all subtasks. The corpus that we provide enables future research on the recognition of emotions and associated entities in text. It supports qualitative literary studies and digital humanities. The corpus is available at http://www.ims.uni-stuttgart.de/data/reman .",
}

```

