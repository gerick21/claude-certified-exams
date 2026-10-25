/**
 * Multi-Track Certification Practice Exam Portal
 * Supports:
 *   1. Claude Certified Developer (Foundations) - CCDV-F
 *   2. Claude Certified Solutions Architect (Foundations) - CCSA-F
 * 5 Full Practice Exams per track • 265 Questions per track • Isolated LocalStorage Persistence
 */

// Fallback Developer Blueprint Domains (used if registry.js is not loaded)
const DOMAINS_META = {
  1: { name: "Agents and Workflows", weight: "14.7%", targetPerExam: 8 },
  2: { name: "Applications and Integration", weight: "33.1%", targetPerExam: 17 },
  3: { name: "Claude Code", weight: "3.1%", targetPerExam: 2 },
  4: { name: "Eval, Testing, and Debugging", weight: "2.6%", targetPerExam: 2 },
  5: { name: "Model Selection and Optimization", weight: "16.8%", targetPerExam: 9 },
  6: { name: "Prompt and Context Engineering", weight: "11.0%", targetPerExam: 6 },
  7: { name: "Security and Safety", weight: "8.1%", targetPerExam: 4 },
  8: { name: "Tools and MCPs", weight: "10.6%", targetPerExam: 5 }
};

// Application State
const appState = {
  activeTrack: 'developer', // 'developer' | 'architect'
  exams: [],                // Active track exam objects
  activeExamId: 1,          // 1 to 5
  currentView: 'home',      // 'home' | 'exam'
  activeFilter: 'all',      // 'all' | 'answered' | 'unanswered' | 'flagged' | 'incorrect'
  timerInterval: null,
  progress: {}              // Per-exam progress: examId -> { currentIndex, userAnswers, submitted, flagged: Set, mode, timerSeconds, completed }
};

// ─── Track & Domain Helper Functions ─────────────────────────────────────────

function getActiveTrack() {
  return appState.activeTrack || 'developer';
}

function getActiveTrackMeta() {
  const track = getActiveTrack();
  if (typeof TRACKS !== 'undefined' && TRACKS[track]) {
    return TRACKS[track];
  }
  return {
    id: track,
    code: track === 'architect' ? 'CCSA-F' : 'CCDV-F',
    name: track === 'architect' ? 'Claude Certified Solutions Architect (Foundations)' : 'Claude Certified Developer (Foundations)',
    heroTitle: track === 'architect' ? 'Claude Certified Architect Practice Portal' : 'Claude Certified Developer Practice Portal',
    heroDescription: track === 'architect'
      ? 'Master all 5 official blueprint domains with <strong>5 full-length, scenario-based practice exams</strong> (265 unique questions total).'
      : 'Master all 8 official blueprint domains with <strong>5 full-length, scenario-based practice exams</strong> (265 unique questions total).',
    domains: track === 'architect' ? (typeof ARCHITECT_DOMAINS !== 'undefined' ? ARCHITECT_DOMAINS : {}) : (typeof DEVELOPER_DOMAINS !== 'undefined' ? DEVELOPER_DOMAINS : DOMAINS_META),
    passingScore: 720
  };
}

function getActiveDomains() {
  const meta = getActiveTrackMeta();
  return meta.domains || DOMAINS_META;
}

function getDomainMeta(domainId) {
  const domains = getActiveDomains();
  return domains[domainId] || { name: `Domain ${domainId}`, weight: '10%' };
}

function getStorageKey() {
  const track = getActiveTrack();
  if (typeof STORAGE_KEYS !== 'undefined' && STORAGE_KEYS[track]) {
    return STORAGE_KEYS[track];
  }
  return `cc_${track}_exam_storage_v1`;
}

// Cached DOM Elements
let el = {};

