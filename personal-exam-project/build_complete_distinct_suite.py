import json
from exam_balancer_util import balance_question_options

# 1. Load Exam 1
with open('questions.json') as f:
    e1_raw = json.load(f)

# 2. Load Exam 2
with open('exam2_suite.json') as f:
    e2_raw = json.load(f)

# 3. Load Exam 3 and fix duplicates
with open('exam3_suite.json') as f:
    e3_raw = json.load(f)

# Replace duplicate Q4 in Exam 3
e3_raw[3] = {
    "id": 4,
    "domainId": 1,
    "domainName": "Agents and Workflows",
    "subSkill": "Agent Architecture",
    "module": "Module 2 (Agent Architecture)",
    "scenario": "An agent orchestrator coordinates a sequence of three external microservice tool calls: reserve hotel, charge card, and book flight. The third tool call throws a 504 Gateway Timeout. What compensation pattern should the orchestrator execute to avoid partial state corruption?",
    "isMultiSelect": False,
    "options": [
      "Execute a compensating saga pattern that issues automated refund and cancellation tool calls for the earlier steps.",
      "Retry the flight booking tool 5,000 times in a synchronous while loop until the gateway responds.",
      "Terminate the conversation and notify the user that their credit card was charged without a flight.",
      "Lower the sampling temperature to 0.0 to force the third microservice to resolve the network timeout."
    ],
    "correctIndices": [0],
    "rationales": {
      "correct": "Option A is correct. When an agent workflow encounters a terminal failure after partial state has been committed, it should execute compensating transactions (the saga pattern) to roll back previously committed actions.",
      "distractors": [
        "Option B is incorrect because infinite retry loops hang the application.",
        "Option C is incorrect because leaving half-completed state damages customer trust.",
        "Option D is incorrect because temperature affects LLM sampling, not external network timeouts."
      ]
    },
    "keyInsight": "Implement compensating saga actions to cleanly roll back multi-step tool workflows when downstream steps fail."
}

# 4. Load Exam 4 and fix duplicates
with open('exam4_suite.json') as f:
    e4_raw = json.load(f)

# Replace duplicate Q25 in Exam 4
e4_raw[24] = {
    "id": 25,
    "domainId": 2,
    "domainName": "Applications and Integration",
    "subSkill": "Claude Application Design",
    "module": "Module 3 (Context Management in Code)",
    "scenario": "An automated code review pipeline running in GitHub Actions uses Claude to evaluate pull requests. A developer opens a pull request modifying 85 files across 12,000 lines of code. What is the recommended strategy to process this review without blowing the context window?",
    "isMultiSelect": False,
    "options": [
      "Decompose the pull request by module, running independent review passes per module before synthesizing top findings.",
      "Concatenate all 85 files into a single prompt and increase max_tokens to 100,000.",
      "Ignore all modified files and approve the pull request automatically to preserve API budget.",
      "Switch the GitHub Action to run on an on-premise mainframe using legacy COBOL scripts."
    ],
    "correctIndices": [0],
    "rationales": {
      "correct": "Option A is correct. Large multi-file tasks should be decomposed into modular chunks (per-file or per-module passes), with a final synthesis step aggregating critical findings to respect context limits.",
      "distractors": [
        "Option B is incorrect because dumping 85 files into one prompt causes severe context dilution and token bloat.",
        "Option C is incorrect because auto-approving without review defeats the purpose of code review.",
        "Option D is incorrect because COBOL mainframes are irrelevant."
      ]
    },
    "keyInsight": "Decompose large multi-file code reviews into modular per-module passes to respect context limits."
}

# Replace duplicate Q50 in Exam 4
e4_raw[49] = {
    "id": 50,
    "domainId": 8,
    "domainName": "Tools and MCPs",
    "subSkill": "Tool Implementation",
    "module": "Module 3 (Model Context Protocol)",
    "scenario": "An MCP database server exposes an execute_sql tool. Claude frequently hallucinates table and column names because the entire enterprise database schema is too large to fit in the tool description. What MCP pattern solves this?",
    "isMultiSelect": False,
    "options": [
      "Expose an on-demand describe_table tool or MCP Resource so Claude can inspect schema details when needed.",
      "Paste the entire 500-table database schema into the system prompt of every single API request.",
      "Configure the SQL database to accept any arbitrary query string without checking table names.",
      "Set sampling temperature to 0.0 so that Claude guesses database table names deterministically."
    ],
    "correctIndices": [0],
    "rationales": {
      "correct": "Option A is correct. When schemas or reference datasets are too large to fit in tool descriptions, provide an on-demand discovery tool (or MCP Resource) that the model invokes dynamically before generating queries.",
      "distractors": [
        "Option B is incorrect because pasting 500 table schemas wastes tens of thousands of tokens per call.",
        "Option C is incorrect because disabling database validation causes SQL crashes.",
        "Option D is incorrect because temperature 0 cannot deduce missing database names."
      ]
    },
    "keyInsight": "Expose on-demand schema discovery tools or MCP Resources for large databases to prevent tool description bloat."
}

