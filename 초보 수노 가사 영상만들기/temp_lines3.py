140:           <textarea id="rawLyrics" placeholder="여기에 가사를 붙여넣으세요. 빈 줄 단위로 단락이 나뉩니다."></textarea>
141:         </div>
142:       </div>
143: 
144:       <div class="file-input-group">
145:         <label>6. 화면 비율 및 해상도</label>
146:         <select id="aspectRatio">
147:           <option value="1k_16:9">1K (FHD) 가로형 - 1920x1080</option>
148:           <option value="1k_9:16">1K (FHD) 세로형 - 1080x1920</option>
149:           <option value="2k_16:9">2K (QHD) 가로형 - 2560x1440</option>
150:           <option value="2k_9:16">2K (QHD) 세로형 - 1440x2560</option>
151:           <option value="4k_16:9">4K (UHD) 가로형 - 3840x2160</option>
152:           <option value="4k_9:16">4K (UHD) 세로형 - 2160x3840</option>
153:         </select>
154:       </div>
155: 
156:       <button id="renderBtn" class="primary-btn" onclick="startRendering()">영상 렌더링 시작</button>
157:       
158:       <div id="statusPanel" class="status-panel">
159:         준비 중...
160:       </div>
161:       
162:     </aside>
163:     
164:     <!-- 오른쪽 프리뷰 영역 -->
165:     <section class="output-panel">
166:       <div class="output-toolbar">
167:         <h2>실시간 렌더링 화면</h2>
168:         <p>영상이 재생되는 동안 백그라운드에서 고음질로 녹화됩니다.</p>
169:       </div>