function initDOMElements() {
  el = {
    // Views
    homeView: document.getElementById('home-view'),
    examView: document.getElementById('exam-view'),
    btnNavHome: document.getElementById('btn-nav-home'),
    btnToggleView: document.getElementById('btn-toggle-view'),
    btnToggleViewText: document.getElementById('btn-toggle-view-text'),
    examSelect: document.getElementById('exam-select'),
    examSwitcherContainer: document.getElementById('exam-switcher-container'),
    headerExamTag: document.getElementById('header-exam-tag'),
    headerExamStats: document.getElementById('header-exam-stats'),
    headerHomeStats: document.getElementById('header-home-stats'),
    examModeToggle: document.getElementById('exam-mode-toggle'),
    examProgressBarContainer: document.getElementById('exam-progress-bar-container'),
    progressBarFill: document.getElementById('progress-bar-fill'),

    // Brand & Track Switcher Elements
    brandText: document.getElementById('brand-text'),
    pillTrackDeveloper: document.getElementById('pill-track-developer'),
    pillTrackArchitect: document.getElementById('pill-track-architect'),
    cardTrackDeveloper: document.getElementById('card-track-developer'),
    cardTrackArchitect: document.getElementById('card-track-architect'),
    heroBadgeText: document.getElementById('hero-badge-text'),
    heroTitle: document.getElementById('hero-title'),
    heroDescription: document.getElementById('hero-description'),

    // Home view header stats
    homeHeadAnswered: document.getElementById('home-head-answered'),
    homeHeadAccuracy: document.getElementById('home-head-accuracy'),
    homeHeadStatus: document.getElementById('home-head-status'),

    // Home view dashboard elements
    statOverallPct: document.getElementById('stat-overall-pct'),
    statOverallAnswered: document.getElementById('stat-overall-answered'),
    statOverallBar: document.getElementById('stat-overall-bar'),
    statAccuracyBadge: document.getElementById('stat-accuracy-badge'),
    statOverallCorrect: document.getElementById('stat-overall-correct'),
    statAccuracySubtext: document.getElementById('stat-accuracy-subtext'),
    statOverallPill: document.getElementById('stat-overall-pill'),
    statOverallScaled: document.getElementById('stat-overall-scaled'),
    statCompletedBadge: document.getElementById('stat-completed-badge'),
    statExamsPassed: document.getElementById('stat-exams-passed'),
    statLastActiveText: document.getElementById('stat-last-active-text'),
    examCardsGrid: document.getElementById('exam-cards-grid'),
    domainAggregateGrid: document.getElementById('domain-aggregate-grid'),

    // Home view storage actions
    btnExportProgress: document.getElementById('btn-export-progress'),
    btnImportProgress: document.getElementById('btn-import-progress'),
    importFileInput: document.getElementById('import-file-input'),
    btnResetAll: document.getElementById('btn-reset-all'),

    // Exam View Live Stats
    scoreCorrect: document.getElementById('score-correct'),
    scoreAttempted: document.getElementById('score-attempted'),
    scorePct: document.getElementById('score-pct'),
    scaledScore: document.getElementById('scaled-score'),
    statusPill: document.getElementById('status-pill'),
    timerDisplay: document.getElementById('timer-display'),
    btnModePractice: document.getElementById('btn-mode-practice'),
    btnModeExam: document.getElementById('btn-mode-exam'),
    btnResetCurrentExam: document.getElementById('btn-reset-current-exam'),

    // Question Workspace
    questionCard: document.getElementById('question-card'),
    qNumberBadge: document.getElementById('q-number-badge'),
    qDomainPill: document.getElementById('q-domain-pill'),
    qSubskillPill: document.getElementById('q-subskill-pill'),
    qModuleTag: document.getElementById('q-module-tag'),
    btnFlag: document.getElementById('btn-flag'),
    flagText: document.getElementById('flag-text'),
    scenarioText: document.getElementById('scenario-text'),
    multiSelectHint: document.getElementById('multi-select-hint'),
    optionsContainer: document.getElementById('options-container'),
    multiSubmitWrapper: document.getElementById('multi-submit-wrapper'),
    btnSubmitMulti: document.getElementById('btn-submit-multi'),

    // Feedback Panel
    feedbackPanel: document.getElementById('feedback-panel'),
    feedbackBanner: document.getElementById('feedback-banner'),
    feedbackIcon: document.getElementById('feedback-icon'),
    feedbackTitle: document.getElementById('feedback-title'),
    feedbackExplanation: document.getElementById('feedback-explanation'),
    mindsetText: document.getElementById('mindset-text'),

    // Navigation Buttons
    btnPrev: document.getElementById('btn-prev'),
    btnNext: document.getElementById('btn-next'),
    btnClear: document.getElementById('btn-clear-selection'),
    btnFinishExam: document.getElementById('btn-finish-exam'),

    // Question Palette Modal
    paletteModal: document.getElementById('palette-modal'),
    paletteSubtitle: document.getElementById('palette-subtitle'),
    btnOpenPalette: document.getElementById('btn-open-palette'),
    btnClosePalette: document.getElementById('btn-close-palette'),
    paletteGrid: document.getElementById('palette-grid'),
    countAnswered: document.getElementById('count-answered'),
    countUnanswered: document.getElementById('count-unanswered'),
    countFlagged: document.getElementById('count-flagged'),
    countIncorrect: document.getElementById('count-incorrect'),

    // Breakdown Modal
    breakdownModal: document.getElementById('breakdown-modal'),
    breakdownTitle: document.getElementById('breakdown-title'),
    btnOpenBreakdown: document.getElementById('btn-open-breakdown'),
    btnCloseBreakdown: document.getElementById('btn-close-breakdown'),
    domainsTableBody: document.getElementById('domains-table-body'),
    breakdownSummaryBanner: document.getElementById('breakdown-summary-banner'),

    // Results Modal
    resultsModal: document.getElementById('results-modal'),
    resultVerdict: document.getElementById('result-verdict'),
    resultsTitle: document.getElementById('results-title'),
    resultsSubtitle: document.getElementById('results-subtitle'),
    reportScaledScore: document.getElementById('report-scaled-score'),
    reportRawScore: document.getElementById('report-raw-score'),
    reportRawPct: document.getElementById('report-raw-pct'),
    reportTimeTaken: document.getElementById('report-time-taken'),
    resultsDomainsList: document.getElementById('results-domains-list'),
    btnReviewMissed: document.getElementById('btn-review-missed'),
    btnReviewAll: document.getElementById('btn-review-all'),
    btnRetakeExam: document.getElementById('btn-retake-exam'),
    btnResultsHome: document.getElementById('btn-results-home')
  };
}

