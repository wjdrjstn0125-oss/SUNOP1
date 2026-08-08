import re

path = r'c:\Users\hp\초보10 태국\lyric-video.html'
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Fix the corrupted block
content = re.sub(
    r'<div class=""file-input-group"">\s*<label>6\. 화면 비율 및 해상도</label>.*?<label>5\. 화면 비율 및 해상도</label>',
    '<div class="file-input-group">\n        <label>6. 화면 비율 및 해상도</label>',
    content,
    flags=re.DOTALL
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
