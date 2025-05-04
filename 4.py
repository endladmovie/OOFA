from github import Github

g = Github("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")  # Токен
repo = g.get_user().get_repo("OOFA")
path = "data.json"

with open("data_with_videos.json", "r", encoding="utf-8") as f:
    content = f.read()

try:
    file = repo.get_contents(path)
    repo.update_file(file.path, "Обновлён JSON", content, file.sha)
except:
    repo.create_file(path, "Создан JSON", content)