// Format basic markdown like backticks
function formatMarkdown(text) {
  if (!text) return '';
  let formatted = text.replace(/`([^`]+)`/g, '<code>$1</code>');
  formatted = formatted.replace(/\n/g, '<br>');
  return formatted;
}

// Get Active Exam Object
function getActiveExam() {
  if (!appState.exams || appState.exams.length === 0) return null;
  return appState.exams.find(e => e.id === appState.activeExamId) || appState.exams[0];
}

// Get or initialize active exam progress
function getExamProgress(examId) {
  if (!appState.progress[examId]) {
    appState.progress[examId] = {
      currentIndex: 0,
      userAnswers: {},     // qId -> array of option indices
      submitted: {},       // qId -> boolean
      flagged: new Set(),  // Set of qIds
      mode: 'practice',    // 'practice' | 'exam'
      timerSeconds: 120 * 60,
      completed: false,
      lastUpdated: Date.now()
    };
  }
  return appState.progress[examId];
}

// Save all progress to localStorage
function saveProgress() {
  try {
    const serializedProgress = {};
    for (const [id, p] of Object.entries(appState.progress)) {
      serializedProgress[id] = {
        currentIndex: p.currentIndex,
        userAnswers: p.userAnswers,
        submitted: p.submitted,
        flagged: Array.from(p.flagged || []),
        mode: p.mode,
        timerSeconds: p.timerSeconds,
        completed: !!p.completed,
        lastUpdated: p.lastUpdated || Date.now()
      };
    }

    const payload = {
      track: appState.activeTrack,
      activeExamId: appState.activeExamId,
      currentView: appState.currentView,
      progress: serializedProgress,
      savedAt: Date.now()
    };

    localStorage.setItem(getStorageKey(), JSON.stringify(payload));
  } catch (err) {
    console.warn('LocalStorage save failed:', err);
  }
}

// Load progress from localStorage
function loadProgress() {
  appState.progress = {};
  try {
    const storageKey = getStorageKey();
    let raw = localStorage.getItem(storageKey);

    // Backwards compatibility migration for Developer track
    if (!raw && appState.activeTrack === 'developer') {
      const legacyKey = (typeof LEGACY_STORAGE_KEY !== 'undefined') ? LEGACY_STORAGE_KEY : 'ccdv_exam_suite_storage_v2';
      raw = localStorage.getItem(legacyKey);
      if (raw) {
        localStorage.setItem(storageKey, raw);
      }
    }

    if (!raw) return;

    const data = JSON.parse(raw);
    if (data.activeExamId) appState.activeExamId = data.activeExamId;
    if (data.currentView) appState.currentView = data.currentView;

    if (data.progress) {
      for (const [id, p] of Object.entries(data.progress)) {
        appState.progress[id] = {
          currentIndex: p.currentIndex || 0,
          userAnswers: p.userAnswers || {},
          submitted: p.submitted || {},
          flagged: new Set(p.flagged || []),
          mode: p.mode || 'practice',
          timerSeconds: typeof p.timerSeconds === 'number' ? p.timerSeconds : 120 * 60,
          completed: !!p.completed,
          lastUpdated: p.lastUpdated || Date.now()
        };
      }
    }
  } catch (err) {
    console.warn('LocalStorage load failed:', err);
  }
}

// Load track-specific questions data
function loadTrackData(trackId) {
  if (trackId === 'architect') {
    if (typeof EXAMS_DATA_ARCHITECT !== 'undefined' && Array.isArray(EXAMS_DATA_ARCHITECT) && EXAMS_DATA_ARCHITECT.length > 0) {
      appState.exams = EXAMS_DATA_ARCHITECT;
      return;
    }
  } else {
    if (typeof EXAMS_DATA_DEVELOPER !== 'undefined' && Array.isArray(EXAMS_DATA_DEVELOPER) && EXAMS_DATA_DEVELOPER.length > 0) {
      appState.exams = EXAMS_DATA_DEVELOPER;
      return;
    }
    if (typeof EXAMS_SUITE !== 'undefined' && Array.isArray(EXAMS_SUITE) && EXAMS_SUITE.length > 0) {
      appState.exams = EXAMS_SUITE;
      return;
    }
  }
}

// Populate the exam dropdown for active track
function populateExamSelect() {
  if (!el.examSelect) return;
  el.examSelect.innerHTML = '';
  appState.exams.forEach(exam => {
    const opt = document.createElement('option');
    opt.value = exam.id;
    const cleanTitle = exam.title.replace(/^Practice Exam \d+:\s*/, '');
    opt.textContent = `Exam ${exam.id}: ${cleanTitle}`;
    el.examSelect.appendChild(opt);
  });
  el.examSelect.value = String(appState.activeExamId || 1);
}

// Update UI branding, cards, and titles based on active track
function updateTrackUI() {
  const meta = getActiveTrackMeta();
  const track = getActiveTrack();

  // Document Title
  document.title = `${meta.name} - Multi-Exam Portal (${meta.code})`;

  // Header Brand & Tag
  if (el.brandText) el.brandText.textContent = `${meta.code} Prep`;
  if (el.headerExamTag) el.headerExamTag.textContent = `${meta.examCount || 5} Exams • ${meta.totalQuestions || 265} Items`;

  // Header Pills
  if (el.pillTrackDeveloper) el.pillTrackDeveloper.classList.toggle('active', track === 'developer');
  if (el.pillTrackArchitect) el.pillTrackArchitect.classList.toggle('active', track === 'architect');

  // Hero Dashboard Cards
  if (el.cardTrackDeveloper) el.cardTrackDeveloper.classList.toggle('active', track === 'developer');
  if (el.cardTrackArchitect) el.cardTrackArchitect.classList.toggle('active', track === 'architect');

  // Hero Text
  if (el.heroBadgeText) el.heroBadgeText.textContent = `${meta.code} Certification Prep Suite`;
  if (el.heroTitle) el.heroTitle.textContent = meta.heroTitle;
  if (el.heroDescription) el.heroDescription.innerHTML = meta.heroDescription;
}

// Switch certification track
function switchTrack(trackId) {
  if (!trackId || (trackId === appState.activeTrack && appState.exams.length > 0)) return;
  saveProgress();
  appState.activeTrack = trackId;
  appState.activeExamId = 1;

  try {
    localStorage.setItem('cc_active_track', trackId);
  } catch (e) {}

  loadTrackData(trackId);
  loadProgress();
  updateTrackUI();
  populateExamSelect();
  renderDashboard();

  if (appState.currentView === 'exam') {
    selectExam(1);
  }
}

// Switch between 'home' and 'exam' views
function switchView(targetView) {
  appState.currentView = targetView;

  if (targetView === 'home') {
    el.homeView.classList.remove('hidden');
    el.examView.classList.add('hidden');

    el.headerHomeStats.classList.remove('hidden');
    el.headerExamStats.classList.add('hidden');
    el.examSwitcherContainer.classList.add('hidden');
    el.examModeToggle.classList.add('hidden');
    el.btnOpenPalette.classList.add('hidden');
    el.btnResetCurrentExam.classList.add('hidden');
    el.examProgressBarContainer.classList.add('hidden');

    el.btnToggleViewText.textContent = `Resume Exam ${appState.activeExamId}`;
    renderDashboard();
  } else {
    el.homeView.classList.add('hidden');
    el.examView.classList.remove('hidden');

    el.headerHomeStats.classList.add('hidden');
    el.headerExamStats.classList.remove('hidden');
    el.examSwitcherContainer.classList.remove('hidden');
    el.examModeToggle.classList.remove('hidden');
    el.btnOpenPalette.classList.remove('hidden');
    el.btnResetCurrentExam.classList.remove('hidden');
    el.examProgressBarContainer.classList.remove('hidden');

    el.btnToggleViewText.textContent = '← Dashboard';
    el.examSelect.value = String(appState.activeExamId);

    const activeExam = getActiveExam();
    if (el.headerExamTag && activeExam) {
      el.headerExamTag.textContent = `Exam ${activeExam.id} • 53 Items`;
    }

    const prog = getExamProgress(appState.activeExamId);
    setMode(prog.mode, false);
    renderCurrentQuestion();
    updateLiveStats();
  }

  saveProgress();
}

// Select an active exam and switch to exam view
function selectExam(examId) {
  appState.activeExamId = Number(examId);
  getExamProgress(appState.activeExamId);
  switchView('exam');
}

// Render the entire Home Page Dashboard
function renderDashboard() {
  const allExams = appState.exams;
  let grandTotalAnswered = 0;
  let grandTotalCorrect = 0;
  let grandTotalQuestions = 0;
  let completedExamsCount = 0;
  let passedExamsCount = 0;

  // Domain aggregates across all exams
  const activeDomains = getActiveDomains();
  const domainAggregates = {};
  Object.keys(activeDomains).forEach(dId => {
    domainAggregates[dId] = {
      name: activeDomains[dId].name,
      weight: activeDomains[dId].weight,
      totalQuestions: 0,
      attempted: 0,
      correct: 0
    };
  });

  // Calculate stats for each exam
  const examStatsList = allExams.map(exam => {
    const prog = getExamProgress(exam.id);
    const questions = exam.questions;
    grandTotalQuestions += questions.length;

    let examAnswered = 0;
    let examCorrect = 0;

    questions.forEach(q => {
      if (domainAggregates[q.domainId]) {
        domainAggregates[q.domainId].totalQuestions++;
      }

      if (prog.submitted[q.id]) {
        examAnswered++;
        grandTotalAnswered++;

        if (domainAggregates[q.domainId]) {
          domainAggregates[q.domainId].attempted++;
        }

        const userSel = prog.userAnswers[q.id] || [];
        const isCorr = userSel.length === q.correctIndices.length &&
          userSel.every(idx => q.correctIndices.includes(idx));

        if (isCorr) {
          examCorrect++;
          grandTotalCorrect++;
          if (domainAggregates[q.domainId]) {
            domainAggregates[q.domainId].correct++;
          }
        }
      }
    });

    const isFinished = examAnswered === questions.length;
    if (isFinished) completedExamsCount++;

    const examPct = examAnswered > 0 ? Math.round((examCorrect / examAnswered) * 100) : 0;
    const examScaled = Math.round(100 + (examCorrect / questions.length) * 900);
    const isPassing = examScaled >= 720;
    if (isFinished && isPassing) passedExamsCount++;

    return {
      exam,
      prog,
      answered: examAnswered,
      correct: examCorrect,
      total: questions.length,
      pct: examPct,
      scaled: examScaled,
      isFinished,
      isPassing
    };
  });

  // Overall Stats Calculations
  const overallAccuracyPct = grandTotalAnswered > 0 ? Math.round((grandTotalCorrect / grandTotalAnswered) * 100) : 0;
  const overallAnsweredPct = grandTotalQuestions > 0 ? Math.round((grandTotalAnswered / grandTotalQuestions) * 100) : 0;
  const overallScaled = grandTotalQuestions > 0 ? Math.round(100 + (grandTotalCorrect / grandTotalQuestions) * 900) : 100;
  const isOverallPassing = overallScaled >= 720;

  // Update Header Summary
  el.homeHeadAnswered.textContent = grandTotalAnswered;
  el.homeHeadAccuracy.textContent = `${overallAccuracyPct}%`;
  el.homeHeadStatus.textContent = isOverallPassing ? 'Passing (≥720)' : (grandTotalAnswered === 0 ? 'Not Started' : 'In Progress');
  el.homeHeadStatus.className = `status-pill ${isOverallPassing ? 'status-pass' : (grandTotalAnswered === 0 ? 'status-neutral' : 'status-fail')}`;

  // Update Big Stat Cards
  el.statOverallPct.textContent = `${overallAnsweredPct}%`;
  el.statOverallAnswered.textContent = grandTotalAnswered;
  el.statOverallBar.style.width = `${overallAnsweredPct}%`;

  el.statAccuracyBadge.textContent = `${overallAccuracyPct}%`;
  el.statOverallCorrect.textContent = grandTotalCorrect;
  el.statAccuracySubtext.textContent = `${grandTotalAnswered} attempted across all 5 exams`;

  el.statOverallScaled.textContent = overallScaled;
  el.statOverallPill.textContent = isOverallPassing ? 'Passing (≥720)' : 'Needs 720';
  el.statOverallPill.className = `status-pill ${isOverallPassing ? 'status-pass' : 'status-fail'}`;

  el.statCompletedBadge.textContent = `${completedExamsCount} / ${allExams.length}`;
  el.statExamsPassed.textContent = passedExamsCount;
  el.statLastActiveText.textContent = `Last active session: Exam ${appState.activeExamId}`;

  // Render Exam Cards Grid
  el.examCardsGrid.innerHTML = '';
  examStatsList.forEach(({ exam, prog, answered, correct, total, pct, scaled, isFinished, isPassing }) => {
    const card = document.createElement('div');
    card.className = `exam-card ${exam.id === appState.activeExamId ? 'active-session' : ''}`;

    let statusLabel = 'Not Started';
    let statusClass = 'status-neutral';

    if (isFinished) {
      if (isPassing) {
        statusLabel = 'Passed (≥720)';
        statusClass = 'status-pass';
      } else {
        statusLabel = 'Needs Review (<720)';
        statusClass = 'status-fail';
      }
    } else if (answered > 0) {
      statusLabel = `In Progress (${answered}/${total})`;
      statusClass = 'status-neutral';
    }

    const progressPct = Math.round((answered / total) * 100);

    card.innerHTML = `
      <div class="exam-card-header">
        <span class="exam-card-number-badge">Exam ${exam.id} • ${total} Items</span>
        <span class="status-pill ${statusClass}">${statusLabel}</span>
      </div>

      <h3 class="exam-card-title">${exam.title}</h3>
      <p class="exam-card-desc">${exam.description}</p>

      <div class="exam-card-metrics">
        <div class="metric-row">
          <span class="metric-label-muted">Progress</span>
          <span class="metric-value-strong">${answered} / ${total} (${progressPct}%)</span>
        </div>
        <div class="progress-track">
          <div class="progress-fill" style="width: ${progressPct}%;"></div>
        </div>

        <div class="metric-row" style="margin-top: 4px;">
          <span class="metric-label-muted">Accuracy & Score</span>
          <span class="metric-value-strong">${correct} / ${answered} (${pct}%) • ${scaled} / 1000</span>
        </div>
      </div>

      <div class="exam-card-actions">
        <button class="btn-card-start" data-exam-id="${exam.id}">
          <span>${answered === 0 ? 'Start Exam' : (isFinished ? 'Review Exam' : 'Resume Exam')}</span>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <polyline points="9 18 15 12 9 6"></polyline>
          </svg>
        </button>
        <button class="btn-card-reset" data-reset-id="${exam.id}" title="Reset Exam ${exam.id}">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path>
            <path d="M3 3v5h5"></path>
          </svg>
        </button>
      </div>
    `;

    card.querySelector('.btn-card-start').addEventListener('click', () => {
      selectExam(exam.id);
    });

    card.querySelector('.btn-card-reset').addEventListener('click', (e) => {
      e.stopPropagation();
      resetSingleExam(exam.id);
    });

    el.examCardsGrid.appendChild(card);
  });

  // Render Aggregate Blueprint Domains Grid
  el.domainAggregateGrid.innerHTML = '';
  Object.keys(activeDomains).forEach(dId => {
    const d = domainAggregates[dId];
    if (!d) return;
    const pct = d.attempted > 0 ? Math.round((d.correct / d.attempted) * 100) : 0;
    const isPassing = pct >= 72;

    const card = document.createElement('div');
    card.className = 'domain-agg-card';
    card.innerHTML = `
      <div class="domain-agg-header">
        <span class="domain-agg-title">D${dId}: ${d.name}</span>
        <span class="domain-agg-weight">${d.weight}</span>
      </div>

      <div class="progress-track">
        <div class="progress-fill" style="width: ${pct}%; background: ${d.attempted === 0 ? 'var(--border-medium)' : (isPassing ? 'var(--correct-green)' : 'var(--incorrect-red)')};"></div>
      </div>

      <div class="domain-agg-stats">
        <span class="domain-agg-numbers">
          <strong>${d.correct}</strong> / ${d.attempted} correct (${pct}%)
        </span>
        <span class="status-pill ${d.attempted === 0 ? 'status-neutral' : (isPassing ? 'status-pass' : 'status-fail')}">
          ${d.attempted === 0 ? 'Unattempted' : (isPassing ? 'Proficient' : 'Needs Focus')}
        </span>
      </div>
    `;
    el.domainAggregateGrid.appendChild(card);
  });
}

// Reset an individual exam with confirmation
function resetSingleExam(examId) {
  if (!confirm(`Are you sure you want to reset all answers and progress for Exam ${examId}?`)) return;

  appState.progress[examId] = {
    currentIndex: 0,
    userAnswers: {},
    submitted: {},
    flagged: new Set(),
    mode: 'practice',
    timerSeconds: 120 * 60,
    completed: false,
    lastUpdated: Date.now()
  };

  saveProgress();
  if (appState.currentView === 'exam' && appState.activeExamId === examId) {
    renderCurrentQuestion();
    updateLiveStats();
  } else {
    renderDashboard();
  }
}

// Reset all 5 exams
function resetAllExams() {
  if (!confirm('CAUTION: Are you sure you want to reset ALL 5 exams? All stored answers, scores, and flags will be permanently cleared.')) return;

  appState.exams.forEach(exam => {
    appState.progress[exam.id] = {
      currentIndex: 0,
      userAnswers: {},
      submitted: {},
      flagged: new Set(),
      mode: 'practice',
      timerSeconds: 120 * 60,
      completed: false,
      lastUpdated: Date.now()
    };
  });

  localStorage.removeItem(getStorageKey());
  saveProgress();
  renderDashboard();
  if (appState.currentView === 'exam') {
    renderCurrentQuestion();
    updateLiveStats();
  }
  alert(`All ${getActiveTrackMeta().code} exam progress has been reset.`);
}

// Export progress as JSON file
function exportProgress() {
  saveProgress();
  const serialized = localStorage.getItem(getStorageKey());
  if (!serialized) {
    alert('No progress to export.');
    return;
  }
  const blob = new Blob([serialized], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${getActiveTrack()}_exam_progress_${new Date().toISOString().slice(0, 10)}.json`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// Import progress from JSON file
