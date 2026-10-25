#!/usr/bin/env python3
"""
Authoring Script for Architect Practice Exam 3:
'Practice Exam 3: Claude Code Workflows & CI/CD'
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
    sub_skill="Workflow Enforcement & Handoff",
    module="Domain 1 (Insurance Claim Prerequisite Gate)",
    scenario="An insurance claims processing agent reviews auto accident damage reports and issues settlement authorizations up to $2,500. Corporate compliance mandates that no settlement check can be authorized before the driver policy status is confirmed active. How should this constraint be enforced in production?",
    options=[
        "Programmatically block the authorize_payout tool call until verify_policy returns active.",
        "Add an urgent instruction in the system prompt stating that checking policy status is required.",
        "Include four few-shot examples in the prompt showing policy verification preceding payouts.",
        "Configure an asynchronous message broker to audit approved payouts every twenty-four hours."
    ],
    correct_idx=0,
    rationales={
        "correct": "When financial settlements are involved, prompt-based approaches (instructions or few-shot examples) carry an inherent failure rate. Only a programmatic gate or PreToolUse hook physically blocking `authorize_payout` until `verify_policy` succeeds provides a 100% deterministic guarantee.",
        "distractors": [
            "Prompt instructions remain probabilistic and have an unacceptable 8-12% failure rate in production.",
            "Few-shot examples improve model guidance but cannot guarantee complete deterministic compliance.",
            "Asynchronous auditing is post-hoc and fails to block unauthorized payouts before they are issued."
        ]
    },
    key_insight="High-stakes financial actions require programmatic prerequisite gates, physically preventing tool execution until prerequisites succeed."
))

# Q2 (Target: B = 1)
questions.append(create_question(
    qid=2,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Multi-Agent Orchestration",
    module="Domain 1 (Supply Chain Coordinator Hub)",
    scenario="An automated supply chain coordinator manages component shortages by interacting with supplier, inventory, and logistics systems. To maintain order integrity, why must all communication route through the coordinator rather than allowing the supplier agent to dispatch logistics tools directly?",
    options=[
        "Direct communication between subagents causes network packet collisions across cloud subnets.",
        "The coordinator must centralize inventory constraints, budget limits, and error handling.",
        "The Claude Agent SDK limits execution environments to exactly one active child subagent.",
        "Direct communication requires compiling custom C++ native bindings for each logistics tool."
    ],
    correct_idx=1,
    rationales={
        "correct": "In hub-and-spoke orchestration, centralizing communication through the coordinator ensures that global constraints (total inventory thresholds, shipping budgets, priority rules, and rollback handling) are enforced holistically rather than fragmented across peer agents.",
        "distractors": [
            "Subagents do not cause network packet collisions; this is an irrelevant low-level networking distractor.",
            "The Agent SDK supports multiple concurrent subagents, not capped at one.",
            "MCP tools and subagents are defined in Python, TypeScript, or JSON, not compiled C++ binaries."
        ]
    },
    key_insight="Centralizing communication through the coordinator in hub-and-spoke systems ensures consistent global state and centralized constraint enforcement."
))

# Q3 (Target: C = 2)
questions.append(create_question(
    qid=3,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Subagent Invocation & Context Passing",
    module="Domain 1 (Legal Document Review Attention Dilution)",
    scenario="A legal analysis agent is given 22 supplier contracts in a single prompt to identify non-standard indemnity clauses. Production testing shows that clauses in the first four contracts are thoroughly scrutinized, while clauses in contracts 15 through 22 are completely overlooked. What architectural pattern resolves this?",
    options=[
        "Switch the underlying model tier to Claude 3.5 Haiku to increase processing throughput.",
        "Instruct the model in the system prompt to read backwards starting from the final contract.",
        "Deploy a multi-pass pipeline analyzing each contract locally before cross-contract synthesis.",
        "Increase the max_tokens output parameter to 16,384 to allow longer review responses."
    ],
    correct_idx=2,
    rationales={
        "correct": "Processing 22 contracts in a single prompt induces severe attention dilution, causing the model to miss subtle clauses in later documents. A multi-pass pipeline resolves this: Pass 1 reviews each contract individually with full attention, while Pass 2 aggregates findings into a cross-contract synthesis.",
        "distractors": [
            "Switching to Haiku reduces reasoning depth without fixing the cognitive overload of 22 contracts.",
            "Prompting to read backwards is an unproven gimmick that merely shifts attention dilution to the beginning.",
            "Increasing max_tokens increases output length capacity but does not solve input attention dilution."
        ]
    },
    key_insight="Overcome attention dilution across multiple documents by implementing a multi-pass pipeline: localized individual document passes followed by cross-document synthesis."
))

# Q4 (Target: D = 3)
questions.append(create_question(
    qid=4,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Workflow Enforcement & Handoff",
    module="Domain 1 (Healthcare Compliance Custom Loop)",
    scenario="A healthcare platform designs an AI triage agent that handles Protected Health Information (PHI). Legal counsel mandates a signed HIPAA Business Associate Agreement (BAA) and Zero Data Retention (ZDR). Why must the team deploy a custom agent loop rather than Anthropic Managed Agents?",
    options=[
        "Managed Agents enforce rate limits that prevent processing multi-turn clinical records.",
        "Managed Agents execute tools client-side, exposing internal healthcare hospital endpoints.",
        "Managed Agents require passing sensitive database credentials in plain text in prompts.",
        "Managed Agents maintain stateful server-side sessions that are ineligible for BAA or ZDR."
    ],
    correct_idx=3,
    rationales={
        "correct": "Anthropic Managed Agents run in persistent, stateful server-side sandbox environments that are currently not covered by HIPAA BAA or Zero Data Retention (ZDR). Applications requiring BAA/ZDR compliance must use a custom agent loop using the Messages API on BAA-covered infrastructure.",
        "distractors": [
            "Compliance eligibility is determined by data residency and retention contracts, not rate limit quotas.",
            "Managed Agents execute on Anthropic-hosted sandboxes, not on customer client devices.",
            "Managed Agents do not require credentials to be sent in plaintext prompts."
        ]
    },
    key_insight="Managed Agent sessions are stored statefully server-side and ineligible for HIPAA BAA or ZDR. Use custom loops on BAA-covered infrastructure for PHI."
))

# Q5 (Target: A = 0)
questions.append(create_question(
    qid=5,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Session State & Resumption",
    module="Domain 1 (Logistics Strategy Branching)",
    scenario="A global logistics coordinator evaluates two competing air freight rerouting options during severe port congestion: chartering private air transport versus booking commercial passenger belly cargo. The architect wants Claude to explore both paths independently from the current cargo state. Which SDK feature is designed for this?",
    options=[
        "Use fork_session to branch two independent sessions from the baseline cargo state.",
        "Execute both options sequentially in the same thread while instructing Claude to forget.",
        "Create an operating system symbolic link to the underlying database transaction journal.",
        "Restart the agent from scratch on each branch and re-read all global shipping manifests."
    ],
    correct_idx=0,
    rationales={
        "correct": "The `fork_session` feature in the Claude Agent SDK allows branching from an established state into multiple independent exploratory sessions. Each branch inherits prior context up to the fork point and develops independently without cross-contaminating sibling sessions.",
        "distractors": [
            "Running sequentially in the same thread pollutes context and causes contradictory reasoning between the two opposing strategies.",
            "Filesystem symlinks do not isolate LLM conversational memory or tool execution histories.",
            "Restarting from scratch forces re-reading thousands of manifests, incurring massive latency and token spend."
        ]
    },
    key_insight="Use fork_session to branch independent exploratory paths from a common baseline state without cross-contaminating context."
))

# Q6 (Target: B = 1)
questions.append(create_question(
    qid=6,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Agent SDK Hooks",
    module="Domain 1 (PreToolUse Discount Policy Gate)",
    scenario="An enterprise e-commerce sales agent is authorized to offer promotional discounts up to 15%. If a customer demands a 25% discount, how should the architecture intercept and prevent this unauthorized discount before the order modification tool executes?",
    options=[
        "Inspect the order database every thirty minutes and cancel any orders exceeding discount caps.",
        "Intercept the tool invocation in a PreToolUse hook, inspect arguments, and return a deny decision.",
        "Allow the tool to execute, then invoke a PostToolUse hook to reverse the completed discount.",
        "Append a warning to the customer chat saying that their discount is pending manual approval."
    ],
    correct_idx=1,
    rationales={
        "correct": "A PreToolUse hook intercepts outgoing tool calls before execution. By inspecting the proposed discount argument (`discount_percentage > 15`), it returns `permissionDecision: 'deny'`, blocking the unauthorized discount deterministically before database modification occurs.",
        "distractors": [
            "Polling every 30 minutes allows invalid orders to be processed and shipped before cancellation.",
            "PostToolUse runs after the tool has already executed, meaning the unauthorized discount was already applied.",
            "Chat warnings do not prevent the underlying database mutation tool from executing."
        ]
    },
    key_insight="Use PreToolUse hooks to intercept and block policy violations before tool execution occurs. PostToolUse is too late to prevent mutations."
))

# Q7 (Target: C = 2)
questions.append(create_question(
    qid=7,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Agent SDK Hooks",
    module="Domain 1 (PostToolUse Currency Normalization)",
    scenario="A procurement agent queries three international supplier APIs. Supplier A returns prices in EUR, Supplier B in JPY, and Supplier C in USD. During final price comparison, Claude occasionally treats JPY values as USD, causing disastrous order miscalculations. Where should currency normalization be implemented?",
    options=[
        "In the coordinator system prompt with mathematical rules for real-time currency conversion.",
        "By prompting the user to manually convert all supplier currencies before submitting queries.",
        "In a PostToolUse hook that converts foreign currency quotes into standardized USD equivalents.",
        "By training a custom neural network adapter to recognize currency symbols during tokenization."
    ],
    correct_idx=2,
    rationales={
        "correct": "PostToolUse hooks intercept tool outputs immediately upon return from external APIs. Converting all foreign currencies into a standardized representation (e.g. USD with original quote metadata) in PostToolUse eliminates conversion errors before data enters Claude's context window.",
        "distractors": [
            "Prompt instructions force the model to perform mental arithmetic on volatile exchange rates, leading to frequent calculation errors.",
            "Asking end users to manually convert quotes defeats the purpose of autonomous procurement.",
            "Custom neural adapters cannot dynamically fetch live foreign exchange conversion rates."
        ]
    },
    key_insight="Use PostToolUse hooks to normalize heterogeneous data formats and currencies before they enter Claude's context window."
))

# Q8 (Multi-select: Target: A = 0 and D = 3)
questions.append(create_question(
    qid=8,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Subagent Invocation & Context Passing",
    module="Domain 1 (Spawning Subagents Requirements)",
    scenario="A platform developer builds a multi-agent system using the Claude Agent SDK where a central dispatcher spawns worker subagents dynamically. Which TWO of the following configurations are required for subagents to execute successfully in an unattended background worker? (Select TWO)",
    options=[
        "The coordinator's allowed_tools configuration must explicitly whitelist 'Task' or 'Agent'.",
        "The host operating system must assign real-time kernel scheduling priority to subagent threads.",
        "The child subagent definitions must share an identical system prompt with the coordinator.",
        "The child subagents must be configured with permissionMode set to 'bypassPermissions'."
    ],
    correct_idx=[0, 3],
    is_multi=True,
    rationales={
        "correct": "Options A and D are correct. Spawning subagents requires that the coordinator's allowed_tools whitelist the orchestration tool (`Task` or `Agent`). Furthermore, unattended background subagents must specify `permissionMode='bypassPermissions'`; otherwise, they block indefinitely waiting for user confirmation.",
        "distractors": [
            "Real-time kernel scheduling is an operating system feature unrelated to Agent SDK execution.",
            "Subagents do not need to share the coordinator's prompt; in fact, they should have specialized prompts tailored to their role."
        ]
    },
    key_insight="To spawn subagents in unattended environments, allowed_tools must include 'Task' or 'Agent', and permissionMode must be set to 'bypassPermissions'."
))

# Q9 (Target: B = 1)
questions.append(create_question(
    qid=9,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Workflow Enforcement & Handoff",
    module="Domain 1 (Deterministic Financial Execution)",
    scenario="A high-frequency cryptocurrency trading execution pipeline accepts market signals and triggers trade orders. A junior developer proposes replacing the existing deterministic Go execution pipeline with an autonomous multi-turn Claude agent loop. Why should the lead architect reject this proposal?",
    options=[
        "The Claude Messages API does not support processing numerical financial floating point data.",
        "Autonomous agent loops introduce non-deterministic latency and routing variance unsuitable for trading.",
        "Enterprise cloud firewalls reject all outgoing HTTP connections initiated by agentic loops.",
        "Language models cannot execute tool use calls when communicating over TLS 1.3 encrypted sockets."
    ],
    correct_idx=1,
    rationales={
        "correct": "High-frequency trade execution requires sub-millisecond determinism, predictable latency, and zero tolerance for routing variance. Autonomous agent loops introduce multi-second LLM sampling latency and non-deterministic decision paths, making them fundamentally inappropriate for high-frequency trade execution.",
        "distractors": [
            "The Messages API handles floating point numbers easily in standard text and JSON.",
            "Enterprise firewalls do not selectively block agentic loops over standard HTTPS.",
            "TLS 1.3 has zero conflict with tool use in modern REST APIs."
        ]
    },
    key_insight="Never replace deterministic, low-latency execution pipelines with autonomous agent loops when the task requires strict determinism and microsecond SLAs."
))

# Q10 (Target: C = 2)
questions.append(create_question(
    qid=10,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Agentic Loops",
    module="Domain 1 (Multi-Turn Conversation Accumulation)",
    scenario="An engineer builds a custom tool loop. After three turns of tool execution, the fourth call to the Messages API fails with an invalid request error indicating alternating user and assistant message role violations. What implementation mistake was made in the loop?",
    options=[
        "The tool execution output was returned with role 'assistant' instead of role 'user'.",
        "The application failed to sleep for five seconds between consecutive Messages API requests.",
        "The application appended tool results as consecutive user messages without assistant turns.",
        "The model context window reached its maximum token capacity during tool execution."
    ],
    correct_idx=2,
    rationales={
        "correct": "The Messages API requires strict role alternation: a user message must be followed by an assistant message, which is followed by a user message containing the tool_result blocks. Appending multiple consecutive user messages or misordering roles violates the API contract.",
        "distractors": [
            "Tool results are legitimately returned under role 'user' (containing tool_result content blocks); that is the expected role.",
            "The Messages API does not require arbitrary 5-second sleep delays between turns.",
            "Token capacity overflow returns a context_window_exceeded stop reason, not a role alternation validation error."
        ]
    },
    key_insight="Maintain strict message role alternation in the Messages API: user -> assistant (tool_use) -> user (tool_result) -> assistant."
))

# Q11 (Target: D = 3)
questions.append(create_question(
    qid=11,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Multi-Agent Orchestration",
    module="Domain 1 (Parallel Fan-Out Cost Traps)",
    scenario="A development team refactors a monolithic service by launching six parallel subagents, each assigned to refactor a tightly coupled subsystem sharing common global state. The monthly token spend increases twenty-fold, yet the output code fails to compile due to conflicting interface definitions. What is the root cause?",
    options=[
        "The Claude Agent SDK enforces a mandatory 15x token surcharge on parallel agent invocations.",
        "The child subagents were configured with temperature zero, suppressing required compiler tokens.",
        "Parallel agents require dedicated hardware GPU instances to synchronize shared memory state.",
        "Fan-out was applied to tightly coupled tasks with shared state rather than independent workstreams."
    ],
    correct_idx=3,
    rationales={
        "correct": "Parallel multi-agent fan-out multiplies token costs (~15-20x) and only delivers value when subtasks are truly independent. On tightly coupled refactorings where components depend on shared state and interfaces, subagents make conflicting assumptions, breaking compilation and wasting massive token spend.",
        "distractors": [
            "Anthropic charges standard per-token pricing; there is no artificial surcharge for parallel agents.",
            "Temperature zero controls sampling randomness, not token generation suppression.",
            "Agent state synchronization is an architectural design issue, not a hardware GPU requirement."
        ]
    },
    key_insight="Parallel multi-agent fan-out only pays off on independent workstreams. On tightly coupled tasks with shared state, it multiplies costs without quality gain."
))

# Q12 (Target: A = 0)
questions.append(create_question(
    qid=12,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Session State & Resumption",
    module="Domain 1 (Session State Persistence)",
    scenario="An interactive coding assistant needs to survive unexpected developer machine restarts without losing conversational history or pending tasks. How should the application architect the session state persistence layer?",
    options=[
        "Serialize conversation turns and active tool states to disk after every completed turn.",
        "Maintain the entire session history exclusively in volatile RAM to maximize read speed.",
        "Rely on the Anthropic cloud infrastructure to retain all uncommitted client terminal history.",
        "Require developers to re-enter their requirements from scratch whenever terminal windows close."
    ],
    correct_idx=0,
    rationales={
        "correct": "Because the Anthropic API is stateless, persistent sessions require the client application harness to serialize conversation turns, tool results, and execution state to durable disk storage after every turn, enabling clean resumption via session IDs.",
        "distractors": [
            "Keeping state solely in volatile RAM ensures total data loss upon machine reboots or crashes.",
            "Anthropic does not store client session transcripts server-side between stateless Messages API calls.",
            "Forcing users to re-enter requirements destroys developer productivity and user experience."
        ]
    },
    key_insight="Persist conversation turns and tool states to durable storage after every turn to ensure session recovery across restarts."
))

# Q13 (Target: B = 1)
questions.append(create_question(
    qid=13,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Task Decomposition Strategies",
    module="Domain 1 (Prompt Chaining vs Agentic Loops)",
    scenario="A data engineering pipeline extracts tables from invoices, translates vendor descriptions into English, and maps line items to ERP account codes. The workflow is completely linear with zero branching. Why is prompt chaining preferred over an autonomous agent loop for this workload?",
    options=[
        "Prompt chaining allows subagents to communicate directly with one another over WebSockets.",
        "Fixed prompt chains provide lower latency, predictable costs, and zero routing non-determinism.",
        "Prompt chaining automatically bypasses all Claude API token rate limits during peak traffic.",
        "Autonomous agent loops are prohibited from processing financial accounting documents by law."
    ],
    correct_idx=1,
    rationales={
        "correct": "For fixed linear sequences with no runtime exploration, prompt chaining (deterministic sequential calls) is vastly superior to an autonomous agent loop: it eliminates tool routing non-determinism, minimizes token overhead, and delivers lower latency at predictable cost.",
        "distractors": [
            "Prompt chaining does not involve peer-to-peer WebSocket communication between subagents.",
            "API rate limits apply equally to all request types regardless of orchestration design.",
            "There is no legal ban on using agent loops for financial document processing."
        ]
    },
    key_insight="Prompt chaining is faster, cheaper, and more reliable than autonomous loops for linear workflows with fixed execution paths."
))

# Q14 (Target: C = 2)
questions.append(create_question(
    qid=14,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Workflow Enforcement & Handoff",
    module="Domain 1 (Root Cause Handoff Dossier)",
    scenario="When an autonomous customer support agent escalates an ambiguous billing issue to a human supervisor, what critical element must be included in the handoff dossier to prevent the supervisor from re-investigating the root cause from scratch?",
    options=[
        "A full hex dump of the customer browser local session storage and cookie jar.",
        "The raw vector embeddings of all customer support tickets filed over the past five years.",
        "A clear summary of steps attempted, failed hypotheses, and the verified root cause.",
        "An encrypted cryptographic hash representing the supervisor employee authorization code."
    ],
    correct_idx=2,
    rationales={
        "correct": "An effective handoff dossier must summarize what has already been attempted, which hypotheses failed, verified facts, and the suspected root cause. This prevents the human specialist from duplicating failed troubleshooting steps and wasting customer time.",
        "distractors": [
            "Hex dumps of browser cookies are unreadable to human supervisors and violate customer privacy.",
            "Raw vector embeddings are mathematical floating point arrays useless to human specialists.",
            "Supervisor authorization hashes belong to authentication layers, not customer troubleshooting dossiers."
        ]
    },
    key_insight="Include attempted troubleshooting steps, ruled-out hypotheses, and verified facts in handoff dossiers to prevent duplicate effort."
))

# ─── DOMAIN 2: Tool Design & MCP Integration (Q15 - Q24) ──────────────────────

# Q15 (Target: D = 3)
questions.append(create_question(
    qid=15,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="Tool Interface Design",
    module="Domain 2 (Tool Description Boundaries)",
    scenario="A warehouse operations agent has access to two inventory tools: `lookup_stock` (queries real-time physical shelf inventory) and `lookup_catalog` (queries global supplier item specifications). Claude frequently calls `lookup_catalog` when users ask if an item is physically in stock. How should the descriptions be modified?",
    options=[
        "Delete lookup_stock and force users to calculate local inventory using shipping invoices.",
        "Add an operating system environment variable named INVENTORY_TOOL_DEFAULT pointing to stock.",
        "Re-train the model weights using reinforcement learning on company inventory logs.",
        "Add explicit boundaries: state lookup_stock is for shelf quantity; lookup_catalog is for specs."
    ],
    correct_idx=3,
    rationales={
        "correct": "Clear boundary statements in tool descriptions are the primary mechanism for resolving semantic tool confusion. Specifying that `lookup_stock` is strictly for real-time physical warehouse shelf counts and `lookup_catalog` is for static product specifications guides accurate tool selection.",
        "distractors": [
            "Deleting the stock lookup tool removes essential functionality.",
            "Environment variables do not influence model tool selection reasoning.",
            "Fine-tuning model weights is a massive, costly undertaking for a simple prompt/description defect."
        ]
    },
    key_insight="Disambiguate overlapping tools by adding explicit boundary statements defining exact use cases and negative boundaries in tool descriptions."
))

# Q16 (Target: A = 0)
questions.append(create_question(
    qid=16,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="Structured Error Responses",
    module="Domain 2 (Transient vs Terminal Errors)",
    scenario="A logistics tracking tool queries a third-party ocean carrier tracking API that returns an HTTP 504 Gateway Timeout due to temporary carrier maintenance. How should the tool return this error to Claude to enable proper recovery?",
    options=[
        "Return isError true with category 'transient' and isRetryable true, suggesting backoff retry.",
        "Return an empty JSON object with HTTP 200 so Claude reports the container arrived safely.",
        "Crash the host application server to force container orchestrators to redeploy the pod.",
        "Categorize as permanent validation error with isRetryable false, permanently canceling shipment."
    ],
    correct_idx=0,
    rationales={
        "correct": "An HTTP 504 Gateway Timeout is a transient infrastructure failure. Returning a structured error object with `isError: true`, category `'transient'`, and `isRetryable: true` instructs Claude that the failure is temporary, allowing backoff and retry.",
        "distractors": [
            "Returning empty objects masks the failure and leads Claude to hallucinate container status.",
            "Crashing the application pod disrupts all concurrent user sessions for a transient external API issue.",
            "Classifying a transient timeout as a permanent error prematurely cancels valid active shipments."
        ]
    },
    key_insight="Classify transient network timeouts as retryable errors (`isError: true, category: 'transient', isRetryable: true`) with backoff recommendations."
))

# Q17 (Target: B = 1)
questions.append(create_question(
    qid=17,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="Tool Distribution & tool_choice",
    module="Domain 2 (Forced Tool Invocation)",
    scenario="A regulatory compliance pipeline must classify internal corporate emails into legal discovery categories. The pipeline requires that Claude execute the `record_classification` tool on every email without exception, strictly forbidding conversational prose summaries. Which parameter enforces this?",
    options=[
        "Set tool_choice to 'auto' while instructing Claude in uppercase prompt text to call the tool.",
        "Set tool_choice to {'type': 'tool', 'name': 'record_classification'} on every request.",
        "Omit the tool definition completely and ask Claude to write JSON strings directly in chat.",
        "Configure temperature to 1.0 to increase model willingness to execute external tools."
    ],
    correct_idx=1,
    rationales={
        "correct": "Setting `tool_choice: {'type': 'tool', 'name': 'record_classification'}` forces the model to call that exact tool, physically disabling text generation or conversational fallbacks for that turn.",
        "distractors": [
            "`tool_choice: 'auto'` allows Claude to freely choose between text and tools regardless of prompt casing.",
            "Omitting tool definitions prevents structured tool use entirely.",
            "Higher temperature increases sampling variance, worsening formatting reliability."
        ]
    },
    key_insight="Use `tool_choice: {'type': 'tool', 'name': '...'}` to force execution of a specific tool in strict processing pipelines."
))

# Q18 (Target: C = 2)
questions.append(create_question(
    qid=18,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="Built-in Tools",
    module="Domain 2 (Grep vs Glob for Legal Discovery)",
    scenario="A legal discovery agent searches a 5,000-file repository of executive communications to find all files mentioning 'Project Titan'. What built-in tool strategy should the agent follow?",
    options=[
        "Use Glob to inspect the internal body text of all emails across the directory structure.",
        "Read all 5,000 files into memory simultaneously using concurrent asynchronous tasks.",
        "Use Grep to search file contents for 'Project Titan', then Read only the matching files.",
        "Execute a Bash sed script to overwrite every occurrence of 'Project Titan' with redactions."
    ],
    correct_idx=2,
    rationales={
        "correct": "`Grep` searches inside file contents for string occurrences ('Project Titan'). Using `Grep` quickly identifies the exact files and line numbers containing the string, allowing targeted `Read` calls on only relevant documents.",
        "distractors": [
            "Glob matches file names and paths, not the text content inside email body files.",
            "Reading 5,000 files into context exhausts token limits and costs thousands of dollars.",
            "Executing sed overwrites data and destroys legal discovery evidence."
        ]
    },
    key_insight="Use Grep to locate text matches within file contents, then Read only the matching files."
))

# Q19 (Target: D = 3)
questions.append(create_question(
    qid=19,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="Tool Distribution & tool_choice",
    module="Domain 2 (Warehouse Subagent Tool Scoping)",
    scenario="A warehouse automation system provides tools for packing, palletizing, shipping, payroll, truck scheduling, and inventory counts. Why should the packing subagent receive only the packing and palletizing tools?",
    options=[
        "Cloud network security groups prohibit agents from connecting to more than two IP subnets.",
        "The Messages API enforces a physical restriction of two tools per registered subagent.",
        "Providing unrelated tools causes operating system buffer overflow crashes in Docker.",
        "Scoping tools to roles maximizes tool selection accuracy and prevents unauthorized actions."
    ],
    correct_idx=3,
    rationales={
        "correct": "Scoping tools strictly to an agent's role (4-5 tools maximum) maximizes tool selection accuracy, minimizes parameter hallucinations, and enforces least privilege (e.g. preventing a packing bot from altering payroll records).",
        "distractors": [
            "Network security groups govern IP packets, not LLM tool schema distributions.",
            "The Messages API supports up to 128 tools per request, not restricted to two.",
            "Unrelated tools do not cause OS buffer overflows in container runtimes."
        ]
    },
    key_insight="Scope tools to agent roles (4-5 tools max) to maximize selection accuracy and enforce least-privilege operational boundaries."
))

# Q20 (Target: A = 0)
questions.append(create_question(
    qid=20,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="MCP Server Integration",
    module="Domain 2 (Custom vs Community MCP)",
    scenario="An organization integrates Claude with an internal proprietary inventory ERP system built in 2004 that communicates over custom TCP sockets, as well as a corporate Slack workspace. What is the recommended MCP integration strategy?",
    options=[
        "Deploy the official community Slack MCP server and author a custom MCP server for the ERP.",
        "Write custom MCP servers from scratch for both Slack and the legacy ERP system in C++.",
        "Avoid MCP and write custom web scrapers that parse the Slack web client interface.",
        "Wait for Anthropic to author a dedicated first-party connector for the legacy 2004 ERP."
    ],
    correct_idx=0,
    rationales={
        "correct": "The recommended architectural practice is deploying verified, maintained community MCP servers for standard platforms (Slack, GitHub, Postgres) while focusing development resources on authoring custom MCP servers for proprietary, in-house legacy systems.",
        "distractors": [
            "Reinventing Slack MCP from scratch wastes valuable engineering effort.",
            "Web scraping Slack violates terms of service, introduces fragility, and lacks API stability.",
            "Anthropic will not author custom connectors for private proprietary 2004 internal enterprise software."
        ]
    },
    key_insight="Use community MCP servers for standard platforms; author custom MCP servers only for proprietary internal systems."
))

# Q21 (Target: B = 1)
questions.append(create_question(
    qid=21,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="Structured Error Responses",
    module="Domain 2 (Payment Gateway Business/Policy Error)",
    scenario="A payment gateway tool receives a credit card charge request for an account that has been frozen due to fraud investigation. How should the payment gateway tool return this result to Claude?",
    options=[
        "Return isError true with category 'transient' and retry the charge every thirty seconds.",
        "Return isError true with category 'business_policy' and isRetryable false, with policy details.",
        "Simulate a successful charge by returning a fake approval authorization code.",
        "Throw an unhandled server exception to crash the customer's active checkout session."
    ],
    correct_idx=1,
    rationales={
        "correct": "A frozen account is a business/policy violation: it is non-retryable (isRetryable: false) and requires halting the transaction and diverting to customer verification. It must not be retried as a transient network error.",
        "distractors": [
            "Retrying a frozen account wastes API quota and risks triggering fraud alert lockouts.",
            "Simulating fake approvals commits financial fraud and causes severe reconciliation failures.",
            "Crashing checkout sessions provides a terrible customer experience and loses cart context."
        ]
    },
    key_insight="Classify account freezes and policy violations as business/policy errors (`isError: true, category: 'business_policy', isRetryable: false`)."
))

# Q22 (Target: C = 2)
questions.append(create_question(
    qid=22,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="MCP Server Integration",
    module="Domain 2 (MCP Environment Variable Expansion)",
    scenario="A software engineer configures a repository `.mcp.json` file for an internal database server requiring a secret password. How should the password be configured to prevent committing credentials to git?",
    options=[
        "Commit the real password in plaintext inside the project root .mcp.json configuration file.",
        "Hardcode the password in a personal file placed in the operating system root /tmp directory.",
        "Use environment variable expansion like 'password': '${DB_PASSWORD}' in the .mcp.json file.",
        "Encrypt the password with ROT13 and commit the encoded string directly to version control."
    ],
    correct_idx=2,
    rationales={
        "correct": "MCP configuration supports environment variable expansion (`${DB_PASSWORD}`). This enables teams to check `.mcp.json` into git while developers supply credentials securely via their local shell environments or CI/CD secret vaults.",
        "distractors": [
            "Committing plaintext passwords to git violates basic enterprise security standards.",
            "Storing credentials in `/tmp` is insecure and inaccessible across distributed machines.",
            "ROT13 is trivial substitution, not encryption, and exposes credentials immediately."
        ]
    },
    key_insight="Use environment variable expansion (`${VAR}`) in `.mcp.json` to keep secrets out of version control."
))

# Q23 (Target: D = 3)
questions.append(create_question(
    qid=23,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="Built-in Tools",
    module="Domain 2 (Edit Tool Surgical Replacement)",
    scenario="A code refactoring agent needs to change an imported utility function name across a 500-line source file without modifying any other code. Why is the built-in `Edit` tool preferred over the `Write` tool for this operation?",
    options=[
        "The Write tool is restricted by cloud security firewalls from opening TypeScript files.",
        "The Edit tool executes asynchronously while Write blocks the operating system kernel.",
        "The Write tool consumes three times fewer tokens when modifying existing source files.",
        "The Edit tool makes surgical replacements, avoiding the risk of truncating untouched code."
    ],
    correct_idx=3,
    rationales={
        "correct": "The `Edit` tool performs targeted string replacement using exact `old_string` and `new_string` anchors. This minimizes token output (emitting only the change) and eliminates the risk of accidentally truncating, reformatting, or hallucinating lines in the rest of the 500-line file, which can happen with `Write`.",
        "distractors": [
            "Firewalls do not selectively restrict the Write tool based on file extensions.",
            "Both tools execute within the same execution loop without OS kernel differences.",
            "Write requires re-emitting the entire 500-line file, consuming vastly MORE output tokens than Edit."
        ]
    },
    key_insight="Prefer the Edit tool for targeted changes to avoid re-emitting full files and eliminate truncation risks associated with Write."
))

# Q24 (Target: A = 0)
questions.append(create_question(
    qid=24,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="Tool Interface Design",
    module="Domain 2 (Input Schema Validation Rules)",
    scenario="An MCP tool accepts customer orders. The input schema defines `order_id` as a string matching regex `^ORD-[0-9]{5}$`. If Claude attempts to call the tool with `order_id: '12345'`, what behavior occurs before tool execution?",
    options=[
        "The MCP client schema validator rejects the call immediately and returns a validation error.",
        "The database automatically pads the number with leading zeros and executes the order.",
        "The Messages API silently terminates the entire conversation without notifying the client.",
        "The host operating system reboots the container to restore baseline regex definitions."
    ],
    correct_idx=0,
    rationales={
        "correct": "MCP tool contracts are enforced via JSON Schema validation on the client harness. When an argument violates schema constraints (pattern regex mismatch), the validator rejects the invocation immediately and returns a structured validation error back to Claude to self-correct.",
        "distractors": [
            "Databases never receive the query because client-side schema validation blocks execution before database submission.",
            "The API does not terminate conversations on tool schema validation failures.",
            "Regex failures belong to application validation, having zero connection to container reboots."
        ]
    },
    key_insight="Client-side JSON Schema validation rejects invalid tool arguments immediately, allowing Claude to self-correct before hitting backend systems."
))

# ─── DOMAIN 3: Claude Code Configuration & Workflows (Q25 - Q35) ─────────────

# Q25 (Target: B = 1)
questions.append(create_question(
    qid=25,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="CLAUDE.md Hierarchy",
    module="Domain 3 (Team-Wide Coding Standards)",
    scenario="An engineering organization with 40 developers wants all Claude Code sessions across the team to enforce strict ESLint standards and ban raw `any` types in TypeScript. Where should these instructions be placed?",
    options=[
        "In each developer's personal home folder configuration file at ~/.claude/CLAUDE.md.",
        "In the repository root configuration file at .claude/CLAUDE.md, committed to git.",
        "In an inline comment block at the top of the repository package-lock.json file.",
        "In a public GitHub gist URL referenced by an environment variable in developer shells."
    ],
    correct_idx=1,
    rationales={
        "correct": "Project-level instructions committed to `.claude/CLAUDE.md` in the repository root are automatically shared with all developers who clone the repository, ensuring uniform team-wide coding standards.",
        "distractors": [
            "Instructions placed in `~/.claude/CLAUDE.md` remain on individual developer machines and are not shared via version control.",
            "`package-lock.json` is a machine-generated package manifest that Claude Code does not parse for instructions.",
            "GitHub gist URLs require custom manual developer setup and are not part of Claude Code's native discovery tree."
        ]
    },
    key_insight="Commit team-wide standards to `.claude/CLAUDE.md` in the repository root so all developers automatically inherit them."
))

# Q26 (Target: C = 2)
questions.append(create_question(
    qid=26,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="Custom Slash Commands & Skills",
    module="Domain 3 (Project-Scoped Slash Commands)",
    scenario="A DevOps lead creates a slash command `/verify-release` that runs pre-deployment integrity tests. Where must the file be located so that any team member working in the repo can run it in Claude Code?",
    options=[
        "In the developer's personal directory at ~/.claude/commands/verify-release.md.",
        "Inside an external Amazon S3 bucket mounted over the local network via NFS.",
        "In the repository directory at .claude/commands/verify-release.md, committed to git.",
        "In an executable bash script located inside the root operating system /usr/bin path."
    ],
    correct_idx=2,
    rationales={
        "correct": "Placing custom slash commands in `.claude/commands/<command>.md` within the repository root makes them project-scoped and version-controlled, sharing them automatically with all repository collaborators.",
        "distractors": [
            "Placing it in `~/.claude/commands/` makes it personal to a single machine and unshared.",
            "Claude Code does not search external NFS-mounted S3 buckets for slash commands.",
            "`/usr/bin` is for system binaries, not Claude Code markdown command definitions."
        ]
    },
    key_insight="Share project slash commands by placing them in `.claude/commands/` within the version-controlled repository."
))

# Q27 (Target: D = 3)
questions.append(create_question(
    qid=27,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="Path-Specific Rules",
    module="Domain 3 (API Controller Path Rules)",
    scenario="A backend team maintains 30 REST controllers located in `src/api/**/*.controller.ts`. The team wants Claude to enforce OpenAPI validation rules strictly on these files without loading those rules during frontend React edits. What is the optimal configuration?",
    options=[
        "Duplicate the OpenAPI rules into 30 separate directory-level CLAUDE.md files.",
        "Instruct developers to verbally remind Claude of OpenAPI rules whenever editing APIs.",
        "Place all OpenAPI rules in root CLAUDE.md so they load across all prompt turns.",
        "Create .claude/rules/api.md with YAML frontmatter paths: ['src/api/**/*.controller.ts']."
    ],
    correct_idx=3,
    rationales={
        "correct": "Creating `.claude/rules/api.md` with YAML frontmatter `paths: ['src/api/**/*.controller.ts']` ensures that OpenAPI rules are loaded dynamically ONLY when matching controller files are accessed, conserving token budgets and avoiding duplication.",
        "distractors": [
            "Duplicating 30 CLAUDE.md files creates an unmaintainable maintenance nightmare.",
            "Relying on manual verbal developer reminders is error-prone and non-deterministic.",
            "Putting all rules in root CLAUDE.md wastes tokens on every unrelated frontend turn."
        ]
    },
    key_insight="Use path-specific rules (`.claude/rules/*.md`) with glob patterns to scope conventions to specific file patterns dynamically."
))

# Q28 (Target: A = 0)
questions.append(create_question(
    qid=28,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="Plan Mode vs Direct Execution",
    module="Domain 3 (Microservice Decomposition Planning)",
    scenario="A software team plans to migrate an e-commerce platform's monolithic billing database into two isolated database clusters, touching 55 files across services. Why should the architect mandate Plan Mode before code edits begin?",
    options=[
        "Plan Mode restricts tool execution to read-only discovery, preventing premature broken edits.",
        "Plan Mode automatically writes unit tests and deploys code directly to production clusters.",
        "Plan Mode enables faster GPU hardware acceleration on the Anthropic cloud cluster.",
        "Plan Mode bypasses all local compiler errors by disabling TypeScript strict mode."
    ],
    correct_idx=0,
    rationales={
        "correct": "Plan Mode (`permission_mode='plan'`) blocks destructive tool execution (writes, edits, shell mutations) and permits only read-only discovery. This forces Claude to map dependencies and generate a verified architectural roadmap before modifying 55 interdependent files.",
        "distractors": [
            "Plan Mode generates architectural plans; it does not deploy code to production clusters.",
            "Plan Mode changes permission levels, not backend cloud GPU hardware allocation.",
            "Plan Mode has no connection to disabling TypeScript strict mode."
        ]
    },
    key_insight="Use Plan Mode on complex, multi-file refactors to map dependencies and formulate an approved roadmap before executing changes."
))

# Q29 (Target: B = 1)
questions.append(create_question(
    qid=29,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="CI/CD Integration",
    module="Domain 3 (Automated Security Scanning in CI)",
    scenario="A security engineer configures Claude Code in a GitLab CI pipeline to perform automated static application security testing (SAST) on pull requests. Which invocation command runs non-interactively and emits typed JSON?",
    options=[
        "claude --interactive --scan-security --export-to-xml-file=sast.xml",
        "claude -p 'Run SAST security scan' --output-format json --json-schema ./schema.json",
        "claude --headless --daemon --background --force-zero-defect-guarantee",
        "cat pr_diff.txt | claude --stdin-only --output-unstructured-markdown-prose"
    ],
    correct_idx=1,
    rationales={
        "correct": "Non-interactive CI pipelines require `-p` (or `--print`) to prevent terminal hanging, and `--output-format json` with `--json-schema` to guarantee typed, machine-readable JSON for automated security gating.",
        "distractors": [
            "`--interactive` causes the pipeline to hang waiting for user keyboard input.",
            "`--headless`, `--daemon`, and `--force-zero-defect-guarantee` are fabricated CLI flags that do not exist.",
            "Unstructured markdown prose cannot be parsed reliably by automated CI security gating scripts."
        ]
    },
    key_insight="Combine `-p` with `--output-format json` and `--json-schema` to run non-interactive, machine-readable CI/CD security checks."
))

# Q30 (Target: C = 2)
questions.append(create_question(
    qid=30,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="SDK setting_sources Parameter",
    module="Domain 3 (Hermetic Air-Gapped CI Builds)",
    scenario="A defense contractor runs security validation in an isolated air-gapped CI environment using the Claude Agent SDK. The build must execute with zero influence from developer home directories, local git configs, or host settings. How should `setting_sources` be configured?",
    options=[
        "Set setting_sources=['user', 'project', 'local'] to load all security configurations.",
        "Set setting_sources=['project'] to ensure repository CLAUDE.md files are active.",
        "Set setting_sources=[] to enforce a strictly hermetic build ignoring all host configs.",
        "Omit the parameter completely to allow the SDK to auto-discover network settings."
    ],
    correct_idx=2,
    rationales={
        "correct": "Passing an empty list `setting_sources=[]` in `ClaudeAgentOptions` enables hermetic execution: the SDK ignores user settings (`~/.claude.json`), project `CLAUDE.md`, and local overrides, executing purely with explicitly supplied code parameters.",
        "distractors": [
            "`setting_sources=['user', 'project', 'local']` loads host settings, which violates air-gapped hermetic requirements.",
            "`setting_sources=['project']` still loads project markdown files from the local filesystem.",
            "Omitting the parameter allows default discovery, which may read host developer preferences."
        ]
    },
    key_insight="Pass `setting_sources=[]` to enforce hermetic execution in automated CI environments where host configs must be ignored."
))

# Q31 (Target: D = 3)
questions.append(create_question(
    qid=31,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="Skills Architecture",
    module="Domain 3 (Skills for DB Migrations)",
    scenario="A database engineer authors a specialized skill `.claude/skills/db-plan/SKILL.md` to analyze production schema changes. Running the skill involves generating 40 temporary SQL query plans. Why should the frontmatter specify `context: fork`?",
    options=[
        "It forces the database driver to commit transaction changes without validation.",
        "It automatically encrypts the local database connection string using AES-256.",
        "It allows the subagent to run on remote GPU clusters without local CPU consumption.",
        "It isolates verbose query plan exploration tokens from polluting the main conversation."
    ],
    correct_idx=3,
    rationales={
        "correct": "Setting `context: fork` runs the skill in an isolated subagent session. Intermediate scratchpad outputs, execution logs, and verbose query plans remain in the sub-session, returning only the synthesized migration plan to the parent conversation context.",
        "distractors": [
            "`context: fork` isolates conversation context; it does not commit database transactions.",
            "Context forking has no connection to connection string encryption.",
            "Subagents run in the same local execution environment, not on remote GPU clusters."
        ]
    },
    key_insight="Use `context: fork` in SKILL.md frontmatter to prevent intermediate verbose exploration logs from cluttering the main conversation."
))

# Q32 (Target: A = 0)
questions.append(create_question(
    qid=32,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="Iterative Refinement",
    module="Domain 3 (Test Failures as Feedback)",
    scenario="Claude Code generates a healthcare eligibility calculation module, but two Jest unit tests fail with edge-case null pointer exceptions. What is the most proportionate and reliable way to prompt Claude for the fix?",
    options=[
        "Provide the exact failing test names, assertion error traces, and input payloads.",
        "Instruct Claude that it failed healthcare compliance and demand that it rewrite all files.",
        "Increase the top-p sampling parameter to 0.95 to encourage diverse code variations.",
        "Restart the computer and rerun Claude Code with the identical original prompt."
    ],
    correct_idx=0,
    rationales={
        "correct": "Providing exact test names, stack traces, and failing input payloads gives the model precise, objective debugging targets, allowing it to trace root causes and apply surgical fixes.",
        "distractors": [
            "Emotional reprimands provide zero technical information about which assertions failed.",
            "Increasing top-p increases randomness, worsening regression errors.",
            "Rerunning the same prompt without error feedback will reproduce the same failure."
        ]
    },
    key_insight="Feed exact failing assertion traces and input payloads back to Claude to guide targeted, reliable bug fixes."
))

# Q33 (Target: B = 1)
questions.append(create_question(
    qid=33,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="CI/CD Integration",
    module="Domain 3 (Reviewing Generated Code Isolation)",
    scenario="An automated pipeline uses Claude Code to generate a microservice boilerplate, then uses the same Claude session to review the generated code for security vulnerabilities. The review flags zero vulnerabilities. Why is this pipeline flawed?",
    options=[
        "Claude Code requires a paid enterprise license to detect security vulnerabilities.",
        "The authoring session retains internal confirmation bias, requiring a fresh instance.",
        "The Messages API disables tool use blocks whenever code generation occurs.",
        "Microservice boilerplates are inherently immune to all common security vulnerabilities."
    ],
    correct_idx=1,
    rationales={
        "correct": "When an agent reviews code it generated in the same session, it suffers from severe confirmation bias, rationalizing its prior decisions. True verification requires launching a completely fresh, isolated Claude instance with zero prior session history.",
        "distractors": [
            "Security vulnerability detection is a standard capability requiring no special license.",
            "The Messages API supports tool use across all generation and review workflows.",
            "No boilerplate is inherently immune to vulnerabilities; thorough review is mandatory."
        ]
    },
    key_insight="Always conduct code reviews in a fresh, independent session to eliminate confirmation bias from the authoring session."
))

# Q34 (Target: C = 2)
questions.append(create_question(
    qid=34,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="CLAUDE.md Hierarchy",
    module="Domain 3 (CLAUDE.md Maintenance & Bloat)",
    scenario="A software team notices that their repository `CLAUDE.md` has grown to 1,200 lines, and Claude Code frequently ignores newer instructions placed at the bottom of the file. What architectural refactor resolves this instruction dilution?",
    options=[
        "Convert the entire CLAUDE.md file into base64 text stored in an environment variable.",
        "Instruct developers to verbally remind Claude of the bottom rules on every turn.",
        "Prune obsolete rules, split domain-specific rules into .claude/rules/, and use @import.",
        "Delete all repository instructions and rely entirely on zero-shot model defaults."
    ],
    correct_idx=2,
    rationales={
        "correct": "When `CLAUDE.md` becomes overly bloated (1,200 lines), instruction dilution occurs: the model struggles to attend to all rules. The established fix is pruning stale instructions, moving path-specific rules to `.claude/rules/` (which load on-demand), and using `@import` for modularity.",
        "distractors": [
            "Base64 encoding destroys natural language comprehension for the model.",
            "Manual verbal reminders are fragile and defeat the purpose of persistent configuration files.",
            "Deleting all instructions throws away all team conventions and quality standards."
        ]
    },
    key_insight="Prevent CLAUDE.md bloat by moving path-specific guidelines to `.claude/rules/` and modularizing core docs with `@import`."
))

# Q35 (Target: D = 3)
questions.append(create_question(
    qid=35,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="Custom Slash Commands & Skills",
    module="Domain 3 (Personal vs Project Commands)",
    scenario="A developer creates a personal slash command `/my-notes` that opens a private scratchpad on their laptop. The developer does NOT want this command visible or committed to the shared company repository. Where should this command file reside?",
    options=[
        "In the shared team git repository directory at .claude/commands/my-notes.md.",
        "Inside an external public GitHub repository configured as a git submodule.",
        "In an inline markdown code block within the project root CLAUDE.md file.",
        "In the developer's personal home directory at ~/.claude/commands/my-notes.md."
    ],
    correct_idx=3,
    rationales={
        "correct": "Personal slash commands that should not be committed to the shared repository belong in the user's home directory: `~/.claude/commands/<command>.md`. They are available on that specific machine across all projects without polluting version control.",
        "distractors": [
            "Placing it in `.claude/commands/` will cause it to be tracked in git and shared with all team members.",
            "Git submodules still commit references to the main repository.",
            "CLAUDE.md does not define custom slash commands; slash commands live in dedicated command markdown files."
        ]
    },
    key_insight="Store personal, uncommitted slash commands in `~/.claude/commands/`. Store shared team commands in `.claude/commands/`."
))

# ─── DOMAIN 4: Prompt Engineering & Structured Output (Q36 - Q45) ────────────

# Q36 (Target: A = 0)
questions.append(create_question(
    qid=36,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Structured Output with tool_use",
    module="Domain 4 (Nullable Fields in Partially Visible Documents)",
    scenario="A mobile document scanning app extracts data from damaged or coffee-stained paper receipts where the vendor tax identification number is frequently smudged and unreadable. How should the JSON Schema be defined to prevent Claude from hallucinating fake tax IDs?",
    options=[
        "Define tax_id as nullable (e.g. type: ['string', 'null']) and instruct Claude to return null when unreadable.",
        "Mark tax_id as a required string and instruct Claude in the prompt never to fabricate numbers.",
        "Configure the schema to reject any receipt where the tax ID is not exactly nine numeric digits.",
        "Instruct Claude to calculate the tax ID by taking the MD5 hash of the receipt total amount."
    ],
    correct_idx=0,
    rationales={
        "correct": "When physical documents frequently lack readable fields, marking those fields as nullable (`type: ['string', 'null']`) or optional allows the model to legitimately emit `null` when data is smudged. Marking the field as required forces the model to choose between schema rejection and hallucinating fake digits.",
        "distractors": [
            "Marking fields as required forces hallucinations regardless of prompt instructions against fabrication.",
            "Rejecting receipts with smudged tax IDs causes high transaction drop-off on legitimate customer purchases.",
            "Hashing receipt amounts fabricates arbitrary synthetic data that has zero legal validity."
        ]
    },
    key_insight="Make missing or damaged fields nullable (`type: ['string', 'null']`) in JSON schemas to eliminate hallucinations."
))

# Q37 (Target: B = 1)
questions.append(create_question(
    qid=37,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Structured Output with tool_use",
    module="Domain 4 (Insurance Form Enum Options)",
    scenario="An insurance intake form contains a checkbox question for 'Marital Status'. On handwritten scanned forms, claimants often write ambiguous notes like 'separated, pending trial'. How should the schema enum be structured?",
    options=[
        "Strictly limit the enum to ['single', 'married'] and let the model guess for all other cases.",
        "Include an 'unclear' or 'other' enum value paired with an optional freeform details field.",
        "Remove the field from the schema completely to avoid dealing with non-standard text.",
        "Throw an unhandled extraction exception and route the entire file to the fraud division."
    ],
    correct_idx=1,
    rationales={
        "correct": "Real-world documents contain ambiguous and non-standard entries. Providing an `'unclear'` or `'other'` enum option paired with a freeform string field (e.g. `marital_status_details`) allows the model to capture the non-standard reality accurately without failing schema validation.",
        "distractors": [
            "Forcing a binary choice forces the model to guess randomly, corrupting legal insurance records.",
            "Removing the field discards valuable demographic data required for policy underwriting.",
            "Routing claimants to the fraud division for handwritten notes is an extreme and unjustified business disruption."
        ]
    },
    key_insight="Pair enum fields with 'unclear' or 'other' and a freeform detail field to handle ambiguous real-world entries gracefully."
))

# Q38 (Target: C = 2)
questions.append(create_question(
    qid=38,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Structured Output with tool_use",
    module="Domain 4 (Self-Auditing Shipping Manifests)",
    scenario="A maritime shipping manifest extraction agent parses cargo container documents. The document states total container weight and lists 20 individual pallet weights. How should the schema be constructed to self-audit weight consistency before filing customs declarations?",
    options=[
        "Rely on customs inspectors at the ocean port to catch mathematical errors in declarations.",
        "Strip individual pallet weights and report only the total stated container gross weight.",
        "Include pallet_weights_sum, stated_total_weight, and weight_mismatch_detected in the schema.",
        "Instruct Claude to mentally add the weights and round all numbers to the nearest thousand."
    ],
    correct_idx=2,
    rationales={
        "correct": "A self-auditing schema includes fields for calculated sum (`pallet_weights_sum`), stated total (`stated_total_weight`), and a boolean discrepancy indicator (`weight_mismatch_detected`). This forces the model to compute and compare both numbers, exposing discrepancies immediately before customs filing.",
        "distractors": [
            "Relying on port customs inspectors triggers expensive penalties, cargo seizures, and shipping delays.",
            "Stripping individual weights violates customs regulations requiring granular cargo manifests.",
            "Rounding numbers to the nearest thousand conceals real weight discrepancies and corrupts vessel balance."
        ]
    },
    key_insight="Design self-auditing schemas with calculated, stated, and conflict-flag fields to catch arithmetic discrepancies before execution."
))

# Q39 (Target: D = 3)
questions.append(create_question(
    qid=39,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Batch Processing",
    module="Domain 4 (Overnight Batch Compliance Audits)",
    scenario="A banking compliance department must audit 100,000 internal emails every weekend for insider trading keywords. The results are not needed until Monday morning. What API feature should be used to minimize costs?",
    options=[
        "Use the synchronous Messages API with maximum concurrency across 50 server threads.",
        "Open 1,000 persistent WebSocket streaming connections from a cloud Kubernetes cluster.",
        "Deploy a self-hosted open-source language model on 20 on-premise GPU server racks.",
        "Use the Message Batches API to process the emails asynchronously with a 50% discount."
    ],
    correct_idx=3,
    rationales={
        "correct": "The Message Batches API is designed specifically for high-volume, non-interactive, latency-tolerant workloads with a 24-hour turnaround SLA. It provides a 50% discount across all token categories, saving thousands of dollars on large weekend compliance audits.",
        "distractors": [
            "The synchronous Messages API costs twice as much as the Batch API and is unnecessary for weekend audits.",
            "WebSockets are for real-time bidirectional streaming, not high-volume weekend batch audits.",
            "Self-hosting GPU racks incurs enormous hardware, power, and maintenance costs compared to serverless Batches."
        ]
    },
    key_insight="Use the Message Batches API for high-volume, latency-tolerant workloads to capture the 50% cost discount."
))

# Q40 (Target: A = 0)
questions.append(create_question(
    qid=40,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Batch Processing",
    module="Domain 4 (Blocking Pre-Merge PR Checks)",
    scenario="A software engineer proposes routing pre-merge pull request code linting through the Message Batches API to save 50% on token costs. Why must the lead architect reject this proposal?",
    options=[
        "Pre-merge CI checks are blocking workflows where developers cannot wait up to 24 hours for results.",
        "The Message Batches API automatically deletes git repositories after processing code files.",
        "The Message Batches API is restricted by Anthropic to processing plain English prose only.",
        "Pre-merge checks require real-time GPU audio rendering that the Batch API does not support."
    ],
    correct_idx=0,
    rationales={
        "correct": "Pre-merge pull request checks are blocking developer workflows: developers are actively waiting for checks to pass to merge their code. The Batch API has a turnaround window of up to 24 hours and offers zero latency SLA, which would paralyze development velocity.",
        "distractors": [
            "The Batch API processes text payloads and never touches or deletes git repositories.",
            "The Batch API supports all standard text, code, JSON, and multimodal inputs.",
            "Code linting does not involve GPU audio rendering."
        ]
    },
    key_insight="Never route blocking, interactive developer workflows (like pre-merge CI checks) to the Batch API, which has up to a 24-hour SLA."
))

# Q41 (Target: B = 1)
questions.append(create_question(
    qid=41,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Few-Shot Prompting",
    module="Domain 4 (Supply Chain Disruption Severity)",
    scenario="A logistics coordinator uses Claude to classify supply chain disruption alerts into 'Low', 'Medium', and 'High' severity. The model struggles with ambiguous supplier delays (e.g. 3-day component delay on a non-critical path). How should few-shot prompting be designed to resolve this?",
    options=[
        "Include fifty raw alert strings with one-word labels, omitting all explanatory notes.",
        "Include 3-4 diverse examples with reasoning chains explaining WHY delays were classified as Medium.",
        "Instruct the model to classify any delay over 24 hours as High severity unconditionally.",
        "Remove all few-shot examples and rely entirely on zero-shot inference with a high temperature."
    ],
    correct_idx=1,
    rationales={
        "correct": "Providing 3-4 diverse few-shot examples with explicit reasoning chains teaches the model how to evaluate borderline trade-offs (e.g. explaining that a 3-day delay on a non-critical component is Medium because buffer inventory exists). This fosters true semantic generalization.",
        "distractors": [
            "Raw input-label pairs without reasoning provide zero insight into why subtle borderline decisions were made.",
            "Rigid unconditional rules ignore whether components are on the critical path, misclassifying minor delays as emergencies.",
            "Zero-shot prompting with high temperature increases randomness and worsens classification inconsistency."
        ]
    },
    key_insight="Include reasoning chains in few-shot examples to teach the model how to weigh nuanced trade-offs on borderline classifications."
))

# Q42 (Target: C = 2)
questions.append(create_question(
    qid=42,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Multi-Instance Review",
    module="Domain 4 (Generation vs Quality Check Sessions)",
    scenario="An AI system generates legal lease agreement clauses, then verifies whether the clauses comply with state tenancy laws. Why should the generation and compliance verification steps run in two separate Claude sessions?",
    options=[
        "State tenancy laws require that AI legal documents be generated on different cloud subnets.",
        "The Messages API limits each active session context to generating exactly one paragraph of text.",
        "A separate review session eliminates conversational confirmation bias, evaluating text impartially.",
        "Running in the same session causes the underlying model weights to be permanently rewritten."
    ],
    correct_idx=2,
    rationales={
        "correct": "Evaluating generated text within the same conversation session induces strong confirmation bias: the model tends to validate its own earlier assumptions. Running compliance checks in a separate, fresh session guarantees an impartial, objective audit.",
        "distractors": [
            "Tenancy laws do not regulate cloud network subnet topologies.",
            "The Messages API supports arbitrarily long documents and multi-paragraph generation.",
            "Standard API calls never rewrite or fine-tune underlying model weights."
        ]
    },
    key_insight="Separate generation and review into distinct sessions to eliminate confirmation bias and ensure rigorous, impartial evaluation."
))

# Q43 (Target: D = 3)
questions.append(create_question(
    qid=43,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Validation-Retry Loops",
    module="Domain 4 (Validation Error Feedback)",
    scenario="An invoice extraction pipeline validates that `subtotal + tax == total`. In a scanned invoice, the extracted subtotal is $100, tax is $8, but extracted total is $118. What specific payload should the validation loop send back to Claude?",
    options=[
        "Send a blank user turn with instructions to re-read the entire source document from scratch.",
        "Send an angry error message threatening to replace the AI system with manual human data entry.",
        "Send a synthetic invoice document where numerical amounts have been modified to equal $108.",
        "The original document, previous output, and the specific mathematical discrepancy description."
    ],
    correct_idx=3,
    rationales={
        "correct": "A validation-retry loop must provide complete context: the original source document, the previous extraction, and the exact mathematical discrepancy (`Subtotal $100 + Tax $8 != Total $118`). This enables Claude to pinpoint where the discrepancy occurred (e.g. discovering a missed $10 shipping fee).",
        "distractors": [
            "A blank turn forces Claude to guess what failed without knowing which field had an error.",
            "Emotional reprimands add noise and provide zero mathematical or structural guidance.",
            "Fabricating synthetic invoices corrupts ground-truth records and introduces financial fraud."
        ]
    },
    key_insight="Validation-retry loops must include the original document, previous output, and the specific discrepancy description to enable targeted correction."
))

# Q44 (Multi-select: Target: A = 0 and B = 1)
questions.append(create_question(
    qid=44,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Structured Output with tool_use",
    module="Domain 4 (JSON Schema Guarantees vs Semantic Validation)",
    scenario="An enterprise architect reviews an automated data pipeline using Claude's tool_use feature with JSON schemas. Which TWO guarantees does JSON Schema enforcement provide, and which must be validated externally? (Select TWO guarantees provided by JSON schema)",
    options=[
        "It guarantees that all extracted output will be 100% syntactically valid JSON.",
        "It guarantees that all output fields match declared types such as string, integer, or array.",
        "It guarantees that numerical line items in tables will sum accurately to the stated total.",
        "It guarantees that extracted customer addresses exist in postal carrier physical databases."
    ],
    correct_idx=[0, 1],
    is_multi=True,
    rationales={
        "correct": "Options A and B are correct. JSON Schema enforcement with `tool_use` guarantees 100% syntactically valid JSON and enforces structural typing (strings, integers, booleans, arrays). It provides ZERO guarantees regarding arithmetic consistency or physical real-world facts (postal addresses), which require external verification.",
        "distractors": [
            "JSON schemas do not perform mathematical proofs or arithmetic audits on table values.",
            "JSON schemas validate structure, not real-world factual existence in external postal databases."
        ]
    },
    key_insight="JSON schema guarantees 100% syntactic validity and structural types, but does NOT guarantee arithmetic consistency or external real-world facts."
))

# Q45 (Target: C = 2)
questions.append(create_question(
    qid=45,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Explicit Criteria",
    module="Domain 4 (Categorical Rules for Code Smells)",
    scenario="A code quality bot instructs Claude: 'Flag all code smells and poor coding practices.' In production, developers complain the bot flags subjective variable names and personal whitespace preferences. How should the prompt be restructured?",
    options=[
        "Instruct the model to apologize to developers in every review comment it posts.",
        "Reduce the model context window to 4,000 tokens to prevent it from reading full functions.",
        "Define explicit categorical rules specifying exact anti-patterns (e.g. unclosed DB connections).",
        "Increase temperature to 0.8 to make code smell detection more creative and holistic."
    ],
    correct_idx=2,
    rationales={
        "correct": "Subjective terms like 'code smells' produce erratic and contentious review feedback. Replacing subjective guidelines with explicit categorical rules (e.g. 'Flag unclosed database connections, raw SQL concatenation, and unhandled promise rejections; do NOT flag naming styles or whitespace') ensures consistent, actionable feedback.",
        "distractors": [
            "Apologetic comments do not fix the underlying noise and false-positive clutter.",
            "Restricting context prevents the model from seeing variable declarations and connection lifecycles.",
            "Higher temperature increases variance and worsens subjective nitpicking."
        ]
    },
    key_insight="Replace subjective directives like 'flag code smells' with explicit categorical rules defining exact anti-patterns to flag."
))

# ─── DOMAIN 5: Context Management & Reliability (Q46 - Q53) ───────────────────

# Q46 (Target: D = 3)
questions.append(create_question(
    qid=46,
    domain_id=5,
    domain_name="Context Management & Reliability",
    sub_skill="Context Preservation",
    module="Domain 5 (Preserving Shipping Identifiers in Case Facts)",
    scenario="An international freight support bot manages shipments across customs, air cargo, and local couriers. During a 10-turn conversation, a 16-character customs declaration number (`CD-99281-X82-2026`) is compressed by a summarizer into 'the customer's customs paperwork', preventing subsequent tracking queries. How should this be prevented?",
    options=[
        "Instruct the customer to memorize their tracking number and paste it in every message.",
        "Increase the max_tokens output parameter of the summarization model to 8,192.",
        "Store the customs tracking number in a public pastebin URL referenced in the prompt.",
        "Pin verified customs declaration numbers in a persistent Case Facts block that bypasses summarizers."
    ],
    correct_idx=3,
    rationales={
        "correct": "Exact alphanumeric identifiers (customs declaration numbers, tracking IDs, dates, dollar amounts) must be preserved in a persistent 'Case Facts' block that is injected verbatim into every turn and NEVER passed through summarizers, preventing destructive compression.",
        "distractors": [
            "Forcing customers to repeatedly paste tracking numbers in every message is unacceptable customer service.",
            "Increasing summarization max_tokens does not prevent the model from abstracting specific strings into prose summaries.",
            "Storing private customs numbers in public pastebins is a severe enterprise data leak."
        ]
    },
    key_insight="Pin exact tracking numbers, customs IDs, and dates in a persistent Case Facts block that completely bypasses summarizers."
))

# Q47 (Target: A = 0)
questions.append(create_question(
    qid=47,
    domain_id=5,
    domain_name="Context Management & Reliability",
    sub_skill="Escalation & Ambiguity Resolution",
    module="Domain 5 (Loyalty Program Disambiguation)",
    scenario="A customer types: 'Redeem my points for a flight voucher.' A database query reveals the customer has two loyalty accounts: a personal silver tier account and a corporate diamond tier account. What is the correct architectural action?",
    options=[
        "Ask the customer to clarify which loyalty account they wish to redeem points from.",
        "Redeem points from the corporate diamond tier account automatically using a value heuristic.",
        "Redeem points from the personal silver tier account because it was created first chronologically.",
        "Throw an unhandled database exception and terminate the customer's active chat session."
    ],
    correct_idx=0,
    rationales={
        "correct": "When encountering duplicate or ambiguous entity matches, an agent must NEVER use heuristics (such as highest tier, most recent, or oldest). It must pause and explicitly ask the customer for clarifying details to ensure state mutations affect the intended entity.",
        "distractors": [
            "Heuristics based on account value often drain corporate points unauthorizedly, causing compliance violations.",
            "Chronological heuristics are arbitrary and risk modifying the wrong customer account.",
            "Crashing the session disrupts service and frustrates customers over a common ambiguity."
        ]
    },
    key_insight="Never use heuristics to resolve ambiguous database matches. Prompt the user to clarify which account they want to modify."
))

# Q48 (Target: B = 1)
questions.append(create_question(
    qid=48,
    domain_id=5,
    domain_name="Context Management & Reliability",
    sub_skill="Error Propagation",
    module="Domain 5 (Annotating Supply Chain Gaps)",
    scenario="A supply chain coordinator orchestrates three subagents to evaluate raw material availability across Europe, Asia, and North America. The Asian supplier API fails due to an earthquake affecting local data centers. How should the coordinator finalize the report?",
    options=[
        "Abort the entire report and discard the European and North American supplier data.",
        "Synthesize Europe and North America findings, explicitly annotating that Asian data was unavailable.",
        "Fabricate synthetic Asian inventory estimates using historical data from three years ago.",
        "Wait in an infinite retry loop until Asian data center communications are fully restored."
    ],
    correct_idx=1,
    rationales={
        "correct": "When a partial subagent failure occurs due to an external outage, the coordinator should synthesize the successful data streams and explicitly annotate the gap (e.g. 'Note: Asian supplier data is omitted due to regional network outage'). This delivers value while maintaining transparent data provenance.",
        "distractors": [
            "Aborting the entire report discards valuable European and American data and cripples business visibility.",
            "Fabricating synthetic inventory estimates based on 3-year-old data introduces severe operational risk.",
            "Infinite retry loops hang system resources during natural disaster communication outages."
        ]
    },
    key_insight="Deliver partial multi-agent findings transparently: synthesize successful streams and explicitly annotate unavailable sections."
))

# Q49 (Target: C = 2)
questions.append(create_question(
    qid=49,
    domain_id=5,
    domain_name="Context Management & Reliability",
    sub_skill="Error Propagation",
    module="Domain 5 (Silent Shipping Rate Suppression)",
    scenario="A shipping comparison tool queries three parcel carriers. Carrier 2 times out, and the tool catch block returns an empty list `[]` marked as success. Downstream, Claude informs the customer that Carrier 2 does not service their region. What anti-pattern occurred?",
    options=[
        "Context window overflow caused by carrier tracking numbers exceeding token limits.",
        "Prompt injection vulnerability where Carrier 2 hijacked the model's system prompt.",
        "Silent error suppression, mistaking a transient network timeout for a valid empty result.",
        "Operating system kernel panic during TCP socket communication with Carrier 2."
    ],
    correct_idx=2,
    rationales={
        "correct": "Silent error suppression occurs when tool catch blocks return empty data marked as successful upon error. Downstream agents cannot distinguish an access failure from a valid empty dataset, misleading Claude into falsely concluding that Carrier 2 does not service the customer's route.",
        "distractors": [
            "Tracking numbers consume negligible tokens and do not trigger context overflow.",
            "Carrier 2 timed out and returned no text; no prompt injection occurred.",
            "A standard HTTP timeout does not trigger an operating system kernel panic."
        ]
    },
    key_insight="Silent error suppression leads to false conclusions. Always return structured error payloads with failure categories rather than empty success lists."
))

# Q50 (Target: D = 3)
questions.append(create_question(
    qid=50,
    domain_id=5,
    domain_name="Context Management & Reliability",
    sub_skill="Human Review & Confidence Calibration",
    module="Domain 5 (Stratified Form Extraction Audit)",
    scenario="An insurance extraction platform achieves 97% overall accuracy across 50,000 scanned forms. However, a customer audit reveals that 35% of handwritten accident diagrams are completely misclassified. What evaluation failure allowed this to reach production?",
    options=[
        "Failing to reboot the cloud server instances every twenty-four hours to clear model drift.",
        "Relying on temperature 0.0 instead of temperature 1.0 during production extraction turns.",
        "Using Python dictionaries instead of native JSON objects to store intermediate form values.",
        "Relying on aggregate accuracy metrics without stratifying performance across document sub-types."
    ],
    correct_idx=3,
    rationales={
        "correct": "The 'aggregate metrics trap' occurs when high volume in simple, typed categories (e.g. 99% accuracy on typed forms) mathematically masks disastrous failure rates (35% error) in smaller, difficult categories (handwritten forms). Evaluation must be stratified across document classes and field types.",
        "distractors": [
            "Server reboots do not impact model weights or OCR performance.",
            "Temperature zero is the standard best practice for deterministic structured extraction.",
            "Python dictionaries serialize identically to JSON and do not cause classification failures."
        ]
    },
    key_insight="Beware the aggregate metrics trap: high overall accuracy can mask catastrophic failure rates on difficult document sub-types. Always evaluate stratified metrics."
))

# Q51 (Target: A = 0)
questions.append(create_question(
    qid=51,
    domain_id=5,
    domain_name="Context Management & Reliability",
    sub_skill="Information Provenance",
    module="Domain 5 (Contradictory Supplier Pricing)",
    scenario="A procurement research agent queries two authoritative chemical supplier databases for wholesale lithium carbonate pricing. Supplier Database X quotes $14,000/ton as of March 2026, while Supplier Database Y quotes $18,500/ton as of January 2026. How should the agent report this?",
    options=[
        "Report both quotes with full attribution, source database names, and effective dates.",
        "Average the two prices to $16,250/ton and report it as the single unified market price.",
        "Discard Database Y because its quoted price is higher, assuming it represents an error.",
        "Crash the agent orchestration pipeline and notify engineering that data is corrupt."
    ],
    correct_idx=0,
    rationales={
        "correct": "When authoritative sources disagree, an agent must never invent synthetic averages or arbitrarily suppress one source. It must report both competing figures along with full provenance metadata: source name, quoted price, and effective publication date.",
        "distractors": [
            "Averaging conflicting quotes creates a synthetic price that neither supplier actually offers.",
            "Discarding higher quotes based on price bias distorts market visibility and procurement planning.",
            "Price variations between suppliers and dates are normal market realities, not system corruptions."
        ]
    },
    key_insight="Report conflicting data with full attribution and dates. Never fabricate synthetic averages or arbitrarily suppress authoritative sources."
))

# Q52 (Target: B = 1)
questions.append(create_question(
    qid=52,
    domain_id=5,
    domain_name="Context Management & Reliability",
    sub_skill="Context Preservation",
    module="Domain 5 (Top of Prompt Positioning)",
    scenario="An AI system answers user questions against a 70-page corporate financial audit report. Users notice that questions about the executive summary at the start and the audit sign-off at the end are answered with high precision, while questions about middle footnotes are frequently missed. What context optimization resolves this?",
    options=[
        "Reverse the byte order of the entire PDF file before submitting it to the API.",
        "Inject the user question and critical instructions at the top of the prompt with section headers.",
        "Instruct the user to append the phrase 'Please read carefully' to every single question.",
        "Switch the model to a legacy snapshot that does not use modern transformer attention."
    ],
    correct_idx=1,
    rationales={
        "correct": "To combat the 'lost in the middle' effect, place critical instructions, user questions, and key summary facts at the very top of the prompt, and structure long reference documents with prominent Markdown section headers to guide model attention.",
        "distractors": [
            "Reversing byte orders corrupts the file into unreadable binary garbage.",
            "Appeals like 'Please read carefully' do not alter mathematical attention distribution mechanics.",
            "Legacy model snapshots have vastly worse attention windows than modern Claude models."
        ]
    },
    key_insight="Place critical questions and instructions at the top of long prompts, and structure reference documents with clear section headers."
))

# Q53 (Target: C = 2)
questions.append(create_question(
    qid=53,
    domain_id=5,
    domain_name="Context Management & Reliability",
    sub_skill="Escalation & Ambiguity Resolution",
    module="Domain 5 (Escalation on Policy Gaps)",
    scenario="A customer requests a price match against a competitor's promotional clearance sale. The customer service agent searches published company policies and confirms that price-matching clearance sales is an undocumented edge case not covered by policy. What is the correct architectural action?",
    options=[
        "Invent a reasonable price-matching rule on the spot and grant the customer a 50% discount.",
        "Reject the customer abruptly and state that anything not explicitly written is illegal.",
        "Recognize the policy gap and escalate the ticket with full context to a human manager.",
        "Put the customer on an infinite hold loop while repeatedly querying the policy database."
    ],
    correct_idx=2,
    rationales={
        "correct": "A policy gap or undocumented exception is one of the three primary valid human escalation triggers. An autonomous agent must never invent corporate policy on the spot; it must compile the customer's request and policy context, and escalate to a human manager for a business decision.",
        "distractors": [
            "Inventing corporate policy unauthorizedly incurs financial liabilities and sets dangerous precedents.",
            "Accusing customers of illegal activity for requesting clearance price matches is abusive customer service.",
            "Infinite loops lock customer support channels and destroy customer satisfaction."
        ]
    },
    key_insight="When a situation falls outside published policy rules (a policy gap), escalate immediately to human managers with full context. Never invent policy on the spot."
))

exam3_data = {
    "id": 3,
    "title": "Practice Exam 3: Claude Code Workflows & CI/CD",
    "description": "Configuration hierarchies, CI/CD automation, batch processing, and cross-domain scenario application.",
    "questions": questions
}

output_path = "data/architect/exam3.json"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(exam3_data, f, indent=2)

print(f"Successfully generated {len(questions)} questions in {output_path}!")
