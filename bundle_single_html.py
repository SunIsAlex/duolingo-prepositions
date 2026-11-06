# -*- coding: utf-8 -*-
import os, base64, json, re

BASE_DIR = 'public'

# Read CSS
with open(os.path.join(BASE_DIR, 'css', 'style.css'), 'r', encoding='utf-8') as f:
    css_content = f.read()

# Read Libs
with open(os.path.join(BASE_DIR, 'libs', 'lottie.min.js'), 'r', encoding='utf-8') as f:
    lottie_js = f.read()

with open(os.path.join(BASE_DIR, 'libs', 'confetti.min.js'), 'r', encoding='utf-8') as f:
    confetti_js = f.read()

# Read Questions
with open(os.path.join(BASE_DIR, 'js', 'questions.js'), 'r', encoding='utf-8') as f:
    questions_js = f.read()

# Read Audio files as Base64 data URIs
audio_files = {
    'correct': 'assets/audio/right_answer.mp3',
    'wrong': 'assets/audio/wrong_answer.mp3',
    'tap': 'assets/audio/tap.mp3',
    'streak': 'assets/audio/streak_5.mp3',
    'ding': 'assets/audio/da_ding.mp3',
    'chime': 'assets/audio/star_chime.mp3',
    'applause': 'assets/audio/applause.mp3'
}

audio_data_uris = {}
for k, rel_path in audio_files.items():
    p = os.path.join(BASE_DIR, rel_path)
    with open(p, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('utf-8')
        audio_data_uris[k] = f"data:audio/mp3;base64,{b64}"

# Read Lottie Animations as JSON
anim_files = {
    'waving': 'assets/anim/duo_waving.json',
    'cheer': 'assets/anim/duo_cheer.json',
    'hop': 'assets/anim/duo_hop.json',
    'sad': 'assets/anim/duo_sad.json',
    'super': 'assets/anim/duo_super_jumping.json',
    'flame': 'assets/anim/flame.json',
    'sparkles': 'assets/anim/sparkles.json',
    'check': 'assets/anim/check_anim.json'
}

anim_json_data = {}
for k, rel_path in anim_files.items():
    p = os.path.join(BASE_DIR, rel_path)
    with open(p, 'r', encoding='utf-8') as f:
        anim_json_data[k] = json.load(f)

# Read Audio Manager and App JS
with open(os.path.join(BASE_DIR, 'js', 'audio-manager.js'), 'r', encoding='utf-8') as f:
    audio_mgr_js = f.read()

with open(os.path.join(BASE_DIR, 'js', 'app.js'), 'r', encoding='utf-8') as f:
    app_js = f.read()

# Update audioManager sound paths to use inlined base64 data URIs
audio_mgr_js = audio_mgr_js.replace(
    "this.soundPaths = {\n      correct: 'assets/audio/right_answer.mp3',\n      wrong: 'assets/audio/wrong_answer.mp3',\n      tap: 'assets/audio/tap.mp3',\n      streak: 'assets/audio/streak_5.mp3',\n      ding: 'assets/audio/da_ding.mp3',\n      chime: 'assets/audio/star_chime.mp3',\n      applause: 'assets/audio/applause.mp3'\n    };",
    "this.soundPaths = " + json.dumps(audio_data_uris) + ";"
)

# In app.js, update playMascot to use animationData directly
app_js = app_js.replace(
    "this.flameAnim = lottie.loadAnimation({\n        container: flameContainer,\n        renderer: 'svg',\n        loop: true,\n        autoplay: true,\n        path: 'assets/anim/flame.json'\n      });",
    "this.flameAnim = lottie.loadAnimation({\n        container: flameContainer,\n        renderer: 'svg',\n        loop: true,\n        autoplay: true,\n        animationData: window.DUO_ANIM_DATA.flame\n      });"
)

app_js = app_js.replace(
    "this.summaryDuoAnim = lottie.loadAnimation({\n        container: summaryBox,\n        renderer: 'svg',\n        loop: true,\n        autoplay: true,\n        path: 'assets/anim/duo_cheer.json'\n      });",
    "this.summaryDuoAnim = lottie.loadAnimation({\n        container: summaryBox,\n        renderer: 'svg',\n        loop: true,\n        autoplay: true,\n        animationData: window.DUO_ANIM_DATA.cheer\n      });"
)

# Replace playMascot implementation to use animationData
play_mascot_replacement = """  playMascot(type) {
    if (!window.lottie || !this.dom.mascotBox) return;

    if (this.mascotAnim) {
      this.mascotAnim.destroy();
    }

    const animData = window.DUO_ANIM_DATA[type] || window.DUO_ANIM_DATA.waving;
    this.mascotAnim = lottie.loadAnimation({
      container: this.dom.mascotBox,
      renderer: 'svg',
      loop: type === 'waving',
      autoplay: true,
      animationData: animData
    });
  }"""

app_js = re.sub(
    r'  playMascot\(type\)\s*\{[\s\S]*?renderer:\s*\'svg\',[\s\S]*?path:\s*animPath\s*\}\);\s*\}',
    lambda m: play_mascot_replacement,
    app_js
)

# Read HTML and replace external links with inline
with open(os.path.join(BASE_DIR, 'index.html'), 'r', encoding='utf-8') as f:
    html = f.read()

# Replace <link rel="stylesheet" href="css/style.css"> with inline style
html = html.replace(
    '<link rel="stylesheet" href="css/style.css">',
    f'<style>\n{css_content}\n</style>'
)

# Scripts block
scripts_block = f"""
  <script>
  {lottie_js}
  </script>
  <script>
  {confetti_js}
  </script>
  <script>
  window.DUO_ANIM_DATA = {json.dumps(anim_json_data, ensure_ascii=False)};
  </script>
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

os.makedirs('dist_single', exist_ok=True)
with open('dist_single/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Bundled standalone index.html: {len(html)} bytes (~{round(len(html)/1024, 1)} KB)")
