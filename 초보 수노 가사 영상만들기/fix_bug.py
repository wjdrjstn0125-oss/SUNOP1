import re

path = r'c:\Users\hp\초보10 태국\lyric-video.html'
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# 1. Promote maxW scope to top of drawFrame & remove local block scope maxW
content = content.replace(
    'let lyricsH = isVertical ? h / 2 : h;',
    'let lyricsH = isVertical ? h / 2 : h;\n      const maxW = lyricsW - (80 * scale);'
)

content = content.replace(
    '           const maxW = lyricsW - (80 * scale); // 텍스트 최대 허용 폭 (좌우 여백)',
    '           // maxW는 drawFrame 최상단 스코프에서 사용'
)

# 2. Add try-catch block inside loop()
old_loop = '''        // 애니메이션 루프
        function loop() {
           const time = audioElement.currentTime;
           drawFrame(ctx, cvs.width, cvs.height, time, duration, isVertical, songTitleStr, fontFamily);
           
           if (!audioElement.ended) {
             animationId = requestAnimationFrame(loop);
           } else {
             mediaRecorder.stop();
           }
        }'''

new_loop = '''        // 애니메이션 루프 (강력한 예외 처리 적용)
        function loop() {
           try {
             const time = audioElement.currentTime;
             drawFrame(ctx, cvs.width, cvs.height, time, duration, isVertical, songTitleStr, fontFamily);
             
             if (!audioElement.ended) {
               animationId = requestAnimationFrame(loop);
             } else {
               mediaRecorder.stop();
             }
           } catch (err) {
             console.error("렌더링 중 오류 발생:", err);
             alert("렌더링 중 오류가 발생하여 안전하게 중단되었습니다: " + err.message);
             if (mediaRecorder && mediaRecorder.state !== 'inactive') mediaRecorder.stop();
             renderBtn.disabled = false;
             statusPanel.innerText = '렌더링 에러 발생!';
           }
        }'''

content = content.replace(old_loop, new_loop)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
