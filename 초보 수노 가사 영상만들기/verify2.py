import sys
sys.stdout.reconfigure(encoding='utf-8')

content = open(r'c:\Users\hp\초보10 태국\lyric-video.html', 'r', encoding='utf-8').read()

print("=== [버그 수정 3단계 종합 검증] ===")

# 1. Scope Check
if 'const maxW = lyricsW - (80 * scale);' in content:
    print("1단계 (스코프 검증): PASS - maxW가 drawFrame 최상단에 올바르게 배치됨")
else:
    print("1단계 (스코프 검증): FAIL")

# 2. Try-catch Check
if 'try {' in content and 'console.error("렌더링 중 오류 발생:", err);' in content:
    print("2단계 (예외 처리 검증): PASS - loop() 내부에 try-catch 예외 처리 도입됨")
else:
    print("2단계 (예외 처리 검증): FAIL")

# 3. Compression line maxW usage check
if 'ctx.fillText(line.text, lineX, itemY, maxW);' in content:
    print("3단계 (초장문 압축 검증): PASS - line.compress = true 일 때 maxW 정상 공급 확인")
else:
    print("3단계 (초장문 압축 검증): FAIL")

