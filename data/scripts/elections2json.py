import json
import warnings
import pandas as pd
from itertools import groupby
from collections import Counter
from utils import find_span_annotation_intersections, split_longest_common_substrings, merge_contiguous_spans
from nltk import TweetTokenizer

Q1_PATH = "../datasets/elections/ElectoralTweetsData/Annotated-US2012-Election-Tweets/Questionnaire1/AnnotatedTweets.txt"
Q2_1_PATH = "../datasets/elections/ElectoralTweetsData/Annotated-US2012-Election-Tweets/Questionnaire2/Batch1/AnnotatedTweets.txt"
Q2_2_PATH = "../datasets/elections/ElectoralTweetsData/Annotated-US2012-Election-Tweets/Questionnaire2/Batch2/AnnotatedTweets.txt"

_emotion2plutchik = {
    'acceptance': ["trust"],
    'admiration': ["trust"],
    'amazement': ["surprise"],
    'anger or annoyance or hostility or fury': ["anger"],
    'anticipation or  expectancy or interest': ["anticipation"],
    'calmness or serenity': ["joy"],
    'disappointment': ["disgust"],
    'disgust': ["disgust"],
    'dislike': ["disgust"],
    'fear or apprehension or panic or terror': ["fear"],
    'hate': ["disgust"],
    'indifference': ["disgust"],
    'joy or happiness or elation': ["joy"],
    'like': ["trust"],
    'sadness or gloominess or grief or sorrow': ["sadness"],
    'surprise': ["surprise"],
    'trust': ["trust"],
    'uncertainty or indecision or confusion': ["surprise"],
    'vigilance': ["anticipation"]
}

_emotion2sentiment = {
    'acceptance': "positive",
    'admiration': "positive",
    'amazement': "positive",
    'anger or annoyance or hostility or fury': "negative",
    'anticipation or  expectancy or interest': "other",
    'calmness or serenity': "positive",
    'disappointment': "negative",
    'disgust': "negative",
    'dislike': "negative",
    'fear or apprehension or panic or terror': "negative",
    'hate': "negative",
    'indifference': "negative",
    'joy or happiness or elation': "positive",
    'like': "positive",
    'sadness or gloominess or grief or sorrow': "negative",
    'surprise': "other",
    'trust': "positive",
    'uncertainty or indecision or confusion': "other",
    'vigilance': "other"
}

_polaritytag2sentiment = {
    'negative emotion': 'negative',
    'neither positive nor negative': 'other',
    'positive emotion': 'positive'
}


_plutchik2sentiment = {
    'anger': 'negative',
    'disgust': 'negative',
    'fear': 'negative',
    'joy': 'positive',
    'anticipation': 'other',
    'sadness': 'negative',
    'surprise': 'other',
    'trust': 'positive'
}
_plutchik_classes = sorted(["trust", "fear", "surprise", "sadness", "disgust", "anger", "anticipation", "joy"])

blank_tags = ["blank", "not specified", "unspecified", "not specifies", "not specified well enough"]
tweeter_tags = ["tweeter", "tweter", "tweeters"]

emotional_content_tags = [
    'There is some emotion here, but the tweet does not give enough context to determine which emotion it is.',
    'This tweet has no emotional content.',
    'This tweet expresses or suggests two or more contrasting emotional attitudes or responses. (For example, the tweeter likes X but dislikes Y and Z.)',
    'It is not possible to decide which of the above options is appropriate because of reasons such as the tweet does not give enough information, one needs additional context to understand the emotion, and the tweet does not make sense because of weird spellings.',
    'This tweet expresses or suggests an emotional attitude or response to something.'
]

def _load(path, questionnaire=1):
    assert questionnaire in [1, 2], "questionnaire can be either 1 or 2"

    data = pd.read_csv(path, sep="\t", error_bad_lines=False)

    if questionnaire == 2:
        # suitable for both batch 1 and batch 2
        data_filtered = data[[
            data.columns[8],  # trust?
            # data.columns[10],  # country
            # data.columns[11],  # region
            # data.columns[12],  # city
            data.columns[13],  # tweet
            data.columns[14],  # experiencer
            data.columns[15],  # emotion
            data.columns[17],  # emotion polarity
            # data.columns[18],  # emotion intensity
            data.columns[19],  # target (towards whom or what is directed)
            data.columns[20],  # span supporting emotion
            data.columns[21],  # emotion cause or stimulus
            # data.columns[22],  # tweet issue (multiple choice)
            # data.columns[23],  # tweet issue (open)
            # data.columns[24]  # tweet purpose
        ]]

        data_filtered = data_filtered.rename(columns={
            data.columns[8]: "trust",
            # data.columns[10]: "country",
            # data.columns[11]: "region",
            # data.columns[12]: "city",
            data.columns[13]: "tweet",
            data.columns[14]: "experiencer",
            data.columns[15]: "emotion",
            data.columns[17]: "emotion_polarity",
            # data.columns[18]: "emotion_intensity",
            data.columns[19]: "target",  # towards whom is directed
            data.columns[20]: "span_supporting_emotion",  # cue
            data.columns[21]: "emotion_stimulus",  # cause
            # data.columns[22]: "tweet_issue_multiple_choice",
            # data.columns[23]: "tweet_issue_open",
            # data.columns[24]: "tweet_purpose"
        })
        # remove rows with nan values
        data_filtered = data_filtered.dropna()
        # drop rows where there is no emotion annotated (should be 1)
        data_filtered = data_filtered[data_filtered.emotion != "BLANK"]
        # convert to dict
        data_filtered = data_filtered.to_dict("records")

    else:
        data_filtered = data[[
            data.columns[5],  # trust
            data.columns[14],  # tweet
            data.columns[10],  # emotional content
            data.columns[20],  # emotional content (gold)
        ]]

        data_filtered = data_filtered.rename(columns={
            data.columns[5]: "trust",
            data.columns[14]: "tweet",
            data.columns[10]: "emotional_content",
            data.columns[20]: "emotional_content_gold"
        })
        # remove rows with nan values
        data_filtered = data_filtered.dropna()
        # convert to dict
        data_filtered = data_filtered.to_dict("records")

    return data_filtered



