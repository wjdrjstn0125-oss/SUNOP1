import os

content = """@echo off
echo =======================================================
echo [자동 리릭 비디오 메이커]
echo.
echo c:\\Users\\hp\\초보12 크롬 자막 폴더의 파일을 기반으로 영상을 만듭니다.
echo cover.jpg, song.mp3 파일이 모두 있는지 확인해 주세요!
echo =======================================================
echo.

cd /d "c:\\Users\\hp\\초보12 크롬 자막"
python auto_lyric_video.py

echo.
echo 작업이 끝났습니다. 창을 닫으려면 아무 키나 누르세요.
pause > nul
"""

desktop_path = r"C:\Users\hp\Desktop\자동 리릭 비디오 만들기.bat"
with open(desktop_path, "w", encoding="cp949") as f:
    f.write(content)

print("Batch file created successfully.")
