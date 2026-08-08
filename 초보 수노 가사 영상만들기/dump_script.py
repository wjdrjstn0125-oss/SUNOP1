301:         const w1 = ctx.measureText(line1).width;
302:         const w2 = ctx.measureText(line2).width;
303:         
304:         return [
305:             { text: line1, w: Math.min(w1, maxW), compress: w1 > maxW, h: 45 * scale },
306:             { text: line2, w: Math.min(w2, maxW), compress: w2 > maxW, h: 45 * scale }
307:         ];
308:     }
309: 
310:     // 캔버스 드로잉 (파이썬 로직 이식)
311:     function drawFrame(ctx, w, h, time, duration, isVertical, songTitleStr = '', fontFamily = "'Malgun Gothic'") {
312:       const scale = Math.max(w, h) / 1920;
313:       
314:       // 배경 (블랙)
315:       ctx.fillStyle = '#000000';
316:       ctx.fillRect(0, 0, w, h);
317:       
318:       // 레이아웃 분할
319:       let leftW = isVertical ? w : w / 2;
320:       let topH = isVertical ? h / 2 : h;
321:       let lyricsX = isVertical ? 0 : w / 2;
322:       let lyricsYStart = isVertical ? topH : 0;
323:       let lyricsW = isVertical ? w : w / 2;
324:       let lyricsH = isVertical ? h / 2 : h;
325:       
326:       // 커버 이미지 그리기
327:       if (coverImageObj) {
328:         ctx.save();
329:         
330:         // 선명한 앨범 커버 (중앙)
331:         ctx.filter = 'none';
332:         const coverMargin = isVertical ? 150 : 200;
333:         const coverSize = Math.min(leftW, topH) - (coverMargin * scale);
334:         
335:         // 정방형 크롭
336:         let sSize = Math.min(coverImageObj.width, coverImageObj.height);
337:         let sx = (coverImageObj.width - sSize) / 2;
338:         let sy = (coverImageObj.height - sSize) / 2;
339:         
340:         const coverX = (leftW - coverSize) / 2;
341:         const coverY = (topH - coverSize) / 2;
342:         ctx.drawImage(coverImageObj, sx, sy, sSize, sSize, coverX, coverY, coverSize, coverSize);
343:         ctx.restore();
344:       }
345:       
346:       // 자막 렌더링
347:       if (!lyricsData.length) return;
348:       
349:       const fontSize = (isVertical ? 40 : 45) * scale;
350:       ctx.font = `bold ${fontSize}px ${fontFamily}, sans-serif`;
351:       ctx.textBaseline = 'top';
352:       const lineSpacing = 35 * scale; // 겹침 방지를 위해 간격을 20->35로 넉넉하게 확장
353:       const blockSpacing = 60 * scale;
354:       
355:       // 각 블록의 크기 계산 (자동 줄바꿈 적용 캐싱)
356:       lyricsData.forEach(item => {
357:         if (!item.parsedLines) {
358:            item.parsedLines = [];
359:            const maxW = lyricsW - (80 * scale); // 텍스트 최대 허용 폭 (좌우 여백)
360:            const paragraphs = item.text.split('\n');
361:            
362:            paragraphs.forEach(pText => {
363:                const lines = smartBalanceWrap(pText, ctx, maxW, scale);
364:                item.parsedLines.push(...lines);
365:            });
366:            
367:            if (item.parsedLines.length > 0) {
368:                item.hTotal = item.parsedLines.reduce((sum, l) => sum + l.h + lineSpacing, 0) - lineSpacing;
369:            } else {
370:                item.hTotal = 0;
371:            }
372:            if (item.isGap) {
373:                item.hTotal = 150 * scale; // 간주 딜레이를 위한 강제 공백 높이 추가
374:            }
375:         }
376:       });
377:       
378:       const getCenterY = (idx) => {
379:         let y = 0;
380:         for (let i = 0; i < idx; i++) y += lyricsData[i].hTotal + blockSpacing;
381:         return y + lyricsData[idx].hTotal / 2;
382:       };
383: 
384:       let currentY = 0;
385:       let targetCenterY = 0;
386:       let activeIdx = -1;
387:       
388:       if (isSynced) {
389:         // 싱크 모드
390:         for (let i = 0; i < lyricsData.length; i++) {
391:           if (time >= lyricsData[i].start) activeIdx = i;
392:           else break;
393:         }
394:         activeIdx = Math.max(0, activeIdx);
395:         targetCenterY = getCenterY(activeIdx);
396:         
397:         // 스무스 트랜지션
398:         if (activeIdx + 1 < lyricsData.length) {
399:           const nextItem = lyricsData[activeIdx + 1];
400:           const transDur = 0.5;
401:           const timeToNext = nextItem.start - time;
402:           if (timeToNext >= 0 && timeToNext < transDur) {
403:              let p = 1.0 - (timeToNext / transDur);
404:              p = p * p * (3 - 2 * p);
405:              const nextY = getCenterY(activeIdx + 1);
406:              targetCenterY += (nextY - targetCenterY) * p;
407:           }
408:         }
409:         
410:         const scrollOffset = (lyricsH / 2) - targetCenterY;
411:         currentY = lyricsYStart + scrollOffset;
412:         
413:       } else {
414:         // 비동기 스크롤 모드
415:         const totalH = lyricsData.reduce((sum, item) => sum + item.hTotal + blockSpacing, 0);
416:         const lastItemH = lyricsData.length > 0 ? lyricsData[lyricsData.length - 1].hTotal : 0;
417:         const totalScrollDist = totalH - lastItemH - blockSpacing;
418:         
419:         const startY = h;
420:         // 스크롤 종료 시 마지막 가사가 화면 정중앙에 오도록 수정
421:         const endY = (lyricsYStart + lyricsH / 2) - totalScrollDist;
422:         
423:         const scrollDur = duration; // 90% 제한 해제 (프리징 버그 원천 차단)
424:         
425:         let p = time / scrollDur;
426:         if (p > 1) p = 1;
427:         currentY = startY + (endY - startY) * p;
428:       }
429:       
430:       // 텍스트 드로잉 및 클리핑 영역 설정 (위아래 2줄 가림 효과)
431:       ctx.save();
432:       ctx.beginPath();
433:       ctx.rect(lyricsX, lyricsYStart, lyricsW, lyricsH);
434:       ctx.clip();
435: 
436:       lyricsData.forEach((item, i) => {
437:         const isActive = (i === activeIdx);
438:         const blockH = item.hTotal;
439:         
440:         // 화면 밖 클리핑
441:         if (currentY + blockH < lyricsYStart || currentY > lyricsYStart + lyricsH) {
442:           currentY += blockH + blockSpacing;
443:           return;
444:         }
445:         
446:         if (isActive && isSynced) {
447:           // 하이라이트 박스
448:           ctx.fillStyle = 'rgba(60, 60, 60, 0.8)';
449:           const padX = 40 * scale, padY = 20 * scale;
450:           const radius = 20 * scale;
451:           ctx.beginPath();
452:           ctx.roundRect(lyricsX + padX, currentY - padY, lyricsW - padX*2, blockH + padY*2, radius);
453:           ctx.fill();
454:         }
455:         
456:         let itemY = currentY;
457:         item.parsedLines.forEach(line => {
458:            ctx.fillStyle = (isActive || !isSynced) ? '#ffffff' : 'rgba(130, 130, 130, 1)';
459:            // 캔버스 자체 중앙 정렬 기능 사용 (수동 X좌표 계산 오류 원천 차단)
460:            ctx.textAlign = 'center';
461:            const lineX = lyricsX + lyricsW / 2;
462:            
463:            if (line.compress) {
464:                // 2안: 가로폭 압축 렌더링
465:                ctx.fillText(line.text, lineX, itemY, maxW);
466:            } else {
467:                ctx.fillText(line.text, lineX, itemY);
468:            }
469:            
470:            itemY += line.h + lineSpacing;
471:         });
472:         
473:         currentY += blockH + blockSpacing;
474:       });
475: 
476:       // 상/하단 스무스 페이드 아웃 (블랙 그라데이션) - 약 2.5줄 높이
477:       const fadeH = 150 * scale;
478:       
479:       const topGrad = ctx.createLinearGradient(0, lyricsYStart, 0, lyricsYStart + fadeH);
480:       topGrad.addColorStop(0, 'rgba(0,0,0,1)');
481:       topGrad.addColorStop(1, 'rgba(0,0,0,0)');
482:       ctx.fillStyle = topGrad;
483:       ctx.fillRect(lyricsX, lyricsYStart, lyricsW, fadeH);
484: 
485:       const bottomGrad = ctx.createLinearGradient(0, lyricsYStart + lyricsH, 0, lyricsYStart + lyricsH - fadeH);
486:       bottomGrad.addColorStop(0, 'rgba(0,0,0,1)');
487:       bottomGrad.addColorStop(1, 'rgba(0,0,0,0)');
488:       ctx.fillStyle = bottomGrad;
489:       ctx.fillRect(lyricsX, lyricsYStart + lyricsH - fadeH, lyricsW, fadeH);
490:       
491:       ctx.restore(); // 클리핑 해제
492:       
493:       // 타이틀 오프닝 효과 (첫 5초)
494:       if (songTitleStr && time < 5) {
495:         ctx.save();
496:         let alpha = 1.0;
497:         if (time < 1) alpha = time;
498:         else if (time > 4) alpha = 1.0 - (time - 4);
499:         
500:         ctx.globalAlpha = alpha;
501:         ctx.fillStyle = '#f5c45e';
502:         const titleFont = (isVertical ? 50 : 60) * scale;
503:         ctx.font = `900 ${titleFont}px ${fontFamily}, sans-serif`;
504:         ctx.textBaseline = 'middle';
505:         ctx.textAlign = 'center';
506:         
507:         const titleX = lyricsX + lyricsW / 2;
508:         let titleY = lyricsYStart + lyricsH / 3;
509:         
510:         // 그림자 효과로 가독성 향상
511:         ctx.shadowColor = 'rgba(0,0,0,0.9)';
512:         ctx.shadowBlur = 15 * scale;
513:         ctx.shadowOffsetX = 2 * scale;
514:         ctx.shadowOffsetY = 2 * scale;
515:         
516:         // 제목에도 1안/2안(스마트 줄바꿈) 적용
517:         const maxTitleW = lyricsW * 0.85;
518:         const titleLines = smartBalanceWrap(songTitleStr, ctx, maxTitleW, scale);
519:         
520:         const titleLineSpacing = 20 * scale;
521:         const totalTitleH = titleLines.length * titleFont + Math.max(0, titleLines.length - 1) * titleLineSpacing;
522:         titleY -= totalTitleH / 4; // 다중 줄일 때 중앙 보정
523:         
524:         titleLines.forEach(tLine => {
525:             if (tLine.compress) {
526:                 ctx.fillText(tLine.text, titleX, titleY, maxTitleW);
527:             } else {
528:                 ctx.fillText(tLine.text, titleX, titleY);
529:             }
530:             titleY += titleFont + titleLineSpacing;
531:         });
532:         
533:         ctx.restore();
534:       }
535:     }
536: 
537:     async function startRendering() {
538:       const coverFile = document.getElementById('coverInput').files[0];
539:       const audioFile = document.getElementById('audioInput').files[0];
540:       const statusPanel = document.getElementById('statusPanel');
541:       const renderBtn = document.getElementById('renderBtn');
542:       
543:       if (!coverFile || !audioFile) {
544:         alert('커버 이미지와 노래 파일을 모두 업로드해주세요!');
545:         return;
546:       }
547:       
548:       renderBtn.disabled = true;
549:       statusPanel.style.display = 'block';
550:       statusPanel.innerText = '재료 준비 중...';