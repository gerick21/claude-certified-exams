/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * Certification Track & Exam Registry
 * Central configuration for all certification paths, domain metadata,
 * exam file mappings, and storage keys.
 * ═══════════════════════════════════════════════════════════════════════════════
 */

// ─── Track Identifiers ──────────────────────────────────────────────────────
const TRACK_ID = Object.freeze({
  DEVELOPER: 'developer',
  ARCHITECT: 'architect',
});

// ─── Developer Domains (Official Pearson VUE CCDV-F Blueprint) ──────────────
const DEVELOPER_DOMAINS = Object.freeze({
  1: { name: 'Agents and Workflows',            weight: '14.7%', weightNum: 14.7, targetPerExam: 8  },
  2: { name: 'Applications and Integration',    weight: '33.1%', weightNum: 33.1, targetPerExam: 17 },
  3: { name: 'Claude Code',                      weight: '3.1%',  weightNum: 3.1,  targetPerExam: 2  },
  4: { name: 'Eval, Testing, and Debugging',    weight: '2.6%',  weightNum: 2.6,  targetPerExam: 2  },
  5: { name: 'Model Selection and Optimization', weight: '16.8%', weightNum: 16.8, targetPerExam: 9  },
  6: { name: 'Prompt and Context Engineering',  weight: '11.0%', weightNum: 11.0, targetPerExam: 6  },
  7: { name: 'Security and Safety',              weight: '8.1%',  weightNum: 8.1,  targetPerExam: 4  },
  8: { name: 'Tools and MCPs',                   weight: '10.6%', weightNum: 10.6, targetPerExam: 5  },
});

// ─── Architect Domains (Official CCSA-F Blueprint) ──────────────────────────
const ARCHITECT_DOMAINS = Object.freeze({
  1: { name: 'Agentic Architecture & Orchestration',  weight: '27.0%', weightNum: 27.0, targetPerExam: 14 },
  2: { name: 'Tool Design & MCP Integration',         weight: '18.0%', weightNum: 18.0, targetPerExam: 10 },
  3: { name: 'Claude Code Configuration & Workflows',  weight: '20.0%', weightNum: 20.0, targetPerExam: 11 },
  4: { name: 'Prompt Engineering & Structured Output', weight: '20.0%', weightNum: 20.0, targetPerExam: 10 },
  5: { name: 'Context Management & Reliability',       weight: '15.0%', weightNum: 15.0, targetPerExam: 8  },
});

// ─── Track Metadata ─────────────────────────────────────────────────────────
const TRACKS = Object.freeze({
  [TRACK_ID.DEVELOPER]: {
    id: TRACK_ID.DEVELOPER,
    code: 'CCDV-F',
    name: 'Claude Certified Developer (Foundations)',
    shortName: 'Developer',
    tagline: 'CCDV-F Certification Prep Suite',
    heroTitle: 'Claude Certified Developer Practice Portal',
    heroDescription: 'Master all 8 official blueprint domains with <strong>5 full-length, scenario-based practice exams</strong> (265 unique questions total). All questions feature balanced option lengths, realistic distractors, and rigorous rationales based strictly on the Anthropic Developer Course.',
    examCount: 5,
    questionsPerExam: 53,
    totalQuestions: 265,
    timeLimitMinutes: 120,
    passingScore: 720,
    scoreScale: { min: 100, max: 1000 },
    accentColor: '#d97706',
    domains: DEVELOPER_DOMAINS,
    domainCount: 8,
    examTitles: {
      1: 'Practice Exam 1: Foundations & Core Integration',
      2: 'Practice Exam 2: Advanced Agents & Tool-Use Loops',
      3: 'Practice Exam 3: Production Evals & Enterprise Security',
      4: 'Practice Exam 4: Claude Code & MCP Systems',
      5: 'Practice Exam 5: Comprehensive Mock Exam (Final Readiness)',
    },
  },
  [TRACK_ID.ARCHITECT]: {
    id: TRACK_ID.ARCHITECT,
    code: 'CCSA-F',
    name: 'Claude Certified Solutions Architect (Foundations)',
    shortName: 'Architect',
    tagline: 'CCSA-F Certification Prep Suite',
    heroTitle: 'Claude Certified Architect Practice Portal',
    heroDescription: 'Master all 5 official blueprint domains with <strong>5 full-length, scenario-based practice exams</strong> (265 unique questions total). Questions cover agentic orchestration, MCP tool design, Claude Code workflows, prompt engineering, and context management.',
    examCount: 5,
    questionsPerExam: 53,
    totalQuestions: 265,
    timeLimitMinutes: 120,
    passingScore: 720,
    scoreScale: { min: 100, max: 1000 },
    accentColor: '#3b82f6',
    domains: ARCHITECT_DOMAINS,
    domainCount: 5,
    examTitles: {
      1: 'Practice Exam 1: Agentic Loops & Orchestration Patterns',
      2: 'Practice Exam 2: Tool Design & MCP Architecture',
      3: 'Practice Exam 3: Claude Code Workflows & CI/CD',
      4: 'Practice Exam 4: Prompt Engineering & Structured Extraction',
      5: 'Practice Exam 5: Comprehensive Mock Exam (Final Readiness)',
    },
  },
});

// ─── Exam File Paths ────────────────────────────────────────────────────────
const EXAM_FILES = Object.freeze({
  [TRACK_ID.DEVELOPER]: [
    'data/developer/exam1.json',
    'data/developer/exam2.json',
    'data/developer/exam3.json',
    'data/developer/exam4.json',
    'data/developer/exam5.json',
  ],
  [TRACK_ID.ARCHITECT]: [
    'data/architect/exam1.json',
    'data/architect/exam2.json',
    'data/architect/exam3.json',
    'data/architect/exam4.json',
    'data/architect/exam5.json',
  ],
});

// ─── LocalStorage Keys (track-specific isolation) ───────────────────────────
const STORAGE_KEYS = Object.freeze({
  [TRACK_ID.DEVELOPER]: 'ccdv_exam_suite_storage_v3',
  [TRACK_ID.ARCHITECT]: 'ccsa_exam_suite_storage_v1',
});

// ─── Legacy Storage Key (for migration) ─────────────────────────────────────
const LEGACY_STORAGE_KEY = 'ccdv_exam_suite_storage_v2';

// ─── Architect Exam Scenarios ───────────────────────────────────────────────
const ARCHITECT_SCENARIOS = Object.freeze({
  1: { name: 'Customer Support Resolution Agent',  primaryDomains: [1, 2, 5] },
  2: { name: 'Code Generation with Claude Code',    primaryDomains: [3, 4]    },
  3: { name: 'Multi-Agent Research System',         primaryDomains: [1, 2, 5] },
  4: { name: 'Developer Productivity Tools',        primaryDomains: [3, 4]    },
  5: { name: 'Claude Code for CI/CD',               primaryDomains: [3, 4]    },
  6: { name: 'Structured Data Extraction',          primaryDomains: [2, 4, 5] },
});

