# -*- coding: utf-8 -*-
import os, json, re

BASE_DIR = 'public'
CDN_BASE = 'https://cdn.jsdelivr.net/gh/SunIsAlex/duolingo-prepositions@main/public'

# Read CSS
with open(os.path.join(BASE_DIR, 'css', 'style.css'), 'r', encoding='utf-8') as f:
    css_content = f.read()

# Read Questions
with open(os.path.join(BASE_DIR, 'js', 'questions.js'), 'r', encoding='utf-8') as f:
    questions_js = f.read()

# Read Audio Manager and App JS
with open(os.path.join(BASE_DIR, 'js', 'audio-manager.js'), 'r', encoding='utf-8') as f:
    audio_mgr_js = f.read()

with open(os.path.join(BASE_DIR, 'js', 'app.js'), 'r', encoding='utf-8') as f:
    app_js = f.read()

# Point audio manager to CDN URLs
cdn_sound_paths = {
    'correct': f'{CDN_BASE}/assets/audio/right_answer.mp3',
    'wrong': f'{CDN_BASE}/assets/audio/wrong_answer.mp3',
    'tap': f'{CDN_BASE}/assets/audio/tap.mp3',
    'streak': f'{CDN_BASE}/assets/audio/streak_5.mp3',
    'ding': f'{CDN_BASE}/assets/audio/da_ding.mp3',
    'chime': f'{CDN_BASE}/assets/audio/star_chime.mp3',
    'applause': f'{CDN_BASE}/assets/audio/applause.mp3'
}

audio_mgr_js = audio_mgr_js.replace(
    "this.soundPaths = {\n      correct: 'assets/audio/right_answer.mp3',\n      wrong: 'assets/audio/wrong_answer.mp3',\n      tap: 'assets/audio/tap.mp3',\n      streak: 'assets/audio/streak_5.mp3',\n      ding: 'assets/audio/da_ding.mp3',\n      chime: 'assets/audio/star_chime.mp3',\n      applause: 'assets/audio/applause.mp3'\n    };",
    "this.soundPaths = " + json.dumps(cdn_sound_paths) + ";"
)

# Point Lottie animations to CDN URLs
app_js = app_js.replace(
    "path: 'assets/anim/flame.json'",
    f"path: '{CDN_BASE}/assets/anim/flame.json'"
)

app_js = app_js.replace(
    "path: 'assets/anim/duo_cheer.json'",
    f"path: '{CDN_BASE}/assets/anim/duo_cheer.json'"
)

app_js = app_js.replace(
    "waving: 'assets/anim/duo_waving.json',\n      cheer: 'assets/anim/duo_cheer.json',\n      hop: 'assets/anim/duo_hop.json',\n      sad: 'assets/anim/duo_sad.json',\n      super: 'assets/anim/duo_super_jumping.json'",
    f"waving: '{CDN_BASE}/assets/anim/duo_waving.json',\n      cheer: '{CDN_BASE}/assets/anim/duo_cheer.json',\n      hop: '{CDN_BASE}/assets/anim/duo_hop.json',\n      sad: '{CDN_BASE}/assets/anim/duo_sad.json',\n      super: '{CDN_BASE}/assets/anim/duo_super_jumping.json'"
)

# Read HTML and replace external links
with open(os.path.join(BASE_DIR, 'index.html'), 'r', encoding='utf-8') as f:
    html = f.read()

# Replace <link rel="stylesheet" href="css/style.css"> with inline style
html = html.replace(
    '<link rel="stylesheet" href="css/style.css">',
    f'<style>\n{css_content}\n</style>'
)

# Scripts block with CDN Lottie and Confetti + inlined app code
scripts_block = f"""
  <script src="https://cdnjs.cloudflare.com/ajax/libs/lottie-web/5.12.2/lottie.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js"></script>
  <script>
  {audio_mgr_js}
  </script>
  <script>
  {questions_js}
  </script>
  <script>
  {app_js}
  </script>
"""

# Replace script tags with inlined script block
pattern = r'  <!-- Client Libraries -->[\s\S]*?</body>'
html = re.sub(pattern, lambda m: scripts_block + "\n</body>", html)

os.makedirs('dist_mcp', exist_ok=True)
with open('dist_mcp/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Bundled dist_mcp/index.html: {len(html)} bytes (~{round(len(html)/1024, 1)} KB)")
