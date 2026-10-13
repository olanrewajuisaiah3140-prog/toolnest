const workspace=document.getElementById('workspace'), body=document.getElementById('workspace-body'),title=document.getElementById('workspace-title'),status=document.getElementById('status');
document.getElementById('year').textContent=new Date().getFullYear();
const names={compress:'Image Compressor',qr:'QR Code Generator',word:'Word Counter',password:'Password Generator',case:'Text Case Converter','pdf-merge':'Merge PDF','pdf-split':'Split / Extract PDF','pdf-compress':'Compress PDF','pdf-rotate':'Rotate PDF','pdf-images':'PDF to JPG','pdf-create':'Images to PDF','pdf-text':'PDF to Text'};
const templates={
compress:`<p class="muted">Select a JPEG, PNG, or WebP image (up to 8 MB). Large images will be resized to fit within 2000 px.</p><label for="image">Choose image</label><input id="image" type="file" accept="image/jpeg,image/png,image/webp"><div class="field-row"><button class="primary" id="compress-btn">Compress & download</button></div>`,
qr:`<label for="qr-data">Text or URL</label><input id="qr-data" type="text" maxlength="2000" placeholder="https://example.com"><div class="field-row"><button class="primary" id="qr-btn">Generate & download QR</button></div>`,
word:`<label for="word-input">Paste your text</label><textarea id="word-input" placeholder="Start typing here..."></textarea><div class="stats" id="word-stats">0 words · 0 characters · 0 sentences</div>`,
password:`<label for="pass-length">Password length</label><input id="pass-length" type="number" min="8" max="64" value="16"><div class="field-row"><label><input id="pass-symbols" type="checkbox" checked> Include symbols</label><label><input id="pass-numbers" type="checkbox" checked> Include numbers</label></div><button class="primary" id="pass-btn">Generate password</button><label for="pass-result">Your password</label><input id="pass-result" type="text" readonly><div class="field-row"><button class="subtle" id="pass-copy">Copy password</button></div><p class="muted">Generated locally in your browser with cryptographically secure randomness.</p>`,
case:`<label for="case-input">Your text</label><textarea id="case-input" placeholder="Enter text to convert..."></textarea><div class="field-row"><button class="primary" data-case="upper">UPPERCASE</button><button class="primary" data-case="lower">lowercase</button><button class="primary" data-case="title">Title Case</button><button class="primary" data-case="sentence">Sentence case</button></div><label for="case-result">Result</label><textarea id="case-result" readonly></textarea><div class="field-row"><button class="subtle" id="case-copy">Copy result</button></div>`};
const pdfConfigs={
'pdf-merge':{action:'merge',multiple:true,accept:'.pdf,application/pdf',label:'Choose 2–20 PDF files',hint:'Files are merged in the order selected.',button:'Merge & download',filename:'merged.pdf'},
'pdf-split':{action:'split',accept:'.pdf,application/pdf',label:'Choose PDF',extra:`<label for="pdf-pages">Pages to extract (optional)</label><input id="pdf-pages" placeholder="e.g. 1,3-5 (blank = all pages)">`,button:'Extract & download',filename:'selected-pages.pdf'},
'pdf-compress':{action:'compress',accept:'.pdf,application/pdf',label:'Choose PDF',hint:'PDF uploads for compression are limited to 14 MB on free hosting. Image quality may change in Balanced or Strong mode.',extra:`<label for="compression-level">Compression level</label><select id="compression-level"><option value="light">Light — preserve images</option><option value="balanced" selected>Balanced — good quality, smaller file</option><option value="strong">Strong — smaller file, lower image quality</option></select>`,button:'Compress & download',filename:'optimized.pdf'},
'pdf-rotate':{action:'rotate',accept:'.pdf,application/pdf',label:'Choose PDF',extra:`<label for="pdf-angle">Rotation</label><select id="pdf-angle"><option value="90">90° clockwise</option><option value="180">180°</option><option value="270">270° clockwise</option></select>`,button:'Rotate & download',filename:'rotated.pdf'},
'pdf-images':{action:'pdf-to-jpg',accept:'.pdf,application/pdf',label:'Choose PDF',extra:`<label for="pdf-pages">Pages to export (optional, max 30)</label><input id="pdf-pages" placeholder="e.g. 1,3-5 (blank = all pages)">`,button:'Convert to JPG (ZIP)',filename:'pdf-pages.zip'},
'pdf-create':{action:'images-to-pdf',accept:'image/jpeg,image/png,image/webp',multiple:true,label:'Choose images (JPG, PNG or WebP)',button:'Create PDF',filename:'images.pdf'},
'pdf-text':{action:'pdf-to-text',accept:'.pdf,application/pdf',label:'Choose PDF',hint:'Extracts selectable text. Scanned documents need OCR, which is not included yet.',button:'Extract text',filename:'extracted-text.txt'}
};
function showPdfTool(which){const c=pdfConfigs[which];body.innerHTML=`<p class="muted">Free PDF tools, no account needed. PDF files up to 150 pages; uploads together up to 30 MB. Password-protected files are not supported.</p>${c.hint?`<p class="muted">${c.hint}</p>`:''}<label for="pdf-files">${c.label}</label><input id="pdf-files" type="file" accept="${c.accept}" ${c.multiple?'multiple':''}>${c.extra||''}<div class="field-row"><button class="primary" id="pdf-submit">${c.button}</button></div>`;document.getElementById('pdf-submit').onclick=()=>{const files=[...document.getElementById('pdf-files').files];if(!files.length){status.textContent='Choose a file first.';return}if(files.reduce((n,f)=>n+f.size,0)>30*1024*1024){status.textContent='Combined upload must be less than 30 MB.';return}const form=new FormData();files.forEach(f=>form.append('files',f));const pages=document.getElementById('pdf-pages');if(pages)form.append('pages',pages.value);const angle=document.getElementById('pdf-angle');if(angle)form.append('angle',angle.value);const level=document.getElementById('compression-level');if(level)form.append('compression_level',level.value);if(which==='pdf-compress'&&files[0].size>14*1024*1024){status.textContent='Compress PDF accepts files up to 14 MB on our free server.';return}postAndDownload('/api/pdf/'+c.action,form,c.filename)}}
function saveBlob(blob,name){const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),2000)}
async function postAndDownload(path,fields,filename){status.textContent='Processing...';try{const response=await fetch(path,{method:'POST',body:fields});if(!response.ok){let message='Could not process request';try{message=(await response.json()).error||message}catch{}throw Error(message)}saveBlob(await response.blob(),filename);status.textContent='';}catch(e){status.textContent=e.message}}
function securePassword(length,chars){const output=[];const max=Math.floor(256/chars.length)*chars.length;while(output.length<length){const numbers=new Uint8Array(Math.max(32,length));crypto.getRandomValues(numbers);for(const n of numbers){if(n<max){output.push(chars[n%chars.length]);if(output.length===length)break}}}return output.join('')}
function showTool(which){title.textContent=names[which];body.innerHTML=templates[which]||'';status.textContent='';workspace.hidden=false;if(!document.body.dataset.toolPage)workspace.scrollIntoView({behavior:'smooth',block:'start'});
if(pdfConfigs[which])showPdfTool(which);
if(which==='compress')document.getElementById('compress-btn').onclick=()=>{const file=document.getElementById('image').files[0];if(!file){status.textContent='Choose an image first.';return}if(file.size>8*1024*1024){status.textContent='File must be smaller than 8 MB.';return}const form=new FormData();form.append('image',file);postAndDownload('/api/compress',form,'compressed-image')};
if(which==='qr')document.getElementById('qr-btn').onclick=()=>{const data=document.getElementById('qr-data').value.trim();if(!data){status.textContent='Enter text or a URL first.';return}const form=new FormData();form.append('data',data);postAndDownload('/api/qr',form,'qr-code.png')};
if(which==='word'){const input=document.getElementById('word-input'),stats=document.getElementById('word-stats');input.oninput=()=>{const value=input.value;const words=value.trim()?value.trim().split(/\s+/u).length:0;const sentences=(value.match(/[^.!?]+[.!?]+|[^.!?]+$/gu)||[]).filter(s=>s.trim()).length;stats.textContent=`${words} words · ${[...value].length} characters · ${sentences} sentences`}};
if(which==='password'){document.getElementById('pass-btn').onclick=()=>{const n=Number(document.getElementById('pass-length').value);if(!Number.isInteger(n)||n<8||n>64){status.textContent='Choose a length from 8 to 64.';return}let chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';if(document.getElementById('pass-numbers').checked)chars+='0123456789';if(document.getElementById('pass-symbols').checked)chars+='!@#$%^&*()-_=+';document.getElementById('pass-result').value=securePassword(n,chars);status.textContent=''};document.getElementById('pass-copy').onclick=()=>copy(document.getElementById('pass-result').value)};
if(which==='case'){body.querySelectorAll('[data-case]').forEach(btn=>btn.onclick=()=>{const t=document.getElementById('case-input').value;const type=btn.dataset.case;document.getElementById('case-result').value=type==='upper'?t.toUpperCase():type==='lower'?t.toLowerCase():type==='title'?t.toLowerCase().replace(/\b\p{L}/gu,c=>c.toUpperCase()):t.toLowerCase().replace(/(^\s*\p{L}|[.!?]\s*\p{L})/gu,c=>c.toUpperCase())});document.getElementById('case-copy').onclick=()=>copy(document.getElementById('case-result').value)}}
async function copy(v){if(!v){status.textContent='Nothing to copy yet.';return}try{await navigator.clipboard.writeText(v);status.textContent='Copied!'}catch{status.textContent='Copy failed. Select the text and copy manually.'}}
// V5 tool cards are real links. Standalone pages initialize the matching V4 tool below.

// V3 tool search and category browsing (keeps V2 tool handlers intact)
const searchBox = document.getElementById('tool-search');
const categoryButtons = [...document.querySelectorAll('[data-filter]')];
const toolCards = [...document.querySelectorAll('.tool-card')];
let currentCategory = 'all';
function filterTools(){
  if (!searchBox) return;
  const query = searchBox.value.toLowerCase().trim();
  let visible = 0;
  for (const card of toolCards){
    const matches = (currentCategory === 'all' || card.dataset.category === currentCategory)
      && card.textContent.toLowerCase().includes(query);
    card.hidden = !matches;
    if(matches)visible++;
  }
  const noResults = document.getElementById('no-results');
  if(noResults) noResults.hidden = visible !== 0;
}
function selectCategory(category){
  currentCategory = category;
  categoryButtons.forEach(button => {
    const active = button.dataset.filter === category;
    button.classList.toggle('active', active);
    button.setAttribute('aria-pressed', String(active));
  });
  filterTools();
}
if(searchBox) searchBox.addEventListener('input', filterTools);
categoryButtons.forEach(button => button.addEventListener('click', () => selectCategory(button.dataset.filter)));
// Honor links like /?category=pdf#tools when visitors arrive on the homepage.
if(searchBox){
  const requested = new URLSearchParams(window.location.search).get('category');
  if(['pdf','image','text'].includes(requested)) selectCategory(requested);
}
// Standalone tool pages use exactly the same tested V4 form and API handlers.
if(document.body.dataset.toolPage) showTool(document.body.dataset.toolPage);

