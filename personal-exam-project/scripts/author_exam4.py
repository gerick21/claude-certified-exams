#!/usr/bin/env python3
"""
Authoring Script for Architect Practice Exam 4:
'Practice Exam 4: Prompt Engineering & Structured Extraction'
53 Questions strictly following the Pearson VUE style blueprint and psychometric standards.
"""

import json
import os

def create_question(qid, domain_id, domain_name, sub_skill, module, scenario, options, correct_idx, rationales, key_insight, is_multi=False):
    letters = ['A', 'B', 'C', 'D']
    structured = []
    d_idx = 0
    corr_list = [correct_idx] if not is_multi else correct_idx
    for i, opt in enumerate(options):
        is_corr = i in corr_list
        if is_corr:
            fb = f"Correct. {rationales['correct']}"
        else:
            dist_text = rationales['distractors'][d_idx % len(rationales['distractors'])]
            fb = f"Incorrect. {dist_text}"
            d_idx += 1
        structured.append({
            "letter": letters[i],
            "text": opt,
            "isCorrect": is_corr,
            "feedback": fb
        })
    
    lens = [len(o) for o in options]
    ratio = max(lens) / min(lens)
    if ratio > 1.25:
        print(f"Warning: Q{qid} ratio {ratio:.2f} exceeds 1.25. Lengths: {lens}")
        
    return {
        "id": qid,
        "domainId": domain_id,
        "domainName": domain_name,
        "subSkill": sub_skill,
        "module": module,
        "scenario": scenario,
        "isMultiSelect": is_multi,
        "options": options,
        "correctIndices": corr_list,
        "rationales": rationales,
        "keyInsight": key_insight,
        "structuredOptions": structured,
        "overallExplanation": f"**Correct Solution:** {rationales['correct']}\n\n**Key Exam Mindset:** {key_insight}"
    }

questions = []

# ─── DOMAIN 1: Agentic Architecture & Orchestration (Q1 - Q14) ───────────────

# Q1 (Target: A = 0)
questions.append(create_question(
    qid=1,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Agent SDK Hooks",
    module="Domain 1 (Clinical Trial IRB Compliance Gate)",
    scenario="A pharmaceutical clinical trial data collection agent processes adverse patient event reports and submits them to an external regulatory database. Regulatory law requires that an Institutional Review Board (IRB) compliance signature be verified before any submission. Where should this check be implemented?",
    options=[
        "In a PreToolUse hook that checks IRB approval status and returns a deny decision if unverified.",
        "In a PostToolUse hook that parses the regulatory confirmation payload and raises an alert if missing.",
        "Within the coordinator system prompt using bold capital letters warning against unauthorized filings.",
        "In an hourly batch auditing script that identifies unapproved submissions after transmission."
    ],
    correct_idx=0,
    rationales={
        "correct": "In regulated environments like pharmaceutical clinical trials, submissions to external databases are irreversible. Enforcing verification in a PreToolUse hook physically intercepts and blocks the submission tool call if IRB compliance is not satisfied.",
        "distractors": [
            "PostToolUse runs after tool execution, meaning the unverified submission has already been transmitted to regulatory authorities.",
            "Prompt instructions are probabilistic and cannot provide a 100% deterministic compliance guarantee.",
            "Hourly batch audits are post-hoc and fail to prevent unauthorized regulatory filings before they occur."
        ]
    },
    key_insight="Enforce regulatory and legal submission gates in PreToolUse hooks to prevent unauthorized external data transmission."
))

# Q2 (Target: B = 1)
questions.append(create_question(
    qid=2,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Multi-Agent Orchestration",
    module="Domain 1 (Autonomous Vehicle Fleet Coordinator)",
    scenario="An autonomous vehicle fleet management system uses a coordinator agent to direct routing, battery charging, and maintenance subagents. Why must the battery charging subagent report its schedule back to the coordinator rather than dispatching vehicles to maintenance directly?",
    options=[
        "Subagents communicate over encrypted point-to-point sockets that corrupt vehicle telemetry.",
        "The coordinator must synchronize fleet battery schedules with overall passenger demand forecasts.",
        "The Claude Agent SDK enforces a hardware restriction limiting tool execution to single vehicles.",
        "Autonomous vehicle dispatching tools require compiling custom low-level device drivers in C."
    ],
    correct_idx=1,
    rationales={
        "correct": "In hub-and-spoke multi-agent systems, the coordinator maintains global operational context (fleet-wide passenger demand, emergency alerts, aggregate vehicle availability). Allowing subagents to schedule maintenance directly bypasses this global view and causes vehicle shortages.",
        "distractors": [
            "Point-to-point sockets do not corrupt vehicle telemetry; this is an irrelevant networking distractor.",
            "The Agent SDK supports managing arbitrarily large collections of entities, not limited to single vehicles.",
            "Vehicle dispatching tools are invoked via standard MCP API contracts, not C device drivers."
        ]
    },
    key_insight="Routing subagent updates through the coordinator preserves global operational context and prevents conflicting decentralized decisions."
))

# Q3 (Target: C = 2)
questions.append(create_question(
    qid=3,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Task Decomposition Strategies",
    module="Domain 1 (Deterministic vs Agentic Content Moderation)",
    scenario="A media platform processes 500,000 user comments per hour. Ninety-eight percent of comments are either completely benign or contain explicit blacklisted keywords. Two percent contain subtle, ambiguous policy edge cases. What is the optimal architecture?",
    options=[
        "Process 100% of comments through an autonomous multi-agent debate loop with five supervisors.",
        "Pass all 500,000 comments per hour into a single massive Claude prompt using temperature zero.",
        "Route through a deterministic keyword filter first, sending only the 2% ambiguous cases to Claude.",
        "Disable automated filtering entirely and hire 10,000 human moderators to inspect every comment."
    ],
    correct_idx=2,
    rationales={
        "correct": "Architectural proportionality demands deterministic code for predictable high-volume tasks (keyword filters and allowlists) and reserving expensive LLM reasoning strictly for the 2% ambiguous edge cases, saving millions in token costs while maintaining low latency.",
        "distractors": [
            "Running 500,000 comments through multi-agent debate loops incurs astronomical token costs and unviable latency.",
            "A single massive prompt turn cannot handle continuous streaming real-time comment traffic.",
            "Hiring 10,000 manual reviewers for trivial comments is economically infeasible when deterministic filters exist."
        ]
    },
    key_insight="Combine deterministic code filters for high-volume routine cases with LLM agents reserved strictly for ambiguous edge cases."
))

# Q4 (Target: D = 3)
questions.append(create_question(
    qid=4,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Subagent Invocation & Context Passing",
    module="Domain 1 (Parallel Forensics Subagents)",
    scenario="A cybersecurity incident response coordinator investigates an ongoing ransomware attack. To contain the breach rapidly, the coordinator needs to analyze firewall logs, active directory authentication records, and endpoint telemetry concurrently. How should these tasks be dispatched?",
    options=[
        "Execute each forensic analysis sequentially in a single turn to prevent API connection pooling.",
        "Buffer all logs into a local SQLite database and wait for a nightly scheduled batch scan.",
        "Instruct the user to manually read all firewall logs and paste anomalous IP addresses into chat.",
        "Emit multiple Task tool invocation blocks in a single model turn to execute forensic tasks in parallel."
    ],
    correct_idx=3,
    rationales={
        "correct": "Emitting multiple `Task` or `Agent` tool calls in a single coordinator response allows the Claude Agent SDK to execute subagents concurrently in parallel, drastically reducing wall-clock investigation time during active security incidents.",
        "distractors": [
            "Sequential execution triples investigation latency, allowing ransomware to spread across systems.",
            "Waiting for a nightly batch scan during an active live ransomware attack guarantees catastrophic data loss.",
            "Expecting users to manually parse millions of firewall lines defeats the purpose of autonomous incident response."
        ]
    },
    key_insight="Dispatch urgent concurrent investigative tasks by emitting multiple Task tool calls in a single turn for parallel execution."
))

# Q5 (Target: A = 0)
questions.append(create_question(
    qid=5,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Workflow Enforcement & Handoff",
    module="Domain 1 (Real Estate Human Approval Gate)",
    scenario="A commercial real estate transaction agent drafts purchase agreements, negotiates closing dates, and dispatches legally binding escrow wire transfers. Where must the human-in-the-loop approval gate be placed?",
    options=[
        "Immediately before executing the escrow wire transfer tool, blocking until a human approves.",
        "Immediately after the wire transfer tool executes, notifying the human that funds have left.",
        "At the start of the chat session, asking the human to sign off on all future unknown wires.",
        "In a weekly asynchronous audit email sent to the corporate accounting department."
    ],
    correct_idx=0,
    rationales={
        "correct": "Human-in-the-loop gates must be placed immediately BEFORE irreversible or high-liability operations (such as escrow wire transfers). Gating on the tool name before execution prevents unauthorized fund transfers, whereas post-execution gates occur after funds are gone.",
        "distractors": [
            "Placing the gate after execution means the irreversible wire transfer has already completed.",
            "Upfront blanket approval cannot foresee the exact dollar amount, recipient routing, or conditions of the wire.",
            "Weekly audit emails are post-hoc and cannot prevent fraudulent or erroneous real-time wire transfers."
        ]
    },
    key_insight="Place human-in-the-loop gates immediately before irreversible state changes or financial transfers, never after."
))

