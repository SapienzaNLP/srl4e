import json
import warnings
from utils import find_span_annotation_intersections
import re

BLOGS_BASE_PATH = "../datasets/blogs/Emotion-Data/Annotated Data/basefile.txt"
BLOGS_1_PATH = "../datasets/blogs/Emotion-Data/Annotated Data/AnnotSet1.txt"
BLOGS_2_PATH = "../datasets/blogs/Emotion-Data/Annotated Data/AnnotSet2.txt"

# sorted(list(set(deep_flatten([[b.strip() for b in a[5].split(",")] for a in _load(...)]))))
_emotion2plutchik = {
    'ag': ["anger"],
    'dg': ["disgust"],
    'fr': ["fear"],
    'hp': ["joy"],  # happiness
    'me': ["other"],  # mixed emotion
    'ne': None,  # "no emotion",
    'sd': ["sadness"],
    'sp': ["surprise"]
}

_emotion2sentiment = {
    'ag': "negative",
    'dg': "negative",
    'fr': "negative",
    'hp': "positive",
    'me': "other",  # mixed emotion
    'ne': "neutral",  # "no emotion",
    'sd': "negative",
    'sp': "other"
}

_emotions = set(list(_emotion2plutchik.keys()))

def _load(data_path):
    result = []
    with open(data_path, "r") as f:
        for line in f:
            found = re.search(r"(\d+)\.\s+(.+)", line)
            if found:
                number = found.group(1)
                text = found.group(2)
                result.append((number.strip(), text.strip()))
    # manual check (annotations 1)
    if result[3384] in [('770', ':D!'), ('770', 'hp h'), ('770', 'hp h')]:
        del result[3384]
    if result[4538] in [('196', 'The presents in the boxes were varied and unusual and very useless.'), ('196', 'dg l'), ('196', 'ne')]:
        del result[4538]
    if result[4809] == ('468', 'hp m'):
        result[4809] = ('468', 'hp m Good deal')
    if result[4875] == ('534', 'dg l'):
        result[4875] = ('534', 'dg l rather stupid')
    # manual check (annotations 2)
    if result[1516] in [('669', '(Its a bit nipply in this house though I know that lol) Welp I better get my ass off the computer.'), ('669', 'ne'), ('669', 'hp l')]:
        del result[1516]
    # fix missing "," in some instances
    if result[1013] == ('166', 'hp m feel happyspent time with my family'):
        result[1013] = ('166', 'hp m feel happy, spent time with my family')
    if result[3987] == ('493', 'dg l old fashioned pretty damn'):
        result[3987] = ('493', 'dg l old fashioned, pretty damn')
    if result[4454] == ('113', 'fr m worried losing'):
        result[4454] = ('113', 'fr m worried, losing')
    if result[4802] == ('462', 'ag m angry troublesome'):
        result[4802] = ('462', 'ag m angry, troublesome')
    if result[351] == ('352', 'hp m celebrated anniversary'):
        result[351] = ('352', 'hp m celebrated, anniversary')
    if result[598] == ('599', 'dg m critical patriotic-fever'):
        result[598] = ('599', 'dg m critical, patriotic-fever')
    return result

if __name__ == "__main__":
    raw_base = _load(BLOGS_BASE_PATH)
    raw_1 = _load(BLOGS_1_PATH)
    raw_2 = _load(BLOGS_2_PATH)

    result = {}
    counter = 0
    for index, data in enumerate(zip(raw_base, raw_1, raw_2)):
        index = "blogs." + str(index).zfill(7)
        result[index] = {}

        (num_base, text), (num_annot_1, annot_1), (num_annot_2, annot_2) = data
        assert num_base == num_annot_1 == num_annot_2

        # some checks to assure the consistency of the annotations (1)
        annot_1_spl = annot_1.split(" ")
        if len(annot_1_spl) == 0:
            raise Exception("Empty annotation.")
        elif len(annot_1_spl) == 1:
            assert annot_1_spl[0] == 'ne'  # = no emotion
        else:
            assert len(annot_1_spl) > 2  # amount of columns (should be 3)
            assert len(annot_1_spl[0]) == 2  # length of emotion label
            assert len(annot_1_spl[1]) == 1  # length of intensity label
            assert len(annot_1_spl[2]) > 0  # length of span/s annotations

        # some checks to assure the consistency of the annotations (2)
        annot_2_spl = annot_2.split(" ")
        if len(annot_2_spl) == 0:
            raise Exception("Empty annotation.")
        elif len(annot_2_spl) == 1:
            assert annot_2_spl[0] == 'ne'  # = no emotion
        else:
            assert len(annot_2_spl) > 2  # amount of columns (should be at least 3)
            assert len(annot_2_spl[0]) == 2  # length of emotion label
            assert len(annot_2_spl[1]) == 1  # length of intensity label
            assert len(annot_2_spl[2]) > 0  # length of span/s annotations

        emotion1, emotion2 = annot_1_spl[0], annot_2_spl[0]
        cues1, cues2 = " ".join(annot_1_spl[2:]).split(","), " ".join(annot_2_spl[2:]).split(",")
        cues1, cues2 = [x.strip() for x in cues1], [x.strip() for x in cues2]

        if emotion1 != "ne" and emotion2 != "ne" and emotion1 != emotion2:
            del result[index]
            continue

        result[index]["text"] = text
        result[index]["emotions"] = {}

        if (emotion1 == emotion2 == "ne"):
            continue

        if emotion1 == emotion2:
            emotion = emotion1
            cues = [cues1, cues2]
                 # list(set(cues1).intersection(set(cues2)))
        elif emotion1 == "ne" and emotion2 != "ne":
            emotion = emotion2
            cues = [cues2]
        elif emotion1 != "ne" and emotion2 == "ne":
            emotion = emotion1
            cues = [cues1]
        else:
            raise Exception("Unexpected data format.")
        try:
            cues = find_span_annotation_intersections(text, cues, fuzzy=True, occurrences_adjudication=False, max_typos=4)
        except ValueError:
            warnings.warn(f"{index}: cannot find one or more of spans {cues} in '{text}'. Skipping...")
            del result[index]
            continue

        if len(cues) == 0:
            warnings.warn(f"{index}: cannot find an intersection for cues [{cues1}, {cues2}] in '{text}'. Skipping...")
            del result[index]
            continue

        '''if not all(c in text for c in cues):
            counter += 1
            print(f"{counter}, {index}, {text}, {cues}")'''


        emotion_index = index + ".00"  # + str(i).zfill(2)
        result[index]["emotions"][emotion_index] = {}

        result[index]["emotions"][emotion_index]["original_emotion"] = [emotion]
        result[index]["emotions"][emotion_index]["plutchik_emotion"] = _emotion2plutchik[emotion]
        result[index]["emotions"][emotion_index]["sentiment"] = _emotion2sentiment[emotion]

        result[index]["emotions"][emotion_index]["roles"] = {}

        result[index]["emotions"][emotion_index]["roles"]["cue"] = cues
        #result[index]["emotions"][emotion_index]["roles"]["experiencer"] = labels["experiencer"]
        #result[index]["emotions"][emotion_index]["roles"]["target"] = labels["target"]
        #result[index]["emotions"][emotion_index]["roles"]["cause"] = labels["cause"]
    with open("SRL4E_blogs.json", "w") as f:
        json.dump(result, f, sort_keys=True, indent=4)
