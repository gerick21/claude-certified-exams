#!/usr/bin/env python3
"""
Authoring Script for Architect Practice Exam 5:
'Practice Exam 5: Comprehensive Mock Exam (Final Readiness)'
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
    module="Domain 1 (Banking Coordinator Stop Reason Evaluation)",
    scenario="A multinational banking platform coordinator orchestrates five subagents to perform cross-currency settlement, anti-money laundering (AML) compliance, fraud analysis, and general ledger reconciliation. When inspecting model output turns, what exact field and value must the application loop check to determine that all agentic processing is complete?",
    options=[
        "Evaluate the stop_reason field and confirm it has returned end_turn before finalizing output.",
        "Check whether the assistant role string contains the keyword 'completed' in its text body.",
        "Inspect the HTTP response status code to ensure it matches HTTP 204 No Content exactly.",
        "Count the total number of processed input tokens until an arbitrary threshold is exceeded."
    ],
    correct_idx=0,
    rationales={
        "correct": "In the Anthropic Messages API, the definitive signal that an agent has completed its task is `stop_reason == 'end_turn'`. If `stop_reason == 'tool_use'`, the loop must execute the requested tools and continue; relying on string matching or token thresholds causes premature termination.",
        "distractors": [
            "Checking for keywords like 'completed' is brittle natural language parsing that fails when commentary text mentions the word.",
            "The Messages API returns HTTP 200 with JSON payloads for successful completions, not HTTP 204.",
            "Token counting is a budget limit, not a logical signal that multi-agent settlement has concluded successfully."
        ]
    },
    key_insight="Evaluate `stop_reason == 'end_turn'` to detect loop completion. Never use string parsing or arbitrary iteration thresholds."
))

# Q2 (Target: B = 1)
questions.append(create_question(
    qid=2,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Workflow Enforcement & Handoff",
    module="Domain 1 (Defense Classified Intelligence Pipeline)",
    scenario="A defense intelligence system ingests satellite imagery, signals intelligence, and diplomatic cables to produce threat assessments. Classified military doctrine mandates that intelligence declassification checks run deterministically on every source document before synthesis. Which architectural pattern must be adopted?",
    options=[
        "An autonomous agent loop where Claude dynamically decides whether declassification is necessary.",
        "A deterministic code pipeline executing declassification verification before passing data to Claude.",
        "A decentralized peer-to-peer agent network communicating over an unencrypted local mesh network.",
        "A prompt-only system instruction asking Claude to promise to respect military classifications."
    ],
    correct_idx=1,
    rationales={
        "correct": "When national security and classified information handling are at stake, probabilistic agent reasoning is unacceptable. A deterministic code pipeline physically executes declassification verification in code before allowing data into the model context, guaranteeing 100% compliance.",
        "distractors": [
            "Allowing an LLM to dynamically decide whether declassification is needed introduces catastrophic security risk.",
            "Decentralized peer-to-peer mesh networks lack centralized compliance auditing and breach controls.",
            "Prompt-only promises are probabilistic and offer zero technical guarantees against leaking classified data."
        ]
    },
    key_insight="Enforce high-stakes classified security policies using deterministic code pipelines prior to model ingestion, not probabilistic agent prompts."
))

# Q3 (Target: C = 2)
questions.append(create_question(
    qid=3,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Task Decomposition Strategies",
    module="Domain 1 (Aerospace Multi-Pass Engineering Review)",
    scenario="An aerospace engineering team analyzes a commercial airliner propulsion specification across 40 complex subsystem requirement documents. When all 40 documents are passed in a single prompt, Claude overlooks critical turbine blade thermal stress tolerances in the middle documents. What architectural pattern resolves this?",
    options=[
        "Instruct Claude in uppercase text to pay extra special attention to thermal stress tolerances.",
        "Switch the model to a faster lightweight model tier to accelerate document processing speed.",
        "Deploy a multi-pass pipeline: extract tolerances per subsystem first, then aggregate globally.",
        "Concatenate all 40 engineering documents into a single unstructured text file without headers."
    ],
    correct_idx=2,
    rationales={
        "correct": "Processing 40 technical documents in a single prompt induces severe attention dilution ('lost in the middle'). The multi-pass architecture resolves this by running focused, independent extraction passes on each subsystem document individually, followed by a global integration pass.",
        "distractors": [
            "Uppercase prompt commands cannot overcome the mathematical realities of transformer attention dilution across 40 files.",
            "Lightweight model tiers have lower reasoning depth and worsen missed technical tolerances.",
            "Removing headers eliminates structural cues, further degrading model retrieval performance."
        ]
    },
    key_insight="Overcome attention dilution across dozens of complex engineering documents by implementing a multi-pass extraction and aggregation pipeline."
))

# Q4 (Target: D = 3)
questions.append(create_question(
    qid=4,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Session State & Resumption",
    module="Domain 1 (Smart City Traffic Algorithm Branching)",
    scenario="A smart city traffic control coordinator monitors urban congestion following a major stadium event. The coordinator needs to simulate two mutually exclusive traffic light re-timing strategies (arterial prioritization vs highway bypass diversion) from the exact same real-time traffic baseline. Which SDK feature is designed for this?",
    options=[
        "Re-run the entire traffic analysis from scratch on each branch, doubling sensor input tokens.",
        "Execute both simulation strategies sequentially in the same thread while clearing prompt memory.",
        "Mount an external NFS filesystem share that duplicates traffic camera bitmap images to disk.",
        "Use fork_session to branch two independent simulation sessions from the shared traffic baseline."
    ],
    correct_idx=3,
    rationales={
        "correct": "`fork_session` branches multiple independent child sessions from a shared baseline state. This allows exploring both traffic diversion strategies concurrently from the exact same live congestion context without cross-contaminating session state or re-ingesting sensor data.",
        "distractors": [
            "Re-running from scratch forces re-reading thousands of sensor inputs, incurring severe latency during an active traffic surge.",
            "Sequential execution in the same thread pollutes context and causes contradictory reasoning between the two opposing strategies.",
            "NFS filesystem shares handle file storage, not LLM conversation state branching."
        ]
    },
    key_insight="Use `fork_session` to branch independent simulation paths from a shared baseline state without re-ingesting raw sensor data."
))

# Q5 (Target: A = 0)
questions.append(create_question(
    qid=5,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Task Decomposition Strategies",
    module="Domain 1 (Agricultural Supply Chain Coordinator Decomposition Failure)",
    scenario="An agricultural supply chain research system is asked: 'Analyze global fertilizer shortages across European, South American, and African farming cooperatives.' The final synthesized report completely ignores African cooperatives. Investigation shows the African subagent was never invoked. What was the root cause?",
    options=[
        "The coordinator agent's task decomposition failed to partition African cooperatives as a subtask.",
        "The African agricultural subagent ran out of virtual memory in its local Docker container pod.",
        "The external weather satellite API rejected HTTP queries due to geographic IP firewall rules.",
        "The synthesis agent encountered a schema validation error and silently dropped African findings."
    ],
    correct_idx=0,
    rationales={
        "correct": "In hub-and-spoke multi-agent systems, worker subagents only execute tasks assigned by the coordinator. If a subagent was never invoked, the defect lies in the coordinator's initial task decomposition failing to partition that topic, not downstream execution.",
        "distractors": [
            "The subagent was never spawned; container memory exhaustion could not have occurred.",
            "No queries were ever initiated for African cooperatives, so external API rejections did not occur.",
            "If the subagent was never invoked, no African findings existed for the synthesis agent to drop."
        ]
    },
    key_insight="When entire topics are missing from multi-agent output, trace to the coordinator's initial task decomposition."
))

# Q6 (Target: B = 1)
questions.append(create_question(
    qid=6,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Agent SDK Hooks",
    module="Domain 1 (Telecom PreToolUse High-Risk Gate)",
    scenario="A telecommunications network operations agent manages cell tower routing. Network engineering policy mandates that any automated routing change that drops transmission power by more than 20% must be blocked and routed to a human network engineer. Where should this policy be enforced in the Agent SDK?",
    options=[
        "In a PostToolUse hook that observes tower power after changes are already committed to the network.",
        "In a PreToolUse hook that inspects proposed power arguments and returns a deny decision if > 20%.",
        "Within the coordinator system prompt using bold font warnings about FCC regulatory penalties.",
        "Through a nightly automated audit script that identifies power violations twelve hours later."
    ],
    correct_idx=1,
    rationales={
        "correct": "PreToolUse hooks intercept outgoing tool calls before execution. By evaluating arguments (`power_reduction > 0.20`), the hook returns `permissionDecision: 'deny'`, blocking the hazardous tower power reduction deterministically before hardware modification occurs.",
        "distractors": [
            "PostToolUse runs after tool execution, meaning tower power has already dropped and customer calls have dropped.",
            "Prompt warnings remain probabilistic and routinely fail under ambiguous network alert conditions.",
            "Nightly batch audits occur hours after customer service outages have already taken place."
        ]
    },
    key_insight="Use PreToolUse hooks to intercept and block high-risk physical or infrastructure actions before tool execution occurs."
))

# Q7 (Target: C = 2)
questions.append(create_question(
    qid=7,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Agent SDK Hooks",
    module="Domain 1 (Telecom Vendor XML to JSON PostToolUse)",
    scenario="A telecommunications diagnostic agent queries legacy microwave backhaul routers that return diagnostic telemetry in proprietary XML format. To ensure that Claude receives clean, standardized JSON without wasting model tokens on XML parsing, where should this translation occur?",
    options=[
        "In the system prompt by instructing Claude to execute internal mental XML string parsing.",
        "By asking human network technicians to retype XML outputs into JSON format before queries.",
        "In a PostToolUse hook that parses the raw vendor XML and returns clean standardized JSON.",
        "By deploying an external machine learning translation subagent that consumes 10,000 tokens."
    ],
    correct_idx=2,
    rationales={
        "correct": "PostToolUse hooks intercept tool results immediately upon execution before they are appended to context. Converting vendor XML into clean JSON in code within PostToolUse normalizes data deterministically without consuming model reasoning tokens.",
        "distractors": [
            "Instructing the model to parse verbose XML consumes massive context tokens and increases parsing errors.",
            "Requiring human technicians to manually retype data defeats autonomous network monitoring.",
            "Deploying an LLM translation subagent introduces heavy latency and token expense for simple deterministic XML parsing."
        ]
    },
    key_insight="Use PostToolUse hooks to transform and normalize legacy raw vendor outputs (like XML) into clean JSON before entering Claude's context."
))

# Q8 (Target: D = 3)
questions.append(create_question(
    qid=8,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Workflow Enforcement & Handoff",
    module="Domain 1 (Banking Handoff Dossier Requirements)",
    scenario="An autonomous banking agent determines that a suspicious wire transfer involves an unresolved international sanctions match and must be escalated to a senior compliance officer. What must the handoff payload contain to ensure an effective handoff?",
    options=[
        "A raw network packet capture of the customer TCP socket connection stream.",
        "An encrypted cryptographic hash representing the compliance officer employee badge ID.",
        "A generic message stating that an unknown compliance issue was detected in banking.",
        "A self-contained dossier with customer ID, transaction amount, sanction hit, and next action."
    ],
    correct_idx=3,
    rationales={
        "correct": "An effective human handoff must assemble a self-contained, structured dossier (account ID, transaction sum, matched sanction entity, flagged risk score, and recommended next action) so compliance officers can act immediately without reading dozens of raw conversation turns.",
        "distractors": [
            "Raw TCP network packets provide zero readable compliance context for human officers.",
            "Employee badge hashes belong to identity access layers, not customer risk dossiers.",
            "Vague notifications fail to communicate urgency or specific sanction entity matches."
        ]
    },
    key_insight="Human handoffs require a self-contained, structured dossier summarizing key facts and proposed actions."
))

# Q9 (Target: A = 0)
questions.append(create_question(
    qid=9,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Agent SDK Hooks",
    module="Domain 1 (Defense SubagentStop Audit Trail)",
    scenario="A military command and control system requires an immutable, verifiable audit trail of all actions taken by autonomous target identification subagents. Which Agent SDK lifecycle hook and property capture this audit record upon subagent conclusion?",
    options=[
        "The SubagentStop hook captures the execution event and exposes the agent_transcript_path.",
        "The PreToolUse hook captures the process thread ID and writes it to an unencrypted text file.",
        "The CoordinatorStart hook records the military base geographic coordinates in browser cookies.",
        "The PostToolUse hook dumps the model neural network weights to an external optical disc drive."
    ],
    correct_idx=0,
    rationales={
        "correct": "The `SubagentStop` lifecycle hook triggers when a subagent finishes execution, providing the immutable `agent_transcript_path` on disk. This file contains the complete record of all turns, prompts, and tool calls executed by that subagent for audit compliance.",
        "distractors": [
            "PreToolUse intercepts tool calls prior to execution and does not contain subagent lifecycle completion transcripts.",
            "CoordinatorStart only records session boot, having zero visibility into child subagent execution trails.",
            "PostToolUse intercepts individual tool outputs and does not dump model weights."
        ]
    },
    key_insight="Use the `SubagentStop` lifecycle hook to capture `agent_transcript_path` for immutable audit logging."
))

# Q10 (Target: B = 1)
questions.append(create_question(
    qid=10,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Subagent Invocation & Context Passing",
    module="Domain 1 (Agricultural Field Assessment Spawning)",
    scenario="An agricultural yield prediction coordinator dispatches specialized soil analysis and satellite drone subagents. When attempting to invoke a child subagent, the coordinator raises an error stating subagent invocation is disallowed. What configuration was omitted in `ClaudeAgentOptions`?",
    options=[
        "The allowed_tools configuration omitted the external Python compiler executable binary.",
        "The allowed_tools configuration omitted the orchestration tool name ('Task' or 'Agent').",
        "The developer failed to register an active cellular satellite modem on the Anthropic console.",
        "The child subagents were not pre-compiled into standalone native Windows executables."
    ],
    correct_idx=1,
    rationales={
        "correct": "In the Claude Agent SDK, coordinator agents require explicit authorization to spawn child agents. The coordinator's `allowed_tools` list must explicitly include `'Task'` or `'Agent'`; otherwise, subagent spawning is disallowed by the runtime.",
        "distractors": [
            "The Agent SDK does not require whitelisting the Python compiler binary in allowed_tools.",
            "Subagent spawning is an SDK runtime capability, not a cellular modem console registration.",
            "Subagents are dynamic agentic loops defined in code, not pre-compiled native Windows executables."
        ]
    },
    key_insight="In the Claude Agent SDK, `allowed_tools` must explicitly include `'Task'` or `'Agent'` for the coordinator to spawn subagents."
))

# Q11 (Target: C = 2)
questions.append(create_question(
    qid=11,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Session State & Resumption",
    module="Domain 1 (Smart City Firmware Resumption Failure)",
    scenario="A smart city traffic agent is paused overnight while engineers update the firmware on all intersection radar sensors, changing sensor data output units from miles-per-hour to kilometers-per-hour. When resumed via `--resume`, the agent reports severe traffic speeding violations. Why?",
    options=[
        "The Claude Agent SDK automatically inverts speed calculations after midnight.",
        "The local operating system kernel lost its network connection to the radar sensors.",
        "The resumed session reasoned using cached baseline assumptions that radar units were mph.",
        "The model context window was erased and replaced with an empty template upon resumption."
    ],
    correct_idx=2,
    rationales={
        "correct": "Resuming an existing session via `--resume` restores prior context where radar units were established as mph. Because physical sensor firmware changed externally during the pause, the agent interprets 60 km/h as 60 mph (speeding). When external hardware or contracts change, a fresh session with updated system state is required.",
        "distractors": [
            "The Agent SDK has no feature that inverts mathematical calculations based on time of day.",
            "The issue is semantic unit discrepancy in cached context, not a physical network disconnect.",
            "If the context window had been erased, prior session state would not have caused the speeding assumption."
        ]
    },
    key_insight="Resuming sessions after external hardware or contract changes causes reasoning on stale cached assumptions. Restart with fresh state."
))

# Q12 (Target: D = 3)
questions.append(create_question(
    qid=12,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Task Decomposition Strategies",
    module="Domain 1 (Telecom Outage vs Routine Health Check)",
    scenario="A telecommunications provider has two workloads: (1) routine hourly pings of 10,000 cell towers, and (2) investigating an active fiber-optic cable cut with cascading regional routing failures. Which architectural pattern matches each workload?",
    options=[
        "Use an autonomous agent loop for routine tower pings, and a fixed script for the fiber cut.",
        "Deploy multi-agent supervisor loops with five LLM debate agents for both workloads.",
        "Use a single massive prompt turn passing all 10,000 cell towers into Claude every hour.",
        "Use a deterministic code pipeline for routine pings; use an autonomous agent for the fiber cut."
    ],
    correct_idx=3,
    rationales={
        "correct": "Architectural proportionality: Routine pinging of 10,000 towers is completely deterministic and linear—a lightweight code pipeline is fast, cheap, and reliable. In contrast, investigating an active fiber-optic cut involves open-ended exploration, hypothesis testing, and dynamic rerouting, requiring an autonomous agent loop.",
        "distractors": [
            "Using an autonomous agent loop for 10,000 routine pings introduces massive token costs and latency for simple ICMP checks.",
            "Multi-agent debate loops for simple hourly pings waste millions of tokens unnecessarily.",
            "Passing 10,000 tower pings into an LLM prompt hourly is extraordinarily expensive and slow."
        ]
    },
    key_insight="Use deterministic code pipelines for invariant routine checks. Reserve autonomous agent loops for complex, open-ended incident investigation."
))

# Q13 (Target: A = 0)
questions.append(create_question(
    qid=13,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="Subagent Invocation & Context Passing",
    module="Domain 1 (Banking Parallel Currency Risk Assessment)",
    scenario="A foreign exchange trading coordinator evaluates currency risk across four independent currency pairs (EUR/USD, GBP/USD, USD/JPY, and USD/CHF). To complete the assessment in minimum wall-clock time, how should the coordinator dispatch the analysis subagents?",
    options=[
        "Emit four Task tool invocation blocks in a single turn response to execute them in parallel.",
        "Execute each currency pair sequentially across four separate hourly cron schedule jobs.",
        "Consolidate all four currency pairs into a single large prompt dispatched to one agent.",
        "Ask human currency traders to evaluate three pairs while Claude evaluates the fourth pair."
    ],
    correct_idx=0,
    rationales={
        "correct": "Emitting multiple `Task` or `Agent` tool blocks in a single turn response enables the Claude Agent SDK to spawn and execute all four currency risk subagents concurrently in parallel, achieving minimum end-to-end wall-clock latency.",
        "distractors": [
            "Sequential execution across hourly cron jobs introduces hours of latency, destroying real-time trading utility.",
            "Consolidating all pairs into a single agent creates context clutter and prevents specialized parallel analysis.",
            "Delegating to human traders defeats the purpose of an automated algorithmic trading assessment platform."
        ]
    },
    key_insight="Spawn independent parallel subagents by emitting multiple Task tool calls in a single coordinator response."
))

# Q14 (Target: B = 1)
questions.append(create_question(
    qid=14,
    domain_id=1,
    domain_name="Agentic Architecture & Orchestration",
    sub_skill="SDK setting_sources Parameter",
    module="Domain 1 (Aerospace Site-Specific Checklists)",
    scenario="An aerospace manufacturer conducts flight software safety reviews across three global research facilities. Each facility defines site-specific security hooks in `.claude/settings.local.json`. How must the Agent SDK script configure `setting_sources` so site hooks are loaded?",
    options=[
        "Set setting_sources=[] to enforce a strictly hermetic build across all three facilities.",
        "Set setting_sources=['project', 'local'] to load repository standards and site-specific hooks.",
        "Set setting_sources=['user'] to ensure only personal developer laptop settings apply.",
        "Omit the setting_sources configuration and hardcode facility credentials inside the script."
    ],
    correct_idx=1,
    rationales={
        "correct": "To load site-specific hooks and configuration overrides defined in `settings.local.json`, the Claude Agent SDK requires explicitly passing `'local'` in `setting_sources` (e.g. `setting_sources=['project', 'local']`).",
        "distractors": [
            "`setting_sources=[]` enables hermetic mode, which explicitly ignores all filesystem configurations and local hooks.",
            "`setting_sources=['user']` loads user home directory settings, ignoring project and local site hooks.",
            "Hardcoding credentials in script code violates aerospace software security standards."
        ]
    },
    key_insight="Pass `setting_sources=['project', 'local']` to load project guidelines and site-specific local hooks."
))

# ─── DOMAIN 2: Tool Design & MCP Integration (Q15 - Q24) ──────────────────────

# Q15 (Target: C = 2)
questions.append(create_question(
    qid=15,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="Tool Interface Design",
    module="Domain 2 (Banking Tool Disambiguation)",
    scenario="A banking assistant provides two tools: `transfer_funds` (moves money between checking and savings within the same bank) and `wire_transfer` (dispatches international SWIFT wires to external institutions). Claude frequently calls `wire_transfer` for domestic checking-to-savings transfers. What is the most effective first fix?",
    options=[
        "Delete the transfer_funds tool and execute all domestic transfers as expensive international wires.",
        "Implement a custom neural network classifier trained on historical banking transcripts to route calls.",
        "Add explicit boundaries: state transfer_funds is for internal accounts; wire_transfer is for external.",
        "Instruct human branch managers to review and manually re-route every automated tool invocation."
    ],
    correct_idx=2,
    rationales={
        "correct": "Tool descriptions are the primary selection surface Claude uses. Clarifying descriptions with explicit boundary statements (e.g. 'Use transfer_funds strictly for internal checking/savings movements within this bank. Do NOT use for external banks—use wire_transfer instead') directly eliminates misrouting.",
        "distractors": [
            "Routing domestic checking transfers through international SWIFT wires incurs massive fees and delays.",
            "Training an external ML classifier is an expensive over-engineering step before basic descriptions have been fixed.",
            "Manual human routing for all tool calls defeats the purpose of an automated banking assistant."
        ]
    },
    key_insight="Disambiguate overlapping tools by adding explicit use cases and negative boundaries to tool descriptions."
))

# Q16 (Target: D = 3)
questions.append(create_question(
    qid=16,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="Tool Distribution & tool_choice",
    module="Domain 2 (Defense Declassification Mandatory Tool Call)",
    scenario="A military intelligence review system must execute the `declassification_review` tool on every ingested cable before any intelligence analyst can view the text. Conversational text generation must be strictly prohibited on this step. Which parameter enforces this?",
    options=[
        "Set tool_choice to 'auto' while writing system prompt instructions in bold capital letters.",
        "Configure temperature to zero to discourage the model from emitting conversational text.",
        "Add a prompt rule stating that failing to call the tool constitutes a military offense.",
        "Set tool_choice to {'type': 'tool', 'name': 'declassification_review'} on every request."
    ],
    correct_idx=3,
    rationales={
        "correct": "Setting `tool_choice: {'type': 'tool', 'name': 'declassification_review'}` forces the model to invoke that specific tool, physically disabling conversational text generation or alternative tool selection for that turn.",
        "distractors": [
            "`tool_choice: 'auto'` permits conversational text responses whenever the model decides text is sufficient.",
            "Temperature zero controls sampling determinism but does not force mandatory tool execution over text.",
            "Prompt instructions threatening military offenses remain probabilistic and do not physically disable text generation."
        ]
    },
    key_insight="Force execution of a mandatory security tool by configuring `tool_choice: {'type': 'tool', 'name': '...'}`."
))

# Q17 (Target: A = 0)
questions.append(create_question(
    qid=17,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="Structured Error Responses",
    module="Domain 2 (Agricultural Weather Timeout vs Crop Not Found)",
    scenario="An agricultural advisory agent queries two tools: (1) a satellite weather tool that times out due to cloud link failure, and (2) a crop database that returns zero records for an exotic tropical fruit. How should each result be categorized?",
    options=[
        "Weather timeout is a transient retryable error; missing crop is a valid successful empty result.",
        "Weather timeout is a permanent terminal error; missing crop is a transient retryable error.",
        "Both occurrences should be classified as fatal database crashes requiring container restarts.",
        "Both occurrences should be returned as empty dictionaries marked with HTTP 200 success."
    ],
    correct_idx=0,
    rationales={
        "correct": "The weather satellite timeout is an access failure (transient network issue, retryable with backoff). In contrast, finding zero records for an exotic fruit is a valid, ground-truth empty result (the database verified no records exist, non-retryable). Confusing them causes infinite loops or false omissions.",
        "distractors": [
            "Classifying a transient timeout as permanent terminates valid queries; retrying a non-existent crop loops endlessly.",
            "Neither occurrence represents a fatal software crash requiring container reboots.",
            "Masking the weather timeout as an empty success list leads Claude to falsely conclude there is no weather."
        ]
    },
    key_insight="Distinguish between access failures (transient, retryable) and valid empty results (successful search, zero records, non-retryable)."
))

# Q18 (Target: B = 1)
questions.append(create_question(
    qid=18,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="Tool Distribution & tool_choice",
    module="Domain 2 (Telecom Subagent Tool Scoping)",
    scenario="A telecommunications incident assistant has tools for ping_tower, check_packet_loss, query_alarms, delete_customer_account, and alter_billing_rate. Why should the diagnostic subagent be scoped only to the first three tools?",
    options=[
        "The Claude Agent SDK throws a fatal exception if any agent is assigned more than three tools.",
        "Restricting tools to the agent's role maximizes selection accuracy and enforces least privilege.",
        "Billing tools can only be invoked over dedicated fiber-optic hardware cables in data centers.",
        "Assigning billing tools to network bots causes Linux operating system kernel memory leaks."
    ],
    correct_idx=1,
    rationales={
        "correct": "Scoping tools strictly to an agent's domain (4-5 tools maximum) maximizes tool selection accuracy, minimizes parameter hallucination, and enforces least privilege, preventing a diagnostic agent from modifying customer billing or accounts.",
        "distractors": [
            "The Agent SDK supports up to 128 tools per request, not restricted to three.",
            "Billing tools execute over standard HTTPS APIs, not dedicated fiber-optic hardware lines.",
            "Tool declarations are JSON schemas that do not cause Linux kernel memory leaks."
        ]
    },
    key_insight="Scope tools strictly to agent roles (4-5 tools max) to maximize selection accuracy and enforce operational boundaries."
))

# Q19 (Target: C = 2)
questions.append(create_question(
    qid=19,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="MCP Server Integration",
    module="Domain 2 (Smart City Proprietary Traffic MCP)",
    scenario="A municipal smart city department operates an in-house proprietary traffic controller protocol built in 1998 communicating over serial ports, as well as a PostgreSQL database. What is the recommended MCP adoption strategy?",
    options=[
        "Author custom MCP servers from scratch for both PostgreSQL and the legacy serial traffic system.",
        "Avoid MCP completely and interact with both systems by writing raw shell scripts with Bash.",
        "Deploy the community PostgreSQL MCP server, authoring a custom MCP server for the traffic system.",
        "Wait for Anthropic to author an official out-of-the-box connector for the 1998 serial hardware."
    ],
    correct_idx=2,
    rationales={
        "correct": "The standard architectural principle is adopting verified, community-maintained MCP servers for standard platforms (PostgreSQL, GitHub, Slack) and focusing engineering resources on authoring custom MCP servers for proprietary, in-house legacy systems.",
        "distractors": [
            "Re-authoring PostgreSQL MCP from scratch wastes engineering time and duplicates mature open-source work.",
            "Raw shell scripts via Bash bypass structured schemas, type validation, and security auditing.",
            "Anthropic does not author connectors for private, proprietary municipal serial hardware."
        ]
    },
    key_insight="Adopt community MCP servers for standard databases and tools; build custom MCP servers only for proprietary legacy systems."
))

# Q20 (Target: D = 3)
questions.append(create_question(
    qid=20,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="Built-in Tools",
    module="Domain 2 (Aerospace Grep for Specs vs Glob for CAD)",
    scenario="An aerospace engineering agent needs to locate all 3D CAD modeling files (`*.step`) in a repository, and then search engineering change order text documents for references to 'titanium fastener torque'. Which built-in tools should be used for each task?",
    options=[
        "Use Grep to search for *.step file paths, and use Glob to search engineering change order text.",
        "Use Read to load all binary CAD files into memory, and use Bash to grep text change orders.",
        "Use Edit to rename all CAD files, and use Write to overwrite the engineering change orders.",
        "Use Glob to pattern-match *.step file paths, and use Grep to search change order text contents."
    ],
    correct_idx=3,
    rationales={
        "correct": "`Glob` matches file paths and names across directory trees (locating `**/*.step` files). `Grep` searches inside file contents for text patterns ('titanium fastener torque'). This correctly matches each tool to its technical capability.",
        "distractors": [
            "Inverting Glob and Grep fails: Glob cannot search text inside files, and Grep is not for path pattern matching.",
            "Reading binary CAD files into text context causes decoding errors and exhausts token limits.",
            "Edit and Write perform file modifications and do not perform file searches."
        ]
    },
    key_insight="Glob matches file PATHS (`*.step`). Grep searches file CONTENTS for text strings."
))

# Q21 (Target: A = 0)
questions.append(create_question(
    qid=21,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="Structured Error Responses",
    module="Domain 2 (Banking Multi-Agent Settlement Error Propagation)",
    scenario="In a banking settlement pipeline, a currency exchange subagent fails because foreign exchange markets are closed for a national holiday. How should this failure be propagated back to the coordinator agent?",
    options=[
        "Return a structured error object detailing category 'business_policy', holiday details, and next open date.",
        "Throw an unhandled Python exception that aborts the entire coordinator process immediately.",
        "Return an empty JSON object with HTTP 200 so the coordinator assumes the trade settled cleanly.",
        "Instruct the user in chat to manually phone the foreign central bank to request emergency access."
    ],
    correct_idx=0,
    rationales={
        "correct": "A market holiday is a business/policy state: the subagent must return a structured error payload (`category: 'business_policy', isRetryable: false until market open`) with context. This allows the coordinator to reschedule settlement or notify the customer cleanly without crashing.",
        "distractors": [
            "Unhandled exceptions crash the coordinator and destroy in-flight settlements for other currencies.",
            "Returning empty objects masks the failure and leads the coordinator to record false trade settlements.",
            "Prompting users to phone foreign central banks is an absurd operational failure."
        ]
    },
    key_insight="Propagate business condition failures across agents as structured error objects with actionable context and retry boundaries."
))

# Q22 (Target: B = 1)
questions.append(create_question(
    qid=22,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="Built-in Tools",
    module="Domain 2 (Defense Edit Tool Unique Anchor Text)",
    scenario="A military software agent needs to update a security classification banner string across an existing 600-line operational script. The line `CLASSIFICATION=SECRET` appears once, but similar configuration keys appear throughout. How should Claude format the `old_string` in the `Edit` tool?",
    options=[
        "Supply only the single word SECRET and allow stochastic sampling to resolve the matching line.",
        "Include unique surrounding anchor lines to guarantee an exact, unambiguous single match.",
        "Execute a Bash sed command with force flags to overwrite all occurrences across the filesystem.",
        "Delete the entire 600-line file using Write and rewrite it completely from model memory."
    ],
    correct_idx=1,
    rationales={
        "correct": "The `Edit` tool requires `old_string` to match uniquely within the file. Including 1-2 lines of unique surrounding context as anchor text ensures an unambiguous match, preventing edit failures or accidental replacements in wrong sections.",
        "distractors": [
            "Supplying a single common word like 'SECRET' fails because Edit requires a unique match in the file.",
            "Executing sed via Bash bypasses safety mechanisms and risks corrupting other configuration lines.",
            "Rewriting 600 lines from memory with Write risks severe truncation, hallucination, and syntax errors."
        ]
    },
    key_insight="Provide unique surrounding context as anchor lines in the Edit tool to guarantee an exact, unambiguous match."
))

# Q23 (Target: C = 2)
questions.append(create_question(
    qid=23,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="MCP Resources vs Tools",
    module="Domain 2 (Agricultural MCP Almanac Resource)",
    scenario="An agricultural advisory agent needs continuous access to an 8,000-line historical regional rainfall and crop calendar almanac that updates once per year. Rather than creating an active tool that queries a database on every turn, what MCP feature should be used?",
    options=[
        "Execute a curl command on every single user turn to download the almanac from a public web server.",
        "Embed the entire 8,000-line almanac directly inside the system prompt of every single API turn.",
        "Expose the almanac as an MCP Resource, providing structured read-only context to Claude.",
        "Configure an active MCP tool that writes almanac lines one by one into local text scratchpads."
    ],
    correct_idx=2,
    rationales={
        "correct": "MCP Resources are designed specifically to expose static or semi-static reference data, documentation, and almanacs directly to Claude without tool execution overhead or embedding thousands of lines into system prompts.",
        "distractors": [
            "Running curl on every turn introduces severe latency, network fragility, and bandwidth waste.",
            "Embedding 8,000 lines in every system prompt rapidly exhausts prompt token budgets and balloons costs.",
            "Writing lines one by one via tool calls is extraordinarily slow and inefficient."
        ]
    },
    key_insight="Use MCP Resources to expose read-only reference data and documentation directly to Claude without tool execution overhead."
))

# Q24 (Target: D = 3)
questions.append(create_question(
    qid=24,
    domain_id=2,
    domain_name="Tool Design & MCP Integration",
    sub_skill="Tool Interface Design",
    module="Domain 2 (Telecom Prompt vs Description Conflict)",
    scenario="A telecommunications agent has an MCP tool `run_optical_reflectometry` with an exhaustive description. However, the system prompt contains an older instruction: 'Always use basic_ping for all network diagnostics.' In production, Claude never calls the optical tool. What is the root cause?",
    options=[
        "Optical reflectometry tools can only be invoked when running on Apple Silicon workstations.",
        "The Claude Messages API disables diagnostic tools whenever ping tools are declared in schemas.",
        "The tool description was written in Markdown instead of valid JSON Schema attribute syntax.",
        "A categorical directive in the system prompt directly contradicts and overrides the tool description."
    ],
    correct_idx=3,
    rationales={
        "correct": "System prompt directives carry immense authority. When a system prompt includes rigid categorical commands ('Always use basic_ping for all diagnostics'), it overrides tool descriptions. System prompts must be audited and updated when new tools are deployed.",
        "distractors": [
            "Diagnostic tools run over standard network APIs and have no Apple Silicon hardware requirement.",
            "The Messages API supports having multiple diagnostic tools available simultaneously.",
            "Tool descriptions are standard text strings and legitimately support Markdown formatting."
        ]
    },
    key_insight="Audit system prompts when deploying new tools. Rigid categorical prompt directives can inadvertently override tool descriptions."
))

# ─── DOMAIN 3: Claude Code Configuration & Workflows (Q25 - Q35) ─────────────

# Q25 (Target: A = 0)
questions.append(create_question(
    qid=25,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="Plan Mode vs Direct Execution",
    module="Domain 3 (Aerospace Avionics Plan Mode)",
    scenario="An aerospace team refactors an avionics flight control software package across 60 interdependent C++ modules. Why should the lead software architect mandate Plan Mode before code modifications begin?",
    options=[
        "Plan Mode enforces read-only discovery, preventing chaotic partial edits across 60 critical modules.",
        "Plan Mode automatically writes unit tests and deploys code directly to flight test aircraft.",
        "Plan Mode enables faster GPU hardware acceleration on the Anthropic cloud cluster.",
        "Plan Mode bypasses all local compiler errors by disabling C++ strict typing checks."
    ],
    correct_idx=0,
    rationales={
        "correct": "Plan Mode (`permission_mode='plan'`) blocks destructive edits and commands, forcing Claude to analyze dependencies, design interfaces, and produce an approved implementation plan before touching 60 safety-critical modules.",
        "distractors": [
            "Plan Mode generates architectural plans; it does not deploy code to flight test aircraft.",
            "Plan Mode changes permission levels, not backend cloud GPU hardware allocation.",
            "Plan Mode has zero connection to compiler typing checks or C++ language semantics."
        ]
    },
    key_insight="Use Plan Mode on large, complex refactors (60 modules) to map architecture and get approval before executing changes."
))

# Q26 (Target: B = 1)
questions.append(create_question(
    qid=26,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="CLAUDE.md Hierarchy",
    module="Domain 3 (Banking SOX Compliance CLAUDE.md)",
    scenario="A banking software group authors Sarbanes-Oxley (SOX) audit logging standards for all backend financial microservices. Where must these instructions be placed so all developers automatically inherit them upon cloning the repository?",
    options=[
        "In each developer's personal home folder configuration file at ~/.claude/CLAUDE.md.",
        "In the repository root configuration file at .claude/CLAUDE.md, committed to git.",
        "In an inline comment block at the top of the repository package-lock.json file.",
        "In an external cloud object storage bucket referenced by an HTTP header variable."
    ],
    correct_idx=1,
    rationales={
        "correct": "Project-level instructions committed to `.claude/CLAUDE.md` in the repository root are automatically shared with all developers who clone the repository, ensuring uniform team-wide compliance standards.",
        "distractors": [
            "Instructions in `~/.claude/CLAUDE.md` remain local to individual laptops and are not shared via git.",
            "`package-lock.json` is a machine-generated package manifest that Claude Code does not parse for instructions.",
            "External cloud buckets require custom manual developer setup and are not part of Claude Code's native discovery tree."
        ]
    },
    key_insight="Commit team-wide standards to `.claude/CLAUDE.md` in the repository root so all developers automatically inherit them."
))

# Q27 (Target: C = 2)
questions.append(create_question(
    qid=27,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="Skills Architecture",
    module="Domain 3 (Smart City Infrastructure Capacity Skill)",
    scenario="A smart city engineer authors a specialized skill `.claude/skills/capacity/SKILL.md` to run complex traffic flow simulations. Generating the simulation creates 200 verbose calculation logs. Why should the frontmatter specify `context: fork`?",
    options=[
        "It forces the municipal traffic controller to apply timing changes to city lights immediately.",
        "It automatically encrypts the local database connection string using AES-256.",
        "It isolates verbose simulation exploration tokens from polluting the main conversation.",
        "It allows the subagent to run on remote GPU clusters without local CPU consumption."
    ],
    correct_idx=2,
    rationales={
        "correct": "Setting `context: fork` runs the skill in an isolated subagent session. Intermediate scratchpad outputs, execution logs, and verbose simulation turns remain in the sub-session, returning only the final synthesized capacity recommendations to the main conversation.",
        "distractors": [
            "`context: fork` isolates conversation context; it does not apply timing changes to physical traffic lights.",
            "Context forking has no connection to connection string encryption.",
            "Subagents run in the same local execution environment, not on remote GPU clusters."
        ]
    },
    key_insight="Use `context: fork` in SKILL.md frontmatter to prevent intermediate verbose exploration logs from cluttering the main conversation."
))

# Q28 (Multi-select: Target: A = 0 and D = 3)
questions.append(create_question(
    qid=28,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="SDK setting_sources Parameter",
    module="Domain 3 (Defense Air-Gapped Hermetic CI)",
    scenario="A defense agency runs automated security vulnerability verification on mission-critical guidance firmware using the Claude Agent SDK in a classified, air-gapped environment. Which TWO configurations ensure that the agent executes in a strictly hermetic environment without loading unauthorized host files? (Select TWO)",
    options=[
        "Set setting_sources=[] in ClaudeAgentOptions to ignore all host filesystem settings.",
        "Set setting_sources=['user', 'project', 'local'] to load all security configurations.",
        "Delete all source code files from the local filesystem before initiating the test run.",
        "Explicitly pass all allowed_tools and system prompts directly in code parameters."
    ],
    correct_idx=[0, 3],
    is_multi=True,
    rationales={
        "correct": "Options A and D are correct. Setting `setting_sources=[]` in `ClaudeAgentOptions` disables all filesystem configuration discovery (ignoring `~/.claude.json`, project `CLAUDE.md`, and local hooks). In this hermetic mode, all tools, prompts, and permissions must be supplied explicitly in code parameters.",
        "distractors": [
            "`setting_sources=['user', 'project', 'local']` loads host settings, which violates air-gapped hermetic requirements.",
            "Deleting source code files destroys the software under test."
        ]
    },
    key_insight="Pass `setting_sources=[]` and provide all configuration parameters explicitly in code to run in hermetic mode."
))

# Q29 (Target: B = 1)
questions.append(create_question(
    qid=29,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="CI/CD Integration",
    module="Domain 3 (Agricultural Crop Yield CI/CD)",
    scenario="An agricultural technology startup integrates Claude Code into GitHub Actions to generate daily automated crop yield forecasting summaries. Which CLI command runs non-interactively and emits typed JSON for downstream dashboard ingestion?",
    options=[
        "claude --interactive --scan-crops-daily --export-to-xml-file=crops.xml",
        "claude -p 'Yield report' --output-format json --json-schema ./schema.json",
        "claude --headless --daemon --background --force-zero-defect-guarantee",
        "cat farm_data.txt | claude --stdin-only --output-unstructured-markdown"
    ],
    correct_idx=1,
    rationales={
        "correct": "Non-interactive automation in CI requires `-p` (or `--print`) to prevent terminal deadlocks, paired with `--output-format json` and `--json-schema` to emit typed, schema-validated JSON for downstream dashboard ingestion.",
        "distractors": [
            "`--interactive` causes the CI runner to hang waiting for keyboard input, and XML is not JSON.",
            "`--headless`, `--daemon`, and `--force-zero-defect-guarantee` are fabricated CLI flags that do not exist.",
            "Unstructured markdown prose cannot be parsed reliably by automated dashboard ingestion scripts."
        ]
    },
    key_insight="Combine `-p` with `--output-format json` and `--json-schema` to run non-interactive, machine-verifiable CI/CD jobs."
))

# Q30 (Target: C = 2)
questions.append(create_question(
    qid=30,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="Path-Specific Rules",
    module="Domain 3 (Telecom Network Config Path Rules)",
    scenario="A telecommunications network repository contains 40 router configuration files located in `configs/routers/**/*.conf`. The engineering team wants strict BGP routing validation guidelines to apply whenever Claude edits these files. What is the optimal configuration?",
    options=[
        "Duplicate identical copies of CLAUDE.md into all 40 router subdirectories.",
        "Add all BGP guidelines to the global user configuration file located at ~/.claude/CLAUDE.md.",
        "Create .claude/rules/bgp.md with YAML frontmatter paths: ['configs/routers/**/*.conf'].",
        "Instruct developers to verbally recite BGP guidelines into their laptop microphones on every turn."
    ],
    correct_idx=2,
    rationales={
        "correct": "Creating `.claude/rules/bgp.md` with YAML frontmatter `paths: ['configs/routers/**/*.conf']` ensures that BGP validation rules load dynamically ONLY when matching configuration files are accessed, avoiding 40 duplicate files and saving tokens.",
        "distractors": [
            "Duplicating 40 identical CLAUDE.md files creates an unmaintainable configuration nightmare.",
            "User-level `~/.claude/CLAUDE.md` is personal to one machine and will not be shared with team members.",
            "Verbal microphone recitation is an unworkable operational workflow."
        ]
    },
    key_insight="Use path-specific rules (`.claude/rules/*.md`) with glob patterns to apply guidelines dynamically across distributed router configuration files."
))

# Q31 (Target: D = 3)
questions.append(create_question(
    qid=31,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="CI/CD Integration",
    module="Domain 3 (Banking Deduplication Across CI Runs)",
    scenario="In an automated banking CI review pipeline, developers frequently push incremental commits to open pull requests. If the review agent reviews the entire PR from scratch on every commit, it repeatedly posts duplicate comments for existing issues. How should the pipeline deduplicate findings?",
    options=[
        "Delete all existing review comments on the pull request before running every single commit check.",
        "Configure git to rebase and squash all developer commits into a single commit before running CI.",
        "Restrict CI code reviews strictly to the final merge commit immediately prior to production deploy.",
        "Inject prior review findings into the prompt with instructions to report ONLY new or unresolved issues."
    ],
    correct_idx=3,
    rationales={
        "correct": "The established architectural pattern for multi-commit PR reviews is injecting prior review findings into the prompt context and explicitly instructing the model: 'Review the latest commit. Report ONLY new issues or verify fixes for previously flagged issues; do not re-report unaddressed known issues.'",
        "distractors": [
            "Deleting existing comments destroys discussion threads, resolution history, and developer notes.",
            "Squashing commits during active development breaks developer workflows and history.",
            "Deferring all reviews until immediately prior to deployment prevents catching errors early during development."
        ]
    },
    key_insight="Prevent duplicate review comments in CI by injecting previous review findings and instructing the agent to report only new or newly resolved issues."
))

# Q32 (Target: A = 0)
questions.append(create_question(
    qid=32,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="Codebase Exploration Subagents",
    module="Domain 3 (Aerospace Avionics Explore Subagent)",
    scenario="An aerospace engineer asks Claude Code: 'How does the primary flight display receive angle-of-attack telemetry across our 400 modules?' Why does Claude Code deploy an Explore subagent to investigate this question?",
    options=[
        "Running exploration in a separate context keeps verbose file search tokens out of the main conversation.",
        "The primary agent lacks read permissions for files located outside the immediate working directory.",
        "The Messages API enforces an account-level cap of three tool executions per primary conversation thread.",
        "Explore subagents execute on dedicated remote supercomputers optimized for graph traversal."
    ],
    correct_idx=0,
    rationales={
        "correct": "Broad codebase exploration generates hundreds of file reads, grep matches, and directory trees. Deploying an Explore subagent isolates this noisy discovery in a disposable sub-context, returning only a synthesized summary to the main conversation and conserving context tokens.",
        "distractors": [
            "The main agent has full workspace read permissions; isolation is for context hygiene, not OS security.",
            "The Messages API supports arbitrarily long multi-turn tool loops, not capped at three turns.",
            "Subagents run within the same execution environment, not on separate remote supercomputers."
        ]
    },
    key_insight="Explore subagents run noisy codebase discovery in an isolated context, returning condensed findings to preserve the main context window."
))

# Q33 (Target: B = 1)
questions.append(create_question(
    qid=33,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="Path-Specific Rules",
    module="Domain 3 (Smart City Path Rules Token Optimization)",
    scenario="A smart city repository contains 30 municipal domain folders. Guidelines for traffic controller firmware only load when files in `traffic/firmware/**` are actively read or edited. What is the primary benefit of this design?",
    options=[
        "It eliminates the requirement to write typed JSON schema definitions for custom tool calls.",
        "It conserves context tokens by avoiding loading irrelevant traffic rules during water or power edits.",
        "It automatically decreases input and output token consumption through specialized compression.",
        "It guarantees strict determinism for all LLM reasoning steps across multiple turns."
    ],
    correct_idx=1,
    rationales={
        "correct": "Path-specific rules load dynamically into context ONLY when matching files are accessed. When developers edit water management or power grid modules, traffic firmware rules remain unloaded, conserving valuable context budget and eliminating distraction.",
        "distractors": [
            "Path rules provide prompt guidelines; they do not eliminate the need for typed tool schemas.",
            "Path rules do not compress token payloads; they simply load conditionally.",
            "LLM sampling remains non-deterministic regardless of how rules files are loaded."
        ]
    },
    key_insight="Path-specific rules conserve tokens by loading dynamically into context ONLY when files matching their glob pattern are actively touched."
))

# Q34 (Target: C = 2)
questions.append(create_question(
    qid=34,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="Custom Slash Commands & Skills",
    module="Domain 3 (Defense Security Briefing Slash Command)",
    scenario="A military cyber defense lead creates a slash command `/threat-brief` that formats incident data into a standard military SITREP template. Where must the command file be placed so that all analysts on the team can run it in Claude Code?",
    options=[
        "In the lead's personal laptop folder at ~/.claude/commands/threat-brief.md.",
        "Inside an external public GitHub repository configured as a git submodule.",
        "In the repository directory at .claude/commands/threat-brief.md, committed to git.",
        "In an inline markdown code block within the project root CLAUDE.md file."
    ],
    correct_idx=2,
    rationales={
        "correct": "Custom slash commands placed in `.claude/commands/<command>.md` within the repository root are tracked in git and shared with all team members cloning the repository, ensuring uniform team-wide command availability.",
        "distractors": [
            "Placing it in `~/.claude/commands/` makes it personal to a single laptop, unshared with team members.",
            "Git submodules add unnecessary configuration overhead for simple markdown commands.",
            "CLAUDE.md defines system instructions, not individual slash command scripts."
        ]
    },
    key_insight="Share project slash commands by placing them in `.claude/commands/` in the repository root."
))

# Q35 (Target: D = 3)
questions.append(create_question(
    qid=35,
    domain_id=3,
    domain_name="Claude Code Configuration & Workflows",
    sub_skill="Iterative Refinement",
    module="Domain 3 (Agricultural Soil Pipeline Test Failures)",
    scenario="Claude Code generates a soil nitrogen leaching calculation pipeline, but two automated PyTest tests fail due to an unhandled zero-division edge case in dry soils. What is the most effective prompt to guide Claude to a fix?",
    options=[
        "Tell Claude that its soil math is broken and demand that it rewrite the entire file from memory.",
        "Delete the zero-division test case and assume dry soils will never occur in commercial agriculture.",
        "Increase the model sampling temperature to 0.95 to encourage creative mathematical solutions.",
        "Provide the exact failing test names, PyTest assertion logs, and the zero-moisture input payload."
    ],
    correct_idx=3,
    rationales={
        "correct": "In test-driven iteration, feeding exact failing test names, PyTest assertion failure logs, and input payloads provides unambiguous, objective feedback, allowing Claude to trace the root cause and apply a surgical zero-division check.",
        "distractors": [
            "Vague complaints ('your math is broken') force the model to guess which edge case failed.",
            "Deleting tests to make broken code pass destroys scientific integrity and guarantees production failures.",
            "Increasing temperature increases randomness, worsening mathematical errors."
        ]
    },
    key_insight="Feed exact failing assertion traces and input payloads back to Claude to guide targeted, reliable bug fixes."
))

# ─── DOMAIN 4: Prompt Engineering & Structured Output (Q36 - Q45) ────────────

# Q36 (Target: A = 0)
questions.append(create_question(
    qid=36,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Structured Output with tool_use",
    module="Domain 4 (Defense Redacted Documents Nullable Fields)",
    scenario="A military intelligence intelligence extraction pipeline parses classified documents where intelligence officer identities and mission dates are frequently redacted with black marker bars. How should the `officer_name` and `mission_date` properties be declared in the extraction JSON Schema?",
    options=[
        "Declare the properties as nullable (e.g. type: ['string', 'null']) and instruct Claude to return null if redacted.",
        "Mark the properties as required strings and instruct Claude in the prompt to guess plausible identities.",
        "Configure the schema to reject any document where an officer name or mission date is redacted.",
        "Instruct Claude to calculate synthetic dates by hashing the document classification level."
    ],
    correct_idx=0,
    rationales={
        "correct": "When physical or classified documents contain redactions, declaring fields as nullable (`type: ['string', 'null']`) allows Claude to output `null` when text is blacked out. Marking fields as required forces the model to either fail validation or fabricate plausible synthetic identities.",
        "distractors": [
            "Instructing the model to guess redacted officer identities fabricates false intelligence.",
            "Rejecting redacted documents causes pipeline failure on legitimate intelligence files.",
            "Hashing classification levels creates arbitrary synthetic dates that corrupt intelligence timelines."
        ]
    },
    key_insight="Declare redacted or missing fields as nullable in JSON schemas to prevent hallucinated data."
))

# Q37 (Target: B = 1)
questions.append(create_question(
    qid=37,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Structured Output with tool_use",
    module="Domain 4 (Banking Self-Auditing Transaction Reconciliation)",
    scenario="A banking transaction reconciliation agent parses bank ledger statements containing debits, credits, and stated ending balances. How should the extraction schema be structured to detect accounting discrepancies before ledger posting?",
    options=[
        "Strip all individual debit and credit line items and output only the stated ending balance.",
        "Include calculated_balance, stated_balance, and a boolean discrepancy_detected flag in the schema.",
        "Rely on the client-side user interface to silently modify ledger balances to match stated totals.",
        "Instruct Claude to mentally balance the ledger without outputting intermediate numbers."
    ],
    correct_idx=1,
    rationales={
        "correct": "A self-auditing schema includes fields for calculated balance (`calculated_balance`), stated balance (`stated_balance`), and a boolean flag (`discrepancy_detected`). This forces the model to calculate and compare values, catching discrepancies immediately.",
        "distractors": [
            "Stripping line items destroys granular accounting audit trails required for banking reconciliation.",
            "Silently rewriting balances conceals fraudulent or missing debit line items.",
            "Asking Claude to 'mentally balance' provides zero structured telemetry or verifiable audit records."
        ]
    },
    key_insight="Design self-auditing schemas with separate calculated and stated fields plus conflict flags to expose arithmetic discrepancies immediately."
))

# Q38 (Target: C = 2)
questions.append(create_question(
    qid=38,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Few-Shot Prompting",
    module="Domain 4 (Aerospace Change Severity Reasoning Chains)",
    scenario="An aerospace engineering assistant classifies engineering change proposals (ECPs) into Class I (major aerodynamic or propulsion impact requiring FAA sign-off) and Class II (minor cosmetic bracket modifications). The model struggles with borderline avionics bracket modifications that carry vibration dampening implications. How should few-shot prompting be designed?",
    options=[
        "Provide fifty raw change proposal text snippets with one-word labels, omitting all rationale.",
        "Add an urgent uppercase prompt warning that misclassifying an ECP will result in FAA fines.",
        "Provide 3-4 diverse examples with reasoning chains explaining why vibration brackets were Class I.",
        "Remove all few-shot examples and rely entirely on zero-shot inference with temperature 1.0."
    ],
    correct_idx=2,
    rationales={
        "correct": "Providing 3-4 diverse few-shot examples with explicit step-by-step reasoning chains teaches the model how to evaluate borderline trade-offs (e.g. explaining that a bracket modification is Class I if it impacts flight vibration harmonics). This fosters genuine reasoning.",
        "distractors": [
            "Raw input-label pairs without reasoning provide zero insight into why subtle borderline decisions were made.",
            "Threatening regulatory fines in prompts adds emotional noise without providing technical classification criteria.",
            "Zero-shot prompting with high temperature increases randomness and worsens engineering misclassifications."
        ]
    },
    key_insight="Include explicit reasoning chains in few-shot examples to teach models how to evaluate borderline engineering classifications."
))

# Q39 (Target: D = 3)
questions.append(create_question(
    qid=39,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Structured Output with tool_use",
    module="Domain 4 (Smart City Physical Traffic Feasibility)",
    scenario="A smart city traffic optimization pipeline extracts predicted vehicle flow volumes from urban sensors using Claude's tool_use feature with a validated JSON Schema. What guarantee does JSON Schema enforcement provide regarding traffic feasibility?",
    options=[
        "It guarantees that all predicted vehicle speeds comply with municipal speed limits.",
        "It guarantees that predicted vehicle volumes are physically possible on narrow urban streets.",
        "It guarantees that all sensor data was collected from verified municipal traffic cameras.",
        "It guarantees output conforms to the declared schema, but not that traffic predictions are feasible."
    ],
    correct_idx=3,
    rationales={
        "correct": "`tool_use` with JSON Schema guarantees 100% syntactically valid JSON matching declared data types (e.g. integers, floats). It provides ZERO guarantees regarding physical feasibility, real-world validity, or aerodynamic/traffic laws, which must be validated by downstream physics engines.",
        "distractors": [
            "JSON schemas validate data structure, not adherence to municipal traffic laws.",
            "JSON schemas do not enforce physical spatial constraints or roadway throughput limits.",
            "Schemas validate JSON payloads, not the physical authenticity of traffic camera hardware."
        ]
    },
    key_insight="tool_use guarantees structural schema conformity, but does NOT guarantee physical real-world feasibility or factual accuracy."
))

# Q40 (Target: A = 0)
questions.append(create_question(
    qid=40,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Batch Processing",
    module="Domain 4 (Agricultural Overnight Field Reports 50% Discount)",
    scenario="An agricultural technology platform processes 50,000 satellite field vegetation health reports every Saturday night to prepare weekly farmer advisory emails delivered on Monday morning. What API feature should be used to minimize costs?",
    options=[
        "Use the Message Batches API to capture a 50% discount across all token categories.",
        "Use the synchronous Messages API with 100 concurrent threads executing in parallel.",
        "Open 500 persistent WebSocket streaming connections from a cloud Kubernetes cluster.",
        "Deploy a self-hosted open-source language model on 20 on-premise GPU server racks."
    ],
    correct_idx=0,
    rationales={
        "correct": "The Message Batches API is designed specifically for high-volume, non-interactive, latency-tolerant workloads with a 24-hour turnaround SLA. It provides a 50% discount across all token categories (input, output, caching), saving thousands of dollars on large weekend batch jobs.",
        "distractors": [
            "The synchronous Messages API costs twice as much as the Batch API and is unnecessary for weekend batch jobs.",
            "WebSockets are for real-time bidirectional streaming, not high-volume weekend batch jobs.",
            "Self-hosting GPU racks incurs enormous hardware, power, and maintenance costs compared to serverless Batches."
        ]
    },
    key_insight="Use the Message Batches API for high-volume, latency-tolerant workloads to capture the 50% cost discount."
))

# Q41 (Target: B = 1)
questions.append(create_question(
    qid=41,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Validation-Retry Loops",
    module="Domain 4 (Telecom Packet Count Retry Boundary)",
    scenario="A telecommunications network diagnostic pipeline includes an automated validation-retry loop. For which of the following discrepancies is a validation-retry loop effective, and for which is it futile?",
    options=[
        "Effective when customer billing addresses are missing; futile when packet counts fail to sum.",
        "Effective when extracted packet counts do not sum to total; futile when route history is omitted.",
        "Effective for detecting fiber cable physical cuts; futile for fixing corrupted date strings.",
        "Effective for predicting future solar flares; futile for calculating network interface bandwidth."
    ],
    correct_idx=1,
    rationales={
        "correct": "Validation-retry loops work well when information is present in the source data and can be recalculated or reformatted (such as packet counts summing). Retries are completely futile when information is genuinely absent from the source data (such as omitted routing history); retrying absent data forces hallucinations.",
        "distractors": [
            "Missing billing addresses cannot be recovered by retrying if absent; arithmetic sum errors are easily fixed.",
            "Physical fiber cuts require physical hardware repair; date formatting errors are easily fixed by retry.",
            "LLMs cannot predict solar flares, but bandwidth arithmetic is straightforward."
        ]
    },
    key_insight="Validation-retry loops are effective for arithmetic and formatting errors where data exists, but futile when data is absent from source."
))

# Q42 (Target: C = 2)
questions.append(create_question(
    qid=42,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Explicit Criteria",
    module="Domain 4 (Banking Categorical AML Rules)",
    scenario="A banking anti-money laundering (AML) prompt instructs Claude: 'Flag all suspicious or unusual financial activity.' In production, the bot flags routine payroll deposits and misses structured sub-$10,000 deposits. How should the prompt be restructured?",
    options=[
        "Instruct the model to apologize to bank customers in every AML flag notification.",
        "Add uppercase warning text: 'FLAG VERY STRICT SUSPICIOUS ACTIVITY UNDER FEDERAL LAW!'",
        "Define explicit categorical rules specifying exact structuring patterns and high-risk jurisdictions.",
        "Increase temperature to 0.8 to make suspicious activity detection more creative and holistic."
    ],
    correct_idx=2,
    rationales={
        "correct": "Vague directives ('flag suspicious activity') produce erratic, noisy results. Replacing vague directives with explicit categorical rules (e.g. 'Flag rapid successive cash deposits just below $10,000 within 48 hours; do NOT flag scheduled recurring payroll deposits') eliminates ambiguity and aligns model behavior with regulatory standards.",
        "distractors": [
            "Apologetic messages do not fix false-positive alerts on legitimate payroll deposits.",
            "Uppercase warnings add emotional noise without defining what constitutes structuring.",
            "Higher temperature increases variance and worsens inconsistent transaction flagging."
        ]
    },
    key_insight="Replace vague directives like 'flag suspicious activity' with explicit categorical rules defining exact patterns to flag."
))

# Q43 (Target: D = 3)
questions.append(create_question(
    qid=43,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Multi-Instance Review",
    module="Domain 4 (Aerospace Multi-Instance Safety Review)",
    scenario="An AI system generates automated flight software patch proposals. Why must the safety and compliance review of these patches run in an independent, fresh Claude instance rather than continuing the generation conversation?",
    options=[
        "The FAA mandates that all AI review software run on distinct physical cloud server racks.",
        "The Claude tokenizer requires re-initializing memory registers after generating C++ code.",
        "The Messages API enforces an account-level quota of one code review per calendar day.",
        "An independent session eliminates self-confirmation bias, evaluating code with fresh scrutiny."
    ],
    correct_idx=3,
    rationales={
        "correct": "When an agent reviews code it generated within the same conversation thread, it carries internal confirmation bias, rationalizing its earlier reasoning. Running evaluation in an independent, fresh Claude instance ensures an objective, unbiased safety audit.",
        "distractors": [
            "FAA software standards are architecture-agnostic and do not mandate distinct server racks.",
            "Tokenizers are stateless algorithms that do not require re-initializing memory registers.",
            "There is no daily one-review quota on the Messages API."
        ]
    },
    key_insight="Always conduct safety and compliance reviews in a fresh, independent session to eliminate confirmation bias."
))

# Q44 (Target: A = 0)
questions.append(create_question(
    qid=44,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Batch Processing",
    module="Domain 4 (Smart City Real-Time Traffic Light Sync API)",
    scenario="A smart city municipality operates an adaptive traffic light system that adjusts green-light timings every 30 seconds based on incoming intersection camera feeds. Why must this system use the synchronous Messages API rather than the Message Batches API?",
    options=[
        "Adaptive traffic light control is a blocking real-time workflow requiring sub-second decisions.",
        "The Message Batches API is prohibited from processing traffic camera images by federal law.",
        "The Message Batches API automatically deletes municipal database tables after processing.",
        "Adaptive traffic lights require real-time GPU audio rendering that the Batch API lacks."
    ],
    correct_idx=0,
    rationales={
        "correct": "Adaptive traffic light timing is a real-time, blocking control loop: decisions must be made in seconds to prevent vehicular gridlock. The Message Batches API has a turnaround window of up to 24 hours and offers zero latency SLA, making it completely unsuited for real-time control.",
        "distractors": [
            "There is no federal law prohibiting batch processing of traffic images.",
            "The Batch API processes text payloads and never touches or deletes municipal database tables.",
            "Traffic light control does not involve GPU audio rendering."
        ]
    },
    key_insight="Never route real-time, blocking control loops to the Message Batches API. Use the synchronous Messages API."
))

# Q45 (Target: B = 1)
questions.append(create_question(
    qid=45,
    domain_id=4,
    domain_name="Prompt Engineering & Structured Output",
    sub_skill="Human Review & Confidence Calibration",
    module="Domain 4 (Defense Confidence Routing against Ground Truth)",
    scenario="A military intelligence translation pipeline processes foreign language radio intercepts. To maintain 99.9% translation fidelity while automating routine military logistics chatter, how should cases be routed to human intelligence linguists?",
    options=[
        "Route all intercepts to human linguists on Mondays and automate processing on weekends.",
        "Calibrate model field-level confidence against ground-truth validation sets; route low-confidence fields.",
        "Rely on the model's self-reported confidence score of 1-10 to route cases below an 8 threshold.",
        "Automate 100% of intercepts and accept that 5% of intelligence summaries will contain errors."
    ],
    correct_idx=1,
    rationales={
        "correct": "Effective human-in-the-loop routing requires calibrating model field-level confidence against empirical ground-truth validation sets. When empirical confidence falls below the required threshold for specific critical terms (e.g. coordinates, call signs), only those borderline segments are routed to human linguists.",
        "distractors": [
            "Day-of-week routing is arbitrary and has no correlation with intelligence translation accuracy or risk.",
            "LLM self-reported confidence scores (1-10) are notoriously poorly calibrated and unreliable.",
            "Accepting 5% false intelligence on military tactical chatter creates catastrophic national security risk."
        ]
    },
    key_insight="Calibrate model confidence against empirical ground-truth validation sets before routing low-confidence cases to human review."
))

# ─── DOMAIN 5: Context Management & Reliability (Q46 - Q53) ───────────────────

# Q46 (Target: C = 2)
questions.append(create_question(
    qid=46,
    domain_id=5,
    domain_name="Context Management & Reliability",
    sub_skill="Context Preservation",
    module="Domain 5 (Banking SWIFT Codes in Case Facts)",
    scenario="A corporate banking assistant conducts a 12-turn international wire transfer setup. In turn 2, the customer provides an 11-character SWIFT bank identifier code (`DEUTDEDDFXX`) and an account number. By turn 10, progressive conversational summarization compresses this to 'the customer provided their German bank details', causing the wire execution tool to fail. How should this be prevented?",
    options=[
        "Instruct the customer to re-enter their 11-character SWIFT code in every chat message.",
        "Increase the max_tokens output parameter of the summarization model to 8,192.",
        "Maintain a persistent Case Facts block containing verified SWIFT codes that bypasses summarizers.",
        "Store the SWIFT code in a public pastebin URL referenced in the prompt header."
    ],
    correct_idx=2,
    rationales={
        "correct": "Exact transactional identifiers (SWIFT codes, IBANs, wire amounts, dates) must be stored in a persistent 'Case Facts' block that is injected verbatim into every turn and NEVER passed through summarizers, preventing destructive compression.",
        "distractors": [
            "Forcing customers to repeatedly paste SWIFT codes in every message causes extreme friction and errors.",
            "Increasing summarization max_tokens does not prevent the model from abstracting specific strings into prose summaries.",
            "Storing private banking codes in public pastebins is a severe financial security violation."
        ]
    },
    key_insight="Pin exact transactional identifiers (SWIFT codes, account numbers, amounts) in a persistent Case Facts block that completely bypasses summarizers."
))

# Q47 (Target: D = 3)
questions.append(create_question(
    qid=47,
    domain_id=5,
    domain_name="Context Management & Reliability",
    sub_skill="Escalation & Ambiguity Resolution",
    module="Domain 5 (Defense Multiple Matching Personnel Records)",
    scenario="A military command assistant queries the defense personnel directory for 'Captain Miller'. The database returns three active officers matching that name with different service numbers and security clearance levels. What must the assistant do?",
    options=[
        "Select the Captain Miller with the highest security clearance using an authority heuristic.",
        "Select the Captain Miller with the most recent deployment date using a timestamp heuristic.",
        "Randomly select one record and transmit classified operational orders to that officer.",
        "Prompt the user for additional identifying details (e.g. service number or unit) to disambiguate."
    ],
    correct_idx=3,
    rationales={
        "correct": "In military and enterprise systems, using heuristics (highest rank, most recent, clearance level) on ambiguous database matches risks modifying the wrong personnel record or leaking classified data. The agent must pause and ask for clarifying identifiers (service number or unit).",
        "distractors": [
            "Selecting by clearance level is an arbitrary heuristic that risks leaking orders to the wrong officer.",
            "Timestamp heuristics are arbitrary and risk transmitting operational orders to the wrong unit.",
            "Random selection on military personnel records constitutes gross operational negligence."
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
    module="Domain 5 (Aerospace Thermal Analysis Partial Failure)",
    scenario="An aerospace engineering coordinator orchestrates four subagents to evaluate a spacecraft heat shield: aerodynamics, structural stress, thermal dissipation, and material fatigue. The thermal subagent fails due to an external simulation server outage. How should the coordinator finalize the report?",
    options=[
        "Synthesize aerodynamics, stress, and fatigue findings, explicitly annotating that thermal data was offline.",
        "Abort the entire spacecraft evaluation and delete all aerodynamics and structural stress findings.",
        "Invent simulated thermal dissipation numbers using statistical averages to ensure zero blank sections.",
        "Freeze the coordinator execution process until the thermal simulation server hardware is repaired."
    ],
    correct_idx=0,
    rationales={
        "correct": "In multi-agent orchestration, partial failure of an optional subagent must not abort the entire mission. The coordinator synthesizes the successful data streams and explicitly annotates the missing segment ('Thermal data unavailable due to simulation server outage'), preserving transparency.",
        "distractors": [
            "Aborting the investigation deletes critical engineering evidence and delays launch schedules.",
            "Inventing simulated thermal data in spacecraft heat shield engineering risks catastrophic loss of vehicle and crew.",
            "Freezing the process during an active launch review wastes engineering hours and locks system resources."
        ]
    },
    key_insight="Deliver available multi-agent findings transparently: synthesize successful data streams and annotate unavailable sections."
))

# Q49 (Target: B = 1)
questions.append(create_question(
    qid=49,
    domain_id=5,
    domain_name="Context Management & Reliability",
    sub_skill="Context Degradation & Codebase Exploration",
    module="Domain 5 (Smart City 6-Hour Session Degradation)",
    scenario="A municipal traffic engineer conducts an extended 6-hour interactive planning session in Claude Code, loading city-wide sensor telemetry and running multiple urban flow simulations. Over time, Claude's suggestions become generic, and it repeatedly forgets intersection constraints established in hour one. How should this be mitigated?",
    options=[
        "Re-read all 6 hours of raw sensor telemetry on every single turn to refresh model memory.",
        "Use /compact to summarize conversation history, or record confirmed constraints in external scratchpads.",
        "Instruct the municipal engineer to complete all city traffic planning in less than fifteen minutes.",
        "Switch the model to a legacy snapshot that does not experience context saturation."
    ],
    correct_idx=1,
    rationales={
        "correct": "Extended interactive sessions accumulate massive context from verbose tool outputs, causing mathematical attention dilution. Offloading confirmed findings to an external scratchpad file or using `/compact` to compress history restores focus.",
        "distractors": [
            "Re-reading all 6 hours of telemetry exacerbates token bloat and triggers context window overflow.",
            "Complex municipal traffic planning inherently takes hours and cannot be rushed arbitrarily.",
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
    sub_skill="Error Propagation",
    module="Domain 5 (Telecom Silent Monitoring Suppression)",
    scenario="A telecommunications monitoring tool queries an optical backbone monitor. The monitor times out, and the tool catch block returns an empty list `[]` marked as success. Downstream, Claude informs the network operations center that zero packet loss occurred across the entire backbone. What anti-pattern occurred?",
    options=[
        "Context window overflow caused by optical wavelengths exceeding token limits.",
        "Prompt injection vulnerability where optical hardware hijacked the model's system prompt.",
        "Silent error suppression, mistaking a transient network timeout for a valid empty result.",
        "Operating system kernel panic during TCP socket communication with the optical monitor."
    ],
    correct_idx=2,
    rationales={
        "correct": "Silent error suppression occurs when tool catch blocks return empty data marked as successful upon error. Downstream agents cannot distinguish an access failure from a valid empty dataset, misleading Claude into falsely concluding that zero packet loss occurred when in reality the monitor was offline.",
        "distractors": [
            "Optical wavelengths consume negligible tokens and do not trigger context overflow.",
            "The optical monitor timed out and returned no text; no prompt injection occurred.",
            "A standard HTTP timeout does not trigger an operating system kernel panic."
        ]
    },
    key_insight="Silent error suppression leads to false conclusions. Always return structured error payloads with failure categories rather than empty success lists."
))

# Q51 (Target: D = 3)
questions.append(create_question(
    qid=51,
    domain_id=5,
    domain_name="Context Management & Reliability",
    sub_skill="Information Provenance",
    module="Domain 5 (Agricultural Contradictory Weather Forecasts)",
    scenario="An agricultural advisory agent queries two authoritative meteorological services for regional freeze risk. Service A forecasts an overnight low of 34°F (above freezing), while Service B forecasts 28°F (hard freeze). How should the agent report this to citrus growers?",
    options=[
        "Average the two temperatures to 31°F and report it as the single unified meteorological forecast.",
        "Discard Service B because hard freeze forecasts cause panic, reporting only Service A.",
        "Crash the agent orchestration pipeline and notify farmers that weather satellites are broken.",
        "Report both forecasts with full attribution, source agency names, and forecast issuance times."
    ],
    correct_idx=3,
    rationales={
        "correct": "When authoritative sources disagree, an agent must never invent synthetic averages or arbitrarily suppress one source. It must report both competing figures along with full provenance metadata: source agency, forecasted temperature, and issuance timestamp, allowing growers to make informed risk mitigation decisions.",
        "distractors": [
            "Averaging conflicting forecasts conceals the hard freeze risk and could result in unmitigated crop destruction.",
            "Discarding freeze warnings based on emotional comfort causes catastrophic agricultural losses.",
            "Forecast variations between meteorological services are normal atmospheric modeling realities, not system corruptions."
        ]
    },
    key_insight="Report conflicting data with full attribution and dates. Never fabricate synthetic averages or arbitrarily suppress authoritative sources."
))

# Q52 (Target: A = 0)
questions.append(create_question(
    qid=52,
    domain_id=5,
    domain_name="Context Management & Reliability",
    sub_skill="Escalation & Ambiguity Resolution",
    module="Domain 5 (Banking Customer Branch Manager Escalation)",
    scenario="A banking customer in an automated chat types: 'I want to speak directly to the branch manager immediately.' The issue is a simple fee waiver that the agent is authorized to grant autonomously. What is the correct architectural action?",
    options=[
        "Honor the customer's explicit request immediately and execute the branch escalation workflow.",
        "Grant the fee waiver autonomously and inform the customer that their request was rejected.",
        "Ask the customer five survey questions regarding why they prefer speaking with a human manager.",
        "Display an error message stating that human branch managers are unavailable for simple fees."
    ],
    correct_idx=0,
    rationales={
        "correct": "An explicit customer demand for a human supervisor is a mandatory, non-negotiable escalation trigger. Regardless of how simple the issue is, attempting to force autonomous resolution after an explicit demand destroys customer trust and violates banking support protocols.",
        "distractors": [
            "Ignoring the demand and forcing autonomous execution enrages customers and violates support protocols.",
            "Interrogating an angry customer with survey questions exacerbates frustration.",
            "Refusing to escalate locks customers in an unhelpful loop."
        ]
    },
    key_insight="When a customer explicitly demands a human representative, escalate immediately. Never attempt to force autonomous resolution."
))

# Q53 (Target: B = 1)
questions.append(create_question(
    qid=53,
    domain_id=5,
    domain_name="Context Management & Reliability",
    sub_skill="Human Review & Confidence Calibration",
    module="Domain 5 (Defense Stratified Intelligence OCR Audit)",
    scenario="A military intelligence transcription platform achieves an overall 98% aggregate accuracy across 100,000 scanned documents. However, an internal audit reveals that typed headquarters memos have 99.5% accuracy, but field-handwritten reconnaissance notes have a 25% error rate. What evaluation failure occurred?",
    options=[
        "The evaluation failed to reboot the cloud servers before testing handwritten reconnaissance notes.",
        "The evaluation relied on aggregate metrics, mathematically concealing the 25% failure rate.",
        "The model was tested using temperature 0.0 instead of temperature 1.0 on reconnaissance notes.",
        "The intelligence analysts submitted reconnaissance notes in non-standard UTF-8 character encoding."
    ],
    correct_idx=1,
    rationales={
        "correct": "The 'aggregate metrics trap' mathematically conceals high error rates in difficult sub-categories (handwritten reconnaissance notes at 25% error) behind high volume in easy sub-categories (typed memos at 99.5% accuracy). Evaluation must always be stratified across document classes and intelligence sources.",
        "distractors": [
            "Server reboots do not impact model weights or handwriting OCR capabilities.",
            "Temperature zero is the standard best practice for deterministic extraction tasks.",
            "Character encoding has zero connection to handwritten note transcription errors."
        ]
    },
    key_insight="Beware the aggregate metrics trap: overall high accuracy frequently conceals catastrophic failure rates in difficult sub-distributions."
))

# Fix any duplicate qids
for i, q in enumerate(questions):
    q["id"] = i + 1

exam5_data = {
    "id": 5,
    "title": "Practice Exam 5: Comprehensive Mock Exam (Final Readiness)",
    "description": "Cross-domain comprehensive assessment covering all five architect domains at exam difficulty level.",
    "questions": questions
}

output_path = "data/architect/exam5.json"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(exam5_data, f, indent=2)

print(f"Successfully generated {len(questions)} questions in {output_path}!")
