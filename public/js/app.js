/**
 * Duolingo English Preposition Learning Web App
 * Fully client-side, zero-login, authentic Duolingo animations and sounds
 */

// Common high-frequency prepositions for quick word bank
const FREQUENT_PREPOSITIONS = [
  'to', 'for', 'in', 'on', 'at', 'with', 'by', 'of', 'from', 'about', 'into', 'against'
];

class DuolingoApp {
  constructor() {
    this.allQuestions = [];
    this.filteredQuestions = [];
    this.currentIndex = 0;
    this.currentQuestion = null;
    this.selectedWord = '';
    this.isAnswerChecked = false;
    this.mode = 'lesson'; // 'lesson' (10 questions per unit) or 'endless'
    this.currentCategory = 'all';

    // Stats & Progress Storage
    this.streak = parseInt(localStorage.getItem('duo_streak') || '0', 10);
    this.lastActiveDate = localStorage.getItem('duo_last_date') || '';
    this.xp = parseInt(localStorage.getItem('duo_xp') || '0', 10);
    this.totalAnswered = parseInt(localStorage.getItem('duo_total_answered') || '0', 10);
    this.totalCorrect = parseInt(localStorage.getItem('duo_total_correct') || '0', 10);
    this.history = JSON.parse(localStorage.getItem('duo_history') || '{}');
    this.mistakes = JSON.parse(localStorage.getItem('duo_mistakes') || '[]');
    this.customQuestions = JSON.parse(localStorage.getItem('duo_custom_questions') || '[]');
    this.saveTimeout = null;

    // Lesson state
    this.lessonSize = 10;
    this.lessonQueue = [];
    this.lessonCorrectCount = 0;
    this.comboCount = 0;

    // Mascot animations
    this.mascotAnim = null;
    this.flameAnim = null;
    this.summaryDuoAnim = null;

    this.initDOM();
    this.initMascot();
    this.loadQuestions();
    this.checkDailyStreak();
    this.bindEvents();
    this.startLesson();
    this.syncWithServer();
  }

  initDOM() {
    this.dom = {
      progressFill: document.getElementById('progress-fill'),
      streakCount: document.getElementById('streak-count'),
      xpCount: document.getElementById('xp-count'),
      soundToggleBtn: document.getElementById('sound-toggle-btn'),
      mistakeBadge: document.getElementById('mistake-badge'),
      mistakeCount: document.getElementById('mistake-count'),

      // Filters
      tabChips: document.querySelectorAll('.tab-chip'),

      // Mascot & Prompt
      mascotBox: document.getElementById('duo-mascot-anim'),
      promptTitle: document.getElementById('prompt-title'),
      categoryTag: document.getElementById('category-tag'),
      bubblePhrase: document.getElementById('bubble-phrase'),
      bubbleCn: document.getElementById('bubble-cn'),
      speakerBtn: document.getElementById('speaker-btn'),

      // Sentence & Input
      clozeSentence: document.getElementById('cloze-sentence'),
      clozeTranslation: document.getElementById('cloze-translation'),
      wordTilesContainer: document.getElementById('word-tiles'),

      // Bottom Bar & Feedback Sheet
      bottomBar: document.getElementById('bottom-bar'),
      checkBtn: document.getElementById('check-btn'),
      skipBtn: document.getElementById('skip-btn'),
      feedbackSheet: document.getElementById('feedback-sheet'),
      feedbackTitle: document.getElementById('feedback-title'),
      feedbackHighlight: document.getElementById('feedback-highlight'),
      feedbackExplanation: document.getElementById('feedback-explanation'),
      feedbackContinueBtn: document.getElementById('feedback-continue-btn'),

      // Summary Modal
      summaryModal: document.getElementById('summary-modal'),
      summaryAccuracy: document.getElementById('summary-accuracy'),
      summaryXp: document.getElementById('summary-xp'),
      summaryStreak: document.getElementById('summary-streak'),
      summaryContinueBtn: document.getElementById('summary-continue-btn'),

      // Stats Dashboard Modal
      statsModal: document.getElementById('stats-modal'),
      openStatsModalBtn: document.getElementById('open-stats-modal-btn'),
      openStatsBadge: document.getElementById('open-stats-badge'),
      closeStatsModalBtn: document.getElementById('close-stats-modal-btn'),
      exportProgressBtn: document.getElementById('export-progress-btn'),
      importProgressBtn: document.getElementById('import-progress-btn'),
      importProgressFile: document.getElementById('import-progress-file'),
      resetProgressBtn: document.getElementById('reset-progress-btn'),
      statTotalAnswered: document.getElementById('stat-total-answered'),
      statAccuracy: document.getElementById('stat-accuracy'),
      statMasteredCount: document.getElementById('stat-mastered-count'),
      statMistakesCount: document.getElementById('stat-mistakes-count'),
      statStreakVal: document.getElementById('stat-streak-val'),
      statXpVal: document.getElementById('stat-xp-val'),

      // Custom Question Modal
      customModal: document.getElementById('custom-modal'),
      openCustomModalBtn: document.getElementById('open-custom-modal-btn'),
      closeCustomModalBtn: document.getElementById('close-custom-modal-btn'),
      saveCustomQuestionBtn: document.getElementById('save-custom-question-btn'),
      customPhraseInput: document.getElementById('custom-phrase'),
      customSentenceInput: document.getElementById('custom-sentence'),
      customAnswerInput: document.getElementById('custom-answer'),
      customCnInput: document.getElementById('custom-cn'),
      customExplInput: document.getElementById('custom-expl')
    };

    // Update initial UI stats
    this.updateStatsUI();
    this.updateSoundToggleIcon();
  }

