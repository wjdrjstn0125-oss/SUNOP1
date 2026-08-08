90:     <a aria-current="page" class="app-nav-btn is-active" href="lyric-video.html">자동 자막 비디오</a>
91:    </nav>
92:   </header>
93:   
94:   <main class="app-shell">
95:    <section class="workspace">
96:     <!-- 왼쪽 제어 패널 -->
97:     <aside class="settings-panel">
98:       <div class="brand-row">
99:              <div class="file-input-group">
100:         <label>1. 노래 제목 및 가수</label>
101:         <input type="text" id="songTitle" placeholder="예: My Awesome Song - Suno" style="width: 100%; border-radius: 4px; border: 1px solid rgba(255,255,255,0.1); padding: 10px; background: #0f1115; color: white;">
102:       </div>
103: 
104:       <div class="file-input-group">
105:         <label>2. 가사 및 제목 글꼴 (폰트)</label>
106:         <select id="fontFamily">
107:           <option value="'Malgun Gothic'">맑은 고딕 (기본)</option>
108:           <option value="'Noto Sans KR'">노토 산스 (깔끔하고 트렌디)</option>
109:           <option value="'Do Hyeon'">도현체 (레트로 감성)</option>
110:           <option value="'Jua'">주아체 (부드럽고 귀여운)</option>
111:           <option value="'Nanum Pen Script'">나눔 펜 스크립트 (손글씨)</option>
112:         </select>
113:       </div>
114: 
115:       <div class="file-input-group">
116:         <label>3. 앨범 커버 이미지 (JPG/PNG)</label>
117:         <input type="file" id="coverInput" accept="image/jpeg, image/png">
118:       </div>
119: 
120:       <div class="file-input-group">
121:         <label>4. 노래 파일 (MP3/WAV)</label>
122:         <input type="file" id="audioInput" accept="audio/mpeg, audio/wav">
123:       </div>
124: 
125:       <div class="file-input-group">
126:         <label>5. 가사 자막 설정 (선택사항)</label>
127:         <select id="subtitleMode" onchange="toggleSubtitleInput()">
128:           <option value="srt">SRT 파일 업로드 (정확한 씽크)</option>
129:           <option value="text">가사 텍스트 직접 입력 (자동 스크롤)</option>
130:         </select>
131:         
132:         <div id="srtInputWrap" style="margin-top: 10px;">
133:           <input type="file" id="srtInput" accept=".srt">
134:         </div>
135:         
136:         <div id="textInputWrap" style="display: none; margin-top: 10px;">
137:           <div style="color: #ff5252; font-size: 12px; margin-bottom: 8px; line-height: 1.4;">
138:             ※ 주의: 텍스트 모드는 음악 박자에 싱크를 맞출 수 없으며 일정한 속도로만 스크롤됩니다. <b>현재 부르는 가사를 화면 중앙에 오게 하려면 반드시 위에서 SRT 방식을 선택하세요!</b>
139:           </div>
140:           <textarea id="rawLyrics" placeholder="여기에 가사를 붙여넣으세요. 빈 줄 단위로 단락이 나뉩니다."></textarea>
141:         </div>
142:       </div>
143: 
144:       <div class="file-input-group">
145:         <label>6. 화면 비율 및 해상도</label>�출 수 없으며 일정한 속도로만 스크롤됩니다. <b>현재 부르는 가사를 화면 중앙에 오게 하려면 반드시 위에서 SRT 방식을 선택하세요!</b>
146:           </div>
147:           <textarea id="rawLyrics" placeholder="여기에 가사를 붙여넣으세요. 빈 줄 단위로 단락이 나뉩니다."></textarea>
148:         </div>
149:       </div>
150: 
151:       <div class="file-input-group">
152:         <label>5. 화면 비율 및 해상도</label>
153:         <select id="aspectRatio">
154:           <option value="1k_16:9">1K (FHD) 가로형 - 1920x1080</option>
155:           <option value="1k_9:16">1K (FHD) 세로형 - 1080x1920</option>
156:           <option value="2k_16:9">2K (QHD) 가로형 - 2560x1440</option>
157:           <option value="2k_9:16">2K (QHD) 세로형 - 1440x2560</option>
158:           <option value="4k_16:9">4K (UHD) 가로형 - 3840x2160</option>
159:           <option value="4k_9:16">4K (UHD) 세로형 - 2160x3840</option>
160:         </select>
161:       </div>
162: 
163:       <button id="renderBtn" class="primary-btn" onclick="startRendering()">영상 렌더링 시작</button>
164:       
165:       <div id="statusPanel" class="status-panel">
166:         준비 중...
167:       </div>
168:       
169:     </aside>
170:     
171:     <!-- 오른쪽 프리뷰 영역 -->
172:     <section class="output-panel">
173:       <div class="output-toolbar">
174:         <h2>실시간 렌더링 화면</h2>
175:         <p>영상이 재생되는 동안 백그라운드에서 고음질로 녹화됩니다.</p>
176:       </div>
177:       <div class="preview-container" id="previewContainer">
178:         <canvas id="renderCanvas" width="1920" height="1080"></canvas>
179:       </div>
180:       
181:       <div style="margin-top: 20px; font-size: 13px; color: #a3a8b2; line-height: 1.6;">
182:         <h3 style="color:#f5c45e; margin-bottom: 5px;">💡 안내사항</h3>
183:         - 영상 렌더링은 음악 길이만큼 실시간으로 진행됩니다.<br>
184:         - 녹화 중에는 다른 탭으로 이동하지 마세요. (브라우저 정책상 렌더링이 멈출 수 있습니다.)<br>
185:         - 작업이 완료되면 고화질(webm) 영상 파일이 자동으로 다운로드됩니다.
186:       </div>
187:     </section>
188:     
189:    </section>
190:   </main>
191: 
192:   <script>
193:     // --- UI 로직 ---
194:     function toggleSubtitleInput() {
195:       const mode = document.getElementById('subtitleMode').value;
196:       if (mode === 'srt') {
197:         document.getElementById('srtInputWrap').style.display = 'block';
198:         document.getElementById('textInputWrap').style.display = 'none';
199:       } else {