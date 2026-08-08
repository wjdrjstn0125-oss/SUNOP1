lines = open(r'c:\Users\hp\초보10 태국\lyric-video.html', 'r', encoding='utf-8').read().split('\n')
maxw_lines = [(i+1, l) for i, l in enumerate(lines) if 'maxW' in l]
print("--- [1단계 정적 검증 결과] ---")
for line_no, content in maxw_lines:
    print(f"Line {line_no}: {content.strip()}")

# Verify top-level declaration in drawFrame
drawframe_start = next(i for i, l in enumerate(lines) if 'function drawFrame' in l)
drawframe_end = next(i for i, l in enumerate(lines[drawframe_start:], start=drawframe_start) if 'async function startRendering' in l)

drawframe_code = '\n'.join(lines[drawframe_start:drawframe_end])
if 'const maxW = lyricsW - (80 * scale);' in drawframe_code:
    print("\n✅ 검증 성공: maxW 변수가 drawFrame 최상단 스코프에 정상 배치되었습니다.")
else:
    print("\n❌ 검증 실패: maxW 변수 위치 오류")
