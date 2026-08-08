lyricsH = 1080
scale = 1.0
lyricsYStart = 0
totalH = 1500
lastItemH = 100
duration = 180 # 3 minutes

# Proposed new startY: bottom of screen minus 200px (shows ~3 lines of first block)
startY = lyricsYStart + lyricsH - (200 * scale)

# endY: last line in middle of screen
totalScrollDist = totalH - lastItemH
endY = (lyricsYStart + lyricsH / 2) - totalScrollDist

totalDistance = startY - endY
speed = totalDistance / duration

print(f"startY: {startY}px (First block starts near 880px, showing top ~3 lines)")
print(f"endY: {endY}px")
print(f"Total distance to travel: {totalDistance}px")
print(f"Scroll speed: {speed:.2f} pixels/sec ({speed*5:.1f} px every 5 sec)")