  initMascot() {
    // Top bar flame animation
    const flameContainer = document.getElementById('flame-anim');
    if (flameContainer && window.lottie) {
      this.flameAnim = lottie.loadAnimation({
        container: flameContainer,
        renderer: 'svg',
        loop: true,
        autoplay: true,
        path: 'assets/anim/flame.json'
      });
    }

    // Default mascot animation
    this.playMascot('waving');
  }

  playMascot(type) {
    if (!window.lottie || !this.dom.mascotBox) return;

    if (this.mascotAnim) {
      this.mascotAnim.destroy();
    }

    const paths = {
      waving: 'assets/anim/duo_waving.json',
      cheer: 'assets/anim/duo_cheer.json',
      hop: 'assets/anim/duo_hop.json',
      sad: 'assets/anim/duo_sad.json',
      super: 'assets/anim/duo_super_jumping.json'
    };

    const animPath = paths[type] || paths.waving;
    this.mascotAnim = lottie.loadAnimation({
      container: this.dom.mascotBox,
      renderer: 'svg',
      loop: type === 'waving',
      autoplay: true,
      path: animPath
    });
  }

  loadQuestions() {
    const baseQuestions = (typeof PREPOSITION_QUESTIONS !== 'undefined') ? PREPOSITION_QUESTIONS : [];
    this.allQuestions = [...baseQuestions, ...this.customQuestions];
    this.applyCategoryFilter('all');
  }

  applyCategoryFilter(category) {
    this.currentCategory = category;
    this.dom.tabChips.forEach(chip => {
      if (chip.dataset.category === category) {
        chip.classList.add('active');
      } else {
        chip.classList.remove('active');
      }
    });

    if (category === 'all') {
      this.filteredQuestions = [...this.allQuestions];
    } else if (category === 'mistakes') {
      this.filteredQuestions = this.allQuestions.filter(q => this.mistakes.includes(q.id));
      if (this.filteredQuestions.length === 0) {
        alert('太棒了！当前错题本为空。为您自动加载全部题目练习。');
        this.applyCategoryFilter('all');
        return;
      }
    } else {
      this.filteredQuestions = this.allQuestions.filter(q => q.category === category);
    }

    this.startLesson();
  }

  startLesson() {
    // Shuffle and pick 10 questions for unit mode, or endless
    const shuffled = [...this.filteredQuestions].sort(() => Math.random() - 0.5);
    if (this.mode === 'lesson') {
      this.lessonQueue = shuffled.slice(0, Math.min(this.lessonSize, shuffled.length));
    } else {
      this.lessonQueue = shuffled;
    }

    this.currentIndex = 0;
    this.lessonCorrectCount = 0;
    this.comboCount = 0;
    this.renderCurrentQuestion();
    this.updateProgressBar();
  }

