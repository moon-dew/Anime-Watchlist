import json
from mal import Anime

class CachedAnime():
    def __init__(self,
                 mal_id,
                 title,
                 episodes,
                 score,
                 image_url,
                 synopsis):
        self.mal_id = mal_id
        self.title = title
        self.episodes = episodes
        self.score = score
        self.image_url = image_url
        self.synopsis = synopsis


def get_cached_anime(mal_id):
    cache = json.load(open("cache.json"))
    if len(cache["Cache"]) > 0 and any(d["id"] == mal_id for d in cache["Cache"]):
        cache = next((item for item in cache["Cache"] if item["id"] == mal_id), None)
        title = cache["title"]
        episodes = cache["episodes"]
        score = cache["score"]
        image_url = cache["image_url"]
        synopsis = cache["description"]

        return CachedAnime(mal_id, title, episodes, score, image_url, synopsis)

    else:
        anime = Anime(mal_id)

        append_cache = {
            "id": mal_id,
            "title": anime.title,
            "episodes": anime.episodes,
            "score": anime.score,
            "image_url": anime.image_url,
            "description": anime.synopsis,
        }

        cache["Cache"].append(append_cache)
        json.dump(cache, open("cache.json", "w"), indent=4)
        return anime