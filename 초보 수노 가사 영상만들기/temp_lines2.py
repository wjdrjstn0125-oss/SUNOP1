140:           <textarea id="rawLyrics" placeholder="여기에 가사를 붙여넣으세요. 빈 줄 단위로 단락이 나뉩니다."></textarea>
141:         </div>
142:       </div>
143: 
144:       <div class="file-input-group">
145:         <label>6. 화면 비율 및 해상도</label>출 수 없으며 일정한 속도로만 스크롤됩니다. <b>현재 부르는 가사를 화면 중앙에 오게 하려면 반드시 위에서 SRT 방식을 선택하세요!</b>
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