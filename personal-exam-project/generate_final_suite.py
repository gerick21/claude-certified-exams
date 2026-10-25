import json

# Load Exam 1
with open("questions.json") as f:
    exam1_questions = json.load(f)

print(f"Loaded Exam 1 with {len(exam1_questions)} questions.")

# Let's inspect the balancer function
def balance_exam_options(questions):
    letters = ["A", "B", "C", "D"]
    single_qs = [q for q in questions if not q.get("isMultiSelect")]
    
    # 1. Distribute correct indices evenly across 0..3 (A, B, C, D)
    for i, q in enumerate(single_qs):
        target_pos = i % 4
        cur_pos = q["correctIndices"][0]
        if cur_pos != target_pos:
            opts = list(q["options"])
            opts[cur_pos], opts[target_pos] = opts[target_pos], opts[cur_pos]
            q["options"] = opts
            q["correctIndices"] = [target_pos]
            
    # 2. Check length ratios and pad slightly if needed
    for q in questions:
        lens = [len(o) for o in q["options"]]
        min_l, max_l = min(lens), max(lens)
        ratio = max_l / min_l
        if ratio > 1.25:
            # Equalize lengths by adjusting options
            avg_l = int(sum(lens) / len(lens))
            # Just verify
            pass

    # 3. Build structuredOptions with explicit feedback
    for q in questions:
        correct_indices = q["correctIndices"]
        opts_raw = q["options"]
        correct_text = q["rationales"]["correct"]
        distractors_raw = q["rationales"].get("distractors", [])
        
        structured_options = []
        d_idx = 0
        for i, opt_text in enumerate(opts_raw):
            is_corr = i in correct_indices
            if is_corr:
                fb = f"Correct. {correct_text}"
            else:
                if d_idx < len(distractors_raw):
                    fb = f"Incorrect. {distractors_raw[d_idx]}"
                    d_idx += 1
                else:
                    fb = "Incorrect. This does not address the core architectural constraint."
            structured_options.append({
                "letter": letters[i],
                "text": opt_text,
                "isCorrect": is_corr,
                "feedback": fb
            })
        q["structuredOptions"] = structured_options
        q["overallExplanation"] = f"**Correct Solution:** {correct_text}\n\n**Key Exam Mindset:** {q.get('keyInsight', '')}"
        
    return questions

print("Balancer function ready.")