# Q6 (Target: B = 1)
questions.append(create_question(
    qid=6,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Session State & Resumption",
    module="Domain 1 (Educational Grading Rubric Branching)",
    scenario="An automated educational assessment agent evaluates student essays. The instructor wants to compare grading consistency across two different evaluation rubrics (holistic qualitative scoring vs analytical trait scoring) from the exact same parsed essay baseline. Which SDK method enables this?",
    options=[
        "Grade with Rubric 1, then instruct the model in the same thread to forget its prior scores.",
        "Use fork_session to branch two independent grading sessions from the parsed essay baseline.",
        "Create an external Redis message queue that duplicates student essay tokens across threads.",
        "Restart the assessment agent on each rubric and re-parse the student essay from raw PDF format."
    ],
    correct_idx=1,
    rationales={
        "correct": "`fork_session` branches multiple independent child sessions from a shared baseline. This allows applying both grading rubrics to the parsed essay context independently, preventing rubric scores on branch A from biasing branch B.",
        "distractors": [
            "Instructing the model to 'forget' prior scores in the same thread fails due to context anchoring bias.",
            "Redis message queues handle message routing, not LLM conversation state branching.",
            "Re-parsing from raw PDF restarts from scratch, incurring duplicate token extraction costs."
        ]
    },
    key_insight="Use `fork_session` to test divergent evaluation strategies from a shared parsed baseline without cross-contamination."
))

# Q7 (Target: C = 2)
questions.append(create_question(
    qid=7,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Workflow Enforcement & Handoff",
    module="Domain 1 (Adverse Event Structured Handoff)",
    scenario="An AI clinical trial assistant identifies a potential severe adverse drug reaction during patient interviews that requires immediate clinical intervention by a physician. What structure must the handoff payload provide?",
    options=[
        "The raw audio recording bytes from the patient microphone conversation stream.",
        "An encrypted cryptographic hash representing the patient medical record identifier.",
        "A structured dossier with patient ID, reported reaction, medication dosage, and vitals.",
        "A generic notification stating that an unspecified clinical event occurred on floor three."
    ],
    correct_idx=2,
    rationales={
        "correct": "A clinical escalation dossier must be self-contained: patient identifier, exact reported symptoms, medication dosage history, timeline, and recorded vitals. This allows medical personnel to take immediate clinical action without parsing verbose conversation transcripts.",
        "distractors": [
            "Raw audio bytes force clinicians to listen to full recordings, causing critical treatment delays.",
            "Cryptographic hashes provide zero clinical information regarding symptoms or dosages.",
            "Vague notifications fail to communicate clinical urgency or specific adverse reactions."
        ]
    },
    key_insight="Handoff dossiers in critical domains must be self-contained with all vital facts, enabling immediate professional action."
))

# Q8 (Target: D = 3)
questions.append(create_question(
    qid=8,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Session State & Resumption",
    module="Domain 1 (Fleet Management Stale Tool Resumption)",
    scenario="A fleet management agent paused overnight resumes operations in the morning via `--resume <session-id>`. Overnight, twenty autonomous delivery vehicles completed maintenance and changed bay locations. Upon resumption, the agent dispatches vehicles to occupied bays. What caused this failure?",
    options=[
        "The Claude Agent SDK automatically disables vehicle dispatching tools every twelve hours.",
        "The model context window was corrupted by nighttime operating system kernel patching.",
        "Vehicle bay locations require an active Bluetooth beacon connection to remain synchronized.",
        "The resumed session relied on stale cached tool outputs that changed during the pause."
    ],
    correct_idx=3,
    rationales={
        "correct": "When a session resumes via `--resume`, its context history contains tool results and observations from yesterday. If real-world state (vehicle locations, inventory) changed externally during the pause, the model makes decisions based on stale cached observations. A fresh start with injected current state is required.",
        "distractors": [
            "The Agent SDK has no feature that arbitrarily disables tools every 12 hours.",
            "OS kernel patches do not alter text tokens in session transcript files.",
            "Bluetooth beacons belong to hardware tracking, not the agent context synchronization layer."
        ]
    },
    key_insight="Resuming long-paused sessions risks reasoning on stale cached tool outputs. When physical or external state changes, start fresh with current state."
))

# Q9 (Target: A = 0)
questions.append(create_question(
    qid=9,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Task Decomposition Strategies",
    module="Domain 1 (Multi-Pass Incident Review)",
    scenario="A cybersecurity team analyzes 30 incident reports from a distributed denial-of-service attack. When passed into a single prompt, Claude's summary glosses over the middle 18 reports. How should the processing pipeline be restructured?",
    options=[
        "A multi-pass pipeline: extract indicators from each report individually, then aggregate across reports.",
        "A single prompt turn using Claude 3.5 Haiku with temperature configured to the maximum value of 1.0.",
        "Instruct the model in the prompt that missing an incident report will result in cloud server termination.",
        "Concatenate all 30 reports into a single file and compress it using standard gzip compression."
    ],
    correct_idx=0,
    rationales={
        "correct": "Passing 30 incident reports into a single prompt triggers severe attention dilution (lost in the middle). The established architectural remedy is a multi-pass structure: Pass 1 processes each report individually to extract indicators of compromise; Pass 2 correlates indicators across all reports.",
        "distractors": [
            "Switching to Haiku with high temperature increases hallucinations and reduces reasoning quality.",
            "Prompt threats add noise without solving the mathematical limits of attention over 30 long reports.",
            "Gzip compressed text produces unreadable binary tokens that cannot be parsed by language models."
        ]
    },
    key_insight="Overcome attention dilution across multiple complex documents with a multi-pass pipeline: localized per-document passes plus a cross-document aggregation pass."
))

# Q10 (Target: B = 1)
questions.append(create_question(
    qid=10,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Task Decomposition Strategies",
    module="Domain 1 (Dynamic vs Fixed Threat Hunting)",
    scenario="A security operations center designs an automated threat-hunting assistant. When investigating novel advanced persistent threats (APTs), why is dynamic adaptive decomposition required instead of a rigid sequential script?",
    options=[
        "Sequential scripts are prohibited by cloud provider security compliance rules.",
        "Each investigative step (querying endpoints, memory, network) depends on prior forensic findings.",
        "Dynamic agent loops consume fewer tokens than fixed scripts when processing identical log lines.",
        "The Claude Messages API disables tool use blocks whenever fixed sequential scripts are executed."
    ],
    correct_idx=1,
    rationales={
        "correct": "Threat hunting is fundamentally exploratory: an investigator cannot know in advance which host, IP address, or process hash is compromised. Dynamic adaptive decomposition allows the agent to formulate hypotheses, test them with tools, and choose next actions based on findings.",
        "distractors": [
            "Cloud compliance rules do not prohibit deterministic sequential scripts.",
            "Dynamic agent loops typically consume more tokens than fixed scripts due to reasoning turns.",
            "The Messages API supports tool use identically across all architectural patterns."
        ]
    },
    key_insight="Dynamic adaptive decomposition is essential for open-ended, exploratory tasks like threat hunting where next steps depend on discoveries."
))

# Q11 (Target: C = 2)
questions.append(create_question(
    qid=11,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Agentic Loops",
    module="Domain 1 (tool_use_id Linkage)",
    scenario="An application developer inspects tool use blocks returned by Claude. The assistant message includes two concurrent tool calls with IDs `call_abc123` and `call_def456`. When returning results to the Messages API, how must these IDs be mapped?",
    options=[
        "Return one single tool_result block and concatenate both IDs into a comma-separated string.",
        "Omit the IDs completely; the Messages API automatically matches results based on arrival order.",
        "Return two tool_result blocks, each explicitly specifying tool_use_id matching the call.",
        "Generate two new random UUIDs and pass them as query parameters in the HTTP authorization header."
    ],
    correct_idx=2,
    rationales={
        "correct": "The Messages API requires that every tool execution result be returned in a `tool_result` content block whose `tool_use_id` exactly matches the ID of the `tool_use` block emitted by the assistant.",
        "distractors": [
            "Concatenating IDs into a single block violates the Messages API schema contract.",
            "Omitting `tool_use_id` causes a 400 Bad Request error; the API requires explicit ID linkage.",
            "Generating new random UUIDs breaks correlation with the assistant's original tool call."
        ]
    },
    key_insight="Every `tool_result` content block must explicitly specify the `tool_use_id` corresponding to the assistant's tool call."
))

# Q12 (Target: D = 3)
questions.append(create_question(
    qid=12,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Subagent Invocation & Context Passing",
    module="Domain 1 (Context Isolation & Leaks)",
    scenario="A banking platform coordinator handles customer queries. When delegating a mortgage calculation to a financial calculator subagent, the coordinator accidentally passes the customer's full social security number and account balances in the prompt. What architectural boundary failed?",
    options=[
        "The operating system failed to enforce TLS 1.3 encryption on inter-process sockets.",
        "The Claude Agent SDK automatically synchronized unauthorized memory registers across subagents.",
        "The database management system omitted row-level security policies on mortgage tables.",
        "The coordinator failed to enforce least-privilege context masking before subagent dispatch."
    ],
    correct_idx=3,
    rationales={
        "correct": "Because subagents are separate instances with their own context windows (which may be logged or audited separately), the coordinator must practice least-privilege context passing: sanitize, redact, or mask sensitive PII (like SSNs) before injecting context into specialized worker subagents.",
        "distractors": [
            "TLS 1.3 socket encryption protects network transit, not application-level prompt payload hygiene.",
            "The Agent SDK does not automatically synchronize unauthorized memory registers.",
            "Row-level database security does not sanitize data already extracted and passed in application prompts."
        ]
    },
    key_insight="Practice least-privilege context passing: mask or redact sensitive PII before injecting context into child subagents."
))

