import json
import warnings
from collections import OrderedDict
from itertools import groupby

from utils import end_overlap
import re
import xml.etree.ElementTree as ET
import xmltodict

class ContinueOuterLoop(Exception):
    pass

NTCIR_TRAIN_EN_PATH = "../datasets/ntcir/13th NTCIR ECA Task/ECA_training_English.xml"
NTCIR_TRAIN_CH_PATH = "../datasets/ntcir/13th NTCIR ECA Task/ECA_training_Chinese.xml"
NTCIR_TEST_EN_PATH = "../datasets/ntcir/13th NTCIR ECA Task/cause_emotion_eng_test.xml"
NTCIR_TEST_CH_PATH = "../datasets/ntcir/13th NTCIR ECA Task/cause_emotion_chi_test.xml"

# sorted(list(set(deep_flatten([[b.strip() for b in a[5].split(",")] for a in _load(...)]))))
_emotion2plutchik = {
    "happiness": ["joy"],
    "sadness": ["sadness"],
    "anger": ["anger"],
    "fear": ["fear"],
    "surprise": ["surprise"],
    "disgust": ["disgust"],
}

_emotion2sentiment = {
    'sadness': 'negative',
    'happiness': 'positive',
    'surprise': 'other',
    'fear': 'negative',
    'disgust': 'negative',
    'anger': 'negative'
}

_emotions = set(list(_emotion2plutchik.keys()))
_nointerrupt_chars = {'#', '&', "'", '"', '(', ')', '-', '?', '[', '`', '±', '‘', '“', '”'}

def _load(path):
    #tree = ET.parse(path)
    with open(path, "r") as f:
        xmlstring = f.read()
        xmlstring = xmlstring.replace("?/text>", "</text>")
        xmlstring = xmlstring.replace("?/cause>", "</cause>")

    data = []
    for m in re.finditer(r"<\?xml version.*?<\/emotionml>", xmlstring, flags=re.DOTALL):
        b, e = m.span()
        match = xmlstring[b:e]
        tree = ET.ElementTree(ET.fromstring(match))
        #tree = ET.fromstring(re.sub(r"(<\?xml[^>]+\?>)", r"\1<root>", xml) + "</root>")

        xml_data = tree.getroot()
        xmlstr = ET.tostring(xml_data, encoding='utf-8', method='xml')
        data_dict = dict(xmltodict.parse(xmlstr, strip_whitespace=False))
        data.append(data_dict)
    return data

