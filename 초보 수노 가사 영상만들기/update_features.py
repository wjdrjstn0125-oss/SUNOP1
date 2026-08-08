import re

path = r'c:\Users\hp\초보10 태국\lyric-video.html'
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# 1. Font dropdown options inline font-family styling & onchange event
old_select = '''        <select id="fontFamily">
          <option value="'Malgun Gothic'">맑은 고딕 (기본)</option>
          <option value="'Noto Sans KR'">노토 산스 (깔끔하고 트렌디)</option>
          <option value="'Do Hyeon'">도현체 (레트로 감성)</option>
          <option value="'Jua'">주아체 (부드럽고 귀여운)</option>
          <option value="'Nanum Pen Script'">나눔 펜 스크립트 (손글씨)</option>
        </select>'''

new_select = '''        <select id="fontFamily" style="font-size: 15px; padding: 10px; font-family: 'Malgun Gothic', sans-serif;" onchange="this.style.fontFamily = this.value + ', sans-serif';">
          <option value="'Malgun Gothic'" style="font-family: 'Malgun Gothic', sans-serif; font-size: 16px;">맑은 고딕 (기본)</option>
          <option value="'Noto Sans KR'" style="font-family: 'Noto Sans KR', sans-serif; font-size: 16px;">노토 산스 (깔끔하고 트렌디)</option>
          <option value="'Do Hyeon'" style="font-family: 'Do Hyeon', sans-serif; font-size: 16px;">도현체 (레트로 감성)</option>
          <option value="'Jua'" style="font-family: 'Jua', sans-serif; font-size: 16px;">주아체 (부드럽고 귀여운)</option>
          <option value="'Nanum Pen Script'" style="font-family: 'Nanum Pen Script', cursive; font-size: 18px;">나눔 펜 스크립트 (손글씨)</option>
        </select>'''

content = content.replace(old_select, new_select)

# 2. Adjust startY in non-synced scroll mode so 3rd line / first lines are visible at t=0
old_starty = '        const startY = h;'
new_starty = '        // 시작 시 가사 상단(약 3번째 줄 위치)부터 보이도록 startY 상향 조정\n        const startY = lyricsYStart + (lyricsH * 0.35);'

content = content.replace(old_starty, new_starty)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