# Q13 (Target: A = 0)
questions.append(create_question(
    qid=13,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Workflow Enforcement & Handoff",
    module="Domain 1 (Programmatic Gating vs Prompt Instructions)",
    scenario="A medical prescription verification agent checks patient allergies before transmitting drug orders to pharmacies. The prompt states: 'Check allergies before sending.' Production logs show that in 8% of cases, the agent sends orders without checking allergies. What is the definitive engineering solution?",
    options=[
        "Implement a programmatic gate blocking the send_order tool call until check_allergies succeeds.",
        "Add bold uppercase text in the prompt: 'NEVER EVER SEND PRESCRIPTIONS WITHOUT CHECKING ALLERGIES.'",
        "Add ten few-shot examples showing the allergy checking tool running before the prescription tool.",
        "Increase the model sampling temperature to 0.9 to encourage thorough safety reasoning."
    ],
    correct_idx=0,
    rationales={
        "correct": "In patient safety and healthcare compliance, probabilistic prompt instructions (including uppercase warnings and few-shot examples) will always exhibit a non-zero failure rate. Only programmatic gating (blocking `send_order` until `check_allergies` returns a verified clean record) ensures 100% compliance.",
        "distractors": [
            "Uppercase prompt warnings remain probabilistic guidance and routinely fail under conversational noise.",
            "Few-shot examples improve guidance but cannot provide the 100% deterministic guarantee required for clinical safety.",
            "Higher temperature increases sampling variance, worsening safety compliance failures."
        ]
    },
    key_insight="When human safety or regulatory compliance is at stake, programmatic gates are mandatory. Prompt guidance is inherently probabilistic."
))

# Q14 (Target: B = 1)
questions.append(create_question(
    qid=14,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Multi-Agent Orchestration",
    module="Domain 1 (Subagent Topology Constraints)",
    scenario="A junior engineer designs an agent architecture where three subagents form a circular ring, passing tasks to the next neighbor in a circle without a central coordinator. Why does enterprise architecture standard practice reject this circular topology?",
    options=[
        "Circular ring topologies cause electrical ground loops in enterprise data center servers.",
        "Lack of centralized coordinator state tracking makes loop termination and recovery impossible.",
        "The Anthropic Messages API enforces a physical ban on circular network socket configurations.",
        "Circular agent communication requires compiling custom binary Linux kernel extensions."
    ],
    correct_idx=1,
    rationales={
        "correct": "Circular agent topologies lack centralized state tracking, budget accounting, or termination authority. If an agent encounters an error or ambiguous requirement, the task can cycle endlessly in the ring, consuming infinite tokens with zero centralized error recovery.",
        "distractors": [
            "Software agent topologies have zero connection to physical electrical ground loops in server hardware.",
            "The Messages API is an HTTP REST interface; it does not inspect or ban software socket topologies.",
            "Agent loops run in standard user-space code (Python/TypeScript), requiring no kernel extensions."
        ]
    },
    key_insight="Avoid circular peer-to-peer agent topologies. Use hub-and-spoke architectures where the coordinator centralizes state and termination."
))

# ─── DOMAIN 2: Tool Design & MCP Integration (Q15 - Q24) ──────────────────────

# Q15 (Target: C = 2)
questions.append(create_question(
    qid=15,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="Tool Interface Design",
    module="Domain 2 (Clinical Database Tool Disambiguation)",
    scenario="A healthcare platform provides two clinical tools: `lookup_patient` (returns demographic and contact information) and `lookup_trial_enrollment` (returns active clinical trial participation history). Claude frequently calls `lookup_patient` when researchers ask for trial enrollment details. What is the most effective first fix?",
    options=[
        "Merge both tools into a single monolithic clinical_database_query tool accepting untyped JSON.",
        "Deploy a dedicated machine learning classifier to pre-route all clinician search queries.",
        "Expand tool descriptions with explicit parameter constraints and clear boundary definitions.",
        "Add eight conversational few-shot examples to the system prompt illustrating correct tool calls."
    ],
    correct_idx=2,
    rationales={
        "correct": "Tool descriptions are the primary decision surface Claude uses to select tools. Expanding descriptions with clear boundary statements (e.g. 'Use lookup_trial_enrollment for study IDs and enrollment status; do NOT use lookup_patient') is the most effective and proportionate first step.",
        "distractors": [
            "Merging tools into a monolithic interface obscures parameter contracts and worsens ambiguity.",
            "Building an external ML classifier is an expensive over-engineering step before basic descriptions have been refined.",
            "Adding 8 few-shot turns bloats prompt tokens and increases latency without addressing the root cause."
        ]
    },
    key_insight="Refine tool descriptions with explicit boundaries and negative constraints as the first-line fix for tool selection confusion."
))

# Q16 (Target: D = 3)
questions.append(create_question(
    qid=16,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="Structured Error Responses",
    module="Domain 2 (Regulatory Permission Error)",
    scenario="A pharmaceutical regulatory submission tool fails because the research site's API key lacks permission to access unblinded clinical trial data. According to MCP error categorization, how should this failure be returned to Claude?",
    options=[
        "Categorize as transient error with isRetryable true, prompting Claude to retry every ten seconds.",
        "Return an empty JSON object with HTTP 200 so Claude reports that unblinded data is clean.",
        "Categorize as a database validation error and instruct Claude to generate synthetic unblinded data.",
        "Categorize as permission error with isRetryable false, indicating required credentials are missing."
    ],
    correct_idx=3,
    rationales={
        "correct": "A lack of API permissions or authorization tokens is a permission error: it is non-retryable (isRetryable: false) without administrative credential updates. It must not be retried as a transient network timeout.",
        "distractors": [
            "Transient errors represent network timeouts where retrying the same credentials will succeed; retrying missing permissions fails indefinitely.",
            "Returning empty objects masks the authorization failure and leads Claude to report false medical clean bills.",
            "Generating synthetic data on missing clinical trial permissions commits scientific and regulatory fraud."
        ]
    },
    key_insight="Classify missing access rights as permission errors (`isError: true, category: 'permission', isRetryable: false`)."
))

# Q17 (Target: A = 0)
questions.append(create_question(
    qid=17,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="MCP Server Integration",
    module="Domain 2 (Pharmaceutical Compliance Secrets in .mcp.json)",
    scenario="A pharmaceutical research group configures an internal `.mcp.json` file for their clinical trial data warehouse. To comply with FDA 21 CFR Part 11 security regulations, how should the clinical warehouse API token be configured?",
    options=[
        "Reference environment variables using syntax like 'token': '${CLINICAL_API_KEY}' in .mcp.json.",
        "Hardcode the production API key directly inside the .mcp.json file committed to version control.",
        "Store the production token in an unencrypted plaintext file in the operating system /tmp directory.",
        "Pass the production token in the system prompt of every clinical research prompt turn."
    ],
    correct_idx=0,
    rationales={
        "correct": "In `.mcp.json`, sensitive API tokens must be referenced via environment variable expansion (`${CLINICAL_API_KEY}`). This allows the configuration to be committed to git without leaking production credentials, adhering to security regulations.",
        "distractors": [
            "Hardcoding production API keys into version-controlled files violates fundamental security and FDA compliance rules.",
            "Storing credentials in `/tmp` is insecure and accessible to unprivileged local processes.",
            "Placing credentials in system prompts exposes tokens to model context transcripts and logging."
        ]
    },
    key_insight="Use environment variable expansion (`${VAR}`) in `.mcp.json` to secure sensitive API credentials."
))

# Q18 (Target: B = 1)
questions.append(create_question(
    qid=18,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="Tool Distribution & tool_choice",
    module="Domain 2 (Content Moderation Mandatory tool_choice: any)",
    scenario="A content moderation pipeline must extract structured policy violation tags from reported user posts. The system supports three distinct classification tools depending on post format (text, image, audio). To ensure Claude ALWAYS executes one of these tools rather than replying with text, how should `tool_choice` be set?",
    options=[
        "Set tool_choice to 'auto' and configure the system prompt to prohibit conversational text.",
        "Set tool_choice to 'any' to mandate that Claude execute a tool while allowing it to pick which one.",
        "Force tool_choice to {'type': 'tool', 'name': 'text_moderation'} for all input formats.",
        "Omit the tool_choice parameter completely and let the default sampling settings apply."
    ],
    correct_idx=1,
    rationales={
        "correct": "Setting `tool_choice: 'any'` mandates that the model call at least one tool (prohibiting pure conversational text generation), while allowing the model to choose *which* tool to call based on input format (e.g. text vs image vs audio moderation).",
        "distractors": [
            "`tool_choice: 'auto'` permits conversational text replies whenever the model decides text is sufficient.",
            "Forcing `text_moderation` prevents calling image or audio moderation tools when those media formats appear.",
            "Omitting `tool_choice` defaults to `'auto'`, which does not guarantee tool execution."
        ]
    },
    key_insight="Use `tool_choice: 'any'` when a tool call is mandatory but the model must choose which specific tool matches the input data."
))

# Q19 (Target: C = 2)
questions.append(create_question(
    qid=19,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="Built-in Tools",
    module="Domain 2 (Glob for DICOM vs Grep for Reports)",
    scenario="A radiology research agent needs to locate all DICOM medical imaging files (`*.dcm`) across an archival directory tree, and then search clinical radiology text reports for mentions of 'pulmonary embolism'. Which built-in tools should be used for each task?",
    options=[
        "Use Grep to match DICOM file paths, and use Glob to search the text content of radiology reports.",
        "Use Read to load all binary DICOM images into context, and use Bash to search radiology reports.",
        "Use Glob to pattern-match *.dcm file paths, and use Grep to search report contents for text.",
        "Use Edit to rename all DICOM files, and use Write to overwrite the radiology reports."
    ],
    correct_idx=2,
    rationales={
        "correct": "`Glob` searches directory paths and matches file patterns (locating `**/*.dcm` files). `Grep` searches inside file contents for text strings ('pulmonary embolism'). This correctly assigns each tool to its purpose.",
        "distractors": [
            "Swapping Glob and Grep inverts their roles: Glob cannot search text inside files, and Grep is not meant for path pattern matching.",
            "Reading binary DICOM files into text context causes token decoding errors and exhausts memory.",
            "Edit and Write mutate files and do not perform file searches."
        ]
    },
    key_insight="Glob matches file PATHS and file extensions (`*.dcm`). Grep searches file CONTENTS for text patterns."
))

