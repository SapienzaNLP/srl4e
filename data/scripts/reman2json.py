import json
import warnings
import xmlschema
from nltk.tokenize import sent_tokenize

class ContinueOuterLoop(Exception):
    pass

REMAN_SCHEMA_PATH = "../datasets/fiction/reman/reman-schema.xsd"
REMAN_PATH = "../datasets/fiction/reman/reman-version1.0.xml"

_emotion_spans = {'joy', 'trust', 'other-emotion', 'anticipation', 'sadness', 'surprise', 'fear', 'anger', 'disgust'}
_allowed_relations = {'target', 'cause', 'experiencer'}
_emotion2sentiment = {
    'joy': 'positive',
    'trust': 'positive',
    'other-emotion': 'other',
    'anticipation': 'other',
    'sadness': 'negative',
    'surprise': 'other',
    'fear': 'negative',
    'anger': 'negative',
    'disgust': 'negative'
}
_emotion2plutchik = {
    'joy': 'joy',
    'trust': 'trust',
    'other-emotion': 'other',
    'anticipation': 'anticipation',
    'sadness': 'sadness',
    'surprise': 'surprise',
    'fear': 'fear',
    'anger': 'anger',
    'disgust': 'disgust'
}

def _load(schema, data):
    schema = xmlschema.XMLSchema(schema)
    reman = schema.to_dict(data)
    return reman

if __name__ == "__main__":
    raw = _load(REMAN_SCHEMA_PATH, REMAN_PATH)["document"]

    skipped_counter = 0
    result = {}

    for index, data in enumerate(raw):
        index = "reman." + str(index).zfill(7)
        result[index] = {}

        try:
            text = data["text"]
            result[index]["text"] = text
            result[index]["emotions"] = {}

            text_spl = sent_tokenize(text)
            assert len(text_spl) == 3, "Cannot split " + index + f": text='{text}'"
            text_left, text_main, text_right = tuple(text_spl)

            position = text.find(text_left)
            text_left = (position, (position + len(text_left)))

            position = text[text_left[1]:].find(text_main) + text_left[1]
            text_main = (position, (position + len(text_main)))

            position = text[text_main[1]:].find(text_right) + text_main[1]
            text_right = (position, (position + len(text_right)))

            result[index]["main_sentence"] = text_main
            result[index]["context_sentences"] = [text_left, text_right]

            # relation types = ['target', 'cause', 'experiencer', 'coreference']
            # span types = ['joy', 'trust', 'other-emotion', 'other', 'anticipation', 'character', 'sadness', 'event', 'surprise', 'fear', 'anger', 'disgust']
            if data["adjudicated"]["spans"] is not None:
                # We add the adjudicated annotations
                spans, cues = {}, {}
                for s in data["adjudicated"]["spans"]["span"]:
                    #assert s["$"] == text[s["@cbegin"]:s["@cend"]]
                    begin, end, type = s["@cbegin"], s["@cend"], s["@type"]
                    spans[s["@annotation_id"]] = (begin, end, type)
                    if type in _emotion_spans:
                        if (begin, end) not in cues:
                            cues[(begin, end)] = {"emotion": [type], "target": [], "cause": [], "experiencer": []}
                        else:
                            cues[(begin, end)]["emotion"].append(type)

                # We also consider other annotations (because some relations refer to them)
                # other_spans, other_cues = {}, {}
                for s in (data["other"]["spans"]["span"] if data["other"]["spans"] is not None else []):
                    # assert s["$"] == text[s["@cbegin"]:s["@cend"]]
                    begin, end, type = s["@cbegin"], s["@cend"], s["@type"]
                    spans[s["@annotation_id"]] = (begin, end, type)
                    '''if type in _emotion_spans:
                        if (begin, end) not in other_cues:
                            other_cues[(begin, end)] = {"emotion": [type], "target": [], "cause": [], "experiencer": []}
                        else:
                            other_cues[(begin, end)]["emotion"].append(type)'''

                if data["adjudicated"]["relations"] is not None:
                    for r in data["adjudicated"]["relations"]["relation"]:
                        source, target = r["@source_annotation_id"], r["@target_annotation_id"]
                        relation_type = r["@type"]
                        assert source in spans and target in spans

                        source_begin, source_end, _ = spans[source]
                        source_span = (source_begin, source_end)

                        target_begin, target_end, _ = spans[target]
                        target_span = (target_begin, target_end)

                        if relation_type in _allowed_relations:
                            if source_span not in cues:
                                raise ContinueOuterLoop
                            if relation_type not in cues[source_span]:
                                warnings.warn(f"Role '{relation_type}' should already be in this emotion set!")
                                cues[source_span][relation_type] = [target_span]
                            else:
                                cues[source_span][relation_type].append(target_span)

                for i, (cue_span, labels) in enumerate(cues.items()):
                    emotion_index = index + "." + str(i).zfill(2)
                    result[index]["emotions"][emotion_index] = {}

                    result[index]["emotions"][emotion_index]["original_emotion"] = labels["emotion"]
                    result[index]["emotions"][emotion_index]["plutchik_emotion"] = [_emotion2plutchik[a] for a in labels["emotion"]]

                    sentiment = [_emotion2sentiment[a] for a in labels["emotion"]]
                    if all(s == "other" for s in sentiment):
                        sentiment = "other"
                    elif all(s in ["positive", "other"] for s in sentiment):
                        sentiment = "positive"
                    elif all(s in ["negative", "other"] for s in sentiment):
                        sentiment = "negative"
                    else:
                        sentiment = "other"
                        warnings.warn(f"Sample {emotion_index} sentiment is ambiguous. Emotions are: {labels['emotion']}")
                    result[index]["emotions"][emotion_index]["sentiment"] = sentiment
                    result[index]["emotions"][emotion_index]["roles"] = {}

                    result[index]["emotions"][emotion_index]["roles"]["cue"] = [cue_span]
                    result[index]["emotions"][emotion_index]["roles"]["experiencer"] = sorted(list(set(labels["experiencer"])))
                    result[index]["emotions"][emotion_index]["roles"]["target"] = sorted(list(set(labels["target"])))
                    result[index]["emotions"][emotion_index]["roles"]["cause"] = sorted(list(set(labels["cause"])))
        except ContinueOuterLoop:
            del result[index]
            skipped_counter += 1
            continue
    with open("SRL4E_reman.json", "w") as f:
        json.dump(result, f, sort_keys=True, indent=4)