# Replace duplicate Q51 in Exam 4
e4_raw[50] = {
    "id": 51,
    "domainId": 8,
    "domainName": "Tools and MCPs",
    "subSkill": "MCP Server Development",
    "module": "Module 3 (MCP Architecture)",
    "scenario": "A company wants to host an internal MCP server on a remote Kubernetes cluster that multiple developers and agents can access over the corporate network. Which transport protocol must the MCP server implement?",
    "isMultiSelect": False,
    "options": [
      "Server-Sent Events (SSE) / Streamable HTTP transport, providing network-accessible endpoints with TLS and auth.",
      "Local standard input and output (stdio) transport piped over a public USB-C serial cable.",
      "Raw unencrypted UDP packet broadcasts across public internet gateways.",
      "Direct neural network weight streaming over high-voltage electrical powerlines."
    ],
    "correctIndices": [0],
    "rationales": {
      "correct": "Option A is correct. For remote, networked MCP servers, the Model Context Protocol specifies Server-Sent Events (SSE) or Streamable HTTP transport, allowing networked clients to connect securely over TLS.",
      "distractors": [
        "Option B is incorrect because stdio is strictly for local processes on the same machine.",
        "Option C is incorrect because unencrypted UDP is unsupported by MCP and insecure.",
        "Option D is incorrect because electrical powerline streaming is fictional."
      ]
    },
    "keyInsight": "Remote networked MCP servers use Server-Sent Events (SSE) / HTTP transport; local tools use stdio."
}

# Replace duplicate Q52 in Exam 4
e4_raw[51] = {
    "id": 52,
    "domainId": 8,
    "domainName": "Tools and MCPs",
    "subSkill": "Agentic Customization",
    "module": "Module 3 (Custom Commands)",
    "scenario": "A developer wants to create a custom slash command in Claude Code (e.g. /benchmark) that executes an automated test suite and passes the report back to Claude. Where and how should this custom command be defined?",
    "isMultiSelect": False,
    "options": [
      "Create a markdown command specification in .claude/commands/benchmark.md containing the instructions and commands.",
      "Edit the Claude Code binary executable using a hex editor on the local machine.",
      "Upload the bash script to an unauthenticated public pastebin and add a comment in CLAUDE.md.",
      "Configure an enterprise deny rule in managed-settings.json that matches 'Bash(benchmark:*)'."
    ],
    "correctIndices": [0],
    "rationales": {
      "correct": "Option A is correct. Custom slash commands in Claude Code are defined as markdown files inside .claude/commands/<command_name>.md, holding instructions and execution steps.",
      "distractors": [
        "Option B is incorrect because hex editing binaries is unsupported and breaks CLI signatures.",
        "Option C is incorrect because public pastebin links are insecure and unsupported.",
        "Option D is incorrect because deny rules block commands rather than defining custom slash commands."
      ]
    },
    "keyInsight": "Custom Claude Code slash commands are authored as markdown files in .claude/commands/<name>.md."
}

# Replace duplicate Q53 in Exam 4
e4_raw[52] = {
    "id": 53,
    "domainId": 8,
    "domainName": "Tools and MCPs",
    "subSkill": "MCP Server Development",
    "module": "Module 3 (Model Context Protocol)",
    "scenario": "In the Model Context Protocol (MCP) specification, what is the fundamental functional distinction between an MCP Tool and an MCP Resource?",
    "isMultiSelect": False,
    "options": [
      "Tools represent executable functions that perform actions or computations; Resources represent readable data and documents.",
      "Tools are read-only text files; Resources are executable binary shell scripts that run as root.",
      "Tools can only be authored in Python; Resources can only be authored in compiled C++.",
      "Tools are limited to 5 characters of output; Resources have unlimited token capacity."
    ],
    "correctIndices": [0],
    "rationales": {
      "correct": "Option A is correct. Under the MCP architecture: Tools are active callable functions that perform actions or computations. Resources are passive readable data sources (like files, logs, or schemas) that provide context.",
      "distractors": [
        "Option B is incorrect because Tools are executable and Resources are readable context.",
        "Option C is incorrect because MCP is language agnostic.",
        "Option D is incorrect because there is no 5-character output limit on Tools."
      ]
    },
    "keyInsight": "MCP Tools are executable functions (actions/computations); MCP Resources are passive readable data sources."
}

print("Exam 1, 2, 3, 4 loaded and cleaned!")