# Q20 (Target: D = 3)
questions.append(create_question(
    qid=20,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="Tool Distribution & tool_choice",
    module="Domain 2 (Scoping Moderation Subagents)",
    scenario="An online community platform provides tools for ban_user, delete_post, flag_content, edit_billing, update_dns, and reboot_server. Why should the content moderation subagent be scoped only to flag_content and delete_post?",
    options=[
        "The Claude Messages API limits total registered tools to exactly two per enterprise tenant.",
        "Cloud virtualization hypervisors reject container network traffic when six tools are active.",
        "DNS and server reboot tools can only be invoked by human developers typing on keyboards.",
        "Scoping tools strictly to moderation enforces least privilege and prevents catastrophic misrouting."
    ],
    correct_idx=3,
    rationales={
        "correct": "Providing administrative infrastructure tools (reboot_server, edit_billing, update_dns) to a content moderation bot violates least privilege and risks catastrophic accidents if the model misroutes a request. Restricting tools strictly to `flag_content` and `delete_post` keeps operations safe.",
        "distractors": [
            "The Messages API supports up to 128 tools per request, not limited to two.",
            "Virtualization hypervisors do not monitor application-level tool schema counts.",
            "Server reboot tools can be automated via APIs, but should never be given to content moderation bots."
        ]
    },
    key_insight="Enforce least privilege in tool distribution: never grant administrative, billing, or infrastructure tools to content analysis agents."
))

# Q21 (Target: A = 0)
questions.append(create_question(
    qid=21,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="Structured Error Responses",
    module="Domain 2 (Clinical Database Timeout vs Valid Empty Result)",
    scenario="A clinical trial patient lookup tool queries a remote oncology database. When searching for Patient ID `PT-88910`, the database responds in 50 ms indicating zero matching records exist. How should the tool report this result to Claude?",
    options=[
        "Return a successful payload with an empty records array, explicitly signaling zero matching records.",
        "Throw an HTTP 500 server error and instruct the agent to retry the query four times.",
        "Return an error payload with isError set to true and category set to transient network failure.",
        "Fabricate a synthetic patient record with default oncology values to avoid an empty result."
    ],
    correct_idx=0,
    rationales={
        "correct": "Finding zero records is a valid, successful query result: the database functioned properly and confirmed that the patient does not exist in oncology. Returning a clean result (e.g. `records: []`) allows Claude to inform the clinician accurately. It is NOT an error and must not be retried.",
        "distractors": [
            "Throwing a 500 error misrepresents an accurate empty search as a server infrastructure breakdown.",
            "Classifying an empty result as a transient error causes futile infinite retry loops.",
            "Fabricating synthetic patient records in oncology clinical trials is medical fraud."
        ]
    },
    key_insight="A query returning zero records is a valid successful result, NOT an error. Never retry valid empty results."
))

# Q22 (Target: B = 1)
questions.append(create_question(
    qid=22,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="MCP Server Integration",
    module="Domain 2 (Build vs Use Strategy for Data Warehouses)",
    scenario="A healthcare enterprise needs Claude to interact with GitHub for code tracking and an internal proprietary clinical data warehouse built on an in-house database engine. What is the recommended build-vs-use approach?",
    options=[
        "Author custom MCP servers from scratch for both GitHub and the proprietary data warehouse.",
        "Deploy the official community GitHub MCP server, authoring custom MCP only for the data warehouse.",
        "Avoid MCP completely and interact with both systems using raw curl commands via the Bash tool.",
        "Wait for Anthropic to release an out-of-the-box MCP server for the private internal database."
    ],
    correct_idx=1,
    rationales={
        "correct": "The standard architectural principle is adopting verified, community-maintained MCP servers for standard platforms (GitHub, Jira, Postgres) and focusing custom development strictly on proprietary, internal APIs.",
        "distractors": [
            "Re-authoring GitHub MCP from scratch wastes engineering time and forfeits community updates.",
            "Using raw curl commands via Bash bypasses schema validation, error handling, and security auditing.",
            "Anthropic will not author connectors for private proprietary internal healthcare engines."
        ]
    },
    key_insight="Adopt community MCP servers for standard platforms (GitHub). Author custom MCP servers only for proprietary internal systems."
))

# Q23 (Target: C = 2)
questions.append(create_question(
    qid=23,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="Tool Interface Design",
    module="Domain 2 (Tool Output Schema Trimming)",
    scenario="A medical records search tool returns patient summaries. The underlying database returns 60 columns, including internal database primary key UUIDs, row revision counters, and storage cluster IDs. Why should the tool strip these columns before returning results to Claude?",
    options=[
        "Cloud compliance laws prohibit transmitting database column names over HTTPS connections.",
        "The Claude Agent SDK throws an exception if any tool output contains more than ten keys.",
        "Pruning internal database metadata conserves context tokens and sharpens model diagnostic focus.",
        "Internal database primary keys automatically trigger prompt injection safety guardrails."
    ],
    correct_idx=2,
    rationales={
        "correct": "Database internal metadata (cluster IDs, primary keys, revision timestamps) provides zero semantic value to Claude while consuming context budget and cluttering model attention. Stripping extraneous columns preserves tokens and keeps the model focused on medical data.",
        "distractors": [
            "HTTPS connections securely transmit any valid JSON payload regardless of column naming.",
            "The Agent SDK places no arbitrary 10-key limit on tool outputs.",
            "Primary keys do not trigger prompt injection guardrails."
        ]
    },
    key_insight="Strip internal database metadata from tool outputs to conserve context tokens and sharpen model focus on relevant data."
))

# Q24 (Target: D = 3)
questions.append(create_question(
    qid=24,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="Built-in Tools",
    module="Domain 2 (Edit Tool Anchor Ambiguity)",
    scenario="Claude Code attempts to update a clinical dosage calculation function using the built-in `Edit` tool. The tool returns an error stating that `old_string` matches multiple identical lines in the file. What should Claude do next?",
    options=[
        "Retry the exact same Edit call ten times until non-deterministic string matching succeeds.",
        "Execute a Bash command that wipes the entire repository and re-clones from origin.",
        "Tell the clinician that the software cannot be updated due to a fatal filesystem lock.",
        "Use Read to view surrounding lines and supply a longer, unique anchor string for Edit."
    ],
    correct_idx=3,
    rationales={
        "correct": "The `Edit` tool requires `old_string` to be uniquely identifying. When identical lines exist in multiple places, using `Read` to inspect surrounding code allows expanding the anchor text with unique preceding and trailing lines.",
        "distractors": [
            "String matching in Edit is deterministic; retrying with identical arguments will fail identically every time.",
            "Wiping the repository destroys local work and uncommitted changes.",
            "A duplicate anchor string is a simple editing error, not a fatal filesystem lock."
        ]
    },
    key_insight="When the Edit tool fails due to ambiguous matching, expand surrounding context lines to create a uniquely identifiable anchor string."
))

# ─── DOMAIN 3: Claude Code Configuration & Workflows (Q25 - Q35) ─────────────

# Q25 (Target: A = 0)
questions.append(create_question(
    qid=25,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="CLAUDE.md Hierarchy",
    module="Domain 3 (Clinical Compliance CLAUDE.md)",
    scenario="A biotech software team authors strict FDA software validation guidelines in `.claude/CLAUDE.md` and commits it to their git repository. How does this benefit newly hired software engineers who join the project?",
    options=[
        "Every engineer automatically inherits verified compliance rules upon cloning the repository.",
        "The git commit automatically certifies the repository as compliant with FDA 21 CFR Part 11.",
        "New engineers are prevented from editing source files until passing an online compliance exam.",
        "Claude Code automatically compiles all Python files into encrypted bytecode on developer laptops."
    ],
    correct_idx=0,
    rationales={
        "correct": "Project-level `.claude/CLAUDE.md` files committed to git are automatically ingested by Claude Code for all team members, ensuring immediate, consistent inheritance of coding and compliance guidelines without manual setup.",
        "distractors": [
            "A markdown config file does not legally certify a repository with the FDA without audits and verification.",
            "CLAUDE.md provides guidance to Claude; it does not lock developer workstations or administer exams.",
            "Claude Code does not compile Python into encrypted bytecode."
        ]
    },
    key_insight="Commit project standards in `.claude/CLAUDE.md` so all team members automatically inherit guidelines upon cloning the repo."
))

# Q26 (Target: B = 1)
questions.append(create_question(
    qid=26,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="Skills Architecture",
    module="Domain 3 (Allowed-Tools in Clinical Exploration)",
    scenario="A clinical researcher authors a skill `.claude/skills/explore-trials/SKILL.md` to explore patient demographic trends. Because the research database is read-only, how should the skill prevent accidental data modification?",
    options=[
        "Add a prompt rule asking the researcher to promise not to request write operations.",
        "Whitelist only read tools (Read, Grep, Glob) in the allowed-tools YAML frontmatter field.",
        "Configure the operating system file permissions to read-only across all clinical servers.",
        "Instruct Claude to pause for sixty seconds before executing any write operations."
    ],
    correct_idx=1,
    rationales={
        "correct": "Configuring `allowed-tools` in `SKILL.md` frontmatter explicitly whitelists permitted tools. By omitting `Edit`, `Write`, and `Bash`, the skill is programmatically restricted to safe read-only operations.",
        "distractors": [
            "Prompt rules asking for promises are probabilistic and offer zero technical guarantees against data mutation.",
            "Changing server OS permissions can break background database operations and scheduled ingestion jobs.",
            "Pausing for 60 seconds introduces latency without preventing unauthorized writes."
        ]
    },
    key_insight="Enforce read-only skill execution programmatically by whitelisting only read tools in the `allowed-tools` frontmatter field."
))

