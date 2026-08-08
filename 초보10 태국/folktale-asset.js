const flowRules = `대본 + 화풍 + 챕터 수를 받아 Google Flow Image(Nano Banana Pro)용 프롬프트를 만든다.
화풍은 텍스트(STYLE_TAIL)로 고정한다(레퍼런스 이미지 색 번짐 방지). 외부 이미지 0개 투입.

## 운영 규칙
1. PHASE를 순서대로 처리한다.
2. 포즈는 아래 축소 POSE_POOL에서 고른다. 자유 창작 대신 풀에서 강도·사건에 맞는 항목 선택.
3. 치환 사전·금지어는 그대로 사용.
4. 한국어로만 응답. 사용자 출력은 템플릿만.

## 핵심 원칙
- 정면 손모음 포즈가 장면에 복붙되면 안 됨: 인물은 POSE_POOL에서 고른 신체 동작.
- 회색 스튜디오 배경 금지: 장면 배경은 실제 조선 로케이션.

## 처리 흐름
PHASE 1   화풍 추출 → STYLE_TAIL (10~30단어, 색상/조명 단어 제외)
PHASE 2   챕터 분할 (40개 챕터로 균등 분할)
PHASE 3   캐릭터 추출 + 조선 복식 앵커 (등장 빈도 상위 5명, 한복/갓 등 앵커 부여)
PHASE 3.5 샷 배정 + 포즈 배정 (POSE_POOL 6종 중 인접 챕터와 안 겹치게)
PHASE 4   STEP 1(배경·포즈 분리 레퍼런스 생성) + STEP 2(40개 장면 조립)
PHASE 5   최소 검증 (앵커 누락, 한글 잔존, 회색 배경 점검)

### STEP 1 — UPLOAD (신원 전용 / 배경분리 / 포즈분리)
캐릭터당 한 장. Flow ingredient 슬롯용 신원 식별 전용 레퍼런스.
=== <n> UPLOAD ===
Character identity reference of <a Korean Joseon-era 인물(영어), anchor_outfit + anchor_hair + anchor_feature>, neutral A-pose standing straight with both arms relaxed at the sides, plain flat neutral gray background, subject fully isolated, this is an identity reference only and the pose, hand position and background must NOT carry over into any scene, no hands clasped, no props no other figures, <STYLE_TAIL>

### STEP 2 — 장면 프롬프트 (조립 공식)
N. @name, anchor1, anchor2, anchor3 — [샷 영문] of [주어] [POSE_POOL 포즈]. [행동·배경·로컬컬러·인원신호] 15~65단어. a single figure, natural mid-action pose, no text no letters no words no modern objects, <STYLE_TAIL>

### 축소 POSE_POOL 6종
- caught mid-stride, weight thrown onto one leg
- turning the head and shoulders to glance back
- reaching out one hand toward another figure
- leaning forward over a surface, weight on the hands
- standing with the body turned away, gazing into the distance
- crouching to examine something on the ground

## 출력 포맷
[STEP 1 - 캐릭터 앵커 생성 프롬프트]
...

[대본 1~40 요약]
...

[영어 프롬프트 1~40]
1. @name, ...
...`;