function importProgress(file) {
  const reader = new FileReader();
  reader.onload = (e) => {
    try {
      const data = JSON.parse(e.target.result);
      if (data && data.progress) {
        localStorage.setItem(getStorageKey(), JSON.stringify(data));
        loadProgress();
        renderDashboard();
        if (appState.currentView === 'exam') {
          renderCurrentQuestion();
          updateLiveStats();
        }
        alert('Progress successfully imported!');
      } else {
        alert('Invalid progress backup file.');
      }
    } catch (err) {
      alert('Failed to parse backup JSON file: ' + err.message);
    }
  };
  reader.readAsText(file);
}

// Timer Management
function startTimer() {
  if (appState.timerInterval) clearInterval(appState.timerInterval);
  appState.timerInterval = setInterval(() => {
    if (appState.currentView === 'exam') {
      const prog = getExamProgress(appState.activeExamId);
      if (prog.mode === 'exam') {
        prog.timerSeconds--;
        if (prog.timerSeconds <= 0) {
          prog.timerSeconds = 0;
          clearInterval(appState.timerInterval);
          alert('Time is up! Submitting exam automatically.');
          finishExam();
        }
      }
      updateTimerDisplay();
    }
  }, 1000);
}

function updateTimerDisplay() {
  const prog = getExamProgress(appState.activeExamId);
  const mins = Math.floor(prog.timerSeconds / 60);
  const secs = prog.timerSeconds % 60;
  el.timerDisplay.textContent = 
    `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

// Mode Switcher (Study Mode vs Timed Exam)
function setMode(newMode, shouldSave = true) {
  const prog = getExamProgress(appState.activeExamId);
  prog.mode = newMode;
  if (newMode === 'practice') {
    el.btnModePractice.classList.add('active');
    el.btnModeExam.classList.remove('active');
  } else {
    el.btnModeExam.classList.add('active');
    el.btnModePractice.classList.remove('active');
  }
  renderCurrentQuestion();
  updateLiveStats();
  if (shouldSave) saveProgress();
}

// Render Current Question
function renderCurrentQuestion() {
  const activeExam = getActiveExam();
  if (!activeExam) return;
  const prog = getExamProgress(activeExam.id);
  const q = activeExam.questions[prog.currentIndex];
  if (!q) return;

  // Header tags
  el.qNumberBadge.textContent = `Question ${prog.currentIndex + 1} of ${activeExam.questions.length}`;
  el.qDomainPill.textContent = `Domain ${q.domainId}: ${q.domainName} (${getDomainMeta(q.domainId).weight || '10%'})`;
  el.qSubskillPill.textContent = q.subSkill || 'General';
  el.qModuleTag.textContent = q.module || (getActiveTrack() === 'architect' ? 'Architect Course' : 'Developer Course');

  // Flag Button
  const isFlagged = prog.flagged.has(q.id);
  el.btnFlag.classList.toggle('flagged', isFlagged);
  el.flagText.textContent = isFlagged ? 'Flagged' : 'Flag for Review';

  // Scenario Text
  el.scenarioText.innerHTML = formatMarkdown(q.scenario);

  // Multi-select Indicator
  if (q.isMultiSelect) {
    el.multiSelectHint.classList.remove('hidden');
    el.multiSubmitWrapper.classList.remove('hidden');
  } else {
    el.multiSelectHint.classList.add('hidden');
    el.multiSubmitWrapper.classList.add('hidden');
  }

  // Render Options
  renderOptions(q);

  // Render Feedback
  renderFeedback(q);

  // Update Navigation Controls
  el.btnPrev.disabled = prog.currentIndex === 0;
  el.btnNext.disabled = prog.currentIndex === activeExam.questions.length - 1;

  const allAnswered = Object.keys(prog.submitted).length === activeExam.questions.length;
  el.btnFinishExam.classList.toggle('hidden', !allAnswered && prog.currentIndex !== activeExam.questions.length - 1);

  // Update Progress Bar
  const answeredCount = Object.keys(prog.submitted).length;
  const progressPct = ((answeredCount / activeExam.questions.length) * 100).toFixed(1);
  el.progressBarFill.style.width = `${progressPct}%`;

  saveProgress();
}

// Render Options
function renderOptions(q) {
  el.optionsContainer.innerHTML = '';
  const prog = getExamProgress(appState.activeExamId);
  const selected = prog.userAnswers[q.id] || [];
  const isSubmitted = !!prog.submitted[q.id];
  const isPractice = prog.mode === 'practice';
  const showResults = isSubmitted && isPractice;

  q.structuredOptions.forEach((opt, idx) => {
    const card = document.createElement('div');
    card.className = 'option-card';

    const isSelected = selected.includes(idx);
    if (isSelected) card.classList.add('selected');

    if (showResults) {
      card.classList.add('locked');
      if (opt.isCorrect) {
        card.classList.add('correct');
      } else if (isSelected) {
        card.classList.add('incorrect');
      } else {
        card.classList.add('dimmed');
      }
    }

    card.innerHTML = `
      <div class="option-letter">${opt.letter}</div>
      <div class="option-content">
        <div class="option-text">${formatMarkdown(opt.text)}</div>
        ${showResults && (isSelected || opt.isCorrect) ? 
          `<div class="option-feedback-inline">${formatMarkdown(opt.feedback)}</div>` : ''}
      </div>
    `;

    card.addEventListener('click', () => {
      handleOptionClick(q, idx);
    });

    el.optionsContainer.appendChild(card);
  });

  // Update multi-select button state
  if (q.isMultiSelect) {
    el.btnSubmitMulti.disabled = isSubmitted || selected.length !== 2;
    el.btnSubmitMulti.textContent = isSubmitted ? 'Answer Submitted' : 'Submit Answer (Select 2)';
  }
}

// Handle Option Click
function handleOptionClick(q, optIndex) {
  const prog = getExamProgress(appState.activeExamId);
  const isPractice = prog.mode === 'practice';
  const isSubmitted = !!prog.submitted[q.id];

  // In practice mode, if already submitted, prevent re-answering unless cleared
  if (isPractice && isSubmitted) return;

  if (q.isMultiSelect) {
    let current = prog.userAnswers[q.id] ? [...prog.userAnswers[q.id]] : [];
    const existingIndex = current.indexOf(optIndex);
    if (existingIndex > -1) {
      current.splice(existingIndex, 1);
    } else {
      if (current.length < 2) {
        current.push(optIndex);
      } else {
        current.shift();
        current.push(optIndex);
      }
    }
    prog.userAnswers[q.id] = current;
    renderOptions(q);
  } else {
    prog.userAnswers[q.id] = [optIndex];
    prog.submitted[q.id] = true;
    prog.lastUpdated = Date.now();
    renderOptions(q);
    renderFeedback(q);
    updateLiveStats();
    saveProgress();
  }
}

// Handle Multi-select Submission
function submitMultiAnswer() {
  const activeExam = getActiveExam();
  if (!activeExam) return;
  const prog = getExamProgress(activeExam.id);
  const q = activeExam.questions[prog.currentIndex];
  if (!q || !q.isMultiSelect) return;
  const selected = prog.userAnswers[q.id] || [];
  if (selected.length !== 2) return;

  prog.submitted[q.id] = true;
  prog.lastUpdated = Date.now();
  renderOptions(q);
  renderFeedback(q);
  updateLiveStats();
  saveProgress();
}

// Render Feedback Panel
function renderFeedback(q) {
  const prog = getExamProgress(appState.activeExamId);
  const isSubmitted = !!prog.submitted[q.id];
  const isPractice = prog.mode === 'practice';

  if (!isSubmitted || !isPractice) {
    el.feedbackPanel.classList.add('hidden');
    return;
  }

  el.feedbackPanel.classList.remove('hidden');

  const selected = prog.userAnswers[q.id] || [];
  const correct = q.correctIndices;
  const isFullyCorrect = 
    selected.length === correct.length && 
    selected.every(idx => correct.includes(idx));

  if (isFullyCorrect) {
    el.feedbackBanner.className = 'feedback-banner correct-banner';
    el.feedbackIcon.textContent = '✓';
    el.feedbackTitle.textContent = 'Correct Answer';
  } else {
    el.feedbackBanner.className = 'feedback-banner incorrect-banner';
    el.feedbackIcon.textContent = '✕';
    el.feedbackTitle.textContent = 'Incorrect Choice';
  }

  el.feedbackExplanation.innerHTML = formatMarkdown(q.overallExplanation || '');
  el.mindsetText.textContent = q.keyInsight || 'Proportionate fix first.';
}

// Clear Current Question Answer
function clearCurrentAnswer() {
  const activeExam = getActiveExam();
  if (!activeExam) return;
  const prog = getExamProgress(activeExam.id);
  const q = activeExam.questions[prog.currentIndex];
  if (!q) return;

  delete prog.userAnswers[q.id];
  delete prog.submitted[q.id];

  renderOptions(q);
  renderFeedback(q);
  updateLiveStats();
  saveProgress();
}

// Toggle Flag
function toggleFlag() {
  const activeExam = getActiveExam();
  if (!activeExam) return;
  const prog = getExamProgress(activeExam.id);
  const q = activeExam.questions[prog.currentIndex];
  if (!q) return;

  if (prog.flagged.has(q.id)) {
    prog.flagged.delete(q.id);
  } else {
    prog.flagged.add(q.id);
  }

  const isFlagged = prog.flagged.has(q.id);
  el.btnFlag.classList.toggle('flagged', isFlagged);
  el.flagText.textContent = isFlagged ? 'Flagged' : 'Flag for Review';

  updateLiveStats();
  saveProgress();
}

// Live Score Tracker Calculations (For Active Exam)
function updateLiveStats() {
  const activeExam = getActiveExam();
  if (!activeExam) return;
  const prog = getExamProgress(activeExam.id);

  let totalAttempted = 0;
  let totalCorrect = 0;
  let totalIncorrect = 0;

  activeExam.questions.forEach(q => {
    if (prog.submitted[q.id]) {
      totalAttempted++;
      const userSel = prog.userAnswers[q.id] || [];
      const correctSel = q.correctIndices;
      const isCorrect = 
        userSel.length === correctSel.length && 
        userSel.every(idx => correctSel.includes(idx));

      if (isCorrect) {
        totalCorrect++;
      } else {
        totalIncorrect++;
      }
    }
  });

  el.scoreCorrect.textContent = totalCorrect;
  el.scoreAttempted.textContent = totalAttempted;

  const pct = totalAttempted > 0 ? ((totalCorrect / totalAttempted) * 100).toFixed(0) : '0';
  el.scorePct.textContent = `(${pct}%)`;

  const scaled = Math.round(100 + (totalCorrect / activeExam.questions.length) * 900);
  el.scaledScore.textContent = scaled;

  if (scaled >= 720) {
    el.statusPill.textContent = 'Passing (≥720)';
    el.statusPill.className = 'status-pill status-pass';
  } else {
    el.statusPill.textContent = 'Needs 720';
    el.statusPill.className = 'status-pill status-fail';
  }

  if (el.countAnswered) el.countAnswered.textContent = totalAttempted;
  if (el.countUnanswered) el.countUnanswered.textContent = activeExam.questions.length - totalAttempted;
  if (el.countFlagged) el.countFlagged.textContent = prog.flagged.size;
  if (el.countIncorrect) el.countIncorrect.textContent = totalIncorrect;
}

// Question Palette Drawer Rendering
function renderPaletteGrid() {
  el.paletteGrid.innerHTML = '';
  const activeExam = getActiveExam();
  if (!activeExam) return;
  const prog = getExamProgress(activeExam.id);
  const filter = appState.activeFilter;

  el.paletteSubtitle.textContent = `Exam ${activeExam.id}: Jump to any of the 53 questions`;

  activeExam.questions.forEach((q, idx) => {
    const isAnswered = !!prog.submitted[q.id];
    const isFlagged = prog.flagged.has(q.id);
    const userSel = prog.userAnswers[q.id] || [];
    const isCorrect = isAnswered && 
      userSel.length === q.correctIndices.length && 
      userSel.every(i => q.correctIndices.includes(i));
    const isIncorrect = isAnswered && !isCorrect;

    // Filter check
    if (filter === 'answered' && !isAnswered) return;
    if (filter === 'unanswered' && isAnswered) return;
    if (filter === 'flagged' && !isFlagged) return;
    if (filter === 'incorrect' && !isIncorrect) return;

    const cell = document.createElement('div');
    cell.className = 'palette-cell';
    cell.textContent = idx + 1;

    if (idx === prog.currentIndex) cell.classList.add('current');
    if (isFlagged) cell.classList.add('flagged');

    if (prog.mode === 'practice' && isAnswered) {
      if (isCorrect) cell.classList.add('correct');
      else cell.classList.add('incorrect');
    } else if (isAnswered) {
      cell.classList.add('answered');
    }

    cell.addEventListener('click', () => {
      prog.currentIndex = idx;
      renderCurrentQuestion();
      closePalette();
    });

    el.paletteGrid.appendChild(cell);
  });
}

function openPalette() {
  renderPaletteGrid();
  el.paletteModal.classList.remove('hidden');
}

function closePalette() {
  el.paletteModal.classList.add('hidden');
}

// Domain Breakdown Modal Rendering
function renderDomainBreakdown() {
  el.domainsTableBody.innerHTML = '';
  const activeExam = getActiveExam();
  if (!activeExam) return;
  const prog = getExamProgress(activeExam.id);

  el.breakdownTitle.textContent = `Exam ${activeExam.id} Domain Breakdown`;

  const activeDomains = getActiveDomains();
  const domainStats = {};
  Object.keys(activeDomains).forEach(dId => {
    domainStats[dId] = {
      id: dId,
      name: activeDomains[dId].name,
      weight: activeDomains[dId].weight,
      total: 0,
      attempted: 0,
      correct: 0
    };
  });

  activeExam.questions.forEach(q => {
    const d = domainStats[q.domainId];
    if (!d) return;
    d.total++;
    if (prog.submitted[q.id]) {
      d.attempted++;
      const sel = prog.userAnswers[q.id] || [];
      if (sel.length === q.correctIndices.length && sel.every(i => q.correctIndices.includes(i))) {
        d.correct++;
      }
    }
  });

  let overallPass = true;
  let domainsNeedingReview = [];

  Object.keys(activeDomains).forEach(dId => {
    const d = domainStats[dId];
    if (!d) return;
    const pct = d.attempted > 0 ? Math.round((d.correct / d.attempted) * 100) : 0;
    const isPassing = pct >= 72;
    if (pct < 72 && d.attempted > 0) {
      overallPass = false;
      domainsNeedingReview.push(`Domain ${dId}: ${d.name}`);
    }

    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td class="domain-name-cell">D${dId}: ${d.name}</td>
      <td class="domain-weight-cell">${d.weight}</td>
      <td>${d.total}</td>
      <td class="domain-score-cell">${d.correct} / ${d.attempted}</td>
      <td>
        <div class="domain-pct-bar">
          <div class="pct-track">
            <div class="pct-fill ${isPassing ? 'pass' : 'fail'}" style="width: ${pct}%;"></div>
          </div>
          <span>${pct}%</span>
        </div>
      </td>
      <td>
        <span class="status-pill ${isPassing ? 'status-pass' : 'status-fail'}">
          ${d.attempted === 0 ? 'Not Started' : (isPassing ? 'Proficient' : 'Needs Review')}
        </span>
      </td>
    `;
    el.domainsTableBody.appendChild(tr);
  });

  const totalCorrect = Object.values(domainStats).reduce((acc, curr) => acc + curr.correct, 0);
  const scaled = Math.round(100 + (totalCorrect / activeExam.questions.length) * 900);

  el.breakdownSummaryBanner.innerHTML = `
    <strong>Exam ${activeExam.id} Scaled Score:</strong> ${scaled} / 1000 (${scaled >= 720 ? 'Passing' : 'Below 720 Passing Standard'}).
    ${domainsNeedingReview.length > 0 ? 
      `<br><strong>Recommended Review Focus:</strong> ${domainsNeedingReview.join(', ')}` : 
      '<br>Strong domain proficiency observed across this exam!'}
  `;
}