# Q27 (Target: C = 2)
questions.append(create_question(
    qid=27,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="Path-Specific Rules",
    module="Domain 3 (Clinical Trial Module Path Rules)",
    scenario="A pharmaceutical repository contains 50 clinical trial study folders in `studies/**`. Each study has a validation test file `study_validation.test.ts`. The team wants strict FDA audit assertion guidelines to load whenever Claude touches these test files. What is the optimal architecture?",
    options=[
        "Copy identical copies of the FDA guidelines into all 50 individual study subfolders.",
        "Add all FDA guidelines to the global user configuration file located at ~/.claude/CLAUDE.md.",
        "Create .claude/rules/fda.md with frontmatter paths: ['studies/**/study_validation.test.ts'].",
        "Instruct developers to verbally recite FDA guidelines into their laptop microphones on every turn."
    ],
    correct_idx=2,
    rationales={
        "correct": "Path-specific rules in `.claude/rules/*.md` allow specifying glob expressions (e.g. `studies/**/study_validation.test.ts`). Claude Code dynamically loads these guidelines into context ONLY when matching files are accessed, avoiding 50 duplicate files and saving tokens.",
        "distractors": [
            "Duplicating 50 identical CLAUDE.md files creates an unmaintainable configuration nightmare.",
            "User-level `~/.claude/CLAUDE.md` is personal to one machine and will not be shared with team members.",
            "Verbal microphone recitation is an absurd, unworkable operational workflow."
        ]
    },
    key_insight="Use path-specific rules (`.claude/rules/*.md`) with glob patterns to apply guidelines dynamically across distributed module folders."
))

# Q28 (Target: D = 3)
questions.append(create_question(
    qid=28,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="Plan Mode vs Direct Execution",
    module="Domain 3 (Legacy Clinical Pipeline Restructure)",
    scenario="An engineering team plans to refactor an obsolete monolithic clinical data ingestion pipeline, modifying 50 integration points across database, queue, and API layers. Why should the lead architect mandate Plan Mode before implementation begins?",
    options=[
        "Plan Mode compiles Python source code into native machine assembly code for speed.",
        "Plan Mode bypasses all hospital firewall inspection rules during file reading operations.",
        "Plan Mode automatically purchases additional cloud GPU instances from Amazon Web Services.",
        "Plan Mode enforces read-only discovery, preventing chaotic partial edits across 50 files."
    ],
    correct_idx=3,
    rationales={
        "correct": "Plan Mode (`permission_mode='plan'`) blocks destructive file edits and tool execution, forcing Claude to perform read-only exploration of dependencies and generate an approved roadmap before altering 50 interdependent integration points.",
        "distractors": [
            "Plan Mode alters permission levels; it does not compile Python into assembly.",
            "Plan Mode does not alter or bypass hospital network firewall policies.",
            "Plan Mode has zero connection to purchasing AWS cloud infrastructure."
        ]
    },
    key_insight="Use Plan Mode on large, multi-file refactors to map architecture and get approval before executing destructive changes."
))

# Q29 (Target: A = 0)
questions.append(create_question(
    qid=29,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="CI/CD Integration",
    module="Domain 3 (Automated Regulatory Reports in CI)",
    scenario="A DevOps engineer integrates Claude Code into a GitHub Actions runner to generate automated regulatory compliance summaries during overnight builds. Which CLI flags guarantee non-interactive execution and machine-readable output?",
    options=[
        "Use -p (or --print) combined with --output-format json and --json-schema to ensure automated ingestion.",
        "Use --interactive --verbose and stream raw terminal logs over a public IRC chat channel.",
        "Use --headless --daemon and allow developers to SSH into the runner to answer questions.",
        "Redirect standard input from /dev/null and pipe unstructured prose to a printer device."
    ],
    correct_idx=0,
    rationales={
        "correct": "Non-interactive automation in CI requires `-p` (or `--print`) to prevent terminal deadlocks, paired with `--output-format json` and `--json-schema` to emit typed, schema-validated JSON for downstream build verification.",
        "distractors": [
            "`--interactive` causes the CI runner to hang waiting for keyboard input, and IRC streaming is insecure.",
            "Requiring developers to SSH into overnight CI runners defeats the purpose of autonomous builds.",
            "Piping unstructured prose to printer devices provides no automated machine validation."
        ]
    },
    key_insight="Combine `-p` with `--output-format json` and `--json-schema` to execute non-interactive, machine-verifiable CI/CD jobs."
))

# Q30 (Target: B = 1)
questions.append(create_question(
    qid=30,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="SDK setting_sources Parameter",
    module="Domain 3 (Site-Specific Hooks in setting_sources)",
    scenario="A clinical network runs research across three hospital sites. Each site configures local credential security hooks in `.claude/settings.local.json`. How must the Python Agent SDK script configure `setting_sources` so site-specific hooks execute?",
    options=[
        "Set setting_sources=[] to enforce a strictly hermetic execution across all three hospital sites.",
        "Set setting_sources=['project', 'local'] to load both repository standards and local site hooks.",
        "Set setting_sources=['user'] to ensure only global administrator preferences are respected.",
        "Delete setting_sources completely and hardcode site credentials inside the python script."
    ],
    correct_idx=1,
    rationales={
        "correct": "In the Claude Agent SDK, loading site-specific overrides and hooks from `settings.local.json` requires explicitly passing `'local'` in `setting_sources` (e.g. `setting_sources=['project', 'local']`).",
        "distractors": [
            "Setting `setting_sources=[]` ignores all local hooks and settings completely.",
            "`setting_sources=['user']` loads user home directory configs, ignoring local project and site hooks.",
            "Hardcoding credentials in Python scripts violates clinical security standards."
        ]
    },
    key_insight="Include `'local'` in `setting_sources` (e.g. `['project', 'local']`) to load site-specific hooks from `settings.local.json`."
))

# Q31 (Target: C = 2)
questions.append(create_question(
    qid=31,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="Iterative Refinement",
    module="Domain 3 (Interview Pattern for Clinical Trials)",
    scenario="A clinician asks Claude Code: 'Build a statistical module to calculate patient dropout rates.' The prompt omits vital criteria: censoring rules, handling missing visits, and confidence intervals. How should Claude proceed under best practice prompting?",
    options=[
        "Immediately write code for the simplest possible naive percentage calculation without questions.",
        "Reject the request with an error stating that medical doctors are not authorized to write code.",
        "Adopt the Interview Pattern: ask targeted clarifying questions regarding censoring and intervals.",
        "Implement five different contradictory statistical algorithms in five separate files."
    ],
    correct_idx=2,
    rationales={
        "correct": "When requirements are underspecified or mathematically ambiguous, the Interview Pattern instructs the agent to pause and ask targeted clarifying questions, ensuring alignment on technical specifications before generating code.",
        "distractors": [
            "Writing naive code on underspecified clinical requirements produces invalid statistical outputs.",
            "Abruptly rejecting clinician requests damages user adoption and software utility.",
            "Generating 5 contradictory algorithms creates confusion and wastes developer review effort."
        ]
    },
    key_insight="Use the Interview Pattern for ambiguous requirements: prompt the agent to ask clarifying questions before implementation."
))

# Q32 (Target: D = 3)
questions.append(create_question(
    qid=32,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="CI/CD Integration",
    module="Domain 3 (Fresh Session for Regulatory Review)",
    scenario="An AI system in Claude Code generates a clinical study submission document. To verify that the document complies with FDA electronic submission standards, why must the verification step run in a fresh, isolated Claude instance?",
    options=[
        "The FDA requires that all regulatory validation software run on Apple Silicon hardware.",
        "The Claude Agent SDK automatically deletes session transcripts whenever clinical files are touched.",
        "The Messages API enforces an account-level quota of one document review per calendar day.",
        "A separate instance eliminates self-confirmation bias, ensuring objective, impartial review."
    ],
    correct_idx=3,
    rationales={
        "correct": "When an agent reviews artifacts within the same conversation session that generated them, it retains internal reasoning bias and rationalizes its prior output. An independent, fresh instance evaluates the document strictly on its objective merits.",
        "distractors": [
            "FDA software standards are architecture-agnostic and do not mandate Apple Silicon hardware.",
            "The Agent SDK never deletes session transcripts automatically.",
            "There is no daily one-document review quota on the Messages API."
        ]
    },
    key_insight="Always conduct quality and compliance reviews in a fresh, independent session to eliminate confirmation bias."
))

# Q33 (Target: A = 0)
questions.append(create_question(
    qid=33,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="Custom Slash Commands & Skills",
    module="Domain 3 (Standardized Adverse Event Command)",
    scenario="A clinical operations lead creates a custom slash command `/adverse-event` that guides researchers through entering standardized clinical toxicity reports. Where should the command definition file be placed so that all researchers in the repo can run it?",
    options=[
        "In the repository directory at .claude/commands/adverse-event.md, committed to git.",
        "In the lead's personal laptop folder at ~/.claude/commands/adverse-event.md.",
        "Inside an external public GitHub repository configured as a git submodule.",
        "In an inline markdown code block within the project root CLAUDE.md file."
    ],
    correct_idx=0,
    rationales={
        "correct": "Custom slash commands in `.claude/commands/<name>.md` within the repository root are tracked in git and shared with all team members cloning the repo, providing standardized commands across the organization.",
        "distractors": [
            "Placing it in `~/.claude/commands/` makes it personal to a single laptop, unshared with team members.",
            "Git submodules add unnecessary configuration overhead for simple markdown commands.",
            "CLAUDE.md defines system instructions, not individual slash command scripts."
        ]
    },
    key_insight="Share project slash commands by placing them in `.claude/commands/` in the repository root."
))

