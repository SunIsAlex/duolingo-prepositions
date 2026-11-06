/**
 * Duolingo Authentic Audio Manager
 * Uses Web Audio API with preloading for 0ms latency audio feedback
 */
class AudioManager {
  constructor() {
    this.enabled = localStorage.getItem('duo_sound_enabled') !== 'false';
    this.speechEnabled = localStorage.getItem('duo_speech_enabled') !== 'false';
    this.audioContext = null;
    this.buffers = {};
    this.soundPaths = {
      correct: 'assets/audio/right_answer.mp3',
      wrong: 'assets/audio/wrong_answer.mp3',
      tap: 'assets/audio/tap.mp3',
      streak: 'assets/audio/streak_5.mp3',
      ding: 'assets/audio/da_ding.mp3',
      chime: 'assets/audio/star_chime.mp3',
      applause: 'assets/audio/applause.mp3'
    };
    this.initialized = false;
  }

  init() {
    if (this.initialized) return;
    try {
      const AudioContextClass = window.AudioContext || window.webkitAudioContext;
      if (AudioContextClass) {
        this.audioContext = new AudioContextClass();
      }
      this.preloadAll();
      this.initialized = true;

      // Unlock AudioContext on very first user interaction
      const unlock = () => {
        if (this.audioContext && this.audioContext.state === 'suspended') {
          this.audioContext.resume();
        }
        window.removeEventListener('pointerdown', unlock);
        window.removeEventListener('keydown', unlock);
      };
      window.addEventListener('pointerdown', unlock, { passive: true });
      window.addEventListener('keydown', unlock, { passive: true });
    } catch (e) {
      console.warn('Web Audio initialization error:', e);
    }
  }

  async preloadAll() {
    for (const [key, path] of Object.entries(this.soundPaths)) {
      try {
        const response = await fetch(path);
        const arrayBuffer = await response.arrayBuffer();
        if (this.audioContext) {
          const audioBuffer = await this.audioContext.decodeAudioData(arrayBuffer);
          this.buffers[key] = audioBuffer;
        }
      } catch (err) {
        // Fallback: create HTML5 Audio element
        const audio = new Audio(path);
        audio.preload = 'auto';
        this.buffers[key] = audio;
      }
    }
  }

  ensureContext() {
    this.init();
    if (this.audioContext && this.audioContext.state === 'suspended') {
      this.audioContext.resume();
    }
  }

  playSound(key, volume = 1.0) {
    if (!this.enabled) return;
    this.ensureContext();

    const bufferOrAudio = this.buffers[key];
    if (!bufferOrAudio) {
      // Fallback direct Audio
      const path = this.soundPaths[key];
      if (path) {
        const a = new Audio(path);
        a.volume = volume;
        a.play().catch(() => {});
      }
      return;
    }

    if (this.audioContext && bufferOrAudio instanceof AudioBuffer) {
      try {
        const source = this.audioContext.createBufferSource();
        const gainNode = this.audioContext.createGain();
        source.buffer = bufferOrAudio;
        gainNode.gain.value = volume;
        source.connect(gainNode);
        gainNode.connect(this.audioContext.destination);
        source.start(0);
      } catch (err) {
        console.warn('Audio play error:', err);
      }
    } else if (bufferOrAudio instanceof Audio) {
      bufferOrAudio.currentTime = 0;
      bufferOrAudio.volume = volume;
      bufferOrAudio.play().catch(() => {});
    }
  }

  playCorrect(isStreak = false) {
    this.playSound('correct', 1.0);
    if (isStreak) {
      setTimeout(() => {
        this.playSound('streak', 0.9);
      }, 240);
    }
  }

  playWrong() {
    this.playSound('wrong', 0.95);
  }

  playTap() {
    this.playSound('tap', 0.6);
  }

  playChime() {
    this.playSound('chime', 0.85);
  }

  playComplete() {
    this.playSound('ding', 1.0);
    setTimeout(() => {
      this.playSound('applause', 0.7);
    }, 450);
  }

  speak(text) {
    if (!('speechSynthesis' in window)) return;
    try {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = 'en-US';
      utterance.rate = 0.92;
      utterance.pitch = 1.0;
      // Prefer natural English voices
      const voices = window.speechSynthesis.getVoices();
      const enVoice = voices.find(v => v.lang.startsWith('en') && (v.name.includes('Natural') || v.name.includes('Google') || v.name.includes('Samantha') || v.name.includes('Daniel')));
      if (enVoice) {
        utterance.voice = enVoice;
      }
      window.speechSynthesis.speak(utterance);
    } catch (e) {
      console.warn('Speech synthesis error:', e);
    }
  }

  toggleSound() {
    this.enabled = !this.enabled;
    localStorage.setItem('duo_sound_enabled', this.enabled ? 'true' : 'false');
    return this.enabled;
  }
}

const audioManager = new AudioManager();
