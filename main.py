import json
import os
import pickle

import sentence_mixing.sentence_mixer as sm

DIR = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(DIR, "config.json")
CACHE_PATH = os.path.join(DIR, ".cache")

try:
    os.mkdir(CACHE_PATH)
except FileExistsError:
    pass


def save(*args, name="save.pckl"):
    with open(os.path.join(CACHE_PATH, name), "wb") as f:
        pickle.dump(args, f)


def load(name="save.pckl"):
    with open(os.path.join(CACHE_PATH, name), "rb") as f:
        return pickle.load(f)


def hash_str(string):
    return sum(ord(c) for u in video_urls for c in u)


def hash_project(video_urls, seed):
    return sum(map(hash_str, video_urls)) + seed


def get_videos(video_urls, seed):
    f_name = f"{hash_project(video_urls, seed)}.pckl"

    videos = None
    try:
        return load(f_name)[0]
    except Exception:
        videos = sm.get_videos(video_urls, seed)
        save(videos, name=f_name)
        return videos


def serialize(combos, urls):
    v_index = {u: i for i, u in enumerate(urls)}
    data = [
        [
            {
                "s": round(p.start),
                "e": round(p.end),
                "v": v_index[p.word.sentence.video.url],
            }
            for p in c.get_audio_phonems()
        ]
        for c in combos
    ]
    return json.dumps(data)


if __name__ == "__main__":
    video_urls, seed = ["_ZZ8oyZUGn8"], 4
    sentence = "je vais te faire la tête au carré"

    sm.prepare_sm_config_file(CONFIG_PATH)
    videos = get_videos(video_urls, seed)
    available_combos = sm.process_sm(sentence, videos)

    print(serialize(available_combos, video_urls))
