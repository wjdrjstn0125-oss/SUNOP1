import re

path = r'c:\Users\hp\초보10 태국\lyric-video.html'
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

old_scroll_code = '''      } else {
        // 비동기 스크롤 모드
        const totalH = lyricsData.reduce((sum, item) => sum + item.hTotal + blockSpacing, 0);
        const lastItemH = lyricsData.length > 0 ? lyricsData[lyricsData.length - 1].hTotal : 0;
        const totalScrollDist = totalH - lastItemH - blockSpacing;
        
        // 시작 시 가사 상단(약 3번째 줄 위치)부터 보이도록 startY 상향 조정
        const startY = lyricsYStart + (lyricsH * 0.35);
        // 스크롤 종료 시 마지막 가사가 화면 정중앙에 오도록 수정
        const endY = (lyricsYStart + lyricsH / 2) - totalScrollDist;
        
        const scrollDur = duration; // 90% 제한 해제 (프리징 버그 원천 차단)
        
        let p = time / scrollDur;
        if (p > 1) p = 1;
        currentY = startY + (endY - startY) * p;
      }'''

new_scroll_code = '''      } else {
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

content = content.replace(old_scroll_code, new_scroll_code)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
