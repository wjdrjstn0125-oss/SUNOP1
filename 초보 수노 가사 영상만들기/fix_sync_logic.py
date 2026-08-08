import re

path = r'c:\Users\hp\초보10 태국\lyric-video.html'
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

old_scroll_code = '''      } else {
        // 비동기 스크롤 모드 (텍스트 직접 입력)
        const totalH = lyricsData.reduce((sum, item) => sum + item.hTotal + blockSpacing, 0);
        const lastItemH = lyricsData.length > 0 ? lyricsData[lyricsData.length - 1].hTotal : 0;
        
        // 시작 시 화면 하단 영역에 첫 가사 3줄 정도만 살짝 보이도록 startY 설정 (200px 여백)
        const startY = lyricsYStart + lyricsH - (200 * scale);
        
        // 종료 시 마지막 가사가 화면 정중앙에 위치하도록 endY 설정
        const totalScrollDist = totalH - lastItemH;
        const endY = (lyricsYStart + lyricsH / 2) - totalScrollDist;
        
        const scrollDur = duration;
        
        let p = time / scrollDur;
        if (p > 1) p = 1;
        currentY = startY + (endY - startY) * p;
      }'''

new_scroll_code = '''      } else {
        // 비동기 스크롤 모드 (정밀 싱크 계산)
        const totalH = lyricsData.reduce((sum, item) => sum + item.hTotal + blockSpacing, 0);
        const lastItemH = lyricsData.length > 0 ? lyricsData[lyricsData.length - 1].hTotal : 0;
        
        // 1. 시작 위치: 화면 하단에서 220px 위 (첫 가사 3줄만 살짝 노출)
        const startY = lyricsYStart + lyricsH - (220 * scale);
        
        // 2. 종료 위치: 노래 끝날 때 마지막 가사의 첫줄이 정확히 화면 정중앙(lyricsH/2)에 도착
        const totalScrollDist = totalH - lastItemH;
        const endY = (lyricsYStart + lyricsH / 2) - totalScrollDist;
        
        // 3. 타이틀 오프닝(첫 4초) 대기 로직 적용 -> 전주 동안 가사 움직임을 대기시켜 싱크 이탈 방지
        const introDelay = 4.0;
        let p = 0;
        if (time >= introDelay && duration > introDelay) {
            p = (time - introDelay) / (duration - introDelay);
        }
        if (p > 1) p = 1;
        currentY = startY + (endY - startY) * p;
      }'''

content = content.replace(old_scroll_code, new_scroll_code)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
