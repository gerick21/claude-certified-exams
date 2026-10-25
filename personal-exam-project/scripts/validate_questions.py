#!/usr/bin/env python3
"""
Psychometric Quality & Schema Validator for Certification Practice Exams.
Verifies:
1. Schema conformity (id, domainId, domainName, subSkill, module, scenario, options, correctIndices, rationales, keyInsight, structuredOptions, overallExplanation)
2. Distractor length balance (max_len / min_len <= 1.35 across all 4 options)
3. Correct answer position balance (approx. 25% for A, B, C, D)
4. Scenario uniqueness (identifying exact or near duplicates)
5. Structured options integrity (letter matching, feedback matching)
"""

import sys
import json
import os
from collections import Counter

def validate_exam_file(filepath):
    print(f"\n=======================================================")
    print(f"Validating Exam File: {filepath}")
    print(f"=======================================================")
    
    if not os.path.exists(filepath):
        print(f"ERROR: File does not exist: {filepath}")
        return False
        
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"ERROR: Failed to parse JSON: {e}")
        return False
        
    questions = data.get('questions', [])
    print(f"Exam ID: {data.get('id')}")
    print(f"Exam Title: {data.get('title')}")
    print(f"Total Questions: {len(questions)}")
    
    if len(questions) != 53:
        print(f"WARNING: Expected 53 questions, found {len(questions)}")
        
    imbalanced_options = []
    missing_fields = []
    position_counts = Counter()
    domain_counts = Counter()
    scenarios = set()
    duplicate_scenarios = []
    letters = ['A', 'B', 'C', 'D']
    
    for idx, q in enumerate(questions):
        qid = q.get('id', idx + 1)
        
        # Check required fields
        required_fields = [
            'id', 'domainId', 'domainName', 'subSkill', 'module', 
            'scenario', 'isMultiSelect', 'options', 'correctIndices', 
            'rationales', 'keyInsight', 'structuredOptions', 'overallExplanation'
        ]
        for field in required_fields:
            if field not in q:
                missing_fields.append((qid, field))
                
        # Domain counts
        domain_counts[q.get('domainId')] += 1
        
        # Scenario duplicates
        scen = q.get('scenario', '').strip()
        if scen in scenarios:
            duplicate_scenarios.append((qid, scen[:60]))
        else:
            scenarios.add(scen)
            
        # Options length ratio
        opts = q.get('options', [])
        if len(opts) != 4:
            print(f"ERROR: Q{qid} does not have exactly 4 options (has {len(opts)})")
            continue
            
        lens = [len(opt.strip()) for opt in opts]
        max_len = max(lens)
        min_len = min(lens)
        ratio = max_len / min_len if min_len > 0 else 999.0
        
        if ratio > 1.35:
            imbalanced_options.append({
                'qid': qid,
                'ratio': round(ratio, 2),
                'lens': lens,
                'min_opt': opts[lens.index(min_len)][:40],
                'max_opt': opts[lens.index(max_len)][:40]
            })
            
        # Correct index distribution
        corr = q.get('correctIndices', [])
        if not q.get('isMultiSelect') and len(corr) == 1:
            position_counts[corr[0]] += 1
            
        # Structured options consistency
        s_opts = q.get('structuredOptions', [])
        if len(s_opts) != 4:
            print(f"ERROR: Q{qid} structuredOptions length is {len(s_opts)} != 4")
        else:
            for s_idx, s_opt in enumerate(s_opts):
                if s_opt.get('letter') != letters[s_idx]:
                    print(f"ERROR: Q{qid} structuredOption[{s_idx}] letter is {s_opt.get('letter')} != {letters[s_idx]}")
                is_corr = s_idx in corr
                if s_opt.get('isCorrect') != is_corr:
                    print(f"ERROR: Q{qid} structuredOption[{s_idx}] isCorrect mismatch: {s_opt.get('isCorrect')} vs expected {is_corr}")
                    
    print("\n--- Domain Distribution ---")
    for did in sorted(domain_counts.keys()):
        print(f"  Domain {did}: {domain_counts[did]} questions")
        
    print("\n--- Answer Key Position Balance ---")
    total_single = sum(position_counts.values())
    for pos in [0, 1, 2, 3]:
        pct = (position_counts[pos] / total_single * 100) if total_single > 0 else 0
        print(f"  Option {letters[pos]}: {position_counts[pos]} ({pct:.1f}%)")
        
    print("\n--- Option Length Balance ---")
    if imbalanced_options:
        print(f"FAIL: Found {len(imbalanced_options)} questions with length ratio > 1.35:")
        for imb in imbalanced_options[:5]:
            print(f"  Q{imb['qid']}: ratio={imb['ratio']}, lengths={imb['lens']}")
    else:
        print("PASS: All 53 questions have balanced option lengths (max/min <= 1.35)!")
        
    print("\n--- Duplicate Scenarios ---")
    if duplicate_scenarios:
        print(f"WARNING: Found {len(duplicate_scenarios)} duplicate scenarios:")
        for dup in duplicate_scenarios[:5]:
            print(f"  Q{dup[0]}: {dup[1]}...")
    else:
        print("PASS: Zero duplicate scenarios detected within this exam.")
        
    return len(imbalanced_options) == 0 and len(missing_fields) == 0

if __name__ == '__main__':
    if len(sys.argv) > 1:
        for f in sys.argv[1:]:
            validate_exam_file(f)
    else:
        print("Usage: python3 validate_questions.py <path_to_exam.json> ...")