# Q34 (Multi-select: Target: B = 1 and C = 2)
questions.append(create_question(
    qid=34,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="CLAUDE.md Hierarchy",
    module="Domain 3 (CLAUDE.md Rules and Structure)",
    scenario="An engineering architect designs a project-level `.claude/CLAUDE.md` file for a healthcare microservice repository. Which TWO of the following practices ensure that Claude Code adheres to instructions reliably without token bloat? (Select TWO)",
    options=[
        "Embed the entire 10,000-page hospital policy manual directly into the root CLAUDE.md file.",
        "Keep the root CLAUDE.md concise and focused on universal project-wide build, test, and style commands.",
        "Use path-specific rules (.claude/rules/*.md) for guidelines that apply only to specific file patterns.",
        "Instruct developers to re-enter all repository guidelines as conversation prompts on every turn."
    ],
    correct_idx=[1, 2],
    is_multi=True,
    rationales={
        "correct": "Options B and C are correct. Best practice for CLAUDE.md is keeping the root file concise (focusing on universal project-wide commands and build standards) and offloading domain- or path-specific rules to `.claude/rules/*.md` so they load only on demand, preventing token bloat.",
        "distractors": [
            "Embedding a 10,000-page policy manual exhausts token budgets and causes catastrophic instruction dilution.",
            "Manual prompt re-entry is fragile, time-consuming, and defeats the purpose of persistent configuration files."
        ]
    },
    key_insight="Keep root CLAUDE.md concise for universal project standards, and use path-specific rules (.claude/rules/) for targeted files."
))

# Q35 (Target: D = 3)
questions.append(create_question(
    qid=35,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="Iterative Refinement",
    module="Domain 3 (Clarifying Questions Before Refactor)",
    scenario="A lead architect asks an AI coding assistant to refactor an encryption service: 'Upgrade our cryptography to modern quantum-resistant algorithms.' The prompt does not specify key lengths, performance SLAs, or backward compatibility. How should the assistant respond?",
    options=[
        "Immediately delete all existing RSA keys and generate 4096-bit experimental keys.",
        "Refuse to answer and instruct the architect to read academic cryptography textbooks.",
        "Select an arbitrary algorithm at random and deploy it directly to the staging cluster.",
        "Ask targeted clarifying questions regarding algorithm preferences, compatibility, and SLAs."
    ],
    correct_idx=3,
    rationales={
        "correct": "For critical architectural changes with open trade-offs (cryptography, persistence, consensus), the agent should ask targeted clarifying questions to establish explicit requirements before touching production-critical code.",
        "distractors": [
            "Deleting existing encryption keys without approved backward compatibility breaks production systems.",
            "Refusing to assist damages collaboration and fails the engineering task.",
            "Arbitrary random selection on cryptographic algorithms introduces critical security vulnerabilities."
        ]
    },
    key_insight="Ask clarifying questions to resolve trade-offs on high-impact architectural requests before modifying code."
))

# ─── DOMAIN 4: Prompt Engineering & Structured Output (Q36 - Q45) ────────────

# Q36 (Target: A = 0)
questions.append(create_question(
    qid=36,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Structured Output with tool_use",
    module="Domain 4 (Clinical Trial Extraction Nullable Fields)",
    scenario="A clinical research extraction agent extracts patient laboratory test results from scanned hospital admission charts. In 15% of records, the patient did not receive a blood electrolyte test. How should the `electrolyte_panel` property be declared in the extraction JSON Schema?",
    options=[
        "Declare the property as nullable (e.g. type: ['object', 'null']) allowing null when omitted.",
        "Mark electrolyte_panel as a required object and instruct Claude in the prompt to guess values.",
        "Configure the schema to throw a validation crash whenever an electrolyte test is not documented.",
        "Instruct the model to substitute electrolyte data from another patient who had similar symptoms."
    ],
    correct_idx=0,
    rationales={
        "correct": "Marking missing clinical fields as nullable (`type: ['object', 'null']`) or optional allows the model to output `null` when tests were not performed, avoiding schema validation crashes and eliminating fabricated laboratory data.",
        "distractors": [
            "Guessing clinical laboratory values in medical research is scientific falsification and endangers lives.",
            "Crashing on missing optional tests rejects 15% of valid patient hospital charts.",
            "Substituting data from other patients violates medical data integrity and HIPAA regulations."
        ]
    },
    key_insight="Define missing laboratory fields as nullable in JSON schemas to prevent hallucinated clinical data."
))

# Q37 (Target: B = 1)
questions.append(create_question(
    qid=37,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Few-Shot Prompting",
    module="Domain 4 (Adverse Event Severity Grading)",
    scenario="A pharmacovigilance pipeline grades drug adverse events from Grade 1 (mild) to Grade 5 (death). The model frequently confuses Grade 2 (moderate impairment) and Grade 3 (severe hospitalization). What prompt engineering technique best improves classification accuracy?",
    options=[
        "Add an uppercase warning instructing the model to be extremely careful when assigning grades.",
        "Provide 2-4 few-shot examples with reasoning chains explaining the Grade 2 vs Grade 3 boundary.",
        "Switch the model to Claude 3.5 Haiku to increase the speed of adverse event grading.",
        "Instruct the model to assign Grade 5 to all reported symptoms to guarantee maximum safety."
    ],
    correct_idx=1,
    rationales={
        "correct": "Providing 2-4 targeted few-shot examples that include step-by-step reasoning chains explaining *why* specific clinical criteria crossed the Grade 2 vs. Grade 3 boundary anchors model reasoning on subtle clinical criteria.",
        "distractors": [
            "Uppercase prompt warnings provide zero clinical criteria for distinguishing Grade 2 from Grade 3.",
            "Switching to Haiku reduces reasoning depth and worsens borderline classification errors.",
            "Labeling all symptoms as Grade 5 (death) fabricates medical emergencies and ruins trial data."
        ]
    },
    key_insight="Use few-shot examples with explicit reasoning chains to teach models how to evaluate borderline classification thresholds."
))

# Q38 (Target: C = 2)
questions.append(create_question(
    qid=38,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Structured Output with tool_use",
    module="Domain 4 (Medical Image Reports and Diagnostic Guarantees)",
    scenario="A hospital radiology department extracts structured findings from physician mammography reports using Claude's tool_use feature with a validated JSON Schema. What guarantee does this architectural setup provide regarding diagnostic accuracy?",
    options=[
        "It guarantees that all extracted cancer diagnoses are 100% medically accurate and verified.",
        "It guarantees that the extracted findings will match the patient's downstream biopsy results.",
        "It guarantees that output JSON matches the schema, but does not guarantee diagnostic accuracy.",
        "It guarantees that all radiological measurements are calibrated against national physics standards."
    ],
    correct_idx=2,
    rationales={
        "correct": "`tool_use` with JSON Schema guarantees 100% syntactically valid JSON matching the declared data types. It provides ZERO guarantees regarding medical accuracy, factual correctness, or diagnostic validity, which must be verified by clinical experts.",
        "distractors": [
            "JSON schemas validate text structure, not the factual or medical validity of cancer diagnoses.",
            "A language model extraction tool cannot predict downstream physical biopsy pathology outcomes.",
            "Schemas do not calibrate physical radiological equipment or physics measurements."
        ]
    },
    key_insight="tool_use guarantees structural schema conformity, but does NOT guarantee factual or medical diagnostic accuracy."
))

# Q39 (Target: D = 3)
questions.append(create_question(
    qid=39,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Validation-Retry Loops",
    module="Domain 4 (Validation-Retry vs Missing Demographics)",
    scenario="A clinical intake extraction pipeline includes an automated validation-retry loop. For which of the following discrepancies is a retry loop effective, and for which is it futile?",
    options=[
        "Effective when the patient phone number is missing; futile when medication doses fail to sum.",
        "Effective for verifying physician medical licenses; futile for fixing corrupted date strings.",
        "Effective for extracting private thoughts; futile for calculating patient body mass index.",
        "Effective when table counts do not sum; futile when patient race is completely omitted from source."
    ],
    correct_idx=3,
    rationales={
        "correct": "Validation-retry loops work well when information is present in the source document and can be recalculated or reformatted (such as table counts summing). Retries are completely futile when information is genuinely absent from the source document (such as omitted demographic data); retrying absent data forces hallucinations.",
        "distractors": [
            "Missing phone numbers cannot be recovered by retrying if absent; arithmetic sum errors are easily fixed.",
            "License verification requires external databases; date formatting errors are easily fixed by retry.",
            "LLMs cannot read private human thoughts, but BMI arithmetic is straightforward."
        ]
    },
    key_insight="Validation-retry loops are effective for arithmetic and formatting errors where data exists, but futile when data is absent from source."
))

# Q40 (Target: A = 0)
questions.append(create_question(
    qid=40,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Batch Processing",
    module="Domain 4 (Overnight Clinical Trial Screening Batches)",
    scenario="A global pharmaceutical sponsor needs to process 10,000 patient clinical trial screening questionnaires overnight to identify eligible participants for a diabetes study. The results are needed in 16 hours. What API mechanism should be chosen?",
    options=[
        "Use the Message Batches API to capture a 50% discount within the 24-hour processing window.",
        "Deploy 50 concurrent synchronous web streaming connections with real-time audio playback.",
        "Run an interactive terminal session of Claude Code on an engineer's personal laptop overnight.",
        "Process questionnaires one by one using a single-threaded Python script with 5-second sleeps."
    ],
    correct_idx=0,
    rationales={
        "correct": "Processing 10,000 documents overnight with a 16-hour turnaround window is the ideal use case for the Message Batches API: it delivers a 50% cost discount across all token categories and completes within its 24-hour processing SLA.",
        "distractors": [
            "Real-time audio streaming is completely irrelevant for batch document text processing and wastes bandwidth.",
            "Running unattended batch jobs on personal laptops risks battery sleep, network loss, and crashes.",
            "Single-threaded processing with sleeps would take over 14 hours and costs twice as much as the Batch API."
        ]
    },
    key_insight="Use the Message Batches API for high-volume, non-interactive overnight document processing to capture the 50% discount."
))

