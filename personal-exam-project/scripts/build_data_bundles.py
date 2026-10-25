#!/usr/bin/env python3
"""
Bundle individual exam JSON files into track-specific JS data files.
Generates:
  - data/developer_data.js (window.EXAMS_DATA_DEVELOPER)
  - data/architect_data.js (window.EXAMS_DATA_ARCHITECT)
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

def bundle_track(track_name, var_name, out_file):
    track_dir = os.path.join(DATA_DIR, track_name)
    exams = []
    for i in range(1, 6):
        exam_path = os.path.join(track_dir, f'exam{i}.json')
        if os.path.exists(exam_path):
            with open(exam_path, 'r', encoding='utf-8') as f:
                exams.append(json.load(f))
        else:
            print(f"Warning: {exam_path} not found!")

    js_content = f"""/**
 * Auto-generated exam bundle for {track_name.upper()} track.
 * Contains {len(exams)} exams, total {sum(len(e.get('questions', [])) for e in exams)} questions.
 */
var {var_name} = {json.dumps(exams, indent=2, ensure_ascii=False)};

if (typeof window !== "undefined") {{
  window.{var_name} = {var_name};
}}
if (typeof module !== "undefined" && module.exports) {{
  module.exports = {var_name};
}}
"""
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(js_content)
    print(f"Bundled {len(exams)} exams to {out_file} ({os.path.getsize(out_file):,} bytes)")

def main():
    dev_out = os.path.join(DATA_DIR, 'developer_data.js')
    arch_out = os.path.join(DATA_DIR, 'architect_data.js')

    bundle_track('developer', 'EXAMS_DATA_DEVELOPER', dev_out)
    bundle_track('architect', 'EXAMS_DATA_ARCHITECT', arch_out)
    print("Bundle generation complete.")

if __name__ == '__main__':
    main()