function openBreakdown() {
  renderDomainBreakdown();
  el.breakdownModal.classList.remove('hidden');
}

function closeBreakdown() {
  el.breakdownModal.classList.add('hidden');
}

// Finish Exam & Results Modal
function finishExam() {
  const activeExam = getActiveExam();
  if (!activeExam) return;
  const prog = getExamProgress(activeExam.id);
  prog.completed = true;

  let totalCorrect = 0;
  const activeDomains = getActiveDomains();
  const domainScores = {};
  Object.keys(activeDomains).forEach(dId => {
    domainScores[dId] = { name: activeDomains[dId].name, total: 0, correct: 0 };
  });

  activeExam.questions.forEach(q => {
    if (domainScores[q.domainId]) {
      domainScores[q.domainId].total++;
    }
    const userSel = prog.userAnswers[q.id] || [];
    const isCorr = userSel.length === q.correctIndices.length && userSel.every(i => q.correctIndices.includes(i));
    if (isCorr) {
      totalCorrect++;
      if (domainScores[q.domainId]) {
        domainScores[q.domainId].correct++;
      }
    }
  });

  const scaled = Math.round(100 + (totalCorrect / activeExam.questions.length) * 900);
  const rawPct = ((totalCorrect / activeExam.questions.length) * 100).toFixed(1);
  const isPass = scaled >= 720;

  el.resultsTitle.textContent = `Exam ${activeExam.id} Completed`;
  el.resultsSubtitle.textContent = `Here is your official scaled score report breakdown for ${activeExam.title}.`;
  el.resultVerdict.textContent = isPass ? 'PASSED' : 'NOT PASSED';
  el.resultVerdict.className = `result-verdict ${isPass ? 'pass' : 'fail'}`;
  el.reportScaledScore.textContent = scaled;
  el.reportRawScore.textContent = `${totalCorrect} / ${activeExam.questions.length}`;
  el.reportRawPct.textContent = `${rawPct}% Accuracy`;

  const secondsSpent = Math.max(0, (120 * 60) - prog.timerSeconds);
  const mins = Math.floor(secondsSpent / 60);
  const secs = secondsSpent % 60;
  el.reportTimeTaken.textContent = `${mins}m ${secs}s`;

  el.resultsDomainsList.innerHTML = '';
  Object.keys(activeDomains).forEach(dId => {
    const d = domainScores[dId];
    if (!d) return;
    const pct = d.total > 0 ? Math.round((d.correct / d.total) * 100) : 0;
    const isProf = pct >= 72;
    const row = document.createElement('div');
    row.className = 'result-domain-row';
    row.innerHTML = `
      <span class="res-domain-title">D${dId}: ${d.name}</span>
      <div class="res-domain-stats">
        <span>${d.correct} / ${d.total} (${pct}%)</span>
        <span class="status-pill ${isProf ? 'status-pass' : 'status-fail'}">${isProf ? 'PASS' : 'REVIEW'}</span>
      </div>
    `;
    el.resultsDomainsList.appendChild(row);
  });

  saveProgress();
  el.resultsModal.classList.remove('hidden');
}

