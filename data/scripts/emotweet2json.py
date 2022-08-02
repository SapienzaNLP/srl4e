import json
import pandas as pd
from utils import fuzzy_search, get_emoji_regexp_pattern
import emoji
import re

EMOTWEET_PATH = "../datasets/emotweet/EmoTweet-28-v1.1/EmoTweet-28-v1.1.txt"
EMOJI_REGEX_PATTERN = emoji.get_emoji_regexp('en').pattern

# sorted(list(set(deep_flatten([[b.strip() for b in a[5].split(",")] for a in _load(...)]))))
_emotion2plutchik = {
    'admiration': ['trust'],
    'amusement': ['joy'],
    'anger': ['anger'],
    'boredom': ['disgust'],
    'confidence': ['trust'],
    'curiosity': ['anticipation'],
    'desperation': ['sadness'],
    'doubt': ['disgust', 'anticipation'],  # todo: vedere se integrare con 'fear'
    'excitement': ['anticipation', 'joy'],
    'exhaustion': ['anger', 'disgust'],  # todo: rivedere se sadness al posto di disgust
    'fascination': ['trust'],  # todo: rivedere se mettere anche/solo anticipation
    'fear': ['fear'],
    'gratitude': ['trust', 'joy'],
    'happiness': ['joy'],
    'hate': ['anger', 'disgust'],
    'hope': ['anticipation', 'trust'],
    'indifference': ['disgust'],
    'inspiration': ['anticipation', 'trust'],
    'jealousy': ['anticipation', 'anger'],
    'longing': ['sadness'],
    'love': ['joy', 'trust'],
    'none': None,
    'pride': ['trust', 'joy'],  # todo: rivedere se mettere joy
    'regret': ['sadness', 'disgust'],
    'relaxed': ['joy'],
    'sadness': ['sadness'],
    'shame': ['anger', 'disgust'],
    'surprise': ['surprise'],
    'sympathy': ['trust']
}

_emotion2sentiment = {
    'admiration': 'positive',
    'amusement': 'positive',
    'anger': 'negative',
    'boredom': 'negative',
    'confidence': 'positive',
    'curiosity': 'other',
    'desperation': 'negative',
    'doubt': 'negative',
    'excitement': 'positive',
    'exhaustion': 'negative',
    'fascination': 'positive',
    'fear': 'negative',
    'gratitude': 'positive',
    'happiness': 'positive',
    'hate': 'negative',
    'hope': 'positive',
    'indifference': 'negative',
    'inspiration': 'positive',
    'jealousy': 'negative',
    'longing': 'negative',
    'love': 'positive',
    'none': None,
    'pride': 'positive',
    'regret': 'negative',
    'relaxed': 'positive',
    'sadness': 'negative',
    'shame': 'negative',
    'surprise': 'other',
    'sympathy': 'positive'
}

_emotions = set(list(_emotion2plutchik.keys()))

def remove_spaces_between_emojis(text):
    f = lambda x: re.sub(EMOJI_REGEX_PATTERN + r"(\s+)" + EMOJI_REGEX_PATTERN, r"\g<1>\g<3>", x)
    return f(f(text))

def _load(data_path):
    result = pd.read_csv(data_path).to_numpy().tolist()
    #result[578][5] = 'anger, happiness'
    result[649][6] = 'hate: you must have loathed; shame: outburst'
    result[466][6] = 'excitement: Looking forward to, Let the good times begin !; relaxed: #relaxation #vacation'
    result[1026][6] = 'hope: Hope, !; fear: Still v concerned over'
    # result[516][6] = 'amusement: 😂 😂 😂; hate: I hate; sadness: 😭 😭 😭 😭 😭 😭 😭 😭 😭'
    result[608][6] = 'hope: Good luck; excitement: Keep up'
    result[648][6] = "hope: hasta la victoria; anger: It wasn't the results that i wanted"
    result[14972][6] = 'sadness: The saddest thing in the world'
    result[970][6] = 'gratitude: Thanks, !; happiness: Greatest., Ever.'
    result[1564][6] = 'admiration: This deserves endless retweets...'
    result[3129][6] = 'confidence: gonna prove that to all the people'
    result[6727][6] = 'love: love these guys with all of my heart!!!'
    result[5499][6] = 'happiness: up, places, :)'
    result[5981][6] = 'hate: hated'
    result[5179][6] = "happiness: feeling like your day simply couldn't get any better"
    result[3786][1] = 'RT @deannajefferson: Our new dance instructor for #ClubFitness has toured w/ Beyonce!!! You know our Beyonce themed night is going to be CRAZY !!!'
    #result[863][5] = 'happiness, sadness'
    return result