  renderCurrentQuestion() {
    if (this.currentIndex >= this.lessonQueue.length) {
      this.finishLesson();
      return;
    }

    this.isAnswerChecked = false;
    this.selectedWord = '';
    this.closeFeedbackSheet();

    const q = this.lessonQueue[this.currentIndex];
    this.currentQuestion = q;

    // Reset mascot to waving/idle
    this.playMascot('waving');

    // Fill Header & Prompt
    this.dom.categoryTag.textContent = q.category || '语法填空';
    this.dom.bubblePhrase.textContent = q.phrase.replace('___', '______');
    this.dom.bubbleCn.textContent = q.sentence_cn || '';

    // Render Cloze Sentence with inline input
    this.renderClozeSentence(q);

    // Render Word Bank Tiles
    this.renderWordTiles(q);

    // Reset Check Button
    this.updateCheckButtonState();
  }

  renderClozeSentence(q) {
    const container = this.dom.clozeSentence;
    container.innerHTML = '';

    const sentence = q.sentence;
    // Split by ___ or placeholder
    const parts = sentence.split(/_{2,}/);

    if (parts.length > 1) {
      const partBefore = document.createTextNode(parts[0]);
      container.appendChild(partBefore);

      const wrap = document.createElement('span');
      wrap.className = 'cloze-input-wrap';

      const input = document.createElement('input');
      input.type = 'text';
      input.className = 'cloze-input';
      input.id = 'active-cloze-input';
      input.autocomplete = 'off';
      input.autocapitalize = 'off';
      input.spellcheck = false;
      input.placeholder = '?';
      input.maxLength = 15;
      input.setAttribute('enterkeyhint', 'done');

      input.addEventListener('input', (e) => {
        this.selectedWord = e.target.value.trim().toLowerCase();
        this.highlightSelectedTile(this.selectedWord);
        this.updateCheckButtonState();
      });

      input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.keyCode === 13) {
          e.preventDefault();
          this.handleCheckOrContinue();
        }
      });

      wrap.appendChild(input);
      container.appendChild(wrap);

      const partAfter = document.createTextNode(parts.slice(1).join('___'));
      container.appendChild(partAfter);

      // Connect form submit
      const form = document.getElementById('cloze-form');
      if (form) {
        form.onsubmit = (ev) => {
          ev.preventDefault();
          this.handleCheckOrContinue();
          return false;
        };
      }

      // Auto-focus after render
      setTimeout(() => input.focus(), 80);
    } else {
      // Fallback
      container.textContent = sentence;
    }

    this.dom.clozeTranslation.textContent = q.sentence_cn || '';
  }

  renderWordTiles(q) {
    const tilesContainer = this.dom.wordTilesContainer;
    tilesContainer.innerHTML = '';

    // Pick candidate prepositions including correct answer and frequent prepositions
    const correctAns = q.answer.toLowerCase();
    const candidateSet = new Set([correctAns]);

    // Add 7 other random frequent prepositions
    const shuffledFreq = [...FREQUENT_PREPOSITIONS].sort(() => Math.random() - 0.5);
    for (const prep of shuffledFreq) {
      if (candidateSet.size >= 8) break;
      candidateSet.add(prep);
    }

    const tileList = Array.from(candidateSet).sort();

    tileList.forEach(word => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'word-tile';
      btn.dataset.word = word;
      btn.textContent = word;

      btn.addEventListener('click', () => {
        audioManager.playTap();
        this.selectWordTile(word);
      });

      tilesContainer.appendChild(btn);
    });
  }

  selectWordTile(word) {
    const input = document.getElementById('active-cloze-input');
    if (this.selectedWord === word) {
      // Toggle off / clear
      this.selectedWord = '';
      if (input) {
        input.value = '';
        input.classList.remove('filled');
        input.focus();
      }
      this.highlightSelectedTile('');
    } else {
      // Select word
      this.selectedWord = word;
      if (input) {
        input.value = word;
        input.classList.add('filled');
        input.focus();
      }
      this.highlightSelectedTile(word);
    }
    this.updateCheckButtonState();
  }

  highlightSelectedTile(word) {
    const tiles = this.dom.wordTilesContainer.querySelectorAll('.word-tile');
    tiles.forEach(tile => {
      if (tile.dataset.word === word) {
        tile.classList.add('selected');
      } else {
        tile.classList.remove('selected');
      }
    });
  }

  updateCheckButtonState() {
    const hasInput = (this.selectedWord && this.selectedWord.trim().length > 0);
    this.dom.checkBtn.disabled = !hasInput;
  }

  handleCheckOrContinue() {
    if (!this.isAnswerChecked) {
      this.checkAnswer();
    } else {
      this.nextQuestion();
    }
  }

  checkAnswer() {
    const inputElem = document.getElementById('active-cloze-input');
    if (inputElem && inputElem.value) {
      this.selectedWord = inputElem.value.trim().toLowerCase();
    }

    if (!this.selectedWord || this.selectedWord.trim().length === 0) {
      if (inputElem) {
        inputElem.classList.add('shake');
        setTimeout(() => inputElem.classList.remove('shake'), 400);
        inputElem.focus();
      }
      return;
    }

    this.isAnswerChecked = true;

    const userInput = this.selectedWord.trim().toLowerCase();
    const q = this.currentQuestion;
    const isCorrect = q.acceptable.map(a => a.toLowerCase()).includes(userInput);

    if (inputElem) {
      inputElem.disabled = true;
    }

    if (isCorrect) {
      this.handleCorrectAnswer(q, userInput);
    } else {
      this.handleWrongAnswer(q, userInput);
    }
  }

  handleCorrectAnswer(q, userInput) {
    this.lessonCorrectCount++;
    this.comboCount++;
    this.xp += 10;
    this.totalAnswered++;
    this.totalCorrect++;

    // Record question mastery history
    if (!this.history[q.id]) {
      this.history[q.id] = { attempts: 0, correct: 0, streak: 0, mastered: false, lastAnswered: Date.now() };
    }
    const h = this.history[q.id];
    h.attempts = (h.attempts || 0) + 1;
    h.correct = (h.correct || 0) + 1;
    h.streak = (h.streak || 0) + 1;
    h.lastAnswered = Date.now();
    if (h.streak >= 2) {
      h.mastered = true;
    }

    // Remove from mistakes if previously missed
    if (this.mistakes.includes(q.id)) {
      this.mistakes = this.mistakes.filter(id => id !== q.id);
      this.updateMistakeBadge();
    }

    this.saveStats(true);

    const isStreakMilestone = (this.comboCount === 5 || this.comboCount === 10);
    audioManager.playCorrect(isStreakMilestone);

    if (isStreakMilestone) {
      this.playMascot('super');
      this.triggerConfetti(false);
    } else {
      this.playMascot(Math.random() > 0.5 ? 'cheer' : 'hop');
    }

    // Open green feedback sheet
    this.openFeedbackSheet(true, q, userInput);
  }

  handleWrongAnswer(q, userInput) {
    this.comboCount = 0;
    this.totalAnswered++;

    // Record question mastery history
    if (!this.history[q.id]) {
      this.history[q.id] = { attempts: 0, correct: 0, streak: 0, mastered: false, lastAnswered: Date.now() };
    }
    const h = this.history[q.id];
    h.attempts = (h.attempts || 0) + 1;
    h.streak = 0;
    h.lastAnswered = Date.now();

    // Record into mistakes
    if (!this.mistakes.includes(q.id)) {
      this.mistakes.push(q.id);
      this.updateMistakeBadge();
    }

    this.saveStats(true);

    audioManager.playWrong();
    this.playMascot('sad');

    // Open red feedback sheet
    this.openFeedbackSheet(false, q, userInput);
  }

  openFeedbackSheet(isCorrect, q, userInput) {
    const sheet = this.dom.feedbackSheet;
    sheet.className = `feedback-sheet ${isCorrect ? 'correct' : 'wrong'} open`;

    if (isCorrect) {
      const titles = ['太棒了！', '回答完全正确！', '太赞了！', '非常出色！'];
      this.dom.feedbackTitle.textContent = titles[Math.floor(Math.random() * titles.length)];
      
      const fullPhrase = q.phrase.replace('___', `<span class="correct-term">${q.answer}</span>`);
      this.dom.feedbackHighlight.innerHTML = `正确搭配：<b>${fullPhrase}</b>`;
    } else {
      this.dom.feedbackTitle.textContent = '正确答案是：';
      this.dom.feedbackHighlight.innerHTML = `<span class="wrong-term">${q.answer}</span> (你的回答: ${userInput || '未填写'})`;
    }

    this.dom.feedbackExplanation.innerHTML = q.explanation || '暂无详细解释。';

    // Focus continue button so space / enter immediately proceeds
    setTimeout(() => {
      this.dom.feedbackContinueBtn.focus();
    }, 120);
  }

  closeFeedbackSheet() {
    this.dom.feedbackSheet.className = 'feedback-sheet';
  }

  nextQuestion() {
    this.currentIndex++;
    this.updateProgressBar();
    this.renderCurrentQuestion();
  }

  updateProgressBar() {
    const total = this.lessonQueue.length || 1;
    const percent = Math.min(100, Math.round((this.currentIndex / total) * 100));
    this.dom.progressFill.style.width = `${percent}%`;
  }

  finishLesson() {
    audioManager.playComplete();
    this.triggerConfetti(true);

    const total = this.lessonQueue.length;
    const accuracy = total > 0 ? Math.round((this.lessonCorrectCount / total) * 100) : 100;
    const earnedXp = this.lessonCorrectCount * 10;

    this.dom.summaryAccuracy.textContent = `${accuracy}%`;
    this.dom.summaryXp.textContent = `+${earnedXp}`;
    this.dom.summaryStreak.textContent = `${this.streak}天`;

    // Render Duo celebration in modal
    const summaryBox = document.getElementById('summary-duo-anim');
    if (summaryBox && window.lottie) {
      if (this.summaryDuoAnim) this.summaryDuoAnim.destroy();
      this.summaryDuoAnim = lottie.loadAnimation({
        container: summaryBox,
        renderer: 'svg',
        loop: true,
        autoplay: true,
        path: 'assets/anim/duo_cheer.json'
      });
    }

    this.dom.summaryModal.classList.add('open');
  }

  triggerConfetti(full = false) {
    if (!window.confetti) return;
    if (full) {
      confetti({
        particleCount: 80,
        spread: 70,
        origin: { y: 0.6 }
      });
    } else {
      confetti({
        particleCount: 30,
        spread: 45,
        origin: { y: 0.7 }
      });
    }
  }

  checkDailyStreak() {
    const today = new Date().toISOString().slice(0, 10);
    if (!this.lastActiveDate) {
      this.streak = 1;
      this.lastActiveDate = today;
    } else if (this.lastActiveDate !== today) {
      const last = new Date(this.lastActiveDate);
      const curr = new Date(today);
      const diffDays = Math.round((curr - last) / (1000 * 3600 * 24));
      if (diffDays === 1) {
        this.streak += 1;
      } else if (diffDays > 1) {
        this.streak = 1;
      }
      this.lastActiveDate = today;
    }
    this.saveStats(true);
  }

  async syncWithServer() {
    try {
      const resp = await fetch('/api/progress');
      if (resp.ok) {
        const s = await resp.json();
        let changed = false;

        if (s.streak && s.streak > this.streak) {
          this.streak = s.streak;
          changed = true;
        }
        if (s.xp && s.xp > this.xp) {
          this.xp = s.xp;
          changed = true;
        }
        if (s.totalAnswered && s.totalAnswered > this.totalAnswered) {
          this.totalAnswered = s.totalAnswered;
          changed = true;
        }
        if (s.totalCorrect && s.totalCorrect > this.totalCorrect) {
          this.totalCorrect = s.totalCorrect;
          changed = true;
        }
        if (s.lastActiveDate && (!this.lastActiveDate || s.lastActiveDate > this.lastActiveDate)) {
          this.lastActiveDate = s.lastActiveDate;
          changed = true;
        }

        // Merge question history
        if (s.history && typeof s.history === 'object') {
          for (const [qid, data] of Object.entries(s.history)) {
            if (!this.history[qid]) {
              this.history[qid] = data;
              changed = true;
            } else {
              if ((data.attempts || 0) > (this.history[qid].attempts || 0)) {
                this.history[qid].attempts = data.attempts;
                this.history[qid].correct = Math.max(this.history[qid].correct || 0, data.correct || 0);
                this.history[qid].mastered = this.history[qid].mastered || data.mastered;
                changed = true;
              }
            }
          }
        }

        // Merge mistakes
        if (Array.isArray(s.mistakes)) {
          const mSet = new Set([...this.mistakes, ...s.mistakes]);
          if (mSet.size !== this.mistakes.length) {
            this.mistakes = Array.from(mSet);
            changed = true;
          }
        }

        // Merge custom questions
        if (Array.isArray(s.customQuestions)) {
          const existingIds = new Set(this.customQuestions.map(q => q.id));
          for (const q of s.customQuestions) {
            if (!existingIds.has(q.id)) {
              this.customQuestions.push(q);
              existingIds.add(q.id);
              changed = true;
            }
          }
          if (changed) {
            this.loadQuestions();
          }
        }

        this.saveStats(false);
        this.updateStatsUI();
      }
    } catch (e) {
      console.warn('Working in offline/local mode:', e);
    }
  }

  saveProgressToServer() {
    clearTimeout(this.saveTimeout);
    this.saveTimeout = setTimeout(async () => {
      const payload = {
        streak: this.streak,
        lastActiveDate: this.lastActiveDate,
        xp: this.xp,
        totalAnswered: this.totalAnswered,
        totalCorrect: this.totalCorrect,
        history: this.history,
        mistakes: this.mistakes,
        customQuestions: this.customQuestions
      };

      const syncBadge = document.getElementById('sync-status-badge');
      const syncText = document.getElementById('sync-status-text');
      if (syncBadge) syncBadge.classList.add('syncing');
      if (syncText) syncText.textContent = '正在自动同步至服务端...';

      try {
        const resp = await fetch('/api/progress', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        if (resp.ok) {
          if (syncBadge) syncBadge.classList.remove('syncing');
          if (syncText) syncText.textContent = '已自动同步至本地与服务端';
        }
      } catch (err) {
        if (syncBadge) syncBadge.classList.remove('syncing');
        if (syncText) syncText.textContent = '已保存至本地 (离线模式)';
      }
    }, 300);
  }

  saveStats(syncServer = true) {
    localStorage.setItem('duo_streak', this.streak.toString());
    localStorage.setItem('duo_last_date', this.lastActiveDate);
    localStorage.setItem('duo_xp', this.xp.toString());
    localStorage.setItem('duo_total_answered', this.totalAnswered.toString());
    localStorage.setItem('duo_total_correct', this.totalCorrect.toString());
    localStorage.setItem('duo_history', JSON.stringify(this.history));
    localStorage.setItem('duo_mistakes', JSON.stringify(this.mistakes));
    localStorage.setItem('duo_custom_questions', JSON.stringify(this.customQuestions));

    this.updateStatsUI();

    if (syncServer) {
      this.saveProgressToServer();
    }
  }

  updateStatsUI() {
    if (this.dom.streakCount) this.dom.streakCount.textContent = this.streak;
    if (this.dom.xpCount) this.dom.xpCount.textContent = this.xp;
    this.updateMistakeBadge();

    // Update Dashboard Modal values
    if (this.dom.statTotalAnswered) this.dom.statTotalAnswered.textContent = this.totalAnswered;
    if (this.dom.statAccuracy) {
      const acc = this.totalAnswered > 0 ? Math.round((this.totalCorrect / this.totalAnswered) * 100) : 100;
      this.dom.statAccuracy.textContent = `${acc}%`;
    }
    if (this.dom.statMasteredCount) {
      const mastered = Object.values(this.history).filter(h => h && h.mastered).length;
      this.dom.statMasteredCount.textContent = `${mastered} / ${this.allQuestions.length}`;
    }
    if (this.dom.statMistakesCount) this.dom.statMistakesCount.textContent = this.mistakes.length;
    if (this.dom.statStreakVal) this.dom.statStreakVal.textContent = `${this.streak}天`;
    if (this.dom.statXpVal) this.dom.statXpVal.textContent = this.xp;
  }

  exportProgress() {
    const data = {
      streak: this.streak,
      lastActiveDate: this.lastActiveDate,
      xp: this.xp,
      totalAnswered: this.totalAnswered,
      totalCorrect: this.totalCorrect,
      history: this.history,
      mistakes: this.mistakes,
      customQuestions: this.customQuestions,
      exportedAt: new Date().toISOString()
    };
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `duolingo_prepositions_progress_${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
  }

  importProgress(file) {
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const d = JSON.parse(e.target.result);
        if (typeof d !== 'object' || d === null) throw new Error('Invalid format');
        this.streak = d.streak || this.streak;
        this.xp = d.xp || this.xp;
        this.totalAnswered = d.totalAnswered || this.totalAnswered;
        this.totalCorrect = d.totalCorrect || this.totalCorrect;
        if (d.history) this.history = d.history;
        if (Array.isArray(d.mistakes)) this.mistakes = d.mistakes;
        if (Array.isArray(d.customQuestions)) this.customQuestions = d.customQuestions;

        this.saveStats(true);
        this.loadQuestions();
        alert('🎉 学习进度成功导入并同步！');
      } catch (err) {
        alert('导入失败：文件格式不正确！' + err.message);
      }
    };
    reader.readAsText(file);
  }

  async resetProgress() {
    if (!confirm('确定要重置所有学习进度吗？这会清空练习统计、经验值与错题本！')) {
      return;
    }
    this.streak = 1;
    this.xp = 0;
    this.totalAnswered = 0;
    this.totalCorrect = 0;
    this.history = {};
    this.mistakes = [];
    this.saveStats(true);
    try {
      await fetch('/api/progress/reset', { method: 'POST' });
    } catch (e) {}
    alert('学习进度已重置。');
    this.updateStatsUI();
    this.startLesson();
  }

  updateMistakeBadge() {
    if (this.dom.mistakeCount) {
      this.dom.mistakeCount.textContent = this.mistakes.length;
    }
  }

  updateSoundToggleIcon() {
    if (!this.dom.soundToggleBtn) return;
    this.dom.soundToggleBtn.innerHTML = audioManager.enabled ? '🔊' : '🔇';
  }

  speakCurrentPhrase() {
    if (!this.currentQuestion) return;
    audioManager.speak(this.currentQuestion.sentence.replace('___', this.currentQuestion.answer));
  }

  bindEvents() {
    // Check & Skip
    this.dom.checkBtn.addEventListener('click', () => {
      this.handleCheckOrContinue();
    });

    this.dom.skipBtn.addEventListener('click', () => {
      audioManager.playTap();
      this.handleWrongAnswer(this.currentQuestion, '');
    });

    this.dom.feedbackContinueBtn.addEventListener('click', () => {
      audioManager.playTap();
      this.nextQuestion();
    });

    // Speaker Speech Synthesis
    this.dom.speakerBtn.addEventListener('click', () => {
      this.speakCurrentPhrase();
    });

    // Sound toggle
    this.dom.soundToggleBtn.addEventListener('click', () => {
      audioManager.toggleSound();
      this.updateSoundToggleIcon();
      audioManager.playTap();
    });

    // Filter Category Chips
    this.dom.tabChips.forEach(chip => {
      chip.addEventListener('click', () => {
        audioManager.playTap();
        this.applyCategoryFilter(chip.dataset.category);
      });
    });

    // Summary Modal Continue
    this.dom.summaryContinueBtn.addEventListener('click', () => {
      audioManager.playTap();
      this.dom.summaryModal.classList.remove('open');
      this.startLesson();
    });

    // Custom Question Modal
    this.dom.openCustomModalBtn.addEventListener('click', () => {
      audioManager.playTap();
      this.dom.customModal.classList.add('open');
    });

    this.dom.closeCustomModalBtn.addEventListener('click', () => {
      this.dom.customModal.classList.remove('open');
    });

    this.dom.saveCustomQuestionBtn.addEventListener('click', () => {
      this.saveCustomQuestion();
    });

    // Stats Dashboard Modal
    if (this.dom.openStatsModalBtn) {
      this.dom.openStatsModalBtn.addEventListener('click', () => {
        audioManager.playTap();
        this.updateStatsUI();
        this.dom.statsModal.classList.add('open');
      });
    }

    if (this.dom.openStatsBadge) {
      this.dom.openStatsBadge.addEventListener('click', () => {
        audioManager.playTap();
        this.updateStatsUI();
        this.dom.statsModal.classList.add('open');
      });
    }

    if (this.dom.closeStatsModalBtn) {
      this.dom.closeStatsModalBtn.addEventListener('click', () => {
        this.dom.statsModal.classList.remove('open');
      });
    }

    if (this.dom.exportProgressBtn) {
      this.dom.exportProgressBtn.addEventListener('click', () => {
        audioManager.playTap();
        this.exportProgress();
      });
    }

    if (this.dom.importProgressBtn) {
      this.dom.importProgressBtn.addEventListener('click', () => {
        audioManager.playTap();
        this.dom.importProgressFile.click();
      });
    }

    if (this.dom.importProgressFile) {
      this.dom.importProgressFile.addEventListener('change', (e) => {
        if (e.target.files && e.target.files[0]) {
          this.importProgress(e.target.files[0]);
          e.target.value = '';
        }
      });
    }

    if (this.dom.resetProgressBtn) {
      this.dom.resetProgressBtn.addEventListener('click', () => {
        audioManager.playTap();
        this.resetProgress();
      });
    }

    // Keyboard Shortcuts (Enter to Submit & Enter to Continue)
    window.addEventListener('keydown', (e) => {
      // Do not intercept if user is inside the custom question modal
      if (this.dom.customModal && this.dom.customModal.classList.contains('open')) {
        return;
      }

      const isEnter = (e.key === 'Enter' || e.keyCode === 13);
      const isSpace = (e.key === ' ' || e.keyCode === 32);

      if (isEnter) {
        e.preventDefault();
        if (this.dom.feedbackSheet.classList.contains('open')) {
          audioManager.playTap();
          this.nextQuestion();
        } else if (this.dom.summaryModal.classList.contains('open')) {
          audioManager.playTap();
          this.dom.summaryModal.classList.remove('open');
          this.startLesson();
        } else {
          // Question answering state: Enter checks & submits answer!
          this.handleCheckOrContinue();
        }
      } else if (isSpace) {
        if (this.dom.feedbackSheet.classList.contains('open')) {
          e.preventDefault();
          audioManager.playTap();
          this.nextQuestion();
        } else if (this.dom.summaryModal.classList.contains('open')) {
          e.preventDefault();
          audioManager.playTap();
          this.dom.summaryModal.classList.remove('open');
          this.startLesson();
        }
      }
    });
  }

  saveCustomQuestion() {
    const phrase = this.dom.customPhraseInput.value.trim();
    const sentence = this.dom.customSentenceInput.value.trim();
    const answer = this.dom.customAnswerInput.value.trim().toLowerCase();
    const cn = this.dom.customCnInput.value.trim();
    const expl = this.dom.customExplInput.value.trim();

    if (!phrase || !sentence || !answer) {
      alert('请至少填写短语、例句和介词答案！');
      return;
    }

    const newQ = {
      id: 'custom_' + Date.now(),
      phrase: phrase.includes('___') ? phrase : `${phrase} ___`,
      sentence: sentence.includes('___') ? sentence : sentence.replace(answer, '___'),
      sentence_cn: cn,
      answer: answer,
      acceptable: [answer],
      category: '自定义',
      difficulty: 1,
      explanation: expl ? `【自定义解析】${expl}` : '【自定义解析】由用户自行录入的专项介词搭配。',
      tags: ['自建题库']
    };

    this.customQuestions.push(newQ);
    localStorage.setItem('duo_custom_questions', JSON.stringify(this.customQuestions));
    this.allQuestions.push(newQ);

    alert('自选题目添加成功！');
    this.dom.customPhraseInput.value = '';
    this.dom.customSentenceInput.value = '';
    this.dom.customAnswerInput.value = '';
    this.dom.customCnInput.value = '';
    this.dom.customExplInput.value = '';
    this.dom.customModal.classList.remove('open');

    this.loadQuestions();
  }
}

// Global initialization
document.addEventListener('DOMContentLoaded', () => {
  window.duoApp = new DuolingoApp();
});
