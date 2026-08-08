lyricsH = 1080
scale = 1.0
lyricsYStart = 0
totalH = 1500
lastItemH = 100
duration = 180 # 3 mins

# startY: bottom minus 220px (shows ~3 lines at bottom)
startY = lyricsYStart + lyricsH - (220 * scale)

# endY: last line top is at center of screen (540px)
totalScrollDist = totalH - lastItemH
endY = (lyricsYStart + lyricsH / 2) - totalScrollDist

intro_delay = 4.0 # holding for first 4 seconds during title intro

print(f"--- [로직 검증 파라미터] ---")
print(f"1. 시작 위치 (startY): {startY}px (화면 하단에서 220px 위, 첫 가사 3줄 노출)")
print(f"2. 종료 위치 (endY): {endY}px")
print(f"3. 0~4초 (타이틀 전주 구간): p = 0.0 (가사 고정, 타이틀 표출)")
print(f"4. 4초~끝 (가사 스크롤): p = (time - 4) / (duration - 4)")

# Test p at t=0, t=4, t=92, t=180
for t in [0, 4, 92, 180]:
    if t < intro_delay:
        p = 0.0
    else:
        p = (t - intro_delay) / (duration - intro_delay)
    currY = startY + (endY - startY) * p
    lastLineY = currY + totalScrollDist
    print(f"  [t={t:3d}s] p={p:.3f} | 첫줄Y={currY:.1f}px | 마지막줄Y={lastLineY:.1f}px")
