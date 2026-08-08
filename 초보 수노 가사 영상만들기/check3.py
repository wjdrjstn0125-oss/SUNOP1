import re
lines = open(r'c:\Users\hp\초보10 태국\lyric-video.html', 'r', encoding='utf-8').read().split('\n')
with open('temp_lines4.py', 'w', encoding='utf-8') as f:
    # Just grab lines 250 to 500 roughly where drawFrame might be
    f.write('\n'.join(f'{i}: {line}' for i, line in enumerate(lines[400:600], start=400)))
