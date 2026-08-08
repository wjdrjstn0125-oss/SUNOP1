import re

path = r'c:\Users\hp\초보10 태국\lyric-video.html'
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

old_end_code = '''        // 2. 종료 위치: 노래 끝날 때 마지막 가사의 첫줄이 정확히 화면 정중앙(lyricsH/2)에 도착
        const totalScrollDist = totalH - lastItemH;
        const endY = (lyricsYStart + lyricsH / 2) - totalScrollDist;'''

new_end_code = '''        // 2. 종료 위치: 노래 끝날 때 마지막 가사가 화면 중앙보다 약 2줄 더 올라간 위치에 오도록 수정
        const totalScrollDist = totalH - lastItemH;
        const endY = (lyricsYStart + lyricsH / 2) - totalScrollDist - (150 * scale);'''

content = content.replace(old_end_code, new_end_code)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
