<!DOCTYPE html>
<html lang="ko">
 <head>
  <meta charset="utf-8"/>
  <meta content="width=device-width,initial-scale=1" name="viewport"/>
  <title>Auto Lyric Video Maker - 브라우저 렌더러</title>
  <link href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%23111827'/%3E%3Cpath d='M42 13v27.5a8.5 8.5 0 1 1-5-7.7V20.2l-18 4.2v21.1a8.5 8.5 0 1 1-5-7.7V20l28-7z' fill='%23ffcf5a'/%3E%3Cpath d='M37 20.2 19 24.4v5.2l18-4.2z' fill='%2367e8f9' opacity='.92'/%3E%3C/svg%3E" rel="icon"/>
  <link href="suno-styles.css" rel="stylesheet"/>
  <link href="https://fonts.googleapis.com/css2?family=Do+Hyeon&family=Jua&family=Nanum+Pen+Script&family=Noto+Sans+KR:wght@400;700;900&display=swap" rel="stylesheet">
  <style>
    /* 웹 툴 전용 스타일 추가 */
    .file-input-group {
      margin-bottom: 20px;
      background: rgba(255, 255, 255, 0.03);
      padding: 15px;
      border-radius: 8px;
      border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .file-input-group label {
      display: block;
      margin-bottom: 10px;
      color: #ff8a3d;
      font-weight: 800;
      font-size: 14px;
    }
    input[type="file"] {
      padding: 10px;
      background: #0f1115;
      cursor: pointer;
    }
    .preview-container {
      width: 100%;
      background: #000;
      border-radius: 8px;
      overflow: hidden;
      aspect-ratio: 16 / 9;
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
      border: 1px solid rgba(255,255,255,0.1);
    }
    canvas {
      width: 100%;
      height: 100%;
      object-fit: contain;
    }
    .primary-btn {
      background: linear-gradient(135deg, #ff8a3d, #e56a1b);
      color: white;
      border: none;
      width: 100%;
      padding: 15px;
      font-size: 16px;
      border-radius: 8px;
      margin-top: 20px;
      transition: all 0.2s;
    }
    .primary-btn:hover {
      transform: translateY(-2px);
      box-shadow: 0 5px 15px rgba(255, 138, 61, 0.4);
      color: white;
    }
    .primary-btn:disabled {
      background: #333;
      color: #777;
      cursor: not-allowed;
      transform: none;
      box-shadow: none;
    }
    .status-panel {
      margin-top: 15px;
      padding: 12px;
      border-radius: 6px;
      background: rgba(57, 208, 200, 0.1);
      border: 1px solid rgba(57, 208, 200, 0.3);
      color: #7ee8dd;
      font-size: 14px;
      text-align: center;
      display: none;
    }
  </style>
 </head>
 <body>
  <header class="app-nav">
   <a class="app-home-chip" href="index.html">AI CONVENIENCE TOOLS</a>
   <nav aria-label="사이트 메뉴" class="app-nav-links">
    <a class="app-nav-btn" href="suno-maker.html">수노 커멘드 메이커</a>
    <a class="app-nav-btn" href="audio-master.html">오디오 배치 마스터</a>
    <a class="app-nav-btn" href="thumbnail-maker.html">썸네일 프롬프트 메이커</a>
    <a aria-current="page" class="app-nav-btn is-active" href="lyric-video.html">자동 자막 비디오</a>
   </nav>
  </header>
  
  <main class="app-shell">
   <section class="workspace">
    <!-- 왼쪽 제어 패널 -->
    <aside class="settings-panel">
      <div class="file-input-group">
        <label>1. 노래 제목 및 가수</label>
        <input type="text" id="songTitle" placeholder="예: My Awesome Song - Suno" style="width: 100%; border-radius: 4px; border: 1px solid rgba(255,255,255,0.1); padding: 10px; background: #0f1115; color: white;">
      </div>

      <div class="file-input-group">
        <label>2. 가사 및 제목 글꼴 (폰트)</label>
        <select id="fontFamily">
          <option value="'Malgun Gothic'">맑은 고딕 (기본)</option>
          <option value="'Noto Sans KR'">노토 산스 (깔끔하고 트렌디)</option>
          <option value="'Do Hyeon'">도현체 (레트로 감성)</option>
          <option value="'Jua'">주아체 (부드럽고 귀여운)</option>
          <option value="'Nanum Pen Script'">나눔 펜 스크립트 (손글씨)</option>
        </select>
      </div>

      <div class="file-input-group">
        <label>3. 앨범 커버 이미지 (JPG/PNG)</label>
        <input type="file" id="coverInput" accept="image/jpeg, image/png">
      </div>

      <div class="file-input-group">
        <label>4. 노래 파일 (MP3/WAV)</label>
        <input type="file" id="audioInput" accept="audio/mpeg, audio/wav">
      </div>

      <div class="file-input-group">
        <label>5. 가사 자막 설정 (선택사항)</label>
        <select id="subtitleMode" onchange="toggleSubtitleInput()">
          <option value="srt">SRT 파일 업로드 (정확한 씽크)</option>
          <option value="text">가사 텍스트 직접 입력 (자동 스크롤)</option>
        </select>
        
        <div id="srtInputWrap" style="margin-top: 10px;">
          <input type="file" id="srtInput" accept=".srt">
        </div>
        
        <div id="textInputWrap" style="display: none; margin-top: 10px;">
          <div style="color: #ff5252; font-size: 12px; margin-bottom: 8px; line-height: 1.4;">
            ※ 주의: 텍스트 모드는 음악 박자에 싱크를 맞출 수 없으며 일정한 속도로만 스크롤됩니다. <b>현재 부르는 가사를 화면 중앙에 오게 하려면 반드시 위에서 SRT 방식을 선택하세요!</b>
          </div>
          <textarea id="rawLyrics" placeholder="여기에 가사를 붙여넣으세요. 빈 줄 단위로 단락이 나뉩니다."></textarea>
        </div>
      </div>

      <div class="file-input-group">
        <label>6. 화면 비율 및 해상도</label>
        <select id="aspectRatio">
          <option value="1k_16:9">1K (FHD) 가로형 - 1920x1080</option>
          <option value="1k_9:16">1K (FHD) 세로형 - 1080x1920</option>
          <option value="2k_16:9">2K (QHD) 가로형 - 2560x1440</option>
          <option value="2k_9:16">2K (QHD) 세로형 - 1440x2560</option>
          <option value="4k_16:9">4K (UHD) 가로형 - 3840x2160</option>
          <option value="4k_9:16">4K (UHD) 세로형 - 2160x3840</option>
        </select>
      </div>

      <button id="renderBtn" class="primary-btn" onclick="startRendering()">영상 렌더링 시작</button>
      
      <div id="statusPanel" class="status-panel">
        준비 중...
      </div>
      
    </aside>
    
    <!-- 오른쪽 프리뷰 영역 -->
    <section class="output-panel">
      <div class="output-toolbar">
        <h2>실시간 렌더링 화면</h2>
        <p>영상이 재생되는 동안 백그라운드에서 고음질로 녹화됩니다.</p>
      </div>
      <div class="preview-container" id="previewContainer">
        <canvas id="renderCanvas" width="1920" height="1080"></canvas>
      </div>
      
      <div style="margin-top: 20px; font-size: 13px; color: #a3a8b2; line-height: 1.6;">
        <h3 style="color:#f5c45e; margin-bottom: 5px;">💡 안내사항</h3>
        - 영상 렌더링은 음악 길이만큼 실시간으로 진행됩니다.<br>
        - 녹화 중에는 다른 탭으로 이동하지 마세요. (브라우저 정책상 렌더링이 멈출 수 있습니다.)<br>
        - 작업이 완료되면 고화질(webm) 영상 파일이 자동으로 다운로드됩니다.
      </div>
    </section>
    
   </section>
  </main>

  <script>
    // --- UI 로직 ---
    function toggleSubtitleInput() {
      const mode = document.getElementById('subtitleMode').value;
      if (mode === 'srt') {
        document.getElementById('srtInputWrap').style.display = 'block';
        document.getElementById('textInputWrap').style.display = 'none';
      } else {
        document.getElementById('srtInputWrap').style.display = 'none';
        document.getElementById('textInputWrap').style.display = 'block';
      }
    }

    document.getElementById('aspectRatio').addEventListener('change', function(e) {
      const cvs = document.getElementById('renderCanvas');
      const container = document.getElementById('previewContainer');
      const val = e.target.value;
      
      if (val.includes('16:9')) {
        container.style.aspectRatio = '16 / 9';
      } else {
        container.style.aspectRatio = '9 / 16';
      }
      
      if (val === '1k_16:9') { cvs.width = 1920; cvs.height = 1080; }
      else if (val === '1k_9:16') { cvs.width = 1080; cvs.height = 1920; }
      else if (val === '2k_16:9') { cvs.width = 2560; cvs.height = 1440; }
      else if (val === '2k_9:16') { cvs.width = 1440; cvs.height = 2560; }
      else if (val === '4k_16:9') { cvs.width = 3840; cvs.height = 2160; }
      else if (val === '4k_9:16') { cvs.width = 2160; cvs.height = 3840; }
    });

    // --- 렌더링 핵심 로직 ---
    let audioElement = null;
    let coverImageObj = null;
    let lyricsData = [];
    let isSynced = false;
    let mediaRecorder = null;
    let recordedChunks = [];
    let animationId = null;

    // SRT 파서 (단순화된 버전)
    function parseSRT(data) {
      const pattern = /(\d+)\n([\d:,]+)\s+-->\s+([\d:,]+)\n([\s\S]*?(?=\n\n\d+|$))/g;
      const result = [];
      let match;

      function timeToSec(timeString) {
        const parts = timeString.replace(',', '.').split(':');
        return parseFloat(parts[0]) * 3600 + parseFloat(parts[1]) * 60 + parseFloat(parts[2]);
      }

      while ((match = pattern.exec(data)) !== null) {
        const cleanText = match[4].replace(/\[.*?\]/g, '').replace(/^\s*[\r\n]/gm, '').trim();
        if (cleanText) {
          result.push({
            start: timeToSec(match[2]),
            end: timeToSec(match[3]),
            text: cleanText
          });
        }
      }
      return result;
    }

    // 파일 로드 헬퍼
    const readFileAsText = (file) => new Promise(r => {
      const reader = new FileReader();
      reader.onload = e => r(e.target.result);
      reader.readAsText(file);
    });

    const loadImage = (url) => new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => resolve(img);
      img.onerror = reject;
      img.src = url;
    });

    // 스마트 줄바꿈 알고리즘 (1안/2안 통합)
    function smartBalanceWrap(text, ctx, maxW, scale) {
        if (!text.trim()) return [];
        const fullWidth = ctx.measureText(text).width;
        
        // 1. 여유로울 때: 그대로 반환
        if (fullWidth <= maxW) {
            return [{ text: text, w: fullWidth, compress: false, h: 45 * scale }];
        }
        
        // 2. 약간 초과할 때 (약 15% 이내) -> 압축 (2안)
        if (fullWidth <= maxW * 1.15) {
            return [{ text: text, w: maxW, compress: true, h: 45 * scale }];
        }
        
        // 3. 많이 초과할 때 -> 2줄 분할 (1안)
        const words = text.split(' ');
        if (words.length <= 1) {
            return [{ text: text, w: maxW, compress: true, h: 45 * scale }]; // 띄어쓰기 없으면 무조건 압축
        }
        
        // 의미(띄어쓰기) 단위로 분할하되, 위아래 길이가 가장 균등해지는 중앙점 찾기
        let bestDiff = Infinity;
        let bestSplitIndex = 1;
        for (let i = 1; i < words.length; i++) {
            const left = words.slice(0, i).join(' ');
            const right = words.slice(i).join(' ');
            const diff = Math.abs(ctx.measureText(left).width - ctx.measureText(right).width);
            if (diff < bestDiff) {
                bestDiff = diff;
                bestSplitIndex = i;
            }
        }
        
        const line1 = words.slice(0, bestSplitIndex).join(' ');
        const line2 = words.slice(bestSplitIndex).join(' ');
        
        const w1 = ctx.measureText(line1).width;
        const w2 = ctx.measureText(line2).width;
        
        return [
            { text: line1, w: Math.min(w1, maxW), compress: w1 > maxW, h: 45 * scale },
            { text: line2, w: Math.min(w2, maxW), compress: w2 > maxW, h: 45 * scale }
        ];
    }

    // 캔버스 드로잉 (파이썬 로직 이식)
    function drawFrame(ctx, w, h, time, duration, isVertical, songTitleStr = '', fontFamily = "'Malgun Gothic'") {
      const scale = Math.max(w, h) / 1920;
      
      // 배경 (블랙)
      ctx.fillStyle = '#000000';
      ctx.fillRect(0, 0, w, h);
      
      // 레이아웃 분할
      let leftW = isVertical ? w : w / 2;
      let topH = isVertical ? h / 2 : h;
      let lyricsX = isVertical ? 0 : w / 2;
      let lyricsYStart = isVertical ? topH : 0;
      let lyricsW = isVertical ? w : w / 2;
      let lyricsH = isVertical ? h / 2 : h;
      
      // 커버 이미지 그리기
      if (coverImageObj) {
        ctx.save();
        
        // 선명한 앨범 커버 (중앙)
        ctx.filter = 'none';
        const coverMargin = isVertical ? 150 : 200;
        const coverSize = Math.min(leftW, topH) - (coverMargin * scale);
        
        // 정방형 크롭
        let sSize = Math.min(coverImageObj.width, coverImageObj.height);
        let sx = (coverImageObj.width - sSize) / 2;
        let sy = (coverImageObj.height - sSize) / 2;
        
        const coverX = (leftW - coverSize) / 2;
        const coverY = (topH - coverSize) / 2;
        ctx.drawImage(coverImageObj, sx, sy, sSize, sSize, coverX, coverY, coverSize, coverSize);
        ctx.restore();
      }
      
      // 자막 렌더링
      if (!lyricsData.length) return;
      
      const fontSize = (isVertical ? 40 : 45) * scale;
      ctx.font = `bold ${fontSize}px ${fontFamily}, sans-serif`;
      ctx.textBaseline = 'top';
      const lineSpacing = 35 * scale; // 겹침 방지를 위해 간격을 20->35로 넉넉하게 확장
      const blockSpacing = 60 * scale;
      
      // 각 블록의 크기 계산 (자동 줄바꿈 적용 캐싱)
      lyricsData.forEach(item => {
        if (!item.parsedLines) {
           item.parsedLines = [];
           const maxW = lyricsW - (80 * scale); // 텍스트 최대 허용 폭 (좌우 여백)
           const paragraphs = item.text.split('\n');
           
           paragraphs.forEach(pText => {
               const lines = smartBalanceWrap(pText, ctx, maxW, scale);
               item.parsedLines.push(...lines);
           });
           
           if (item.parsedLines.length > 0) {
               item.hTotal = item.parsedLines.reduce((sum, l) => sum + l.h + lineSpacing, 0) - lineSpacing;
           } else {
               item.hTotal = 0;
           }
        }
      });
      
      const getCenterY = (idx) => {
        let y = 0;
        for (let i = 0; i < idx; i++) y += lyricsData[i].hTotal + blockSpacing;
        return y + lyricsData[idx].hTotal / 2;
      };

      let currentY = 0;
      let targetCenterY = 0;
      let activeIdx = -1;
      
      if (isSynced) {
        // 싱크 모드
        for (let i = 0; i < lyricsData.length; i++) {
          if (time >= lyricsData[i].start) activeIdx = i;
          else break;
        }
        activeIdx = Math.max(0, activeIdx);
        targetCenterY = getCenterY(activeIdx);
        
        // 스무스 트랜지션
        if (activeIdx + 1 < lyricsData.length) {
          const nextItem = lyricsData[activeIdx + 1];
          const transDur = 0.5;
          const timeToNext = nextItem.start - time;
          if (timeToNext >= 0 && timeToNext < transDur) {
             let p = 1.0 - (timeToNext / transDur);
             p = p * p * (3 - 2 * p);
             const nextY = getCenterY(activeIdx + 1);
             targetCenterY += (nextY - targetCenterY) * p;
          }
        }
        
        const scrollOffset = (lyricsH / 2) - targetCenterY;
        currentY = lyricsYStart + scrollOffset;
        
      } else {
        // 비동기 스크롤 모드
        const totalH = lyricsData.reduce((sum, item) => sum + item.hTotal + blockSpacing, 0);
        const startY = h;
        const endY = lyricsYStart - totalH - 100;
        const scrollDur = duration * 0.9;
        
        let p = time / scrollDur;
        if (p > 1) p = 1;
        currentY = startY + (endY - startY) * p;
      }
      
      // 텍스트 드로잉 및 클리핑 영역 설정 (위아래 2줄 가림 효과)
      ctx.save();
      ctx.beginPath();
      ctx.rect(lyricsX, lyricsYStart, lyricsW, lyricsH);
      ctx.clip();

      lyricsData.forEach((item, i) => {
        const isActive = (i === activeIdx);
        const blockH = item.hTotal;
        
        // 화면 밖 클리핑
        if (currentY + blockH < lyricsYStart || currentY > lyricsYStart + lyricsH) {
          currentY += blockH + blockSpacing;
          return;
        }
        
        if (isActive && isSynced) {
          // 하이라이트 박스
          ctx.fillStyle = 'rgba(60, 60, 60, 0.8)';
          const padX = 40 * scale, padY = 20 * scale;
          const radius = 20 * scale;
          ctx.beginPath();
          ctx.roundRect(lyricsX + padX, currentY - padY, lyricsW - padX*2, blockH + padY*2, radius);
          ctx.fill();
        }
        
        let itemY = currentY;
        item.parsedLines.forEach(line => {
           ctx.fillStyle = (isActive || !isSynced) ? '#ffffff' : 'rgba(130, 130, 130, 1)';
           // 캔버스 자체 중앙 정렬 기능 사용 (수동 X좌표 계산 오류 원천 차단)
           ctx.textAlign = 'center';
           const lineX = lyricsX + lyricsW / 2;
           
           if (line.compress) {
               // 2안: 가로폭 압축 렌더링
               ctx.fillText(line.text, lineX, itemY, maxW);
           } else {
               ctx.fillText(line.text, lineX, itemY);
           }
           
           itemY += line.h + lineSpacing;
        });
        
        currentY += blockH + blockSpacing;
      });

      // 상/하단 스무스 페이드 아웃 (블랙 그라데이션) - 약 2.5줄 높이
      const fadeH = 150 * scale;
      
      const topGrad = ctx.createLinearGradient(0, lyricsYStart, 0, lyricsYStart + fadeH);
      topGrad.addColorStop(0, 'rgba(0,0,0,1)');
      topGrad.addColorStop(1, 'rgba(0,0,0,0)');
      ctx.fillStyle = topGrad;
      ctx.fillRect(lyricsX, lyricsYStart, lyricsW, fadeH);

      const bottomGrad = ctx.createLinearGradient(0, lyricsYStart + lyricsH, 0, lyricsYStart + lyricsH - fadeH);
      bottomGrad.addColorStop(0, 'rgba(0,0,0,1)');
      bottomGrad.addColorStop(1, 'rgba(0,0,0,0)');
      ctx.fillStyle = bottomGrad;
      ctx.fillRect(lyricsX, lyricsYStart + lyricsH - fadeH, lyricsW, fadeH);
      
      ctx.restore(); // 클리핑 해제
      
      // 타이틀 오프닝 효과 (첫 5초)
      if (songTitleStr && time < 5) {
        ctx.save();
        let alpha = 1.0;
        if (time < 1) alpha = time;
        else if (time > 4) alpha = 1.0 - (time - 4);
        
        ctx.globalAlpha = alpha;
        ctx.fillStyle = '#f5c45e';
        const titleFont = (isVertical ? 50 : 60) * scale;
        ctx.font = `900 ${titleFont}px ${fontFamily}, sans-serif`;
        ctx.textBaseline = 'middle';
        ctx.textAlign = 'center';
        
        const titleX = lyricsX + lyricsW / 2;
        let titleY = lyricsYStart + lyricsH / 3;
        
        // 그림자 효과로 가독성 향상
        ctx.shadowColor = 'rgba(0,0,0,0.9)';
        ctx.shadowBlur = 15 * scale;
        ctx.shadowOffsetX = 2 * scale;
        ctx.shadowOffsetY = 2 * scale;
        
        // 제목에도 1안/2안(스마트 줄바꿈) 적용
        const maxTitleW = lyricsW * 0.85;
        const titleLines = smartBalanceWrap(songTitleStr, ctx, maxTitleW, scale);
        
        const titleLineSpacing = 20 * scale;
        const totalTitleH = titleLines.length * titleFont + Math.max(0, titleLines.length - 1) * titleLineSpacing;
        titleY -= totalTitleH / 4; // 다중 줄일 때 중앙 보정
        
        titleLines.forEach(tLine => {
            if (tLine.compress) {
                ctx.fillText(tLine.text, titleX, titleY, maxTitleW);
            } else {
                ctx.fillText(tLine.text, titleX, titleY);
            }
            titleY += titleFont + titleLineSpacing;
        });
        
        ctx.restore();
      }
    }

    async function startRendering() {
      const coverFile = document.getElementById('coverInput').files[0];
      const audioFile = document.getElementById('audioInput').files[0];
      const statusPanel = document.getElementById('statusPanel');
      const renderBtn = document.getElementById('renderBtn');
      
      if (!coverFile || !audioFile) {
        alert('커버 이미지와 노래 파일을 모두 업로드해주세요!');
        return;
      }
      
      renderBtn.disabled = true;
      statusPanel.style.display = 'block';
      statusPanel.innerText = '재료 준비 중...';
      
      try {
        // 1. 이미지 로드
        coverImageObj = await loadImage(URL.createObjectURL(coverFile));
        
        // 2. 가사 준비
        const mode = document.getElementById('subtitleMode').value;
        lyricsData = [];
        if (mode === 'srt') {
          const srtFile = document.getElementById('srtInput').files[0];
          if (srtFile) {
            const srtText = await readFileAsText(srtFile);
            lyricsData = parseSRT(srtText);
            isSynced = true;
          }
        } else {
          const rawText = document.getElementById('rawLyrics').value;
          const paragraphs = rawText.split('\n\n').filter(p => p.trim());
          lyricsData = paragraphs.map(p => ({ 
            text: p.replace(/\[.*?\]/g, '').replace(/^\s*[\r\n]/gm, '').trim() 
          })).filter(p => p.text);
          isSynced = false;
        }
        
        // 3. 오디오 셋업
        if (audioElement) {
          audioElement.pause();
          audioElement.src = '';
        }
        audioElement = new Audio(URL.createObjectURL(audioFile));
        
        await new Promise(r => {
          audioElement.onloadedmetadata = r;
          // 모바일 대응 등 버퍼링을 위해 약간 대기
        });
        
        const duration = audioElement.duration;
        const cvs = document.getElementById('renderCanvas');
        const ctx = cvs.getContext('2d');
        const val = document.getElementById('aspectRatio').value;
        const isVertical = val.includes('9:16');
        
        let songTitleInput = document.getElementById('songTitle');
        const songTitleStr = songTitleInput ? songTitleInput.value.trim() : '';
        const fontFamily = document.getElementById('fontFamily') ? document.getElementById('fontFamily').value : "'Malgun Gothic'";
        
        // 폰트 로딩 완전 대기 (웹 폰트 적용 시 캔버스 공백 방지)
        if (document.fonts && document.fonts.ready) {
            await document.fonts.ready;
        }
        
        // 4. MediaRecorder 셋업 (고품질 녹화)
        // 화면 스트림 30fps
        const canvasStream = cvs.captureStream(30);
        
        // 오디오 스트림 추출 (Web Audio API)
        const audioCtx = new AudioContext();
        const dest = audioCtx.createMediaStreamDestination();
        const source = audioCtx.createMediaElementSource(audioElement);
        source.connect(dest);
        source.connect(audioCtx.destination); // 스피커로도 출력
        
        // 두 스트림 병합
        const combinedStream = new MediaStream([
          ...canvasStream.getVideoTracks(),
          ...dest.stream.getAudioTracks()
        ]);
        
        // 비트레이트 설정 (고화질, 고음질 보장)
        let videoBitrate = 8000000; // 8Mbps (1k)
        if (val.includes('2k')) videoBitrate = 16000000; // 16Mbps
        if (val.includes('4k')) videoBitrate = 35000000; // 35Mbps
        
        const options = { 
          mimeType: 'video/webm;codecs=vp9,opus',
          videoBitsPerSecond: videoBitrate,
          audioBitsPerSecond: 320000   // 320kbps
        };
        
        try {
          mediaRecorder = new MediaRecorder(combinedStream, options);
        } catch (e) {
          // vp9 지원 안하는 브라우저 롤백
          mediaRecorder = new MediaRecorder(combinedStream); 
        }
        
        recordedChunks = [];
        mediaRecorder.ondataavailable = e => {
          if (e.data.size > 0) recordedChunks.push(e.data);
        };
        
        mediaRecorder.onstop = () => {
          cancelAnimationFrame(animationId);
          const blob = new Blob(recordedChunks, { type: 'video/webm' });
          const url = URL.createObjectURL(blob);
          
          // 다운로드 트리거
          const a = document.createElement('a');
          a.href = url;
          a.download = 'lyric_video_result.webm';
          a.click();
          
          statusPanel.innerText = '렌더링 완료 및 다운로드 시작!';
          renderBtn.disabled = false;
        };
        
        // 5. 렌더링 시작
        statusPanel.innerText = `녹화 진행 중... 음악이 끝날 때까지 기다려주세요.`;
        
        // 애니메이션 루프
        function loop() {
           const time = audioElement.currentTime;
           drawFrame(ctx, cvs.width, cvs.height, time, duration, isVertical, songTitleStr, fontFamily);
           
           if (!audioElement.ended) {
             animationId = requestAnimationFrame(loop);
           } else {
             mediaRecorder.stop();
           }
        }
        
        mediaRecorder.start();
        audioElement.play();
        loop();

      } catch (err) {
        console.error(err);
        alert('렌더링 준비 중 오류가 발생했습니다: ' + err.message);
        renderBtn.disabled = false;
        statusPanel.style.display = 'none';
      }
    }
  </script>
 </body>
</html>
