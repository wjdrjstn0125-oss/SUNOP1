400:              let p = 1.0 - (timeToNext / transDur);
401:              p = p * p * (3 - 2 * p);
402:              const nextY = getCenterY(activeIdx + 1);
403:              targetCenterY += (nextY - targetCenterY) * p;
404:           }
405:         }
406:         
407:         const scrollOffset = (lyricsH / 2) - targetCenterY;
408:         currentY = lyricsYStart + scrollOffset;
409:         
410:       } else {
411:         // 비동기 스크롤 모드
412:         const totalH = lyricsData.reduce((sum, item) => sum + item.hTotal + blockSpacing, 0);
413:         const startY = h;
414:         const endY = lyricsYStart - totalH - 100;
415:         const scrollDur = duration * 0.9;
416:         
417:         let p = time / scrollDur;
418:         if (p > 1) p = 1;
419:         currentY = startY + (endY - startY) * p;
420:       }
421:       
422:       // 텍스트 드로잉 및 클리핑 영역 설정 (위아래 2줄 가림 효과)
423:       ctx.save();
424:       ctx.beginPath();
425:       ctx.rect(lyricsX, lyricsYStart, lyricsW, lyricsH);
426:       ctx.clip();
427: 
428:       lyricsData.forEach((item, i) => {
429:         const isActive = (i === activeIdx);
430:         const blockH = item.hTotal;
431:         
432:         // 화면 밖 클리핑
433:         if (currentY + blockH < lyricsYStart || currentY > lyricsYStart + lyricsH) {
434:           currentY += blockH + blockSpacing;
435:           return;
436:         }
437:         
438:         if (isActive && isSynced) {
439:           // 하이라이트 박스
440:           ctx.fillStyle = 'rgba(60, 60, 60, 0.8)';
441:           const padX = 40 * scale, padY = 20 * scale;
442:           const radius = 20 * scale;
443:           ctx.beginPath();
444:           ctx.roundRect(lyricsX + padX, currentY - padY, lyricsW - padX*2, blockH + padY*2, radius);
445:           ctx.fill();
446:         }
447:         
448:         let itemY = currentY;
449:         item.parsedLines.forEach(line => {
450:            ctx.fillStyle = (isActive || !isSynced) ? '#ffffff' : 'rgba(130, 130, 130, 1)';
451:            // 캔버스 자체 중앙 정렬 기능 사용 (수동 X좌표 계산 오류 원천 차단)
452:            ctx.textAlign = 'center';
453:            const lineX = lyricsX + lyricsW / 2;
454:            
455:            if (line.compress) {
456:                // 2안: 가로폭 압축 렌더링
457:                ctx.fillText(line.text, lineX, itemY, maxW);
458:            } else {
459:                ctx.fillText(line.text, lineX, itemY);
460:            }
461:            
462:            itemY += line.h + lineSpacing;
463:         });
464:         
465:         currentY += blockH + blockSpacing;
466:       });
467: 
468:       // 상/하단 스무스 페이드 아웃 (블랙 그라데이션) - 약 2.5줄 높이
469:       const fadeH = 150 * scale;
470:       
471:       const topGrad = ctx.createLinearGradient(0, lyricsYStart, 0, lyricsYStart + fadeH);
472:       topGrad.addColorStop(0, 'rgba(0,0,0,1)');
473:       topGrad.addColorStop(1, 'rgba(0,0,0,0)');
474:       ctx.fillStyle = topGrad;
475:       ctx.fillRect(lyricsX, lyricsYStart, lyricsW, fadeH);
476: 
477:       const bottomGrad = ctx.createLinearGradient(0, lyricsYStart + lyricsH, 0, lyricsYStart + lyricsH - fadeH);
478:       bottomGrad.addColorStop(0, 'rgba(0,0,0,1)');
479:       bottomGrad.addColorStop(1, 'rgba(0,0,0,0)');
480:       ctx.fillStyle = bottomGrad;
481:       ctx.fillRect(lyricsX, lyricsYStart + lyricsH - fadeH, lyricsW, fadeH);
482:       
483:       ctx.restore(); // 클리핑 해제
484:       
485:       // 타이틀 오프닝 효과 (첫 5초)
486:       if (songTitleStr && time < 5) {
487:         ctx.save();
488:         let alpha = 1.0;
489:         if (time < 1) alpha = time;
490:         else if (time > 4) alpha = 1.0 - (time - 4);
491:         
492:         ctx.globalAlpha = alpha;
493:         ctx.fillStyle = '#f5c45e';
494:         const titleFont = (isVertical ? 50 : 60) * scale;
495:         ctx.font = `900 ${titleFont}px ${fontFamily}, sans-serif`;
496:         ctx.textBaseline = 'middle';
497:         ctx.textAlign = 'center';
498:         
499:         const titleX = lyricsX + lyricsW / 2;
500:         let titleY = lyricsYStart + lyricsH / 3;
501:         
502:         // 그림자 효과로 가독성 향상
503:         ctx.shadowColor = 'rgba(0,0,0,0.9)';
504:         ctx.shadowBlur = 15 * scale;
505:         ctx.shadowOffsetX = 2 * scale;
506:         ctx.shadowOffsetY = 2 * scale;
507:         
508:         // 제목에도 1안/2안(스마트 줄바꿈) 적용
509:         const maxTitleW = lyricsW * 0.85;
510:         const titleLines = smartBalanceWrap(songTitleStr, ctx, maxTitleW, scale);
511:         
512:         const titleLineSpacing = 20 * scale;
513:         const totalTitleH = titleLines.length * titleFont + Math.max(0, titleLines.length - 1) * titleLineSpacing;
514:         titleY -= totalTitleH / 4; // 다중 줄일 때 중앙 보정
515:         
516:         titleLines.forEach(tLine => {
517:             if (tLine.compress) {
518:                 ctx.fillText(tLine.text, titleX, titleY, maxTitleW);
519:             } else {
520:                 ctx.fillText(tLine.text, titleX, titleY);
521:             }
522:             titleY += titleFont + titleLineSpacing;
523:         });
524:         
525:         ctx.restore();
526:       }
527:     }
528: 
529:     async function startRendering() {
530:       const coverFile = document.getElementById('coverInput').files[0];
531:       const audioFile = document.getElementById('audioInput').files[0];
532:       const statusPanel = document.getElementById('statusPanel');
533:       const renderBtn = document.getElementById('renderBtn');
534:       
535:       if (!coverFile || !audioFile) {
536:         alert('커버 이미지와 노래 파일을 모두 업로드해주세요!');
537:         return;
538:       }
539:       
540:       renderBtn.disabled = true;
541:       statusPanel.style.display = 'block';
542:       statusPanel.innerText = '재료 준비 중...';
543:       
544:       try {
545:         // 1. 이미지 로드
546:         coverImageObj = await loadImage(URL.createObjectURL(coverFile));
547:         
548:         // 2. 가사 준비
549:         const mode = document.getElementById('subtitleMode').value;
550:         lyricsData = [];
551:         if (mode === 'srt') {
552:           const srtFile = document.getElementById('srtInput').files[0];
553:           if (srtFile) {
554:             const srtText = await readFileAsText(srtFile);
555:             lyricsData = parseSRT(srtText);
556:             isSynced = true;
557:           }
558:         } else {
559:           const rawText = document.getElementById('rawLyrics').value;
560:           const paragraphs = rawText.split('\n\n').filter(p => p.trim());
561:           lyricsData = paragraphs.map(p => ({ 
562:             text: p.replace(/\[.*?\]/g, '').replace(/^\s*[\r\n]/gm, '').trim() 
563:           })).filter(p => p.text);
564:           isSynced = false;
565:         }
566:         
567:         // 3. 오디오 셋업
568:         if (audioElement) {
569:           audioElement.pause();
570:           audioElement.src = '';
571:         }
572:         audioElement = new Audio(URL.createObjectURL(audioFile));
573:         
574:         await new Promise(r => {
575:           audioElement.onloadedmetadata = r;
576:           // 모바일 대응 등 버퍼링을 위해 약간 대기
577:         });
578:         
579:         const duration = audioElement.duration;
580:         const cvs = document.getElementById('renderCanvas');
581:         const ctx = cvs.getContext('2d');
582:         const val = document.getElementById('aspectRatio').value;
583:         const isVertical = val.includes('9:16');
584:         
585:         let songTitleInput = document.getElementById('songTitle');
586:         const songTitleStr = songTitleInput ? songTitleInput.value.trim() : '';
587:         const fontFamily = document.getElementById('fontFamily') ? document.getElementById('fontFamily').value : "'Malgun Gothic'";
588:         
589:         // 폰트 로딩 완전 대기 (웹 폰트 적용 시 캔버스 공백 방지)
590:         if (document.fonts && document.fonts.ready) {
591:             await document.fonts.ready;
592:         }
593:         
594:         // 4. MediaRecorder 셋업 (고품질 녹화)
595:         // 화면 스트림 30fps
596:         const canvasStream = cvs.captureStream(30);
597:         
598:         // 오디오 스트림 추출 (Web Audio API)
599:         const audioCtx = new AudioContext();