// Setup Event Listeners
function setupEventListeners() {
  // Navigation View Toggle & Home Nav
  el.btnNavHome.addEventListener('click', () => switchView('home'));
  el.btnToggleView.addEventListener('click', () => {
    switchView(appState.currentView === 'home' ? 'exam' : 'home');
  });

  // Exam Selector in Header
  el.examSelect.addEventListener('change', (e) => {
    selectExam(Number(e.target.value));
  });

  // Home view backup/restore actions
  el.btnExportProgress.addEventListener('click', exportProgress);
  el.btnImportProgress.addEventListener('click', () => el.importFileInput.click());
  el.importFileInput.addEventListener('change', (e) => {
    if (e.target.files && e.target.files[0]) {
      importProgress(e.target.files[0]);
    }
  });
  el.btnResetAll.addEventListener('click', resetAllExams);

  // Exam Navigation
  el.btnPrev.addEventListener('click', () => {
    const prog = getExamProgress(appState.activeExamId);
    if (prog.currentIndex > 0) {
      prog.currentIndex--;
      renderCurrentQuestion();
    }
  });

  el.btnNext.addEventListener('click', () => {
    const activeExam = getActiveExam();
    if (!activeExam) return;
    const prog = getExamProgress(activeExam.id);
    if (prog.currentIndex < activeExam.questions.length - 1) {
      prog.currentIndex++;
      renderCurrentQuestion();
    }
  });

  el.btnClear.addEventListener('click', clearCurrentAnswer);
  el.btnFlag.addEventListener('click', toggleFlag);
  el.btnSubmitMulti.addEventListener('click', submitMultiAnswer);
  el.btnFinishExam.addEventListener('click', finishExam);

  // Modes & Reset Exam
  el.btnModePractice.addEventListener('click', () => setMode('practice'));
  el.btnModeExam.addEventListener('click', () => setMode('exam'));
  el.btnResetCurrentExam.addEventListener('click', () => resetSingleExam(appState.activeExamId));

  // Modals
  el.btnOpenPalette.addEventListener('click', openPalette);
  el.btnClosePalette.addEventListener('click', closePalette);
  el.paletteModal.addEventListener('click', (e) => {
    if (e.target === el.paletteModal) closePalette();
  });

  el.btnOpenBreakdown.addEventListener('click', openBreakdown);
  el.btnCloseBreakdown.addEventListener('click', closeBreakdown);
  el.breakdownModal.addEventListener('click', (e) => {
    if (e.target === el.breakdownModal) closeBreakdown();
  });

  // Palette Filters
  document.querySelectorAll('.palette-filters .filter-chip').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.palette-filters .filter-chip').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      appState.activeFilter = btn.dataset.filter;
      renderPaletteGrid();
    });
  });

  // Results Actions
  el.btnReviewAll.addEventListener('click', () => {
    el.resultsModal.classList.add('hidden');
    const prog = getExamProgress(appState.activeExamId);
    prog.currentIndex = 0;
    renderCurrentQuestion();
  });

  el.btnReviewMissed.addEventListener('click', () => {
    el.resultsModal.classList.add('hidden');
    const activeExam = getActiveExam();
    if (!activeExam) return;
    const prog = getExamProgress(activeExam.id);
    const missedIdx = activeExam.questions.findIndex(q => {
      const userSel = prog.userAnswers[q.id] || [];
      return userSel.length !== q.correctIndices.length || !userSel.every(i => q.correctIndices.includes(i));
    });
    if (missedIdx > -1) {
      prog.currentIndex = missedIdx;
      renderCurrentQuestion();
    }
  });

  el.btnRetakeExam.addEventListener('click', () => {
    el.resultsModal.classList.add('hidden');
    resetSingleExam(appState.activeExamId);
  });

  el.btnResultsHome.addEventListener('click', () => {
    el.resultsModal.classList.add('hidden');
    switchView('home');
  });

  // Track Switcher (Header Pills)
  if (el.pillTrackDeveloper) {
    el.pillTrackDeveloper.addEventListener('click', () => switchTrack('developer'));
  }
  if (el.pillTrackArchitect) {
    el.pillTrackArchitect.addEventListener('click', () => switchTrack('architect'));
  }

  // Track Switcher (Hero Dashboard Cards)
  if (el.cardTrackDeveloper) {
    el.cardTrackDeveloper.addEventListener('click', () => switchTrack('developer'));
    el.cardTrackDeveloper.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); switchTrack('developer'); }
    });
  }
  if (el.cardTrackArchitect) {
    el.cardTrackArchitect.addEventListener('click', () => switchTrack('architect'));
    el.cardTrackArchitect.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); switchTrack('architect'); }
    });
  }

  // Keyboard Shortcuts
  window.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

    if (e.key === 'Escape') {
      closePalette();
      closeBreakdown();
      el.resultsModal.classList.add('hidden');
      return;
    }

    if (appState.currentView !== 'exam') return;

    const activeExam = getActiveExam();
    if (!activeExam) return;
    const prog = getExamProgress(activeExam.id);

    if (e.key === 'ArrowRight' || e.key === 'n' || e.key === 'N') {
      if (prog.currentIndex < activeExam.questions.length - 1) {
        prog.currentIndex++;
        renderCurrentQuestion();
      }
    } else if (e.key === 'ArrowLeft' || e.key === 'p' || e.key === 'P') {
      if (prog.currentIndex > 0) {
        prog.currentIndex--;
        renderCurrentQuestion();
      }
    } else if (e.key === 'f' || e.key === 'F') {
      toggleFlag();
    } else if (e.key === 'g' || e.key === 'G') {
      if (el.paletteModal.classList.contains('hidden')) openPalette();
      else closePalette();
    } else if (e.key === 'd' || e.key === 'D') {
      if (el.breakdownModal.classList.contains('hidden')) openBreakdown();
      else closeBreakdown();
    } else if (['1', '2', '3', '4'].includes(e.key)) {
      const optIdx = parseInt(e.key, 10) - 1;
      const q = activeExam.questions[prog.currentIndex];
      if (q && q.structuredOptions[optIdx]) {
        handleOptionClick(q, optIdx);
      }
    }
  });
}

// App Initialization
async function initApp() {
  initDOMElements();

  // Restore active track from localStorage (default: developer)
  try {
    const savedTrack = localStorage.getItem('cc_active_track');
    if (savedTrack && (savedTrack === 'developer' || savedTrack === 'architect')) {
      appState.activeTrack = savedTrack;
    }
  } catch (e) {}

  loadTrackData(appState.activeTrack);

  // Fallback to fetch or legacy if empty
  if (!appState.exams || appState.exams.length === 0) {
    if (typeof EXAMS_SUITE !== 'undefined' && Array.isArray(EXAMS_SUITE) && EXAMS_SUITE.length > 0) {
      appState.exams = EXAMS_SUITE;
    } else {
      try {
        const resp = await fetch('exams_suite.json');
        appState.exams = await resp.json();
      } catch (err) {
        console.error('Failed to load exam data:', err);
      }
    }
  }

  loadProgress();
  updateTrackUI();
  populateExamSelect();
  setupEventListeners();
  startTimer();

  // Initial View
  if (appState.currentView === 'exam') {
    switchView('exam');
  } else {
    switchView('home');
  }
}

// Kick off when DOM is ready
document.addEventListener('DOMContentLoaded', initApp);
