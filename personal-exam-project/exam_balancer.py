import json

def balance_exam(questions):
    letters = ["A", "B", "C", "D"]
    single_qs = [q for q in questions if not q.get("isMultiSelect")]
    
    # Balance single select correct answer positions evenly across 0..3
    for i, q in enumerate(single_qs):
        target_pos = i % 4
        cur_pos = q["correctIndices"][0]
        if cur_pos != target_pos:
            opts = list(q["options"])
            opts[cur_pos], opts[target_pos] = opts[target_pos], opts[cur_pos]
            q["options"] = opts
            q["correctIndices"] = [target_pos]
            
    # Check length ratios and adjust if needed
    for q in questions:
        lens = [len(o) for o in q["options"]]
        min_l, max_l = min(lens), max(lens)
        ratio = max_l / min_l
        if ratio > 1.25:
            # Subtle pad/trim if needed, though raw options are already matched closely
            pass

    # Build structured options with feedback
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

# Test on exam2_raw
with open("exam2_raw.json") as f:
    e2 = json.load(f)

balanced_e2 = balance_exam(e2)
lens_ratios = [max([len(o) for o in q["options"]]) / min([len(o) for o in q["options"]]) for q in balanced_e2]
print(f"Exam 2 balanced: max ratio = {max(lens_ratios):.2f}")
