import json

questions = [
    # Domain 1: Agents and Workflows (8 questions)
    {
        "id": 1,
        "domainId": 1,
        "domainName": "Agents and Workflows",
        "subSkill": "Agent Architecture",
        "module": "Module 2 (Agent Construction)",
        "scenario": "An architect is designing an incident triage system. High-severity alerts require an autonomous investigation loop to query disparate logs, while low-severity alerts follow a static, three-step notification template. What architectural principle applies?",
        "isMultiSelect": False,
        "options": [
            "Use an autonomous agent loop for low-severity alerts and a fixed pipeline for high-severity alerts.",
            "Use a deterministic workflow pipeline for low-severity alerts and an autonomous agent for high-severity.",
            "Deploy a supervisor-worker multi-agent system across all alert severity levels for consistency.",
            "Run all incident alerts through an external Model Context Protocol server state engine."
        ],
        "correctIndices": [1],
        "rationales": {
            "correct": "When requirements follow a static template, write a deterministic workflow pipeline in code. Autonomous agent loops are proportionate only when dynamic investigation and routing are required.",
            "distractors": [
                "Reversing the patterns wastes tokens on simple tasks and fails to provide investigation capabilities where needed.",
                "Deploying multi-agent supervisors for static low-severity alerts introduces massive token overhead without benefit.",
                "MCP servers provide tool integration interfaces, not end-to-end workflow execution logic."
            ]
        },
        "keyInsight": "Decide workflow vs agent before writing the loop. When steps are static, write code; when tasks require dynamic exploration, use an agent."
    },
    {
        "id": 2,
        "domainId": 1,
        "domainName": "Agents and Workflows",
        "subSkill": "Agent Architecture",
        "module": "Module 4 (Topic 5: Cost Levers)",
        "scenario": "A development team assigns an autonomous agent to refactor a monolithic codebase. The agent enters an unbounded loop, querying the same failing test suite over 40 iterations before timing out. Which control mechanism directly prevents this failure?",
        "isMultiSelect": False,
        "options": [
            "Enforce a strict `max_iterations` counter inside the agent loop with an explicit exit condition.",
            "Increase the model context window to allow the agent to absorb more historical test outputs.",
            "Lower the sampling temperature to zero to ensure the agent stops generating duplicate queries.",
            "Switch the underlying model tier to Claude Opus to improve autonomous reasoning quality."
        ],
        "correctIndices": [0],
        "rationales": {
            "correct": "Agent loops must have deterministic circuit breakers. Enforcing a hard `max_iterations` limit with a fallback exit condition stops runaway loops from consuming budget and hanging pipelines.",
            "distractors": [
                "Expanding the context window increases the token spend per iteration without addressing the infinite loop.",
                "Temperature controls token sampling probability, not iteration termination conditions.",
                "Switching model tiers does not stop an agent from repeating actions when stuck on a failing test."
            ]
        },
        "keyInsight": "Always configure a `max_iterations` ceiling inside custom agent loops to prevent unbounded execution and runaway token spend."
    },
    {
        "id": 3,
        "domainId": 1,
        "domainName": "Agents and Workflows",
        "subSkill": "Agent Construction with Claude",
        "module": "Module 2 (Topic 6: Agent Construction)",
        "scenario": "A team builds an agent loop using the Python Claude Agent SDK. The agent receives a `ResultMessage` indicating that task execution has finished. How should the application extract the final output from the message?",
        "isMultiSelect": False,
        "options": [
            "Parse `message.content` as raw JSON and extract the `result_payload` attribute.",
            "Inspect `isinstance(message, ResultMessage)` and read `message.result` directly.",
            "Concatenate all incoming text blocks across the stream and strip XML boundary tags.",
            "Call `client.messages.retrieve()` passing the message identifier from the event."
        ],
        "correctIndices": [1],
        "rationales": {
            "correct": "In the Claude Agent SDK, `ResultMessage` signals task completion. The code checks `isinstance(message, ResultMessage)` and reads `message.result` directly, as shown in the api-code-reference.",
            "distractors": [
                "The SDK returns typed message instances rather than raw JSON strings requiring manual deserialization.",
                "Concatenating raw text across the stream misses the SDK's structured completion object.",
                "Messages API `retrieve` endpoints are not part of the Agent SDK's streaming query loop."
            ]
        },
        "keyInsight": "In the Agent SDK, discriminate on SDK classes like `isinstance(message, ResultMessage)` and read `message.result` directly."
    },
    {
        "id": 4,
        "domainId": 1,
        "domainName": "Agents and Workflows",
        "subSkill": "Agent Patterns and Frameworks",
        "module": "Exam Blueprint (Gap Brief: Agentic Frameworks)",
        "scenario": "An enterprise development team requires typed validation on all tool inputs and outputs using Pydantic models. Which agentic framework specifically provides this typed schema validation out of the box?",
        "isMultiSelect": False,
        "options": [
            "PydanticAI, which models agent tools and results as validated Pydantic data schemas.",
            "LangGraph, which organizes agent state as an untyped directed acyclic graph of nodes.",
            "Claude Code CLI, which executes shell commands without parameter validation layers.",
            "Anthropic Managed Agents, which converts all tool arguments to plain text strings."
        ],
        "correctIndices": [0],
        "rationales": {
            "correct": "PydanticAI is designed specifically for typed agent development, where tool inputs, outputs, and agent state are enforced through validated Pydantic models.",
            "distractors": [
                "LangGraph focuses on graph-based state machines and checkpointing rather than Pydantic-first tool validation.",
                "Claude Code is a command-line developer tool, not an in-process typed agent framework.",
                "Managed Agents enforce JSON schemas via the API, but are not a client-side Pydantic framework."
            ]
        },
        "keyInsight": "PydanticAI provides typed agent construction where inputs and outputs are validated Pydantic models; LangGraph provides graph state and checkpointing."
    },
    {
        "id": 5,
        "domainId": 1,
        "domainName": "Agents and Workflows",
        "subSkill": "Agent Patterns and Frameworks",
        "module": "Module 2 (Topic 7: Agent Memory and Skills)",
        "scenario": "A long-running customer research agent accumulates multi-page company profiles across 15 turns. The developer notices that early user instructions are being forgotten. What context engineering fix is required?",
        "isMultiSelect": False,
        "options": [
            "Increase the sampling temperature to encourage Claude to recall earlier context blocks.",
            "Prune verbose tool outputs from early turns and compact state before reaching window limits.",
            "Move the tool definitions into user turns instead of defining them in the API tools list.",
            "Upgrade the model tier to Claude Opus to permanently eliminate context window limits."
        ],
        "correctIndices": [1],
        "rationales": {
            "correct": "Context bloat causes attention drift. Pruning large raw tool outputs once used and performing state-preserving compaction keeps the prompt focused and within budget.",
            "distractors": [
                "Temperature controls token sampling diversity and does not improve historical context retention.",
                "Moving tool schemas into user turns is an anti-pattern that breaks the Messages API tool-use protocol.",
                "Opus has a fixed context budget like all models; it does not eliminate the need for context hygiene."
            ]
        },
        "keyInsight": "Context engineering is mandatory in long sessions. Prune large raw tool outputs after consumption and compact history before reaching limits."
    },
    {
        "id": 6,
        "domainId": 1,
        "domainName": "Agents and Workflows",
        "subSkill": "Agent Construction with Claude",
        "module": "Module 2 (Topic 6: Agent Construction)",
        "scenario": "An autonomous code assistant proposes deleting an obsolete database migration file. To prevent accidental data loss, the system halts and prompts the engineer for confirmation before calling `delete_file`. What pattern does this illustrate?",
        "isMultiSelect": False,
        "options": [
            "Human-in-the-loop (HITL) gate placed inside the harness loop before irreversible actions.",
            "Post-execution audit verification that logs file deletion events to an external database.",
            "Model-graded evaluation asserting that the file deletion satisfied repository guidelines.",
            "Deterministic workflow chaining where human input replaces all tool calling mechanisms."
        ],
        "correctIndices": [0],
        "rationales": {
            "correct": "Human-in-the-loop (HITL) gates belong inside the execution harness loop immediately prior to invoking irreversible tools (like deletions, write operations, or payments).",
            "distractors": [
                "Post-execution audits occur after the file is already deleted, failing to prevent the loss.",
                "Model-graded evaluations test output quality, not runtime permission boundaries.",
                "HITL inside an agent loop preserves autonomy for safe steps while gating critical actions."
            ]
        },
        "keyInsight": "Place the human gate where the action is irreversible: inside the loop, immediately before tool execution."
    },
    {
        "id": 7,
        "domainId": 1,
        "domainName": "Agents and Workflows",
        "subSkill": "Agent Patterns and Frameworks",
        "module": "Module 2 (Topic 7: Subagents)",
        "scenario": "An orchestrator agent delegates data aggregation to three worker subagents. The orchestrator needs the final outputs from all three workers before generating an executive summary. How should worker results be handled?",
        "isMultiSelect": False,
        "options": [
            "Have workers write directly into the parent orchestrator's conversation history turn.",
            "Collect structured result payloads from workers and return them to the orchestrator.",
            "Allow subagents to call the parent orchestrator's private internal tool functions.",
            "Merge all subagent context windows into a single shared multi-turn memory pool."
        ],
        "correctIndices": [1],
        "rationales": {
            "correct": "Subagents run in isolated contexts. They return structured results or summaries back to the orchestrator, which consumes the outputs as data in its own conversation loop.",
            "distractors": [
                "Subagents cannot write directly into the parent's conversation turns; they communicate via return values.",
                "Subagents operate within their own tool scopes and cannot invoke parent internal functions.",
                "Context windows are independent per model call and cannot be dynamically merged."
            ]
        },
        "keyInsight": "Subagents execute in isolated contexts and return concise results back to the orchestrator. They do not share memory or write to parent turns directly."
    },
    {
        "id": 8,
        "domainId": 1,
        "domainName": "Agents and Workflows",
        "subSkill": "Agent Construction with Claude",
        "module": "Module 3 (Topic 2: Durable Project Context)",
        "scenario": "A developer runs the `Explore` subagent in Claude Code to research a codebase bug. The developer notices that the subagent ignores specific guidelines written in `CLAUDE.md`. What is the documented reason for this behavior?",
        "isMultiSelect": False,
        "options": [
            "The `Explore` and `Plan` built-in subagents intentionally skip `CLAUDE.md` and git status.",
            "Subagents only load `CLAUDE.md` if the file size is under 200 lines of plain text.",
            "Claude Code requires passing `--include-claude-md` to all subagent invocations.",
            "The `Explore` subagent operates exclusively in read-only sandbox container environments."
        ],
        "correctIndices": [0],
        "rationales": {
            "correct": "As documented in Module 3 and the code reference, the built-in `Explore` and `Plan` subagents skip `CLAUDE.md` and git status to optimize speed and context. Custom subagents or general-purpose sessions must be used if `CLAUDE.md` rules are required.",
            "distractors": [
                "Line count does not govern whether `CLAUDE.md` loads; it is an architectural design of the `Explore` subagent.",
                "There is no `--include-claude-md` CLI flag in Claude Code.",
                "While `Explore` is read-only, its omission of `CLAUDE.md` is an intentional context optimization."
            ]
        },
        "keyInsight": "The built-in `Explore` and `Plan` subagents skip `CLAUDE.md` and git status. Use general-purpose sessions or custom subagents when project rules must apply."
    }
]

print(f"Exam 2 loaded with {len(questions)} questions")
