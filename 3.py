import json
import requests
import xml.etree.ElementTree as ET
from tqdm import tqdm

VIDEO_EXTENSIONS = (".mp4", ".ogv", ".webm", ".mkv", ".avi", ".mpg")

def get_video_urls_from_xml(identifier):
    xml_url = f"https://archive.org/download/{identifier}/{identifier}_files.xml"
    try:
        r = requests.get(xml_url)
        if not r.ok:
            return None
        root = ET.fromstring(r.content)
        urls = []
        for file in root.findall("file"):
            name = file.attrib.get("name", "")
            if name.lower().endswith(VIDEO_EXTENSIONS):
                url = f"https://archive.org/download/{identifier}/{name}"
                urls.append(url)
        if not urls:
            return None
        return urls[0] if len(urls) == 1 else urls
    except Exception as e:
        print(f"[!] Ошибка XML для {identifier}: {e}")
        return None

# Загружаем JSON
with open("data_with_torrents.json", "r", encoding="utf-8") as f:
    films = json.load(f)

# Обновляем поле video с прогресс-баром
for film in tqdm(films, desc="📺 Обновляем видео", unit="фильм"):
    try:
        if "page" in film:
            identifier = film["page"].split("/")[-1]
            video = get_video_urls_from_xml(identifier)
            film["video"] = video
    except Exception as e:
        print(f"Ошибка в фильме {film.get('title')}: {e}")

# Сохраняем результат
with open("data_with_videos.json", "w", encoding="utf-8") as f:
    json.dump(films, f, indent=2, ensure_ascii=False)

print("✅ Видео-ссылки обновлены и сохранены в data_with_videos.json")
