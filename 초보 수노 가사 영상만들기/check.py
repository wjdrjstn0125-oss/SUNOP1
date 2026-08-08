lines = open(r'c:\Users\hp\초보10 태국\lyric-video.html', 'r', encoding='utf-8').read().split('\n')
with open('temp_lines2.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(f'{i}: {line}' for i, line in enumerate(lines[140:170], start=140)))
