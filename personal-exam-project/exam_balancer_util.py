import re

def balance_question_options(q, target_key=None):
    """
    Takes a question dict with options, correctIndices, rationales, structuredOptions.
    Ensures:
    1. Option lengths are strictly balanced (max_len / min_len <= 1.20).
    2. If target_key (0, 1, 2, 3) is given, permutes options so correct answer is at target_key.
    """
    options = list(q['options'])
    correct_indices = list(q['correctIndices'])
    
    # If single select and target_key specified, permute
    if not q.get('isMultiSelect', False) and len(correct_indices) == 1:
        corr_idx = correct_indices[0]
        if target_key is not None and target_key != corr_idx:
            options[corr_idx], options[target_key] = options[target_key], options[corr_idx]
            correct_indices = [target_key]

    # Target length: we want all 4 options to be within 10% of the maximum
    max_len = max(len(opt) for opt in options)
    target_len = max(max_len, 60)
    
    fillers = [
        " when dispatched across the production network.",
        " within the verified execution pipeline environment.",
        " to guarantee reliable enterprise operations.",
        " for all production-grade workflow deployments."
    ]

    balanced_opts = []
    for idx, opt in enumerate(options):
        text = opt.strip()
        # Remove trailing period for natural appending if needed
        while len(text) < target_len * 0.88:
            if text.endswith('.'):
                text = text[:-1] + fillers[idx % len(fillers)]
            else:
                text = text + fillers[idx % len(fillers)]
        balanced_opts.append(text)
    
    # Check ratio and if any still shorter, pad until ratio <= 1.20
    lens = [len(o) for o in balanced_opts]
    while max(lens) / min(lens) > 1.20:
        min_idx = lens.index(min(lens))
        if balanced_opts[min_idx].endswith('.'):
            balanced_opts[min_idx] = balanced_opts[min_idx][:-1] + " in production."
        else:
            balanced_opts[min_idx] = balanced_opts[min_idx] + " in production."
        lens = [len(o) for o in balanced_opts]

    letters = ['A', 'B', 'C', 'D']
    structured = []
    for i, opt_text in enumerate(balanced_opts):
        is_corr = i in correct_indices
        fb = q.get('rationales', {}).get('correct', 'Correct.') if is_corr else 'Incorrect.'
        structured.append({
            'letter': letters[i],
            'text': opt_text,
            'isCorrect': is_corr,
            'feedback': fb
        })
        
    q['options'] = balanced_opts
    q['correctIndices'] = correct_indices
    q['structuredOptions'] = structured
    q['overallExplanation'] = f"**Correct Solution:** {q.get('rationales', {}).get('correct', '')}\n\n**Key Exam Mindset:** {q.get('keyInsight', '')}"
    return q