if __name__ == "__main__":
    raw = _load(EMOTWEET_PATH)

    result = {}

    for index, data in enumerate(raw):
        index = "emotweet." + str(index).zfill(7)
        result[index] = {}

        text = remove_spaces_between_emojis(data[1])
        emotions = data[6]

        result[index]["text"] = text
        result[index]["emotions"] = {}

        if emotions != "none":
            emotions_check = [a.strip() for a in data[5].split(",")]
            emotions_check_ = []

            emotions_cues = {}

            # some texts may contain ";", so we re-join the cues where it appears
            splitted = data[6].split(";")
            clean_splitted = []
            for e in splitted:
                if len(clean_splitted) == 0:
                    clean_splitted.append(e)
                else:
                    emot = e.split(":")[0].strip()
                    if emot in _emotions:
                        clean_splitted.append(e)
                    else:
                        clean_splitted[-1] = ";".join([clean_splitted[-1], e])

            for e in clean_splitted:
                e = e.strip().split(":")
                # note: assertion below cannot be just == 2 because there are tweets with ":"
                assert len(e) >= 2, f"Error in splitting {index}: text='{text}', emotions='{data[6]}'"
                emotion, cues = e[0], ":".join(e[1:])
                emotion = emotion.strip()
                assert emotion != "" , f"Error in {index}: text='{text}', emotions='{data[6]}'"
                # assert emotion in emotions_check, f"Error in {index}: text='{text}', emotions='{data[6]}'"
                emotions_check_.append(emotion)
                cues = [a.strip() for a in cues.split(",") if a.strip() != ""]
                assert len(cues) > 0

                cues_positions = []
                for cue in cues:
                    cue = cue.strip()
                    assert cue != "", f"Error in {index}: text='{text}', emotions='{data[6]}'"

                    # pos = text.find(cue)
                    #span = fuzzy_search(cue, text, max_typos=4)
                    #if span == None:
                        #span = fuzzy_search(remove_spaces_between_emojis(cue), text, max_typos=4)
                    span = fuzzy_search(remove_spaces_between_emojis(cue), text, max_typos=4)
                    assert span != None, f"cue='{cue}', emotions='{emotions}', text='{text}', index='{index}'"
                    # span = (pos, pos + len(cue))
                    cues_positions.append(span)
                assert len(cues_positions) != 0
                emotions_cues[emotion] = cues_positions

            # assert sorted(emotions_check) == sorted(emotions_check_), f"Error in {index}: text='{text}', emotions='{data[6]}'"

            for i, (emotion, cues) in enumerate(emotions_cues.items()):
                emotion_index = index + "." + str(i).zfill(2)
                result[index]["emotions"][emotion_index] = {}

                result[index]["emotions"][emotion_index]["original_emotion"] = [emotion]
                result[index]["emotions"][emotion_index]["plutchik_emotion"] = _emotion2plutchik[emotion]
                result[index]["emotions"][emotion_index]["sentiment"] = _emotion2sentiment[emotion]

                '''
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
                '''
                result[index]["emotions"][emotion_index]["roles"] = {}

                result[index]["emotions"][emotion_index]["roles"]["cue"] = cues
                #result[index]["emotions"][emotion_index]["roles"]["experiencer"] = labels["experiencer"]
                #result[index]["emotions"][emotion_index]["roles"]["target"] = labels["target"]
                #result[index]["emotions"][emotion_index]["roles"]["cause"] = labels["cause"]
    with open("SRL4E_emotweet.json", "w") as f:
        json.dump(result, f, sort_keys=True, indent=4)