const grokRules = `Grok 이미지+영상 인트로 훅 프롬프트 생성 (Sonnet판 / 압축본)
대본(대사·나레이션)의 가장 첫 부분(발단)을 분석하여, 인트로 영상을 만들기 위한 총 8개의 연속된 프롬프트 세트를 자동 생성한다.
- 1번~7번 프롬프트: 대본의 도입부 이야기를 7개의 씬(Scene)으로 분할하여 작성 (플로우 영상이 8초 단위이므로 7개를 합쳐 약 1분 분량 구성).
- 8번 프롬프트: 본편이 시작하기 직전, 시청자에게 "구독과 좋아요를 부탁합니다"라는 메시지를 전달하는 특별 씬(호스트 등장 또는 타이포그래피 등)으로 구성.
- 영어 본문은 삼중 백틱 코드블록으로만 감싼다.
- 스포일러 금지(정체·반전·플롯 노출 금지).
- 스타일 라인 고정: Drawn illustration in webtoon manhwa comic style with clear bold line art and flat cel-shaded coloring like the attached reference. 16:9 aspect ratio.
- 금지어: semi-realistic, painterly soft shading, photorealistic, cinematic, shallow depth of field, bokeh, lens blur, sharp focus, soft-focus.

## 카메라군 결정 트리 (각 씬별로 적용)
Q1. 인물 2명 이상인가? → 예: PUSH-IN 전용 / 아니오(단독): Q2
Q2. 엣지에 미리 심은 인물·실루엣 있나? → 예: PUSH-IN 전용 / 아니오: Q3
Q3. 배경 단순한가? → 단순: 바깥 기법 허용 / 복잡: PUSH-IN 전용

## 영상 규칙
- 대사 vs 나레이션 = 큰따옴표로 구분. 한 씬에 섞지 않는다.
- "" 안 = lip-sync(인물 정지·입만) / "" 밖 = 완전 무음 + 카메라 더 과감 가능.
- 과잉 수식 금지(He shouts the line. 처럼 담백하게).

## 출력 포맷 (씬 1부터 8까지 각각 아래 포맷 반복)
===== 씬 [번호] =====
[A] 이미지 프롬프트 (영어, 복사용):
\`\`\`
[@태그 + 동작 + 위치 + 배경 + 조명, 산문. 극적 구도 3개+ 포함]. no text no letters no words no modern objects, [single figure / two figures / several figures]. Drawn illustration in webtoon manhwa comic style with clear bold line art and flat cel-shaded coloring like the attached reference. 16:9 aspect ratio.
\`\`\`

[B] 영상 프롬프트 (영어, 복사용):
\`\`\`
ACTION: The subject stays completely in place, only the mouth moves. He says the line: "[대사 원문]"
CAMERA: [대사 씬은 hard push-in까지]. Camera moves, the subject does not walk or change position.
DIALOGUE: "[대사 원문]"
With precise lip synchronization to spoken dialogue only, accurate mouth movements matching every Korean syllable and word, [톤] Korean [성별] voice, in-scene live spoken dialogue for the line: "[대사 원문]"
CRITICAL: NO text, NO subtitles, NO captions, NO speech bubbles, NO Korean/Chinese characters on any surface. NO written words in any language.
\`\`\``;

document.getElementById('generateAssetBtn').addEventListener('click', function() {
    const moodSelect = document.getElementById('mood');
    const mood = moodSelect ? moodSelect.options[moodSelect.selectedIndex].text : "슬프고 애절한 동양풍";
    const scriptInput = document.getElementById('scriptInput').value.trim();

    if (!scriptInput) {
        alert("Claude가 작성해준 대본을 입력창에 붙여넣어 주세요!");
        return;
    }

    const flowPrompt = `당신은 최고 수준의 이미지 프롬프트 엔지니어입니다.
아래의 [대본]과 [Google Flow 운영 규칙]을 완벽하게 숙지한 뒤, 40장의 장면 이미지와 캐릭터 기준(UPLOAD) 프롬프트를 정확한 양식으로 추출해 주세요.

[대본]
${scriptInput}

[Google Flow 운영 규칙]
${flowRules}`;

    const grokPrompt = `당신은 최고 수준의 영상 인트로 감독입니다.
아래의 [대본]과 [Grok 영상 규칙]을 숙지하고, 대본의 도입부(약 1분 분량)를 연속된 8개의 Grok 훅(Hook) 프롬프트 씬으로 분할 작성해 주세요.

[대본 도입부]
${scriptInput.substring(0, 1000)}... (이하 생략)

[Grok 영상 규칙]
${grokRules}`;

    const sunoPrompt = `당신은 음악 감독입니다. 아래 대본의 분위기를 파악해 Suno AI용 프롬프트 1줄을 작성하세요.
- 분위기: ${mood}
- 필수 포함 악기: gayageum, haegeum, daegeum, janggu (상황에 맞게 선택)
- 작성 예시: "Korean traditional acoustic relaxing background music, gayageum, cinematic, ${mood} mood"`;

    const combinedOutput = `========== [1번 복사: Google Flow 40챕터 & 캐릭터 앵커 생성용] ==========
${flowPrompt}

\n\n========== [2번 복사: Grok 인트로 영상 생성용 (총 8씬)] ==========
${grokPrompt}

\n\n========== [3번 복사: Suno 배경음악 생성용] ==========
${sunoPrompt}`;

    const resultCard = document.getElementById('resultCard');
    const promptOutput = document.getElementById('promptOutput');
    
    promptOutput.textContent = combinedOutput;
    resultCard.style.display = 'block';
});

document.getElementById('copyAssetBtn').addEventListener('click', function() {
    const promptOutput = document.getElementById('promptOutput');
    if (!promptOutput) return;
    
    navigator.clipboard.writeText(promptOutput.textContent).then(() => {
        const copyBtn = document.getElementById('copyAssetBtn');
        const originalText = copyBtn.textContent;
        copyBtn.textContent = '전체 복사 완료!';
        copyBtn.style.background = '#00d2ff';
        copyBtn.style.color = '#06111f';
        
        setTimeout(() => {
            copyBtn.textContent = originalText;
            copyBtn.style.background = '';
            copyBtn.style.color = '';
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy text: ', err);
        alert('복사에 실패했습니다.');
    });
});