def _process_data(in_path, out_path, language):
    assert language in ["english", "chinese"]
    raw = _load(in_path)

    raw_preprocessed = []

    counter, skipped, overlapping_cue = 0, 0, 0
    for data in raw:
        data = data["ns0:emotionml"]["ns0:emotion"]
        index = f"id={int(data['@id'])}"
        try:
            emotion = data["ns0:category"]["@name"]
            if not "ns0:clause" in data:
                continue
            clauses = data["ns0:clause"]
            counter += 1
            text = ""
            cue, cause = [], []
            if type(clauses) == OrderedDict:
                clauses = [clauses]
            for clause in clauses:
                if "ns0:text" not in clause:
                    continue
                clause_text = clause["ns0:text"]

                overlap = end_overlap(text, clause_text)
                if overlap > 1:
                    raise ContinueOuterLoop(
                        f"Text end is overlapping with beginning of clause! text='{text}', clause='{clause_text}', overlap={overlap}")

                if language == "english":
                    # check if the clause has leading whitespace
                    clause_lstrip = clause_text.lstrip()
                    hasspace = len(clause_lstrip) < len(clause_text)
                    # check if the clause begins with an uppercase letter
                    isupperc = clause_lstrip[0].isupper()
                    # do nothing if the next character is in the set
                    nointerr = clause_lstrip[0] in _nointerrupt_chars

                    # adds a space only if needed (if there is no space between the parts and the other part is not an end of discourse)
                    if len(text.rstrip()) == len(text) and len(clause_text) > 1 and clause_text[
                        1] != " " and text != "":
                        text = text + " "
                    if text != "" and not nointerr:
                        text = text.rstrip()
                        text = text + ("." if isupperc else ",")
                        text = text + ("" if hasspace else " ")
                else:
                    if text != "":
                        text = text + "。"

                clause_lstrip_shift = 0
                if text == "" and language == "english":
                    clause_lstrip_shift = len(clause_text) - len(clause_text.lstrip())

                assert clause["@cause"] in ["Y", "N"] and clause["@cause"] in ["Y", "N"]
                # causes (stimulus)
                if clause["@cause"] == "Y":
                    begin, length = int(clause["ns0:cause"]["@begin"]), int(clause["ns0:cause"]["@lenth"])
                    cause_text = clause["ns0:cause"]["#text"]
                    if begin == -1:
                        raise ContinueOuterLoop(f"Wrong begin value: {begin}")
                    if clause_text[begin:begin + length] != cause_text:
                        if begin >= 2 and clause_text[begin - 2:begin + length - 2] == cause_text:
                            begin -= 2
                        elif cause_text in clause_text:
                            begin = clause_text.find(cause_text)
                            length = len(cause_text)
                        else:
                            raise ContinueOuterLoop(
                                f"Clause span with cause indicated not corresponding with its text: span='{clause_text[begin:begin + length]}', cause_text='{cause_text}'")
                    cause_span = (
                    len(text) + begin - clause_lstrip_shift, len(text) + begin + length - clause_lstrip_shift)
                    cause.append(cause_span)
                # keyword (cue)
                if clause["@keywords"] == "Y":
                    begin, length = int(clause["ns0:keywords"]["@keywords-begin"]), int(
                        clause["ns0:keywords"]["@keywords-lenth"])
                    keyword_text = clause["ns0:keywords"]["#text"]
                    if begin == -1:
                        raise ContinueOuterLoop(f"Wrong begin value: {begin}")
                    if clause_text[begin:begin + length] != keyword_text:
                        if begin >= 1 and clause_text[begin - 1:begin + length - 1] == keyword_text:
                            begin -= 1
                        elif begin >= 2 and clause_text[begin - 2:begin + length - 2] == keyword_text:
                            begin -= 2
                        elif keyword_text in clause_text:
                            begin = clause_text.find(keyword_text)
                            length = len(keyword_text)
                        else:
                            raise ContinueOuterLoop(
                                f"Clause span with keyword indicated not corresponding with its text: span='{clause_text[begin:begin + length]}', cause_text='{keyword_text}'")
                    keyword_span = (
                    len(text) + begin - clause_lstrip_shift, len(text) + begin + length - clause_lstrip_shift)
                    cue.append(keyword_span)

                if text == "" and language == "english":
                    text = clause_text.lstrip()
                else:
                    text = text + clause_text

            if len(cue) > 0 or len(cause) > 0:
                raw_preprocessed.append({
                    "emotion": emotion,
                    "cue": cue,
                    "cause": cause,
                    "text": text
                })

        except ContinueOuterLoop as e:
            warnings.warn("Inconsistencies found in " + index + f": {str(e)}. Skipping...")
            skipped += 1
            continue

    result = {}
    raw_preprocessed = sorted(raw_preprocessed, key=lambda x: x["text"])
    for index, (key, group) in enumerate(groupby(raw_preprocessed, lambda x: x["text"])):
        group = list(group)
        index = "ntcir." + str(index).zfill(7)
        result[index] = {}

        result[index]["text"] = key
        result[index]["emotions"] = {}

        _overlapping_cue = False
        seen_cues = set()  # key: cues, values: causes
        for i, g in enumerate(group):
            if not all(q not in seen_cues for q in g["cue"]):
                _overlapping_cue = True
                warnings.warn(f"Duplicate (conflict) cue annotation? seen_cues={seen_cues}, cues={g['cue']}")
            for c in g["cue"]:
                seen_cues.add(c)

            emotion_index = index + "." + str(i).zfill(2)
            result[index]["emotions"][emotion_index] = {}

            emotion = g["emotion"]

            result[index]["emotions"][emotion_index]["original_emotion"] = [emotion]
            result[index]["emotions"][emotion_index]["plutchik_emotion"] = _emotion2plutchik[emotion]
            result[index]["emotions"][emotion_index]["sentiment"] = _emotion2sentiment[emotion]

            result[index]["emotions"][emotion_index]["roles"] = {}

            result[index]["emotions"][emotion_index]["roles"]["cue"] = g["cue"]
            result[index]["emotions"][emotion_index]["roles"]["cause"] = g["cause"]
        if _overlapping_cue:
            overlapping_cue += 1

    print(
        f"skipped={skipped}/{counter}={round(skipped / counter, 3)}, overlapping_cue={overlapping_cue}/{counter}={round(overlapping_cue / counter, 3)}")

    with open(out_path, "w") as f:
        json.dump(result, f, sort_keys=True, indent=4)


if __name__ == "__main__":
    _process_data(in_path=NTCIR_TRAIN_EN_PATH, out_path="SRL4E_ntcir_en_train.json", language="english")
    _process_data(in_path=NTCIR_TEST_EN_PATH, out_path="SRL4E_ntcir_en_test.json", language="english")
    _process_data(in_path=NTCIR_TRAIN_CH_PATH, out_path="SRL4E_ntcir_ch_train.json", language="chinese")
    _process_data(in_path=NTCIR_TEST_CH_PATH, out_path="SRL4E_ntcir_ch_test.json", language="chinese")