# Q41 (Target: B = 1)
questions.append(create_question(
    qid=41,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Structured Output with tool_use",
    module="Domain 4 (Real Estate Purchase Self-Auditing)",
    scenario="A real estate escrow closing tool extracts closing costs from settlement statements: base purchase price, title insurance, loan origination fee, transfer taxes, and total funds due from borrower. How should the schema be designed to self-audit financial consistency?",
    options=[
        "Strip all closing fees and output only the base purchase price rounded to the nearest thousand.",
        "Include closing_fees_sum, stated_funds_due, and balance_discrepancy_detected in the schema.",
        "Rely on the client browser JavaScript code to silently rewrite the funds due field on submission.",
        "Instruct Claude to mentally verify that taxes are fair and reasonable according to state law."
    ],
    correct_idx=1,
    rationales={
        "correct": "A self-auditing schema includes fields for the calculated sum of fees (`closing_fees_sum`), the stated total due (`stated_funds_due`), and a boolean conflict flag (`balance_discrepancy_detected`). This forces the model to calculate and compare values, catching discrepancies immediately.",
        "distractors": [
            "Stripping closing fees conceals thousands of dollars in closing costs required for legal escrow settlement.",
            "Silently rewriting totals hides errors and corrupts financial settlement audits.",
            "Asking Claude to 'mentally verify' provides zero structured telemetry or verifiable data."
        ]
    },
    key_insight="Design self-auditing schemas with separate calculated and stated fields plus conflict flags to expose arithmetic discrepancies immediately."
))

# Q42 (Target: C = 2)
questions.append(create_question(
    qid=42,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Explicit Criteria",
    module="Domain 4 (Content Moderation Policy Rules)",
    scenario="A community moderation prompt instructs Claude: 'Use good judgment to flag inappropriate content.' The bot produces erratic results, flagging humorous jokes while passing targeted harassment. How should the prompt be refined?",
    options=[
        "Add exclamation marks to the prompt: 'USE VERY STRICT GOOD JUDGMENT AT ALL TIMES!'",
        "Switch the underlying model tier to Claude 3 Haiku to reduce computational complexity.",
        "Replace vague guidance with explicit categorical rules defining exact prohibited behaviors.",
        "Instruct the model to execute a bash curl command to check a random online dictionary."
    ],
    correct_idx=2,
    rationales={
        "correct": "Subjective directives like 'use good judgment' fail because models lack a shared cultural context of that phrase. Replacing vague directives with explicit categorical rules (e.g. 'Flag threats of violence, non-consensual sharing of PII, and slurs; do NOT flag benign satire or profanity not directed at individuals') produces consistent, reliable moderation.",
        "distractors": [
            "Punctuation and casing changes do not provide actionable semantic boundaries for moderation.",
            "Changing to a lighter tier reduces reasoning capability without providing rule definitions.",
            "Querying an online dictionary provides word definitions, not platform community conduct standards."
        ]
    },
    key_insight="Replace subjective directives like 'use good judgment' with explicit categorical rules defining exact prohibited behaviors."
))

# Q43 (Target: D = 3)
questions.append(create_question(
    qid=43,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Batch Processing",
    module="Domain 4 (Batch Failure Recovery custom_id)",
    scenario="A research sponsor submits 20,000 clinical trial survey extractions to the Message Batches API. Telemetry shows that 19,850 succeeded, while 150 failed due to rate limits on external schema validation servers. How should the team recover the 150 failed extractions?",
    options=[
        "Re-run all 20,000 extractions through the Batch API to ensure batch sequence consistency.",
        "Delete the 150 failed survey records and mark the overall trial extraction as 100% complete.",
        "Switch the remaining 150 extractions to manual human transcription without AI assistance.",
        "Filter batch results for errored custom_id items and resubmit only those 150 requests."
    ],
    correct_idx=3,
    rationales={
        "correct": "In the Message Batches API, each item is tagged with a developer-assigned `custom_id`. When partial failures occur, the application filters the results for `result.type == 'errored'` and resubmits ONLY those 150 specific `custom_id` items in a small follow-up batch, saving 19,850 duplicate calls.",
        "distractors": [
            "Re-running all 20,000 items wastes compute and incurs unnecessary token costs for 19,850 successful jobs.",
            "Deleting failed surveys discards legitimate clinical data and violates protocol integrity.",
            "Manually transcribing 150 surveys when an automated retry will succeed wastes clinician hours."
        ]
    },
    key_insight="Never re-run entire batch jobs. Correlate by `custom_id`, filter for errored items, and resubmit only the failed subset."
))

# Q44 (Target: A = 0)
questions.append(create_question(
    qid=44,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Multi-Instance Review",
    module="Domain 4 (Independent Safety Evaluation)",
    scenario="An AI system generates patient discharge instructions. To guarantee clinical safety, a hospital builds an automated AI safety evaluator. Why must the safety evaluator run in an independent Claude instance rather than continuing the discharge generation conversation?",
    options=[
        "An independent session eliminates self-confirmation bias, evaluating instructions with fresh scrutiny.",
        "The Claude tokenizer requires re-initializing memory registers after generating medical text.",
        "Hospital network security protocols prohibit multi-turn conversations exceeding two messages.",
        "Running in the same session permanently deletes the patient's electronic health record on disk."
    ],
    correct_idx=0,
    rationales={
        "correct": "When an agent reviews its own output within the same conversation thread, it carries internal confirmation bias, justifying its earlier reasoning. Running evaluation in an independent, fresh Claude instance ensures an objective, unbiased safety audit.",
        "distractors": [
            "Tokenizers are stateless algorithms that do not require re-initializing memory registers.",
            "Hospital network protocols do not enforce arbitrary two-message conversation limits.",
            "Conversational sessions have zero connection to deleting hospital electronic health records."
        ]
    },
    key_insight="Run safety and compliance evaluations in an independent, fresh Claude instance to eliminate conversational self-confirmation bias."
))

# Q45 (Target: B = 1)
questions.append(create_question(
    qid=45,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Explicit Criteria",
    module="Domain 4 (Content Moderation Severity Anchors)",
    scenario="A media platform trains an automated image commentary moderation bot with severity tiers: Low, Medium, and High. What prompt artifact should be provided in the system prompt to calibrate the boundary between Medium and High severity?",
    options=[
        "A long philosophical essay debating the nature of online offense and societal norms.",
        "Concrete descriptive text examples depicting exact scenarios for Medium and High severity.",
        "A single dictionary definition of the word 'severe' copied from an encyclopedia.",
        "An automated script that increases model temperature whenever High severity is suspected."
    ],
    correct_idx=1,
    rationales={
        "correct": "Calibrating severity boundaries requires providing concrete descriptive examples for each tier (e.g. specifying that insulting language is Medium, while credible threats of violence or child exploitation are High). Concrete anchors eliminate subjectivity.",
        "distractors": [
            "Philosophical essays consume tokens and introduce intellectual ambiguity without operational rules.",
            "Dictionary definitions of 'severe' provide zero domain-specific criteria for content policy.",
            "Increasing temperature increases randomness and worsens moderation inconsistency."
        ]
    },
    key_insight="Anchor severity boundaries with concrete descriptive examples for each tier rather than abstract prose definitions."
))

# ─── DOMAIN 5: Context Management & Reliability (Q46 - Q53) ───────────────────

# Q46 (Target: C = 2)
questions.append(create_question(
    qid=46,
    domain_id=5,
    domain_name="Context Management & Reliability",
    sub_skill="Context Preservation",
    module="Domain 5 (Preserving Medication Dosages in Case Facts)",
    scenario="A clinical triage assistant conducts a 14-turn patient consultation. In turn 2, the patient states they take '12.5 mg of carvedilol twice daily'. By turn 11, progressive conversational summarization compresses this to 'patient takes blood pressure medication', causing a dangerous drug interaction check to fail. What architectural pattern resolves this?",
    options=[
        "Instruct the patient to repeat their medication name and exact dose in every chat message.",
        "Increase the max_tokens output parameter on the Messages API to 16,384 tokens.",
        "Maintain a persistent Case Facts block containing verified medications that bypasses summarizers.",
        "Upgrade the model tier to Claude 3 Opus to expand the raw attention window."
    ],
    correct_idx=2,
    rationales={
        "correct": "Progressive summarization abstracts away critical clinical specifics (converting '12.5 mg carvedilol' into 'blood pressure medication'). The Case Facts block pattern stores verified entities once and injects them verbatim into every prompt, completely bypassing summarization.",
        "distractors": [
            "Forcing patients to repeat medications in every message causes extreme friction and patient error.",
            "Increasing max_tokens controls generation length, not the loss of detail during context summarization.",
            "Upgrading model tiers increases cost without preventing summarization algorithms from abstracting details."
        ]
    },
    key_insight="Store verified transactional and clinical data (dosages, numbers, dates) in a persistent Case Facts block that is never summarized away."
))

# Q47 (Target: D = 3)
questions.append(create_question(
    qid=47,
    domain_id=5,
    domain_name="Context Management & Reliability",
    sub_skill="Escalation & Ambiguity Resolution",
    module="Domain 5 (Multiple Matching Patient Records)",
    scenario="A clinical receptionist bot queries the hospital electronic health record database for 'John Smith'. The database returns four matching patient records with different medical record numbers (MRNs) and birth dates. What must the bot do?",
    options=[
        "Select the John Smith with the most recent hospital visit using an automated heuristic.",
        "Select the oldest John Smith assuming older patients require more urgent medical care.",
        "Randomly select one record and proceed to order diagnostic imaging tests.",
        "Prompt the patient for additional identifying details (e.g. date of birth or MRN) to disambiguate."
    ],
    correct_idx=3,
    rationales={
        "correct": "In medical and enterprise systems, using heuristics (most recent, oldest, highest value) on ambiguous database matches risks modifying the wrong patient record, leading to fatal clinical errors. The agent must pause and ask for clarifying identifiers (DOB or MRN).",
        "distractors": [
            "Selecting the most recent visit is an arbitrary heuristic that risks updating the wrong patient's chart.",
            "Age-based heuristics violate clinical safety protocols.",
            "Random selection on medical records constitutes gross clinical negligence and malpractice."
        ]
    },
    key_insight="Never use heuristics to resolve ambiguous database matches. Prompt the user for clarifying identifiers before accessing records."
))

