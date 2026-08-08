import re

path = r'c:\Users\hp\초보10 태국\lyric-video.html'
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# 1. Update parser logic for text mode
old_parser = '''        } else {
          const rawText = document.getElementById('rawLyrics').value;
          const paragraphs = rawText.split('\\n\\n').filter(p => p.trim());
          lyricsData = paragraphs.map(p => ({ 
            text: p.replace(/\\[.*?\\]/g, '').replace(/^\\s*[\\r\\n]/gm, '').trim() 
          })).filter(p => p.text);
          isSynced = false;
        }'''

new_parser = '''        } else {
          const rawText = document.getElementById('rawLyrics').value;
          const paragraphs = rawText.split('\\n\\n').filter(p => p.trim());
          lyricsData = paragraphs.map(p => {
             const cleanText = p.replace(/\\[.*?\\]/g, '').replace(/^\\s*[\\r\\n]/gm, '').trim();
             const hasTag = /\\[.*?\\]/.test(p);
             if (!cleanText && hasTag) {
                 return { text: '', isGap: true };
             }
             return { text: cleanText, isGap: false };
          }).filter(p => p.text || p.isGap);
          isSynced = false;
        }'''
content = content.replace(old_parser, new_parser)

# 2. Update hTotal calculation for isGap
old_hcalc = '''           if (item.parsedLines.length > 0) {
               item.hTotal = item.parsedLines.reduce((sum, l) => sum + l.h + lineSpacing, 0) - lineSpacing;
           } else {
               item.hTotal = 0;
           }'''

new_hcalc = '''           if (item.parsedLines.length > 0) {
               item.hTotal = item.parsedLines.reduce((sum, l) => sum + l.h + lineSpacing, 0) - lineSpacing;
           } else {
               item.hTotal = 0;
           }
           if (item.isGap) {
               item.hTotal = 150 * scale; // 간주 딜레이를 위한 강제 공백 높이 추가
           }'''
content = content.replace(old_hcalc, new_hcalc)

# 3. Update non-synced scroll calculation
old_scroll = '''      } else {
        // 비동기 스크롤 모드
        const totalH = lyricsData.reduce((sum, item) => sum + item.hTotal + blockSpacing, 0);
        const startY = h;
        const endY = lyricsYStart - totalH - 100;
        const scrollDur = duration * 0.9;
        
        let p = time / scrollDur;
        if (p > 1) p = 1;
        currentY = startY + (endY - startY) * p;
      }'''

new_scroll = '''      } else {
        // 비동기 스크롤 모드
        const totalH = lyricsData.reduce((sum, item) => sum + item.hTotal + blockSpacing, 0);
        const lastItemH = lyricsData.length > 0 ? lyricsData[lyricsData.length - 1].hTotal : 0;
        const totalScrollDist = totalH - lastItemH - blockSpacing;
        
        const startY = h;
        // 스크롤 종료 시 마지막 가사가 화면 정중앙에 오도록 수정
        const endY = (lyricsYStart + lyricsH / 2) - totalScrollDist;
        
        const scrollDur = duration; // 90% 제한 해제 (프리징 버그 원천 차단)
        
        let p = time / scrollDur;
        if (p > 1) p = 1;
        currentY = startY + (endY - startY) * p;
      }'''
content = content.replace(old_scroll, new_scroll)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
