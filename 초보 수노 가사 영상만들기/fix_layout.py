path = r'c:\Users\hp\초보10 태국\lyric-video.html'
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Remove the offending brand-row tag
content = content.replace('<div class="brand-row">\n             <div class="file-input-group">', '<div class="file-input-group">')
content = content.replace('<div class="brand-row">\n      <div class="file-input-group">', '<div class="file-input-group">')
content = content.replace('<div class="brand-row">', '')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