if __name__ == "__main__":
    raw_q1 = _load(Q1_PATH, questionnaire=1)
    raw_q2 = _load(Q2_1_PATH, questionnaire=2) + _load(Q2_2_PATH, questionnaire=2)

    # Clean Q2

    # Lists must be sorted for the groupby!
    raw_q2 = sorted(raw_q2, key=lambda x: x["tweet"])

    tweets_with_emotion = set()
    raw_q2_clean = []
    sentiment_tags = set()
    tot_with_emotion_count, tot_no_emotion_count = 0, 0
    for tweet, group in groupby(raw_q2, lambda x: x["tweet"]):
        tot_with_emotion_count += 1
        tweet = " ".join(tweet.split())
        tweets_with_emotion.add(tweet)

        group = list(group)

        emotions = [x["emotion"] for x in group]
        emotions_plutchik = [_emotion2plutchik[x["emotion"]][0] for x in group]
        trusts = [x["trust"] for x in group]
        # sentiments = [x["emotion_polarity"] for x in group]

        emotions_plutchik_counts_class = Counter(emotions_plutchik)
        emotions_plutchik_counts = dict(emotions_plutchik_counts_class.most_common())
        # are there more then one category with the maximum?
        _max_p = max(v for k, v in emotions_plutchik_counts.items())
        if sum(1 for k, v in emotions_plutchik_counts.items() if v == _max_p) > 1:
            continue  # cannot adjudicate an emotion (no unanimity)
        # adjudicate using Plutchik emotion
        emotion, _ = emotions_plutchik_counts_class.most_common(1)[0]

        cues, tgts, stms, exps = [], [], [], []
        polarities = []
        for g in group:
            if _emotion2plutchik[g["emotion"]][0] == emotion:
                cue = g["span_supporting_emotion"]
                tgt = g["target"]
                stm = g["emotion_stimulus"]
                exp = g["experiencer"]
                polarity = g["emotion_polarity"]

                if polarity.lower() not in blank_tags:
                    polarities.append(polarity)
                if cue.lower() not in blank_tags:
                    cues.append(cue)
                if tgt.lower() not in blank_tags:
                    tgts.append(tgt)
                if stm.lower() not in blank_tags:
                    stms.append(stm)
                if exp.lower() not in blank_tags:
                    exps.append(exp)

        sentiment_counts_class = Counter(polarities)
        sentiment_counts = dict(sentiment_counts_class.most_common())
        if len(sentiment_counts) == 0:
            sentiment = _plutchik2sentiment[emotion]  # cannot adjudicate sentiment, must infer from emotion
        else:
            # are there more then one category with the maximum?
            _max_p = max(v for k, v in sentiment_counts.items())
            if sum(1 for k, v in sentiment_counts.items() if v == _max_p) > 1:
                sentiment = _plutchik2sentiment[emotion]  # cannot adjudicate sentiment (no unanimity), must infer from emotion
            else:
                sentiment, _ = sentiment_counts_class.most_common(1)[0]
                sentiment = _polaritytag2sentiment[sentiment]  # adjudicated sentiment (unanimity)


        twitter_tokenizer = TweetTokenizer()

        # Adjudicate cue spans
        cues = [e for e in cues if e.strip().lower() not in tweeter_tags]
        if len(cues) != 0:
            cues_smart_split = []
            for x in cues:
                smart_split = split_longest_common_substrings(x, tweet, twitter_tokenizer.tokenize)
                if smart_split is not None:
                    cues_smart_split.append(smart_split)
            try:
                # cues_smart_split = [split_longest_common_substrings(x, tweet, twitter_tokenizer.tokenize) for x in cues]
                cues = find_span_annotation_intersections(tweet, cues_smart_split, fuzzy=True,
                                                          occurrences_adjudication=True, max_typos=5)
            except:
                warnings.warn(f"Unable to find cue spans {cues} in text '{tweet}'. Skipping...")
                continue

        # Adjudicate target spans
        if sum(1 for e in tgts if e.strip().lower() in tweeter_tags) > len(tgts) / 2:
            tgts = [(-1, -1)]  # target is author
        else:
            tgts = [e for e in tgts if e.strip().lower() not in tweeter_tags]
            if len(tgts) != 0:
                tgts_smart_split = []
                for x in tgts:
                    smart_split = split_longest_common_substrings(x, tweet, twitter_tokenizer.tokenize)
                    if smart_split is not None:
                        tgts_smart_split.append(smart_split)
                try:
                    # tgts_smart_split = [split_longest_common_substrings(x, tweet, twitter_tokenizer.tokenize) for x in tgts]
                    tgts = find_span_annotation_intersections(tweet, tgts_smart_split, fuzzy=True,
                                                              occurrences_adjudication=True, max_typos=5)
                except:
                    warnings.warn(f"Unable to find target spans {tgts} in text '{tweet}'. Skipping...")
                    continue

        # Adjudicate stimulus spans
        stms = [e for e in stms if e.strip().lower() not in tweeter_tags]
        if len(stms) != 0:
            stms_smart_split = []
            for x in stms:
                smart_split = split_longest_common_substrings(x, tweet, twitter_tokenizer.tokenize)
                if smart_split is not None:
                    stms_smart_split.append(smart_split)
            try:
                # stms_smart_split = [split_longest_common_substrings(x, tweet, twitter_tokenizer.tokenize) for x in stms]
                stms = find_span_annotation_intersections(tweet, stms_smart_split, fuzzy=True,
                                                          occurrences_adjudication=True, max_typos=5)
            except:
                warnings.warn(f"Unable to find stimulus spans {stms} in text '{tweet}'. Skipping...")
                continue

        # Adjudicate experiencer spans
        if sum(1 for e in exps if e.strip().lower() in tweeter_tags) > len(exps) / 2:
            exps = [(-1, -1)]  # experiencer is author
        else:
            exps = [e for e in exps if e.strip().lower() not in tweeter_tags]
            if len(exps) != 0:
                exps_smart_split = []
                for x in exps:
                    smart_split = split_longest_common_substrings(x, tweet, twitter_tokenizer.tokenize)
                    if smart_split is not None:
                        exps_smart_split.append(smart_split)
                try:
                    # exps_smart_split = [split_longest_common_substrings(x, tweet, twitter_tokenizer.tokenize) for x in exps]
                    exps = find_span_annotation_intersections(tweet, exps_smart_split, fuzzy=True,
                                                              occurrences_adjudication=True, max_typos=5)
                except:
                    warnings.warn(f"Unable to find experiencer spans {exps} in text '{tweet}'. Skipping...")
                    continue

        # Merge contiguous spans that are separated by space, dash or other special chars
        cues = merge_contiguous_spans(tweet, cues)
        tgts = merge_contiguous_spans(tweet, tgts)
        exps = merge_contiguous_spans(tweet, exps)
        stms = merge_contiguous_spans(tweet, stms)

        raw_q2_clean.append({
            "text": tweet,
            "emotion": emotion,
            "sentiment": sentiment,
            "cue": cues,
            "target": tgts,
            "experiencer": exps,
            "stimulus": stms
        })

    # Clean Q1
    raw_q1_clean = []

    # Lists must be sorted for the groupby!
    raw_q1 = sorted(raw_q1, key=lambda x: x["tweet"])
    for tweet, group in groupby(raw_q1, lambda x: x["tweet"]):

        group = list(group)
        tweet = " ".join(tweet.split())

        if tweet in tweets_with_emotion:
            continue

        emotional_content = [e["emotional_content"] for e in group]
        count_noemotion = emotional_content.count("This tweet has no emotional content.")

        if count_noemotion / len(group) > 0.5:
            raw_q1_clean.append(tweet)
        tot_no_emotion_count += 1
    result = {}
    for index, data in enumerate(raw_q2_clean):
        index = "elections." + str(index).zfill(7)
        result[index] = {}

        result[index]["text"] = data["text"]
        result[index]["emotions"] = {}

        emotion_index = index + ".00"
        result[index]["emotions"][emotion_index] = {}

        result[index]["emotions"][emotion_index]["original_emotion"] = data["emotion"]
        result[index]["emotions"][emotion_index]["sentiment"] = data["sentiment"]
        result[index]["emotions"][emotion_index]["plutchik_emotion"] = [data["emotion"]]
        result[index]["emotions"][emotion_index]["roles"] = {}

        result[index]["emotions"][emotion_index]["roles"]["cue"] = data["cue"]
        result[index]["emotions"][emotion_index]["roles"]["experiencer"] = data["experiencer"]
        result[index]["emotions"][emotion_index]["roles"]["target"] = data["target"]
        result[index]["emotions"][emotion_index]["roles"]["cause"] = data["stimulus"]

    for index, text in enumerate(raw_q1_clean, start=len(raw_q2_clean)):
        index = "elections." + str(index).zfill(7)
        result[index] = {}

        result[index]["text"] = text
        result[index]["emotions"] = {}

    with open("SRL4E_elections.json", "w") as f:
        json.dump(result, f, sort_keys=True, indent=4)