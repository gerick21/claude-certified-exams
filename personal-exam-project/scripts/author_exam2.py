#!/usr/bin/env python3
"""
Authoring Script for Architect Practice Exam 2:
'Practice Exam 2: Tool Design & MCP Architecture'
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
    sub_skill="Agentic Loops",
    module="Domain 1 (Agentic Loops & ResultMessage)",
    scenario="A platform developer monitors an agent workflow built with the Claude Agent SDK. The application loop processes incoming streaming events and must log overall token consumption and cost immediately upon task completion. Which SDK message type and attribute signal the loop completion?",
    options=[
        "A ResultMessage containing the final text output, stop_reason, and total_cost_usd.",
        "A SystemMessage broadcasting an operating system signal indicating process termination.",
        "An AssistantMessage whose content array contains an empty string without tool calls.",
        "A StreamEvent message carrying an HTTP 204 status header emitted by the Claude client."
    ],
    correct_idx=0,
    rationales={
        "correct": "In the Claude Agent SDK, `ResultMessage` signals loop completion. It encapsulates `message.result` (the final text), `message.stop_reason`, and `message.total_cost_usd`, providing complete telemetry upon task conclusion.",
        "distractors": [
            "SystemMessage defines system prompt context at initialization, not termination telemetry.",
            "An empty AssistantMessage content array does not reliably signal completion and may occur during malformed turns.",
            "StreamEvent messages deliver incremental tokens and do not contain HTTP 204 completion headers."
        ]
    },
    key_insight="In the Claude Agent SDK, `ResultMessage` signals loop termination and contains final results, stop_reason, and total cost."
))

# Q2 (Target: B = 1)
questions.append(create_question(
    qid=2,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Multi-Agent Orchestration",
    module="Domain 1 (Coordinator Scope Partitioning)",
    scenario="A coordinator agent delegates research on corporate mergers to two subagents. Both subagents retrieve identical public press releases and summarize the same financial figures, wasting 70,000 redundant tokens. What orchestration responsibility did the coordinator fail to execute?",
    options=[
        "The coordinator failed to assign cryptographic tokens to the child subagent network sockets.",
        "The coordinator failed to partition non-overlapping subtopic scopes in subagent task prompts.",
        "The coordinator failed to mount a shared local SQLite database across both subagent processes.",
        "The coordinator failed to enforce temperature zero across external web retrieval interfaces."
    ],
    correct_idx=1,
    rationales={
        "correct": "A core responsibility of the coordinator in hub-and-spoke orchestration is scope partitioning: decomposing the overarching objective into distinct, non-overlapping assignments with explicit boundaries. When scopes overlap, subagents duplicate work and waste tokens.",
        "distractors": [
            "Cryptographic socket tokens govern network security, having no bearing on task decomposition overlap.",
            "Shared SQLite databases provide persistence but do not prevent agents from querying the same web URLs.",
            "Temperature zero controls sampling randomness, not semantic research topic assignment."
        ]
    },
    key_insight="The coordinator must partition research tasks into non-overlapping scopes with explicit boundaries to prevent redundant subagent work."
))

# Q3 (Target: C = 2)
questions.append(create_question(
    qid=3,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Subagent Invocation & Context Passing",
    module="Domain 1 (Context Passing Protocols)",
    scenario="A coordinator agent delegates financial ratio calculations to an analysis subagent. The subagent needs balance sheet numbers extracted by a prior document parsing subagent. Since subagents do not share memory, how must the coordinator pass this data?",
    options=[
        "Instruct the analysis subagent to query the parsing subagent directly via local IPC sockets.",
        "Rely on the Claude Agent SDK to automatically inject historical turns into child contexts.",
        "Inject the extracted balance sheet findings directly into the analysis subagent prompt.",
        "Store the numbers in an operating system environment variable read during agent boot."
    ],
    correct_idx=2,
    rationales={
        "correct": "Because subagents do not inherit conversation history from the coordinator or other subagents, the coordinator must explicitly inject all necessary prior findings, figures, and constraints directly into the child subagent's task prompt.",
        "distractors": [
            "Subagents in hub-and-spoke architectures are prohibited from direct peer-to-peer IPC communication.",
            "The Agent SDK deliberately isolates child contexts and never automatically injects prior history.",
            "Environment variables are process-level configurations unsuitable for dynamic, request-specific conversational data."
        ]
    },
    key_insight="Context must be explicitly injected: pass findings from prior steps directly in the subagent's prompt, as subagents share zero memory."
))

# Q4 (Target: D = 3)
questions.append(create_question(
    qid=4,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Workflow Enforcement & Handoff",
    module="Domain 1 (Deterministic vs Probabilistic)",
    scenario="A banking assistant processes fund transfers between customer accounts. To ensure compliance, every transfer over $1,000 must be preceded by a multi-factor authentication (MFA) verification tool call. Which implementation provides the required guarantee?",
    options=[
        "Add a prompt rule stating: 'Always verify MFA prior to authorizing any transfer over $1000.'",
        "Include three few-shot examples showing the model executing MFA checks before fund transfers.",
        "Prompt the user after every transfer asking if they intended to complete the transaction.",
        "Implement a PreToolUse hook that blocks the transfer tool unless a verified MFA token exists."
    ],
    correct_idx=3,
    rationales={
        "correct": "When financial transactions and security compliance are at stake, prompt instructions and few-shot examples are probabilistic and have a measurable failure rate. Only programmatic enforcement via a PreToolUse hook or prerequisite gate provides a 100% deterministic guarantee.",
        "distractors": [
            "Prompt rules are probabilistic and fail when customer inputs are ambiguous or adversarial.",
            "Few-shot examples improve model alignment but cannot guarantee 100% compliance in production.",
            "Asking users after transfers occur is post-hoc and fails to block unauthorized transactions before execution."
        ]
    },
    key_insight="Programmatic enforcement (PreToolUse hooks) is mandatory for financial and security compliance. Prompt instructions are probabilistic."
))

# Q5 (Target: A = 0)
questions.append(create_question(
    qid=5,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Agent SDK Hooks",
    module="Domain 1 (PreToolUse Denial Output)",
    scenario="A developer authors a PreToolUse hook in Python to prevent an autonomous agent from modifying protected production configuration files. What exact dictionary structure must the hook return to deny tool execution?",
    options=[
        "A dictionary containing hookSpecificOutput with hookEventName, permissionDecision, and reason.",
        "A dictionary returning status 403 with an unauthorized exception message string in the payload.",
        "A dictionary containing boolean flag allowExecution set to false without accompanying text.",
        "An empty dictionary accompanied by raising an unhandled Python RuntimeError on the main thread."
    ],
    correct_idx=0,
    rationales={
        "correct": "In the Claude Agent SDK, a PreToolUse hook denies tool execution by returning a structured dictionary: `{'hookSpecificOutput': {'hookEventName': 'PreToolUse', 'permissionDecision': 'deny', 'permissionDecisionReason': '<reason>'}}`. This informs Claude why the tool was blocked so it can adapt.",
        "distractors": [
            "The Agent SDK does not use HTTP 403 status codes inside hook return dictionaries.",
            "A plain boolean flag without the standard hookSpecificOutput structure is rejected by the SDK schema.",
            "Raising unhandled RuntimeErrors crashes the host process rather than communicating denial back to the agent."
        ]
    },
    key_insight="PreToolUse hooks deny execution via `hookSpecificOutput` with `permissionDecision: 'deny'` and an explicit reason."
))

# Q6 (Target: B = 1)
questions.append(create_question(
    qid=6,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Agent SDK Hooks",
    module="Domain 1 (Lifecycle Observability)",
    scenario="A security compliance team requires a complete audit trail of all subagent invocations, including the exact inputs, outputs, and intermediate tool transcripts for regulatory review. Which SDK lifecycle event and property provide this audit log?",
    options=[
        "The PreToolUse hook inspects the operating system process identifier for external syslog storage.",
        "The SubagentStop hook captures the execution event and exposes the agent_transcript_path.",
        "The CoordinatorStart hook records the initial user session IP address in an encrypted cookie.",
        "The PostToolUse hook dumps the model memory cache to an Amazon S3 cold storage Glacier vault."
    ],
    correct_idx=1,
    rationales={
        "correct": "The `SubagentStop` lifecycle hook triggers whenever a child subagent finishes execution. It provides event metadata including `agent_transcript_path`, which references the complete, immutable on-disk transcript of all turns and tool calls executed by that subagent.",
        "distractors": [
            "PreToolUse intercepts tool invocations prior to execution and does not contain subagent lifecycle transcripts.",
            "CoordinatorStart only records session initialization, not child subagent execution trails.",
            "PostToolUse intercepts individual tool outputs and does not manage transcript archiving to Glacier."
        ]
    },
    key_insight="Use the SubagentStop hook to capture subagent lifecycle events and record the agent_transcript_path for compliance auditing."
))

# Q7 (Target: C = 2)
questions.append(create_question(
    qid=7,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Task Decomposition Strategies",
    module="Domain 1 (Fixed Pipeline vs Dynamic Decomposition)",
    scenario="A software architect evaluates an automated compliance pipeline that executes four invariant steps: extract tax IDs, check sanction lists, calculate risk score, and generate a signed audit certificate. The order never changes. Which architecture is most appropriate?",
    options=[
        "A dynamic multi-agent system where three LLM supervisors debate the next execution step.",
        "An autonomous agent loop where Claude determines the tool invocation sequence at runtime.",
        "A deterministic code pipeline executing functions in a fixed, non-agentic linear sequence.",
        "A decentralized peer-to-peer agent network communicating over an external gossip protocol."
    ],
    correct_idx=2,
    rationales={
        "correct": "When the required steps are invariant, predictable, and linear, a standard deterministic code pipeline is vastly superior: it is faster, cheaper, 100% reliable, and introduces zero model non-determinism. Agents should only be used when tasks require dynamic routing or open-ended reasoning.",
        "distractors": [
            "A supervisor multi-agent debate introduces massive latency and token cost for a static linear workflow.",
            "An autonomous agent loop introduces unnecessary non-determinism and latency to a fixed sequential task.",
            "Peer-to-peer gossip protocols are completely unsuited for deterministic enterprise compliance pipelines."
        ]
    },
    key_insight="Decide workflow vs agent before writing code. When steps are deterministic and sequential, write standard code, not an autonomous agent loop."
))

# Q8 (Target: D = 3)
questions.append(create_question(
    qid=8,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Subagent Invocation & Context Passing",
    module="Domain 1 (Attribution Preservation)",
    scenario="A multi-agent research system retrieves information from academic journals. In the final report, claims from different authors are merged, and citations are lost. How should the coordinator structure context passed from retrieval subagents to the synthesis subagent?",
    options=[
        "Concatenate all journal texts into a single raw string and instruct the agent to guess origins.",
        "Strip all metadata from source documents to maximize the token budget available for synthesis.",
        "Instruct the retrieval subagents to write anonymous summaries without author or date fields.",
        "Pass structured data separating content from metadata including source_url, author, and date."
    ],
    correct_idx=3,
    rationales={
        "correct": "To preserve attribution across subagent boundaries, data must be structured so that content is explicitly paired with metadata: `{'excerpt': ..., 'source_url': ..., 'author': ..., 'publication_date': ...}`. This enables the synthesis agent to cite sources accurately without losing attribution.",
        "distractors": [
            "Concatenating raw text without delimiters forces the synthesis agent to guess source attribution.",
            "Stripping metadata completely destroys provenance and makes proper citation impossible.",
            "Anonymous summaries explicitly erase author and date information needed for research validation."
        ]
    },
    key_insight="Preserve source attribution across agent boundaries by passing structured objects separating content from metadata (author, date, URL)."
))

# Q9 (Target: A = 0)
questions.append(create_question(
    qid=9,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Session State & Resumption",
    module="Domain 1 (Fresh Start with Injected Summary)",
    scenario="An interactive agent has accumulated 150,000 tokens of conversational context during a 3-hour code debugging session. The developer now wants to switch focus to writing integration tests for a completely different module. What is the recommended context management strategy?",
    options=[
        "Start a fresh session and inject a concise structured summary of the verified module contracts.",
        "Continue the current session and instruct the model to forget all prior conversation turns.",
        "Delete the project CLAUDE.md configuration file to reset the underlying model tokenizer.",
        "Execute a bash kill command on the local terminal to wipe operating system process memory."
    ],
    correct_idx=0,
    rationales={
        "correct": "When switching to a distinct task after accumulating heavy conversational context (150k tokens), continuing the session wastes input tokens and degrades model attention. Starting a fresh session with an injected concise summary of needed contracts provides clean focus and low latency.",
        "distractors": [
            "Language models cannot selectively 'forget' historical turns in an active context window; earlier tokens still consume budget and dilute attention.",
            "Deleting CLAUDE.md removes project standards and has no effect on active conversation context.",
            "Killing terminal processes does not address context window management and risks losing uncommitted files."
        ]
    },
    key_insight="When pivoting to a new task after a long session, start a fresh session and inject a concise summary of relevant state rather than carrying 150k tokens."
))

# Q10 (Target: B = 1)
questions.append(create_question(
    qid=10,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Multi-Agent Orchestration",
    module="Domain 1 (Iterative Refinement Loop)",
    scenario="A research coordinator dispatches a subagent to write a competitive analysis report. The returned draft fails to address competitor pricing models. Rather than presenting the incomplete report, what should the coordinator agent do in a hub-and-spoke pattern?",
    options=[
        "Terminate the research task and display an unhandled missing data exception to the user.",
        "Evaluate the draft against requirements and re-delegate a focused pricing research subtask.",
        "Modify the user original prompt to remove all mentions of competitor pricing requirements.",
        "Immediately publish the partial report and schedule an automated follow-up ticket in Jira."
    ],
    correct_idx=1,
    rationales={
        "correct": "A primary role of the coordinator is quality evaluation and iterative refinement. If a worker subagent returns output with gaps, the coordinator evaluates the output against original user requirements, formulates a targeted follow-up subtask, and re-delegates to fill the gap before final delivery.",
        "distractors": [
            "Terminating the workflow on partial output creates a poor user experience and fails the objective.",
            "Modifying user prompts to ignore requirements violates user intent and degrades system quality.",
            "Publishing incomplete reports compromises research reliability and damages user trust."
        ]
    },
    key_insight="The coordinator must evaluate subagent deliverables against the original prompt and re-delegate targeted tasks to fill identified gaps."
))

# Q11 (Target: C = 2)
questions.append(create_link_question := create_question(
    qid=11,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Agentic Loops",
    module="Domain 1 (Handling tool_result Content Blocks)",
    scenario="A custom agent loop executes a tool call requested by Claude. To properly maintain the Messages API conversation contract for the subsequent request turn, how must the application format the tool execution output?",
    options=[
        "Append the raw tool output as a system message placed at the top of the conversation list.",
        "Transmit the tool execution output as a top-level HTTP query parameter in the API request URL.",
        "Append a user message containing a tool_result content block referencing the tool_use_id.",
        "Overwrite the preceding assistant message content array with the raw tool output JSON string."
    ],
    correct_idx=2,
    rationales={
        "correct": "Under the Anthropic Messages API specification, tool results must be appended as a new `user` message containing one or more `tool_result` content blocks, each explicitly linking to the corresponding `tool_use_id` emitted by the assistant.",
        "distractors": [
            "Tool results cannot be sent as system messages; system messages define behavioral personas.",
            "HTTP query parameters cannot carry multi-kilobyte conversational tool results.",
            "Overwriting the assistant's previous message destroys conversation history and violates the API turn contract."
        ]
    },
    key_insight="Tool outputs must be returned in a `user` role message containing `tool_result` blocks that reference the specific `tool_use_id`."
))

# Q12 (Target: D = 3)
questions.append(create_question(
    qid=12,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Subagent Invocation & Context Passing",
    module="Domain 1 (AgentDefinition Specification)",
    scenario="A software engineer defines a specialized documentation writer subagent using `AgentDefinition` in the Claude Agent SDK. Which set of properties defines the operational boundary and capabilities of the subagent?",
    options=[
        "database_url, connection_timeout, max_retries, and operating_system_thread_priority.",
        "git_commit_hash, branch_name, repository_uri, and pull_request_reviewer_credentials.",
        "websocket_endpoint, ssl_certificate_path, ip_whitelist, and load_balancer_affinity.",
        "description, prompt, tools, and permissionMode specifying execution boundaries and capabilities."
    ],
    correct_idx=3,
    rationales={
        "correct": "In the Claude Agent SDK, `AgentDefinition` takes: `description` (tells the coordinator when to invoke the agent), `prompt` (the agent's specialized system instructions), `tools` (whitelisted tools), and `permissionMode` (governing interactive approval or bypass).",
        "distractors": [
            "Database URLs and OS thread priorities are infrastructure parameters, not SDK agent definitions.",
            "Git properties are version control parameters, not the configuration contract for an AgentDefinition.",
            "Network endpoints and SSL certificates belong to web transport layers, not agent definitions."
        ]
    },
    key_insight="An `AgentDefinition` consists of description, prompt, tools, and permissionMode to establish the subagent's role and boundaries."
))

# Q13 (Target: A = 0)
questions.append(create_question(
    qid=13,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Task Decomposition Strategies",
    module="Domain 1 (Dynamic Adaptive Decomposition)",
    scenario="An incident triage agent analyzes an unexpected server outage. The root cause is unknown beforehand: it could be a memory leak, network partition, or disk saturation. Why is dynamic adaptive decomposition required over a fixed prompt-chained pipeline?",
    options=[
        "Subsequent diagnostic tools must be chosen dynamically based on findings uncovered at each step.",
        "Dynamic decomposition guarantees that all network monitoring APIs respond in less than ten milliseconds.",
        "Fixed pipelines consume three times more input tokens when reading identical server log files.",
        "The Messages API disables tool use blocks whenever fixed sequential pipelines are executed."
    ],
    correct_idx=0,
    rationales={
        "correct": "Dynamic adaptive decomposition allows the agent to decide its next action based on evolving discoveries (e.g. if memory logs show a leak, investigate heap dumps; if network logs show timeouts, test DNS). A fixed pipeline cannot branch dynamically based on exploratory diagnostic data.",
        "distractors": [
            "Decomposition architecture cannot control or guarantee third-party API response latency.",
            "Token consumption is determined by context volume, not whether a sequence is static or dynamic.",
            "The Messages API supports tool use identically across all architectural patterns."
        ]
    },
    key_insight="Dynamic adaptive decomposition is necessary when the solution path cannot be known upfront and subsequent steps depend on discoveries."
))

# Q14 (Target: B = 1)
questions.append(create_question(
    qid=14,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Workflow Enforcement & Handoff",
    module="Domain 1 (Handoff Summary Autonomous Requirements)",
    scenario="When an automated billing agent escalates an unresolvable invoice dispute to a human Tier-2 support representative, why is it critical that the handoff summary be completely self-contained and autonomous?",
    options=[
        "The human support ticketing software automatically deletes prior conversation history upon escalation.",
        "The human specialist must understand context and act immediately without reading raw model history.",
        "Data privacy regulations prohibit human customer service staff from reading AI assistant messages.",
        "Self-contained summaries allow the agent to immediately purge the customer profile from the database."
    ],
    correct_idx=1,
    rationales={
        "correct": "Human support representatives handle high ticket volumes under strict SLAs. Forcing a specialist to read dozens of turns of raw conversational messages and tool JSON payloads drastically slows resolution. A self-contained dossier (ID, verified state, root cause, proposed resolution) enables immediate action.",
        "distractors": [
            "Ticketing software does not automatically delete conversation history upon escalation.",
            "Privacy regulations do not ban human support agents from reading support transcripts.",
            "Customer profiles are not deleted upon ticket escalation; doing so would destroy user accounts."
        ]
    },
    key_insight="Handoff summaries must be self-contained dossiers so human specialists can resolve issues immediately without reading raw transcripts."
))

# ─── DOMAIN 2: Tool Design & MCP Integration (Q15 - Q24) ──────────────────────

# Q15 (Target: C = 2)
questions.append(create_question(
    qid=15,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="Tool Interface Design",
    module="Domain 2 (Tool Splitting)",
    scenario="A software team designs an MCP tool named `manage_customer` that accepts 14 optional parameters and performs lookups, balance updates, refunds, address changes, and email verification. In production, Claude frequently confuses parameters and triggers unintended actions. What is the proportionate architectural fix?",
    options=[
        "Add twenty detailed few-shot examples to the system prompt demonstrating every parameter combination.",
        "Train an external machine learning router to parse user input and invoke manage_customer safely.",
        "Split the overloaded tool into distinct, single-purpose tools with clear input and output schemas.",
        "Convert all numeric fields into freeform strings to allow loose type casting by the model."
    ],
    correct_idx=2,
    rationales={
        "correct": "Overloaded monolithic tools with dozens of optional parameters create severe parameter ambiguity and hallucination. The established architectural remedy is 'tool splitting': dividing the multifunction tool into distinct, cohesive tools (`lookup_customer`, `update_address`, `process_refund`) with strict schemas.",
        "distractors": [
            "Adding 20 few-shot examples introduces heavy token cost without fixing the underlying schema overload.",
            "An external router adds operational complexity and fails to address the flawed tool design.",
            "Converting numeric fields to freeform strings weakens schema validation and increases errors."
        ]
    },
    key_insight="Split overloaded multifunction tools into distinct, single-purpose tools with unambiguous input/output contracts."
))

# Q16 (Target: D = 3)
questions.append(create_question(
    qid=16,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="Structured Error Responses",
    module="Domain 2 (The Four Error Categories)",
    scenario="An MCP tool connecting to a cloud billing gateway encounters an invalid credit card number submitted by a user. According to production MCP error handling best practices, how should the tool categorize and flag this error in its response?",
    options=[
        "Categorize as transient error with isRetryable set to true, prompting immediate automatic retries.",
        "Categorize as permission error with isRetryable set to true, requesting elevated IAM credentials.",
        "Categorize as system crash error with isRetryable set to false, terminating the host server container.",
        "Categorize as validation error with isRetryable set to true after the user corrects their input."
    ],
    correct_idx=3,
    rationales={
        "correct": "An invalid card number is a validation error: the input format or data is incorrect. It is retryable only after correcting the input data (isRetryable: true after input fix). It is neither a transient infrastructure timeout nor an IAM permission failure.",
        "distractors": [
            "Transient errors represent network timeouts or rate limits where retrying the exact same input is valid; an invalid card will never succeed without input changes.",
            "Permission errors represent missing IAM access or unauthorized tokens, not invalid user data.",
            "An invalid credit card does not constitute a server crash and must not terminate server containers."
        ]
    },
    key_insight="Classify errors accurately: validation errors require input correction before retry; transient errors can be retried immediately."
))

# Q17 (Target: A = 0)
questions.append(create_question(
    qid=17,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="MCP Resources vs Tools",
    module="Domain 2 (MCP Resources Architecture)",
    scenario="An enterprise Claude deployment needs access to a 5,000-line read-only product catalog and API schema documentation that rarely changes. Rather than authoring an executable tool that queries a database on every turn, what MCP architectural feature should be used?",
    options=[
        "Expose the documentation as an MCP Resource, providing direct read-only context to Claude.",
        "Execute a Bash curl command on every single user turn to download the catalog from an S3 bucket.",
        "Embed the entire 5,000-line catalog directly into the system prompt of every single API request.",
        "Configure an active MCP tool that writes the catalog lines one by one into local text scratchpads."
    ],
    correct_idx=0,
    rationales={
        "correct": "MCP Resources are designed specifically to expose read-only data catalogs, schemas, documentation, and configuration files directly to Claude. They provide structured read access without requiring active code execution or tool invocation loops.",
        "distractors": [
            "Running curl on every turn introduces latency, network fragility, and high compute overhead.",
            "Embedding 5,000 lines in every system prompt exhausts prompt token budgets and balloons costs.",
            "Writing lines one by one via tool calls is extraordinarily slow and inefficient."
        ]
    },
    key_insight="Use MCP Resources to expose read-only reference data, schemas, and catalogs directly to Claude without tool execution overhead."
))

# Q18 (Target: B = 1)
questions.append(create_question(
    qid=18,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="Tool Interface Design",
    module="Domain 2 (Prompt vs Description Conflicts)",
    scenario="A developer adds an MCP tool `fetch_web_article` with a thorough description. However, the system prompt contains an older instruction: 'Always use local_file_reader for all text research.' In production, Claude never calls `fetch_web_article`. What is the root cause?",
    options=[
        "The model context window prioritizes tool descriptions over all system prompt instructions.",
        "A keyword-sensitive directive in the system prompt directly contradicts and overrides the tool.",
        "The Messages API disables web fetching tools whenever local file reader tools are present.",
        "The fetch_web_article tool description was formatted in Markdown instead of valid JSON syntax."
    ],
    correct_idx=1,
    rationales={
        "correct": "Directives in the system prompt carry immense authority. When a system prompt includes categorical commands ('Always use X for research'), it frequently overrides the model's willingness to select newer, appropriate tools like `fetch_web_article`. System prompts must be audited when tools are added.",
        "distractors": [
            "System prompt instructions frequently override tool descriptions when they contain rigid categorical keywords.",
            "The Messages API places no restriction on having both web fetch and local file tools available.",
            "Tool descriptions are standard text strings and legitimately support Markdown formatting."
        ]
    },
    key_insight="Audit system prompts when adding new tools. Rigid categorical prompt directives can inadvertently override tool descriptions."
))

# Q19 (Target: C = 2)
questions.append(create_question(
    qid=19,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="Structured Error Responses",
    module="Domain 2 (Multi-Agent Error Propagation)",
    scenario="In a multi-agent system, an image generation subagent fails because the user prompt requested a resolution exceeding GPU limits. How should the subagent propagate this failure back to the coordinator agent?",
    options=[
        "Throw an unhandled operating system exception that aborts the coordinator parent process.",
        "Return an empty text string to allow the coordinator to assume the image generated cleanly.",
        "Return a structured error object detailing category, attempted parameters, and valid limits.",
        "Instruct the user in a new browser modal to select a different cloud service provider."
    ],
    correct_idx=2,
    rationales={
        "correct": "When an unrecoverable error occurs in a subagent, it must propagate a structured error object back to the coordinator: failure category (`validation`), attempted parameters, and suggested corrective action (e.g., maximum permitted resolution). This allows the coordinator to adjust parameters or inform the user cleanly.",
        "distractors": [
            "Unhandled exceptions crash the coordinator and destroy intermediate work from other subagents.",
            "Returning an empty string misleads the coordinator into reporting successful completion.",
            "Subagents cannot open arbitrary client browser modals outside the coordination protocol."
        ]
    },
    key_insight="Propagate errors across agent boundaries as structured objects containing the failure category, attempted parameters, and valid constraints."
))

# Q20 (Target: D = 3)
questions.append(create_question(
    qid=20,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="MCP Server Integration",
    module="Domain 2 (Project vs User MCP Config)",
    scenario="A lead architect configures MCP servers for a team of 15 developers. Developer A puts the configuration in `~/.claude.json`, while Developer B puts it in `.mcp.json` in the git repository root. Why is Developer B's configuration the correct architectural practice?",
    options=[
        "The ~/.claude.json configuration file is automatically purged upon system reboot by macOS.",
        "The Claude Agent SDK rejects all tool declarations defined outside of user home directories.",
        "Configurations in ~/.claude.json can only execute shell commands written in Python syntax.",
        "The .mcp.json file is version-controlled and shared across all developers cloning the repository."
    ],
    correct_idx=3,
    rationales={
        "correct": "`.mcp.json` in the project root is tracked in version control, ensuring all team members share identical MCP server configurations, environment variable contracts, and tools. `~/.claude.json` is personal to a single machine and cannot be version-controlled across a team.",
        "distractors": [
            "`~/.claude.json` is a standard permanent file and is never deleted upon reboot.",
            "The Agent SDK and Claude Code fully support project-level `.mcp.json` configurations.",
            "`~/.claude.json` supports all standard MCP transport and command types, not just Python."
        ]
    },
    key_insight="Use project-level `.mcp.json` for team-wide, version-controlled MCP configurations. Use `~/.claude.json` only for machine-specific personal tools."
))

# Q21 (Target: A = 0)
questions.append(create_question(
    qid=21,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="Built-in Tools",
    module="Domain 2 (Incremental Exploration Strategy)",
    scenario="A developer asks Claude Code to investigate a bug in an unfamiliar 500,000-line repository. Rather than reading dozens of files immediately, what is the recommended token-efficient exploration pattern?",
    options=[
        "Grep for error strings or symbol definitions first, then Read only the targeted imported files.",
        "Run Glob to match all repository files, then load every file into context using concurrent Read calls.",
        "Execute a Bash find command that prints the raw text of every source file into conversation history.",
        "Ask the user to manually copy and paste the relevant source files into the chat conversation window."
    ],
    correct_idx=0,
    rationales={
        "correct": "The incremental exploration pattern preserves context and minimizes token consumption: use `Grep` to locate exact error strings, symbol definitions, or call sites, then use `Read` selectively on the specific imported modules identified.",
        "distractors": [
            "Loading all repository files via Read rapidly exhausts token budgets and triggers context window overflow.",
            "Dumping full repository text via Bash find destroys context focus and incurs enormous token costs.",
            "Expecting users to manually paste files defeats the core autonomous capability of Claude Code."
        ]
    },
    key_insight="Follow incremental exploration: Grep for entry points and symbol definitions first, then Read targeted imported files selectively."
))

# Q22 (Multi-select: Target: B = 1 and D = 3)
questions.append(create_question(
    qid=22,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="Built-in Tools",
    module="Domain 2 (Built-in Tool Selection Rules)",
    scenario="A developer instructs Claude Code to inspect a software project. Which TWO of the following statements correctly describe the distinct capabilities and selection rules for built-in tools? (Select TWO)",
    options=[
        "The Glob tool should be used to search file contents for regular expression function patterns.",
        "The Grep tool searches file contents for matching regex patterns, error codes, and symbol names.",
        "The Edit tool replaces files completely and should be preferred over Write when creating new files.",
        "The Glob tool matches file paths and names across directory trees using pattern expressions."
    ],
    correct_idx=[1, 3],
    is_multi=True,
    rationales={
        "correct": "Options B and D are correct. `Grep` searches inside file contents for text/regex matches (code lines, errors, symbols). `Glob` searches filesystem directory structures to match file names and paths (e.g. `**/*.spec.ts`).",
        "distractors": [
            "Glob matches file paths and names; it does not search inside file contents.",
            "The Edit tool performs surgical string replacement on existing files; creating new files is handled by the Write tool."
        ]
    },
    key_insight="Grep searches file CONTENTS. Glob matches file PATHS and directory structures. Edit performs surgical updates; Write creates or overwrites."
))

# Q23 (Target: C = 2)
questions.append(create_question(
    qid=23,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="Tool Distribution & tool_choice",
    module="Domain 2 (tool_choice: auto vs forced)",
    scenario="A customer support agent answers open-ended technical questions and occasionally checks order status via `check_order`. During a casual conversation where the user says 'Hello, I love your service!', Claude unnecessarily invokes `check_order` with empty arguments. What configuration was mistakenly set?",
    options=[
        "The temperature parameter was configured to 0.7 instead of remaining at the default 1.0.",
        "The model tier was pinned to an older legacy snapshot rather than current Claude Sonnet.",
        "tool_choice was forced to 'any' or {'type': 'tool'}, compelling Claude to execute a tool.",
        "The system prompt lacked explicit mathematical proofs demonstrating customer satisfaction."
    ],
    correct_idx=2,
    rationales={
        "correct": "When `tool_choice` is set to `'any'` or `{'type': 'tool', 'name': '...'}`, Claude is strictly forbidden from returning pure conversational text; it is forced to emit a tool call even when the user's input is a simple conversational greeting. Conversational bots should use `tool_choice: 'auto'`.",
        "distractors": [
            "Temperature 0.7 influences token randomness but does not force mandatory tool execution on greetings.",
            "Model snapshot pinning controls behavioral stability, not tool execution enforcement.",
            "Mathematical proofs have no bearing on conversational tool choice configuration."
        ]
    },
    key_insight="Setting `tool_choice: 'any'` or forced tool modes compels Claude to call a tool even on casual greetings. Use `'auto'` for open-ended conversational agents."
))

# Q24 (Target: D = 3)
questions.append(create_question(
    qid=24,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="Tool Interface Design",
    module="Domain 2 (Negative Constraints in Tool Descriptions)",
    scenario="An application provides two tools: `search_internal_knowledge_base` and `search_public_internet`. Telemetry shows Claude frequently queries the public internet for confidential internal company policies. What is the most effective change to the tool definitions?",
    options=[
        "Rename both tools to generic labels such as tool_one and tool_two to eliminate search bias.",
        "Add a 10-second sleep delay to the public internet tool to discourage the model from calling it.",
        "Instruct users in the chat interface never to mention company policies in their questions.",
        "Add explicit negative boundaries to search_public_internet: 'Do NOT use for internal company policies'."
    ],
    correct_idx=3,
    rationales={
        "correct": "Explicit negative boundary statements in tool descriptions (e.g. 'Use for external industry data. Do NOT use for internal company policies, org charts, or employee benefits—use search_internal_knowledge_base instead') provide direct semantic signals that prevent misrouting.",
        "distractors": [
            "Obscuring tool names behind generic labels destroys semantic routing and severely degrades selection accuracy.",
            "Network sleep delays occur after tool selection and do not influence model decision-making.",
            "Shifting operational responsibility to end users creates a fragile and unacceptable customer experience."
        ]
    },
    key_insight="Include explicit negative boundary statements in tool descriptions to clearly demarcate when a tool should NOT be selected."
))

# ─── DOMAIN 3: Claude Code Configuration & Workflows (Q25 - Q35) ─────────────

# Q25 (Target: A = 0)
questions.append(create_question(
    qid=25,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="CLAUDE.md Hierarchy",
    module="Domain 3 (Directory-Level CLAUDE.md Scope)",
    scenario="A monorepo contains a frontend React application in `/frontend` and a Go backend in `/backend`. The backend team authors strict Go formatting and linting rules in `/backend/CLAUDE.md`. When Claude Code edits a file in `/frontend`, why are the Go rules ignored?",
    options=[
        "Directory-level CLAUDE.md files only govern files within their specific subfolder and children.",
        "Claude Code automatically disables markdown configuration files when processing React components.",
        "The Go rules must be translated into TypeScript syntax before Claude Code can ingest them.",
        "Directory-level rules require an explicit @import statement inside the root package.json file."
    ],
    correct_idx=0,
    rationales={
        "correct": "In the CLAUDE.md hierarchy, directory-level configuration files (`<subfolder>/CLAUDE.md`) apply strictly to files within that subfolder and its nested subdirectories. They never leak or apply to sibling or parent directories, ensuring clean scope isolation in monorepos.",
        "distractors": [
            "Claude Code processes markdown configurations identically across all programming languages.",
            "Go rules do not need translation into TypeScript; they are natural language guidelines for the model.",
            "`package.json` is a Node.js manifest and has no connection to Claude Code's directory scoping."
        ]
    },
    key_insight="Directory-level CLAUDE.md files are strictly scoped to their directory and descendants, never leaking into sibling folders."
))

# Q26 (Target: B = 1)
questions.append(create_question(
    qid=26,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="Path-Specific Rules",
    module="Domain 3 (Token Optimization via Rules)",
    scenario="A large enterprise repository contains 25 distinct domain modules. The architect wants to establish dedicated guidelines for database migrations, API controllers, and UI components without bloating the context window of every Claude Code turn. Why do path-specific rules achieve this?",
    options=[
        "Path-specific rules compress prompt tokens using a proprietary neural dictionary algorithm.",
        "Rules load dynamically into context ONLY when files matching their glob patterns are actively accessed.",
        "Path-specific rules bypass the Messages API and execute directly within the local operating system kernel.",
        "Rules files are pre-compiled into binary machine code that consumes zero context window memory."
    ],
    correct_idx=1,
    rationales={
        "correct": "Path-specific rules in `.claude/rules/*.md` feature YAML frontmatter with glob patterns (`paths: [...]`). Claude Code dynamically loads a rule into context ONLY when a file matching its glob pattern is actively read or edited, conserving context budget on unrelated tasks.",
        "distractors": [
            "Path rules do not use proprietary compression algorithms; they are standard markdown strings.",
            "Rules do not execute in the OS kernel; they are behavioral prompt guidelines for Claude.",
            "Rules are text prompts, not binary machine code, and consume standard tokens when loaded."
        ]
    },
    key_insight="Path-specific rules conserve tokens by loading dynamically into context ONLY when files matching their glob pattern are actively touched."
))

# Q27 (Target: C = 2)
questions.append(create_question(
    qid=27,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="Skills Architecture",
    module="Domain 3 (allowed-tools in Skills)",
    scenario="A security architect authors a specialized skill `.claude/skills/audit/SKILL.md` designed strictly for passive, read-only security auditing of source code. How can the architect guarantee that Claude will never make code modifications when running this skill?",
    options=[
        "Add a prompt rule stating: 'Please be careful and do not modify any files during this audit.'",
        "Set the file permissions of all source code files to read-only using a bash chmod script.",
        "Whitelist only Read, Grep, and Glob in the skill's allowed-tools YAML frontmatter field.",
        "Instruct developers to monitor Claude's terminal output and press Ctrl-C if an edit occurs."
    ],
    correct_idx=2,
    rationales={
        "correct": "In `SKILL.md` frontmatter, the `allowed-tools` property specifies the exact whitelist of tools available during skill execution. By including only `Read`, `Grep`, and `Glob` (and omitting `Edit` and `Write`), the skill is physically prevented from executing file modifications.",
        "distractors": [
            "Prompt instructions are probabilistic and do not physically prevent tool execution.",
            "Changing filesystem permissions via chmod can break builds, git hooks, and developer workflows.",
            "Relying on manual Ctrl-C cancellation is unreliable and fails in automated pipelines."
        ]
    },
    key_insight="Enforce read-only skill execution by whitelisting only `Read`, `Grep`, and `Glob` in the `allowed-tools` YAML frontmatter."
))

# Q28 (Target: D = 3)
questions.append(create_question(
    qid=28,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="Plan Mode vs Direct Execution",
    module="Domain 3 (Exiting Plan Mode)",
    scenario="A software engineer enters Plan Mode (`permission_mode='plan'`) in Claude Code to design an API schema refactor. After Claude generates a comprehensive architectural plan, the engineer approves it. What specific tool call or action transitions Claude Code from planning to implementation?",
    options=[
        "Execute a bash shell script that sends an interrupt signal to the Claude Code daemon.",
        "Close the terminal session and restart Claude Code with the direct execution flag.",
        "Modify the root CLAUDE.md file to delete the plan mode configuration property block.",
        "Claude invokes the ExitPlanMode function after receiving user approval for the plan."
    ],
    correct_idx=3,
    rationales={
        "correct": "In Claude Code, Plan Mode is exited when Claude calls `ExitPlanMode()` following user confirmation. This transitions the agent back to execution mode where editing and command execution tools become active.",
        "distractors": [
            "Sending interrupt signals kills the session rather than transitioning to execution.",
            "Restarting the session loses intermediate planning context and forces re-evaluation.",
            "CLAUDE.md does not store transient interactive session modes like Plan Mode."
        ]
    },
    key_insight="Claude transitions out of Plan Mode into execution by invoking the `ExitPlanMode()` tool call upon user approval."
))

# Q29 (Target: A = 0)
questions.append(create_question(
    qid=29,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="SDK setting_sources Parameter",
    module="Domain 3 (Loading Local Hooks)",
    scenario="An organization defines custom security hooks in `.claude/settings.local.json` to block access to internal secrets. When running an automated script with the Claude Agent SDK, the local hooks fail to trigger. What must be included in `setting_sources`?",
    options=[
        "The setting_sources list must explicitly include 'local' (e.g. ['project', 'local']).",
        "The setting_sources list must be empty to allow all local hooks to execute by default.",
        "The setting_sources list only accepts 'user' because local settings are disallowed in the SDK.",
        "The developer must set an operating system environment variable CLAUDE_LOAD_HOOKS=1."
    ],
    correct_idx=0,
    rationales={
        "correct": "In the Claude Agent SDK, loading settings from `settings.local.json` (where local developer hooks and overrides reside) requires explicitly including `'local'` in `setting_sources` (e.g. `setting_sources=['project', 'local']`).",
        "distractors": [
            "An empty list `setting_sources=[]` enables hermetic mode, which ignores all filesystem settings.",
            "`setting_sources` accepts `'user'`, `'project'`, and `'local'`; local settings are fully supported.",
            "There is no `CLAUDE_LOAD_HOOKS` environment variable in the Claude Agent SDK."
        ]
    },
    key_insight="To load local hooks from `settings.local.json` in the Claude Agent SDK, `setting_sources` must explicitly include `'local'`."
))

# Q30 (Target: B = 1)
questions.append(create_question(
    qid=30,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="Iterative Refinement",
    module="Domain 3 (Test-Driven Iteration)",
    scenario="Claude Code generates a complex regex parser for log analysis that fails on three edge cases. What is the most effective, test-driven way to iterate with Claude to fix the implementation?",
    options=[
        "Tell Claude that the code is broken and demand that it rewrite the entire file from memory.",
        "Provide the failing test cases with exact assertion failure logs and ask Claude to resolve them.",
        "Delete the test file and ask Claude to write new tests that pass against its current implementation.",
        "Switch the model to a faster tier with a lower context budget to regenerate code quickly."
    ],
    correct_idx=1,
    rationales={
        "correct": "In test-driven iteration, feeding exact failing test inputs alongside assertion failure logs provides unambiguous, objective feedback. Claude analyzes the discrepancy between expected and actual output to make targeted corrections.",
        "distractors": [
            "Vague complaints ('it is broken') force the model to guess which edge cases failed.",
            "Deleting tests to make broken code pass destroys software quality and guarantees production defects.",
            "Switching to lower tiers reduces reasoning ability and exacerbates subtle regex bugs."
        ]
    },
    key_insight="In test-driven refinement, provide the exact failing test cases and assertion logs to guide targeted fixes."
))

# Q31 (Target: C = 2)
questions.append(create_question(
    qid=31,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="Iterative Refinement",
    module="Domain 3 (Feedback Packaging)",
    scenario="A code review identifies three distinct issues in Claude's code: Issue 1 and Issue 2 are interdependent changes to a database transaction, while Issue 3 is a cosmetic variable rename in a separate file. How should the developer package this feedback?",
    options=[
        "Send all three issues across three separate sequential turns without mentioning relations.",
        "Submit Issue 3 first, wait for completion, then restart the entire session for Issues 1 and 2.",
        "Batch interdependent Issues 1 and 2 in a single message; address Issue 3 in a separate turn.",
        "Ask Claude to generate random code variations until all three issues disappear organically."
    ],
    correct_idx=2,
    rationales={
        "correct": "Feedback packaging rules dictate: when changes are interdependent (modifying one impacts the other, as with transaction logic), batch them together in a single prompt so the model evaluates their coupled constraints. Independent cosmetic changes should be handled in separate turns.",
        "distractors": [
            "Splitting interdependent issues into separate turns causes thrashing, where resolving Issue 2 breaks Issue 1.",
            "Restarting the session loses conversational context and wastes token overhead.",
            "Generating random code variations without feedback is completely ineffective."
        ]
    },
    key_insight="Batch interdependent feedback in a single message so the model reasons over coupled constraints together; isolate independent concerns."
))

# Q32 (Target: D = 3)
questions.append(create_question(
    qid=32,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="Skills Architecture",
    module="Domain 3 (argument-hint in Skills)",
    scenario="A developer authors a skill `.claude/skills/benchmark/SKILL.md` that requires an endpoint URL to run. To ensure users are prompted for this mandatory parameter if they forget to type it, which YAML frontmatter property should be configured?",
    options=[
        "Set `enforce-params: true` in the frontmatter to validate terminal input arguments.",
        "Configure `required: ['url']` inside the system prompt markdown code block.",
        "Add an operating system bash prompt check in the project Makefile configuration.",
        "Configure `argument-hint: '<endpoint-url>'` in the skill YAML frontmatter."
    ],
    correct_idx=3,
    rationales={
        "correct": "In Claude Code `SKILL.md` YAML frontmatter, `argument-hint` specifies the expected arguments (e.g. `argument-hint: '<endpoint-url>'`). When users invoke the skill without required parameters, Claude Code uses this hint to prompt for the missing input.",
        "distractors": [
            "`enforce-params` is not a valid YAML frontmatter property in Claude Code skills.",
            "System prompt markdown blocks do not configure CLI interactive argument hints.",
            "Makefiles do not control Claude Code skill argument prompting mechanics."
        ]
    },
    key_insight="Use `argument-hint: '<arg>'` in SKILL.md YAML frontmatter to guide users on required parameters when invoking skills."
))

# Q33 (Target: A = 0)
questions.append(create_question(
    qid=33,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="Modular Imports in CLAUDE.md",
    module="Domain 3 (@import Syntax)",
    scenario="A team's `.claude/CLAUDE.md` has grown to 800 lines, making it difficult to maintain. The team wants to break it into modular files (`architecture.md`, `style.md`, `testing.md`) while keeping a central entry point. Which mechanism is natively supported in CLAUDE.md?",
    options=[
        "Use `@import` syntax in CLAUDE.md (e.g. `@import ./style.md`) to include modular files.",
        "Write a Python script that concatenates all markdown files into a single string on boot.",
        "Embed HTML iframe tags inside CLAUDE.md pointing to local filesystem path locations.",
        "Create symlinks in the operating system root folder linking back to the documentation."
    ],
    correct_idx=0,
    rationales={
        "correct": "Claude Code supports `@import <path>` syntax directly within `CLAUDE.md`. This allows teams to break large monolithic instruction files into modular, domain-specific markdown files that are resolved and pulled in automatically.",
        "distractors": [
            "Manual Python concatenation scripts add unnecessary maintenance overhead when native `@import` exists.",
            "Claude Code parses markdown, not rendered HTML iframes for context loading.",
            "Operating system symlinks in root directories are fragile and violate repository containment."
        ]
    },
    key_insight="Modularize large CLAUDE.md files using native `@import ./path.md` syntax to keep instructions organized and maintainable."
))

# Q34 (Target: B = 1)
questions.append(create_question(
    qid=34,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="Codebase Exploration Subagents",
    module="Domain 3 (Explore Subagent Architecture)",
    scenario="A developer asks Claude Code a broad conceptual question: 'How does our notification dispatching pipeline work across all microservices?' Why does Claude Code deploy an Explore subagent rather than running searches in the main context?",
    options=[
        "The main agent lacks read permissions for files located outside the immediate working directory.",
        "Running exploration in a separate context keeps verbose search noise out of the main conversation.",
        "The Messages API enforces a strict cap of three tool executions per primary conversation thread.",
        "Explore subagents execute on dedicated remote supercomputers optimized for graph traversal."
    ],
    correct_idx=1,
    rationales={
        "correct": "Codebase-wide exploration generates hundreds of file reads, grep outputs, and directory listings. Deploying a dedicated Explore subagent isolates this noisy discovery in a disposable sub-context, returning only a synthesized summary to the main conversation and conserving context tokens.",
        "distractors": [
            "The main agent has full workspace read permissions; isolation is for context hygiene, not OS security.",
            "The Messages API supports arbitrarily long multi-turn tool loops, not capped at three turns.",
            "Subagents run within the same execution environment, not on separate remote supercomputers."
        ]
    },
    key_insight="Explore subagents run noisy codebase discovery in an isolated context, returning condensed findings to preserve the main context window."
))

# Q35 (Target: C = 2)
questions.append(create_question(
    qid=35,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="Iterative Refinement",
    module="Domain 3 (The Interview Pattern)",
    scenario="A product manager provides a vague, ambiguous feature request to an engineering agent: 'Add support for multi-region data syncing.' Rather than guessing implementation details, what architectural prompt technique should the agent use first?",
    options=[
        "Immediately write code for the most complex possible distributed consensus algorithm.",
        "Reject the task with an unhandled exception and notify the engineering manager.",
        "Adopt the Interview Pattern: ask clarifying questions to resolve trade-offs before coding.",
        "Deploy ten parallel subagents to implement ten different speculative synchronization models."
    ],
    correct_idx=2,
    rationales={
        "correct": "The Interview Pattern instructs the agent to ask targeted clarifying questions (consistency models, conflict resolution, latency targets) when specifications are ambiguous, ensuring alignment before writing code. Guessing requirements on ambiguous tasks results in massive rework.",
        "distractors": [
            "Speculatively implementing complex algorithms without knowing requirements leads to wasted effort.",
            "Rejecting the task abruptly damages usability; clarifying questions are the professional approach.",
            "Deploying 10 speculative implementations wastes massive token and compute budgets."
        ]
    },
    key_insight="Use the Interview Pattern for ambiguous requirements: prompt the agent to ask clarifying questions before implementation."
))

# ─── DOMAIN 4: Prompt Engineering & Structured Output (Q36 - Q45) ────────────

# Q36 (Target: D = 3)
questions.append(create_question(
    qid=36,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Explicit Criteria",
    module="Domain 4 (Severity Calibration with Code Snippets)",
    scenario="A code review bot categorizes issues into 'Critical', 'Major', and 'Minor'. Developers complain that minor formatting issues are constantly labeled as 'Critical'. How should the prompt engineer calibrate the severity ratings?",
    options=[
        "Add uppercase warning text stating that incorrect severity labels will trigger penalties.",
        "Tell the model to 'be thoughtful and balanced when assigning severity to developer code'.",
        "Switch the underlying model tier to Claude 3.5 Haiku to downgrade all severity outputs.",
        "Provide concrete code snippets illustrating exact examples of Critical, Major, and Minor issues."
    ],
    correct_idx=3,
    rationales={
        "correct": "Severity calibration is most effectively achieved by providing concrete code snippets for each severity tier (e.g. SQL injection snippet for Critical, unhandled null for Major, trailing whitespace for Minor). Abstract prose definitions fail; concrete examples anchor model calibration.",
        "distractors": [
            "Threatening penalties in prompts adds emotional noise without defining what constitutes Critical.",
            "Vague directives ('be thoughtful and balanced') provide zero objective criteria for severity boundaries.",
            "Changing model tiers does not calibrate severity definitions and degrades overall reasoning."
        ]
    },
    key_insight="Calibrate severity classifications by providing concrete code snippets for each tier, rather than relying on abstract prose definitions."
))

# Q37 (Target: A = 0)
questions.append(create_question(
    qid=37,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Explicit Criteria",
    module="Domain 4 (False-Positive Trust Erosion)",
    scenario="An automated PR review bot flags security, performance, and documentation issues. The documentation checks have a 45% false-positive rate, causing developers to completely ignore ALL comments from the bot, including critical security alerts. What is the immediate architectural remediation?",
    options=[
        "Temporarily disable the high-error documentation category while refining its explicit rules.",
        "Increase the frequency of bot notifications to force developers to acknowledge comments.",
        "Threaten developers with disciplinary action if pull request review comments are ignored.",
        "Instruct the bot to post all documentation comments anonymously under a synthetic user."
    ],
    correct_idx=0,
    rationales={
        "correct": "High false-positive rates in a single category destroy developer trust across all categories (false-positive trust erosion). The recommended remediation is immediately disabling the noisy category while refining its prompt rules, preserving trust in high-stakes security findings.",
        "distractors": [
            "Increasing notification frequency amplifies alert fatigue and worsens developer frustration.",
            "Disciplinary threats treat a technical quality defect as an employee compliance failure.",
            "Posting anonymously obscures telemetry and does not solve the underlying false-positive rate."
        ]
    },
    key_insight="High false-positive rates in one category erode trust across all findings. Temporarily disable noisy categories while refining rules."
))

# Q38 (Target: B = 1)
questions.append(create_question(
    qid=38,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Structured Output with tool_use",
    module="Domain 4 (Enum Design for Ambiguity)",
    scenario="A medical intake extraction pipeline extracts a patient's primary symptom into an enum field: `['headache', 'chest_pain', 'fever']`. When a patient presents with an atypical symptom like 'numbness in fingers', the extraction fails schema validation. How should the schema be designed?",
    options=[
        "Instruct the model to pick whichever of the three existing enum values is closest alphabetically.",
        "Include an 'other' or 'unclear' enum value paired with a freeform symptom_details string field.",
        "Remove the enum entirely and replace it with an unvalidated integer representing symptom severity.",
        "Configure the system to reject patient admission whenever an unlisted symptom is reported."
    ],
    correct_idx=1,
    rationales={
        "correct": "Restricting real-world polymorphic data to rigid enums without fallback options forces schema validation failures or inaccurate forced classifications. Best practice is including an `'other'` or `'unclear'` enum option paired with a freeform string field (e.g. `other_details`) to capture unexpected variations.",
        "distractors": [
            "Alphabetical matching produces clinically dangerous misdiagnoses.",
            "Replacing symptoms with an unvalidated integer loses qualitative clinical data.",
            "Rejecting patients based on schema constraints violates medical care obligations."
        ]
    },
    key_insight="Pair enum fields with an 'other' or 'unclear' option and a freeform detail field to handle real-world variations gracefully."
))

# Q39 (Target: C = 2)
questions.append(create_question(
    qid=39,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Validation-Retry Loops",
    module="Domain 4 (Telemetry via detected_pattern)",
    scenario="A legal contract extraction pipeline extracts termination notice periods. Over time, prompt engineers want to analyze which contractual phrasing patterns cause the highest validation failure rates. What metadata field should the extraction schema include?",
    options=[
        "A field storing the current operating system CPU utilization during the extraction turn.",
        "A field containing the raw base64 string encoding of the entire contract PDF document.",
        "A detected_pattern field tagging the syntactic phrasing style identified in the source text.",
        "A boolean flag indicating whether the prompt engineer was logged into the admin dashboard."
    ],
    correct_idx=2,
    rationales={
        "correct": "Including a `detected_pattern` metadata field in structured extraction allows the model to tag the phrasing style or clause structure observed in source text. Downstream analytics can aggregate these tags against validation failures to pinpoint which phrasing patterns require refined prompt examples.",
        "distractors": [
            "Host CPU utilization provides no semantic information about document text patterns.",
            "Storing raw base64 PDF strings balloons database storage without providing analytical telemetry.",
            "Engineer login status has zero correlation with contract clause syntax."
        ]
    },
    key_insight="Include metadata fields like `detected_pattern` in extraction schemas to capture phrasing styles for downstream failure telemetry."
))

# Q40 (Target: D = 3)
questions.append(create_question(
    qid=40,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Few-Shot Prompting",
    module="Domain 4 (Hallucination Suppression via Diverse Examples)",
    scenario="A receipt extraction system frequently hallucinates tip amounts on retail store receipts where no tip line exists. How can few-shot prompting be used to suppress this specific hallucination?",
    options=[
        "Add ten few-shot examples of restaurant receipts showing tips ranging from 15% to 25%.",
        "Add a prompt rule stating that tips should be calculated at 18% automatically if missing.",
        "Remove all few-shot examples from the prompt and rely strictly on zero-shot inference.",
        "Include diverse few-shot examples showing retail receipts where tip is explicitly set to null."
    ],
    correct_idx=3,
    rationales={
        "correct": "Models often hallucinate missing fields if few-shot examples only depict cases where that field is present. Including diverse negative examples—specifically showing retail receipts where no tip exists and demonstrating the output field set to `null`—teaches the model when to omit values.",
        "distractors": [
            "Showing restaurant receipts with tips reinforces the model's assumption that tips are always present.",
            "Calculating automatic tips on retail receipts fabricates charges that customers never paid.",
            "Zero-shot prompting lacks concrete guidance on handling missing fields."
        ]
    },
    key_insight="Suppress field hallucination by including few-shot examples that explicitly demonstrate setting missing fields to null."
))

# Q41 (Target: A = 0)
questions.append(create_question(
    qid=41,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Multi-Pass Architecture",
    module="Domain 4 (Local vs Integration Review Passes)",
    scenario="An architectural compliance checker reviews a microservice pull request spanning 12 files. To prevent attention dilution and ensure both local code quality and cross-service interface contracts are verified, how should the review pipeline be structured?",
    options=[
        "A multi-pass pipeline: independent per-file review passes plus a separate integration pass.",
        "A single massive prompt turn passing all twelve files concurrently with temperature zero.",
        "Twelve independent reviews of File 1, followed by discarding the remaining eleven files.",
        "A bash script that compiles all twelve files into a single minified JavaScript bundle."
    ],
    correct_idx=0,
    rationales={
        "correct": "The multi-pass architecture separates concerns: Phase 1 conducts independent per-file review passes focusing on localized syntax, typing, and logic; Phase 2 executes an integration pass evaluating cross-file interface contracts, schema compatibility, and end-to-end data flow.",
        "distractors": [
            "A single massive prompt turn passing 12 files causes severe attention dilution and inconsistent scrutiny.",
            "Reviewing only File 1 leaves 11 files completely unreviewed.",
            "Minification strips comments, types, and variable names, making semantic review impossible."
        ]
    },
    key_insight="Structure complex multi-file reviews into a multi-pass pipeline: independent local file passes followed by a cross-file integration pass."
))

# Q42 (Target: B = 1)
questions.append(create_question(
    qid=42,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Human Review & Confidence Calibration",
    module="Domain 4 (Confidence Routing against Ground Truth)",
    scenario="A mortgage application parsing system processes borrower tax forms. To minimize manual human labor while maintaining 99.9% accuracy, how should the routing between autonomous processing and human underwriting be calibrated?",
    options=[
        "Route all applications to human underwriters on Fridays and automate processing on weekdays.",
        "Calibrate field-level confidence against ground-truth validation sets; route low-confidence fields.",
        "Rely on the model's self-reported confidence score of 1-10 to route cases below an 8 threshold.",
        "Automate 100% of applications and accept that 5% of mortgage approvals will contain false data."
    ],
    correct_idx=1,
    rationales={
        "correct": "Effective human-in-the-loop routing requires calibrating field-level model confidence against empirical ground-truth validation sets. When empirical confidence falls below the required threshold for specific fields, only those borderline fields are routed to human review queues.",
        "distractors": [
            "Day-of-week routing is arbitrary and has no correlation with application accuracy or risk.",
            "LLM self-reported confidence scores (1-10) are notoriously poorly calibrated and unreliable.",
            "Accepting 5% false data on mortgage approvals creates catastrophic financial and legal liability."
        ]
    },
    key_insight="Calibrate field-level confidence against empirical ground-truth validation sets before routing low-confidence cases to human review."
))

# Q43 (Target: C = 2)
questions.append(create_question(
    qid=43,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Batch Processing",
    module="Domain 4 (custom_id Correlation)",
    scenario="A data engineering team submits 15,000 document extraction requests in a single Message Batches API job. Because the Batch API processes requests asynchronously out of order, how does the application map completed results back to source documents?",
    options=[
        "By matching the exact microsecond timestamp of when the batch response was downloaded.",
        "By relying on the physical array order of elements in the returned JSONL response file.",
        "By correlating the unique developer-assigned custom_id parameter submitted with each request.",
        "By performing fuzzy text matching between the extracted output and the original document text."
    ],
    correct_idx=2,
    rationales={
        "correct": "In the Message Batches API, every request includes a developer-assigned `custom_id` string (e.g. `doc_invoice_88291`). The batch response echoes this `custom_id` alongside each result, providing guaranteed deterministic correlation regardless of processing order.",
        "distractors": [
            "Timestamps do not uniquely identify individual documents processed in parallel batches.",
            "Batch responses are written asynchronously as items complete; array order is not guaranteed.",
            "Fuzzy text matching is computationally expensive, non-deterministic, and prone to cross-document collisions."
        ]
    },
    key_insight="Correlate Message Batches API requests and results using the developer-assigned `custom_id` parameter."
))

# Q44 (Target: D = 3)
questions.append(create_question(
    qid=44,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Few-Shot Prompting",
    module="Domain 4 (Few-Shot Construction Guidelines)",
    scenario="A lead architect reviews a prompt authored by a junior engineer containing 25 few-shot examples for classifying customer support tickets. The prompt consumes 6,000 input tokens per turn and experiences high latency. What is the recommended few-shot optimization?",
    options=[
        "Double the number of examples to 50 to maximize classification statistical power.",
        "Remove all few-shot examples and rely entirely on zero-shot inference without guidelines.",
        "Replace the prompt text with an encrypted binary embedding vector stored in Redis.",
        "Prune to 2-4 diverse, high-leverage examples that clearly illustrate boundary edge cases."
    ],
    correct_idx=3,
    rationales={
        "correct": "Few-shot prompting exhibits diminishing returns beyond 2-4 carefully chosen, diverse examples. Packing 25 examples bloats input token costs, increases latency, and dilutes model focus. Curating 2-4 high-leverage examples that demonstrate boundary cases achieves superior accuracy at a fraction of the cost.",
        "distractors": [
            "Expanding to 50 examples doubles token cost and latency while degrading attention focus.",
            "Removing all examples loses guidance on subtle edge cases.",
            "The Messages API accepts text prompts, not raw encrypted embedding vectors."
        ]
    },
    key_insight="Curate 2-4 diverse, high-leverage few-shot examples targeting boundary cases. Excessive examples bloat token costs with diminishing returns."
))

# Q45 (Target: A = 0)
questions.append(create_question(
    qid=45,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Structured Output with tool_use",
    module="Domain 4 (Validation of Arithmetic Consistency)",
    scenario="A shipping manifest parser extracts package weights and a stated total weight. In 5% of cases, the extracted individual package weights sum to 450 kg, while the extracted total weight field states 500 kg. How should the pipeline resolve this discrepancy?",
    options=[
        "Run an automated validation check that compares the sum to the total and triggers a retry loop.",
        "Instruct the model to hallucinate an extra 50 kg phantom package to balance the ledger.",
        "Silently overwrite the total weight field with the arithmetic sum without auditing.",
        "Drop all package weight records and report only the total manifest weight to the database."
    ],
    correct_idx=0,
    rationales={
        "correct": "When arithmetic discrepancies occur between line items and stated totals, an external validation script should detect the mismatch (`sum != total`) and feed both values back to Claude in a validation-retry loop: 'The individual weights sum to 450 kg, but total stated is 500 kg. Re-examine the document and resolve.'",
        "distractors": [
            "Inventing phantom packages fabricates non-existent cargo and corrupts logistics tracking.",
            "Silently overwriting totals conceals potential omissions (e.g. a missed package on page 2).",
            "Dropping individual line items destroys granular cargo manifests required for customs compliance."
        ]
    },
    key_insight="Detect arithmetic discrepancies programmatically and initiate a validation-retry loop with the specific mathematical discrepancy."
))

# ─── DOMAIN 5: Context Management & Reliability (Q46 - Q53) ───────────────────

# Q46 (Target: B = 1)
questions.append(create_question(
    qid=46,
    domain_id=5,
    domain_name="Context Management & Reliability",
    sub_skill="Context Preservation",
    module="Domain 5 (Tool Output Trimming)",
    scenario="An e-commerce customer support tool `get_order` returns a raw JSON object containing 48 database fields, including internal warehouse rack IDs, courier vehicle telemetry, and database audit hashes. The agent only needs the order status and tracking number. What context optimization should be applied?",
    options=[
        "Compress the raw JSON object using gzip compression before appending to conversation context.",
        "Trim tool output to return only the specific fields needed by the agent before adding to history.",
        "Store the raw 48 fields in the system prompt on every turn to ensure total data availability.",
        "Upgrade the model tier to Claude 3 Opus to accommodate the unneeded database metadata fields."
    ],
    correct_idx=1,
    rationales={
        "correct": "Tool output trimming is a fundamental context engineering practice: strip extraneous internal database fields (rack IDs, vehicle telemetry, internal hashes) before returning tool results to Claude. Injecting only the 2-3 fields required preserves context budget, reduces latency, and sharpens model focus.",
        "distractors": [
            "Gzip compressed bytes are illegible binary tokens to language model tokenizers.",
            "Putting unneeded database fields in the system prompt multiplies token costs across every turn.",
            "Upgrading model tiers increases costs significantly without solving unnecessary context bloat."
        ]
    },
    key_insight="Trim tool outputs to return only the fields the agent needs. Extraneous database metadata wastes context and dilutes focus."
))

# Q47 (Target: C = 2)
questions.append(create_question(
    qid=47,
    domain_id=5,
    domain_name="Context Management & Reliability",
    sub_skill="Context Preservation",
    module="Domain 5 (History Completeness in Messages API)",
    scenario="A developer builds a multi-turn support chatbot using the raw Messages API. To save bandwidth, the client application sends only the initial system prompt and the latest user turn on turn 5, dropping turns 1 through 4. How does Claude behave on turn 5?",
    options=[
        "Claude accesses its internal server-side session cache to reconstruct the missing conversation turns.",
        "Claude throws an HTTP 400 Bad Request error indicating that prior message hashes are missing.",
        "Claude loses all prior conversational context and answers as if starting a brand new conversation.",
        "Claude queries the client's local browser storage to retrieve the omitted conversational turns."
    ],
    correct_idx=2,
    rationales={
        "correct": "The Anthropic Messages API is strictly stateless: it does not store conversational session history server-side. Every request must include the complete array of prior messages. Dropping turns 1-4 causes Claude to treat turn 5 as a brand new conversation with zero awareness of prior interactions.",
        "distractors": [
            "The Messages API maintains no server-side conversation memory between standard API calls.",
            "The API does not validate message hashes; it processes whatever messages array is supplied.",
            "Language models cannot reach out to query local client browser storage."
        ]
    },
    key_insight="The Messages API is stateless. You must pass the complete message history on every turn; dropping earlier turns destroys conversational context."
))

# Q48 (Target: D = 3)
questions.append(create_question(
    qid=48,
    domain_id=5,
    domain_name="Context Management & Reliability",
    sub_skill="Escalation & Ambiguity Resolution",
    module="Domain 5 (Customer Explicit Escalation)",
    scenario="A customer in an automated support chat types: 'I do not want to talk to a robot anymore. Connect me to a real person right now.' The issue is a simple password reset that the agent can execute autonomously in two seconds. What is the correct architectural action?",
    options=[
        "Ignore the customer's request and immediately execute the password reset autonomously.",
        "Ask the customer three survey questions regarding why they dislike automated AI assistants.",
        "Display an error message stating that human representatives are unavailable for simple tasks.",
        "Honor the customer's explicit request immediately and execute the escalation workflow."
    ],
    correct_idx=3,
    rationales={
        "correct": "An explicit customer request for a human agent is a mandatory, non-negotiable escalation trigger. Regardless of how simple the issue is, attempting to force the customer through autonomous resolution after they have explicitly demanded a human damages trust and causes extreme frustration.",
        "distractors": [
            "Ignoring the explicit demand and forcing autonomous execution enrages customers and violates support protocols.",
            "Interrogating an angry customer with survey questions exacerbates frustration.",
            "Refusing to escalate locks customers in an unhelpful loop."
        ]
    },
    key_insight="When a customer explicitly demands a human representative, escalate immediately. Never attempt to force autonomous resolution."
))

# Q49 (Target: A = 0)
questions.append(create_question(
    qid=49,
    domain_id=5,
    domain_name="Context Management & Reliability",
    sub_skill="Error Propagation",
    module="Domain 5 (Premature Termination Anti-Pattern)",
    scenario="A multi-agent system orchestrates five parallel subagents to compile a comprehensive country risk report. Four subagents return complete analyses, while the fifth subagent (geopolitical risk) times out due to an API outage. How should the coordinator handle this failure?",
    options=[
        "Synthesize the four successful reports and explicitly annotate that geopolitical risk data timed out.",
        "Abort the entire orchestration pipeline and throw an unhandled exception, discarding all work.",
        "Invent synthetic geopolitical risk statistics to ensure the final report has zero missing sections.",
        "Hang the coordinator process indefinitely until the third-party geopolitical API comes back online."
    ],
    correct_idx=0,
    rationales={
        "correct": "Premature termination (aborting an entire multi-agent job because one optional subagent failed) is an anti-pattern that discards valuable work. The coordinator should synthesize the successful deliverables and explicitly annotate the missing section with a clear explanation of the timeout.",
        "distractors": [
            "Aborting the entire job discards valuable completed work and wastes significant token spend.",
            "Inventing synthetic data is severe hallucination that compromises intelligence reporting.",
            "Hanging indefinitely exhausts server timeouts and locks system resources."
        ]
    },
    key_insight="Avoid premature pipeline termination on partial subagent failure. Synthesize available findings and explicitly annotate missing sections."
))

# Q50 (Target: B = 1)
questions.append(create_question(
    qid=50,
    domain_id=5,
    domain_name="Context Management & Reliability",
    sub_skill="Codebase Exploration Subagents",
    module="Domain 5 (External Scratchpads for State)",
    scenario="An autonomous migration agent performs a 6-hour codebase modernization task involving 80 source files. To prevent context degradation and ensure progress survives potential process interruptions, how should intermediate state be preserved?",
    options=[
        "Keep all intermediate diffs and file states solely within the volatile in-memory prompt context.",
        "Persist intermediate state, completed files, and next steps to a structured manifest on disk.",
        "Transmit continuous terminal screen recordings over a local WebSocket to a video server.",
        "Instruct the model to memorize its progress using an internal associative memory register."
    ],
    correct_idx=1,
    rationales={
        "correct": "For long-running autonomous tasks (6+ hours across 80 files), relying solely on conversation context risks catastrophic progress loss upon network disconnection or context limits. Writing state to an external scratchpad or manifest file on disk enables crash recovery and clean state tracking.",
        "distractors": [
            "Keeping state solely in volatile memory ensures total progress loss if the process crashes or context overflows.",
            "Screen recordings are unstructured video pixels that cannot restore programmatic execution state.",
            "LLMs do not have persistent internal associative memory registers across turns."
        ]
    },
    key_insight="Persist progress and intermediate state to structured manifest files on disk for long-running workflows, enabling crash recovery."
))

# Q51 (Target: C = 2)
questions.append(create_question(
    qid=51,
    domain_id=5,
    domain_name="Context Management & Reliability",
    sub_skill="Information Provenance",
    module="Domain 5 (Temporal Discrepancies in Data)",
    scenario="A market intelligence research agent analyzes quarterly revenue for a cloud provider across two financial reports. Source 1 reports $10B revenue, while Source 2 reports $11.5B revenue. What provenance metadata explains this discrepancy most frequently?",
    options=[
        "The cryptographic hash of the server that hosted the downloaded PDF document.",
        "The screen resolution of the developer machine running the Claude Agent SDK.",
        "The publication dates and reporting periods (e.g. Q1 2024 vs Q1 2025) of the reports.",
        "The programming language used to construct the HTTP GET web request connection."
    ],
    correct_idx=2,
    rationales={
        "correct": "Apparent factual discrepancies in business and financial data are most frequently explained by temporal differences: different publication dates, fiscal years, or reporting quarters (e.g., Q1 2024 vs Q1 2025). Maintaining timestamps and reporting periods in metadata is essential.",
        "distractors": [
            "Server cryptographic hashes have no connection to business revenue figures.",
            "Client screen resolution does not alter financial report data.",
            "Programming languages used for HTTP requests do not modify the content of corporate filings."
        ]
    },
    key_insight="Track publication dates and reporting periods in metadata. Temporal differences frequently explain apparent data discrepancies."
))

# Q52 (Target: D = 3)
questions.append(create_question(
    qid=52,
    domain_id=5,
    domain_name="Context Management & Reliability",
    sub_skill="Human Review & Confidence Calibration",
    module="Domain 5 (Stratified Random Sampling)",
    scenario="An automated claim processing pipeline processes 50,000 claims per month with zero human intervention for high-confidence predictions. How should the enterprise monitor for silent model drift or emergent extraction failures over time?",
    options=[
        "Rerun the entire historical dataset from month one through the pipeline every Friday night.",
        "Disable automated claim processing completely and return to 100% manual human review.",
        "Assume that high model confidence scores guarantee zero errors will ever emerge in production.",
        "Perform recurring stratified random sampling of automated claims for manual quality audits."
    ],
    correct_idx=3,
    rationales={
        "correct": "Automated pipelines that operate without human intervention risk silent failures when document layouts drift or edge cases emerge. The established quality assurance practice is ongoing stratified random sampling: pulling a small percentage of automated claims across all categories for human audit.",
        "distractors": [
            "Re-running 50,000 historical claims every week wastes massive compute and does not evaluate new document templates.",
            "Abandoning automation discards all business efficiency gains.",
            "Assuming high confidence guarantees zero errors ignores model overconfidence and data drift."
        ]
    },
    key_insight="Deploy stratified random sampling on automated pipelines to continuously audit high-confidence outputs and detect silent drift."
))

# Q53 (Target: A = 0)
questions.append(create_question(
    qid=53,
    domain_id=5,
    domain_name="Context Management & Reliability",
    sub_skill="Context Preservation",
    module="Domain 5 (The Case Facts Block)",
    scenario="A customer support assistant handles complex returns involving multi-item orders, partial discounts, and return shipping deductions. To ensure that dollar amounts, order IDs, and dates are never distorted during conversational turn management, what architectural pattern should be used?",
    options=[
        "Maintain a persistent Case Facts block injected verbatim into prompts, never passing through summarizers.",
        "Re-summarize the entire conversation history on every single turn using a smaller model tier.",
        "Instruct the user to repeat all order numbers and dollar amounts in every message they send.",
        "Store dollar amounts as base64-encoded binary strings inside the user system prompt header."
    ],
    correct_idx=0,
    rationales={
        "correct": "The Case Facts block is the definitive architectural pattern for preventing fact distortion in transactional chats: verified numbers, order IDs, customer names, and dates are recorded once in a structured block and injected verbatim into every subsequent prompt, completely bypassing summarizers.",
        "distractors": [
            "Re-summarizing on every turn compounds distortion and rapidly degrades numeric precision.",
            "Forcing users to repeat transactional numbers in every message destroys customer experience.",
            "Base64-encoded strings cannot be reasoned over natively by the model."
        ]
    },
    key_insight="Store critical transactional data in a persistent Case Facts block that is injected verbatim into every prompt and never summarized away."
))

exam2_data = {
    "id": 2,
    "title": "Practice Exam 2: Tool Design & MCP Architecture",
    "description": "Tool interface design, MCP server integration, error propagation, and cross-agent tool scoping.",
    "questions": questions
}

output_path = "data/architect/exam2.json"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(exam2_data, f, indent=2)

print(f"Successfully generated {len(questions)} questions in {output_path}!")
