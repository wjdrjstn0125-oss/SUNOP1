import re

path = r'c:\Users\hp\초보10 태국\lyric-video.html'
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

old_download_code = '''          // 다운로드 트리거
          const a = document.createElement('a');
          a.href = url;
          a.download = 'lyric_video_result.webm';
          a.click();'''

new_download_code = '''          // 다운로드 트리거 (노래 제목으로 파일명 지정)
          const a = document.createElement('a');
          a.href = url;
          let filename = 'lyric_video_result.webm';
          if (songTitleStr) {
              const cleanTitle = songTitleStr.replace(/[/\\\\:*?"<>|]/g, '_').trim();
              if (cleanTitle) filename = ${cleanTitle}.webm;
          }
          a.download = filename;
          a.click();'''

content = content.replace(old_download_code, new_download_code)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