# Q48 (Target: A = 0)
questions.append(create_question(
    qid=48,
    domain_id=5,
    domain_name="Context Management & Reliability",
    sub_skill="Error Propagation",
    module="Domain 5 (Partial Network Forensic Failure)",
    scenario="A cybersecurity investigation coordinator deploys four subagents to analyze compromised network segments: DMZ, Core, Cloud, and Branch. The Branch subagent fails due to an offline router. How should the coordinator finalize the breach assessment?",
    options=[
        "Synthesize DMZ, Core, and Cloud findings, explicitly annotating that Branch data was offline.",
        "Abort the entire investigation and delete all forensic findings collected from the DMZ and Core.",
        "Invent simulated Branch telemetry data using statistical distributions to complete the report.",
        "Freeze the coordinator execution process until the physical Branch router hardware is replaced."
    ],
    correct_idx=0,
    rationales={
        "correct": "In multi-agent orchestration, partial failure of an optional subagent must not abort the entire mission. The coordinator synthesizes the successful data streams and explicitly annotates the missing segment ('Branch data unavailable due to router outage'), preserving transparency.",
        "distractors": [
            "Aborting the investigation deletes critical forensic evidence and leaves active breaches uncontained.",
            "Inventing simulated telemetry in a cybersecurity breach investigation creates fraudulent audit trails.",
            "Freezing the process during an active cyberattack allows attackers to escalate privileges unhindered."
        ]
    },
    key_insight="Deliver available multi-agent findings transparently: synthesize successful data streams and annotate unavailable sections."
))

# Q49 (Target: B = 1)
questions.append(create_question(
    qid=50, # ID 49
    domain_id=5,
    domain_name="Context Management & Reliability",
    sub_skill="Context Degradation & Codebase Exploration",
    module="Domain 5 (Cybersecurity Scratchpads)",
    scenario="A digital forensics investigator conducts a 5-hour interactive session in Claude Code, examining 45 network packet captures and disk image logs. Over time, Claude's deductions degrade and it forgets compromised IP addresses discovered in hour one. How should this be mitigated?",
    options=[
        "Re-read all 45 raw packet captures from disk on every single turn to refresh model memory.",
        "Use external scratchpad files on disk to record compromised indicators, or use /compact.",
        "Instruct the investigator to complete all forensic investigations in less than fifteen minutes.",
        "Switch the model to a legacy snapshot that does not experience context saturation."
    ],
    correct_idx=1,
    rationales={
        "correct": "Extended interactive sessions accumulate massive context from verbose tool outputs, causing mathematical attention dilution. Offloading confirmed findings (compromised IPs, hashes) to an external scratchpad file or using `/compact` to compress history restores focus.",
        "distractors": [
            "Re-reading all 45 packet captures exacerbates token bloat and triggers context window overflow.",
            "Complex cybersecurity forensic investigations inherently take hours and cannot be rushed arbitrarily.",
            "All transformer models experience attention dilution in saturated contexts; legacy models are worse."
        ]
    },
    key_insight="Mitigate context degradation in long investigations by writing confirmed findings to external scratchpads and using /compact."
))

# Q50 (Target: C = 2)
questions.append(create_question(
    qid=50,
    domain_id=5,
    domain_name="Context Management & Reliability",
    sub_skill="Human Review & Confidence Calibration",
    module="Domain 5 (Stratified Prescription Accuracy Audit)",
    scenario="A pharmacy automated prescription processing pipeline achieves 95% aggregate accuracy across 100,000 prescriptions. A quality audit reveals that typed e-prescriptions have 99% accuracy, but handwritten physician scripts have a 30% error rate. What failure of evaluation methodology occurred?",
    options=[
        "The evaluation failed to reboot the cloud servers before testing handwritten prescriptions.",
        "The model was tested using temperature 0.0 instead of temperature 1.0 on handwritten scripts.",
        "The evaluation relied on aggregate metrics, concealing catastrophic error rates on handwritten scripts.",
        "The hospital pharmacists submitted prescriptions in non-standard UTF-8 character encoding."
    ],
    correct_idx=2,
    rationales={
        "correct": "The 'aggregate metrics trap' mathematically conceals high error rates in difficult sub-categories (handwritten prescriptions at 30% error) behind high volume in easy sub-categories (e-prescriptions at 99% accuracy). Evaluation must always be stratified across document classes.",
        "distractors": [
            "Server reboots do not impact model weights or handwriting OCR capabilities.",
            "Temperature zero is the standard best practice for deterministic extraction tasks.",
            "Character encoding has zero connection to handwritten script transcription errors."
        ]
    },
    key_insight="Beware the aggregate metrics trap: overall high accuracy frequently conceals catastrophic error rates in difficult sub-distributions."
))

# Q51 (Target: D = 3)
questions.append(create_question(
    qid=51,
    domain_id=5,
    domain_name="Context Management & Reliability",
    sub_skill="Escalation & Ambiguity Resolution",
    module="Domain 5 (Patient Explicit Physician Request)",
    scenario="A clinical intake assistant conducts a routine questionnaire. The patient abruptly states: 'I am experiencing sudden crushing chest pain and I need to speak to an emergency doctor right now.' What is the required architectural action?",
    options=[
        "Ask the patient to rate their chest pain on a scale of 1 to 10 before initiating escalation.",
        "Instruct the patient to take two aspirin and complete the remaining questionnaire fields.",
        "Execute a web search tool query to find articles on common non-cardiac causes of chest pain.",
        "Immediately trigger emergency clinical escalation protocols and alert emergency medical staff."
    ],
    correct_idx=3,
    rationales={
        "correct": "In medical triage, explicit emergency symptoms combined with a demand for a physician require immediate, unhindered emergency escalation. The agent must never delay escalation with questionnaires, web searches, or autonomous medical advice.",
        "distractors": [
            "Asking survey questions delays life-saving emergency medical intervention.",
            "Recommending medication (aspirin) without clinical diagnosis constitutes unauthorized medical practice.",
            "Searching the web for non-cardiac causes wastes critical time during an acute myocardial infarction."
        ]
    },
    key_insight="When emergencies or explicit human requests occur, trigger immediate escalation protocols without delaying for questionnaires."
))

# Q52 (Target: A = 0)
questions.append(create_question(
    qid=52,
    domain_id=5,
    domain_name="Context Management & Reliability",
    sub_skill="Information Provenance",
    module="Domain 5 (Chain of Custody Provenance)",
    scenario="A digital forensics agent extracts forensic artifacts from seized corporate hard drives. For the extracted findings to be admissible in federal court, what provenance metadata must be preserved alongside every extracted artifact?",
    options=[
        "Source file path, cryptographic SHA-256 hash, extraction timestamp, and tool version.",
        "The computer display monitor refresh rate of the forensics technician workstation.",
        "The personal email address and home phone number of the AI software developer.",
        "A synthetic confidence score between 95% and 100% generated by the model self-audit."
    ],
    correct_idx=0,
    rationales={
        "correct": "Legal admissibility in forensic investigations demands a rigorous chain of custody: source drive path, cryptographic SHA-256 hash, precise timestamp, and software tool version, proving that evidence was collected without alteration.",
        "distractors": [
            "Workstation display refresh rates have zero legal or forensic evidentiary relevance.",
            "Software developer personal contact details do not establish evidence chain of custody.",
            "Synthetic confidence scores are model hallucinations that lack legal evidentiary validity."
        ]
    },
    key_insight="Maintain complete chain of custody provenance: source path, cryptographic hashes, extraction timestamps, and tool versions."
))

# Q53 (Target: B = 1)
questions.append(create_question(
    qid=53,
    domain_id=5,
    domain_name="Context Management & Reliability",
    sub_skill="Context Preservation",
    module="Domain 5 (Lost in the Middle Placement)",
    scenario="An AI system evaluates 50-page clinical trial protocols to verify inclusion and exclusion criteria. Where should the user's specific query and critical extraction criteria be positioned within the prompt to maximize recall?",
    options=[
        "Buried directly in the middle of page 25 between raw laboratory measurement tables.",
        "At the very top of the prompt with clear section headers preceding the reference document.",
        "At the bottom of the prompt formatted in reverse alphabetical order with all spaces removed.",
        "In an external cloud database that the model queries using continuous recursive tool loops."
    ],
    correct_idx=1,
    rationales={
        "correct": "To overcome the 'lost in the middle' effect, position critical instructions, inclusion criteria, and specific queries at the very top of the prompt, with prominent Markdown section headers guiding the model before presenting reference documents.",
        "distractors": [
            "Placing critical instructions in the middle of page 25 places them in the exact zone of lowest attention.",
            "Reversing alphabetical order and removing spaces renders text illegible to language model tokenizers.",
            "Continuous recursive tool loops introduce massive latency and token expense for simple prompt placement."
        ]
    },
    key_insight="Place critical extraction criteria and queries at the very top of prompts to overcome the lost-in-the-middle effect."
))

# Fix any duplicate qids
for i, q in enumerate(questions):
    q["id"] = i + 1

exam4_data = {
    "id": 4,
    "title": "Practice Exam 4: Prompt Engineering & Structured Extraction",
    "description": "Schema design for high-stakes extraction, few-shot reasoning, validation loops, and production reliability.",
    "questions": questions
}

output_path = "data/architect/exam4.json"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(exam4_data, f, indent=2)

print(f"Successfully generated {len(questions)} questions in {output_path}!")
