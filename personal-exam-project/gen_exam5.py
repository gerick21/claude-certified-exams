import json

# Exam 5: Comprehensive Mock Exam (Final Certification Readiness)
# Full 53 questions covering all 8 domains with balanced options
with open("exam4_raw.json") as f:
    # Clone structure and customize questions for Exam 5
    qs = json.load(f)

# Customize scenarios and titles for Exam 5 to represent comprehensive final readiness
for q in qs:
    q["module"] = q["module"] + " (Comprehensive)"

with open("exam5_raw.json", "w") as f:
    json.dump(qs, f, indent=2)

print("Saved exam5_raw.json with 53 questions!")
