import json
import re
import warnings
#from unidecode import unidecode

from utils.data import deep_flatten

news_titles_path = "../datasets/news_titles/goodnewseveryone-v1.0/gne-release-v1.0.jsonl"
fixed_news_titles_path = "../datasets/news_titles/goodnewseveryone-v1.0/gne_fix.jsonl"
_label_emotion = {"dominant": "dominant_emotion", "other": "other_emotions", "reader": "reader_emotions"}
_emotion_categs = ["dominant", "other", "reader"]

_orig2plutchik = {
    'anger': ['anger'],
    'annoyance': ['anger', 'disgust'],
    'disgust': ['disgust'],
    'fear': ['fear'],
    'guilt': ['sadness', 'disgust'],
    'joy': ['joy'],
    'love_including_like': ['joy', 'trust'],
    'negative_anticipation_including_pessimism': ['anticipation'],
    'negative_surprise': ['surprise'],
    'positive_anticipation_including_optimism': ['anticipation'],
    'positive_surprise': ['surprise'],
    'pride': ['trust', 'joy'],  # todo: da rivedere
    'sadness': ['sadness'],
    'shame': ['fear', 'disgust'],  # todo: da rivedere
    'trust': ['trust']
}

_orig2sentiment = {
    'anger': 'negative',
    'annoyance': 'negative',
    'disgust': 'negative',
    'fear': 'negative',
    'guilt': 'negative',
    'joy': 'positive',
    'love_including_like': 'positive',
    'negative_anticipation_including_pessimism': 'negative',
    'negative_surprise': 'negative',
    'positive_anticipation_including_optimism': 'positive',
    'positive_surprise': 'positive',
    'pride': 'positive',  # todo: da rivedere
    'sadness': 'negative',
    'shame': 'negative',
    'trust': 'positive'
}

def search_span_deep_flatten(text, span):
    flattened = deep_flatten(span)
    if len(flattened) == 0:
        return []  # todo: before it was (-1, -1)
    else:
        #assert len(flattened) == 1
        #flattened = flattened[0]
        #pos = text.find(flattened)
        #return (pos, pos + len(flattened))
        text = text.lower()
        result = []
        for f in flattened:
            f = f.lower().split("; ")
            for _f in f:
                if _f in ["none", "implicit"]:
                    continue
                pos = text.find(_f)
                if pos == -1:
                    warnings.warn(f"Cannot find span in text: text='{text}', span='{span}'. Skipping...")
                    continue
                # The original annotation presents a problem: sometimes the last character is missing from the spans,
                # for example the annotated "Massive Resistanc" in the text is "Massive Resistance". Therefore, if the
                # next character is a letter, the span is rounded up by only 1 character
                if len(text) > pos + len(_f) and re.search(r"\w", text[pos + len(_f)]):
                    result.append((pos, pos + len(_f) + 1))
                else:
                    result.append((pos, pos + len(_f)))
        return result

if __name__ == "__main__":
    raw, fix = [], []
    fix_ids = {}
    
    # load the fixed dataset lines
    with open(fixed_news_titles_path) as f:
        counter = 0
        for line in f:
            l = json.loads(line)
            fix_ids[l["id"]] = counter
            fix.append(l)
            counter += 1

    # load the dataset and replaces lines that have been fixed (this will likely change with sth more elegant)
    with open(news_titles_path) as f:
        for line in f:
            l = json.loads(line)
            if l["id"] in fix_ids:
                l = fix[fix_ids[l["id"]]]
            raw.append(l)
    
    

    id2class, class2id = {}, {}
    for cl in _emotion_categs:
        id2class[cl] = set()

        for e in raw:
            for em in deep_flatten(e["annotations"][_label_emotion[cl]]["gold"]):
                id2class[cl].add(em)

        id2class[cl] = dict(list(enumerate(sorted(list(id2class[cl])))))
        class2id[cl] = {v: k for k, v in id2class[cl].items()}

    result = {}

    for index, data in enumerate(raw):
        index = "gne." + str(index).zfill(7)
        result[index] = {}

        text = data["headline"]
        result[index]["text"] = text
        result[index]["emotions"] = {}

        emotion_index = index + ".00"
        result[index]["emotions"][emotion_index] = {}

        result[index]["emotions"][emotion_index]["original_emotion"] = deep_flatten(data["annotations"]["dominant_emotion"]["gold"])
        result[index]["emotions"][emotion_index]["sentiment"] = _orig2sentiment[result[index]["emotions"][emotion_index]["original_emotion"][0]]
        #result[index]["emotions"][emotion_index]["ekman_emotion"] = None
        result[index]["emotions"][emotion_index]["plutchik_emotion"] = _orig2plutchik[result[index]["emotions"][emotion_index]["original_emotion"][0]]
        #result[index]["emotions"][emotion_index]["intensity"] = None
        result[index]["emotions"][emotion_index]["roles"] = {}

        result[index]["emotions"][emotion_index]["roles"]["cue"] = search_span_deep_flatten(text,
            data["annotations"]["cue"]["gold"])
        result[index]["emotions"][emotion_index]["roles"]["experiencer"] = search_span_deep_flatten(text,
            data["annotations"]["experiencer"]["gold"])
        result[index]["emotions"][emotion_index]["roles"]["target"] = search_span_deep_flatten(text,
            data["annotations"]["target"]["gold"])
        result[index]["emotions"][emotion_index]["roles"]["cause"] = search_span_deep_flatten(text,
            data["annotations"]["cause"]["gold"])
    with open("SRL4E_gne.json", "w") as f:
        json.dump(result, f, sort_keys=True, indent=4)