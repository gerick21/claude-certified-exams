import json

# Exam 2: Advanced Agents, Tool-Use Loops & Context Engineering
# 53 completely distinct questions mapped to the CCDV-F blueprint

questions = [
  # --- DOMAIN 1: Agents and Workflows (8 Questions) ---
  {
    "id": 1,
    "domainId": 1,
    "domainName": "Agents and Workflows",
    "subSkill": "Agent Architecture",
    "module": "Module 2 (Agent Construction)",
    "scenario": "A development team is designing an autonomous code migration assistant. The agent needs to explore a repository, formulate a multi-step refactoring plan, and execute file modifications. However, management requires that no file on disk be modified without explicit developer review. How should the team architect this boundary?",
    "isMultiSelect": False,
    "options": [
      "Implement a Human-in-the-Loop approval gate right before executing the file-writing tool.",
      "Instruct Claude in the system prompt to ask the user for confirmation before each file save.",
      "Configure the agent loop with a low temperature so that all proposed refactorings stay safe.",
      "Dispatch each file modification to a background subagent running in non-interactive mode."
    ],
    "correctIndices": [0],
    "rationales": {
      "correct": "Option A is correct. Irreversible or high-stakes actions (such as writing to production files) require a deterministic Human-in-the-Loop gate in the execution harness, rather than relying on system prompt convention.",
      "distractors": [
        "Option B is incorrect because system prompt instructions are conventions that can be overlooked during complex autonomous reasoning.",
        "Option C is incorrect because temperature affects sampling variance, not permission gating or file write safety.",
        "Option D is incorrect because background subagents without approval gates would execute unconfirmed writes."
      ]
    },
    "keyInsight": "Put a human gate where the action is irreversible. Enforcement at the harness layer beats convention in the prompt."
  },
  {
    "id": 2,
    "domainId": 1,
    "domainName": "Agents and Workflows",
    "subSkill": "Agent Patterns and Frameworks",
    "module": "Module 2 (Tool-Use Loop)",
    "scenario": "An engineer implements an agent loop using the Messages API. During testing, the agent makes a tool call, the tool executes successfully, but the next request to Claude fails with a 400 Bad Request error stating that message alternation was violated. What is the root cause?",
    "isMultiSelect": False,
    "options": [
      "The client sent the tool execution result inside a user message instead of an assistant message.",
      "The client appended the tool_result block in a user message without preserving the prior tool_use assistant turn.",
      "The client forgot to include the base64 encoded environment variables in the tool response payload.",
      "The client executed the tool asynchronously while the Messages API strictly requires synchronous webhooks."
    ],
    "correctIndices": [1],
    "rationales": {
      "correct": "Option B is correct. In the Messages API tool-use loop, when Claude returns a tool_use block in an assistant turn, the conversation history must retain that assistant message, followed immediately by a user message containing the tool_result block with matching tool_use_id.",
      "distractors": [
        "Option A is incorrect because tool_result blocks must actually be sent with role 'user', not 'assistant'.",
        "Option C is incorrect because tool responses contain result content strings or JSON, not base64 environment variables.",
        "Option D is incorrect because tool execution happens entirely on the client side in whatever manner the developer chooses."
      ]
    },
    "keyInsight": "The tool-use loop requires strict alternation: assistant message containing tool_use must be paired with subsequent user message containing tool_result."
  },
  {
    "id": 3,
    "domainId": 1,
    "domainName": "Agents and Workflows",
    "subSkill": "Agent Construction with Claude",
    "module": "Module 2 (Agent Construction)",
    "scenario": "A long-running customer support agent runs into an infinite loop where Claude calls the same search tool repeatedly with slight variations of the same query without terminating. Which control mechanism should the harness implement to terminate this failure mode reliably?",
    "isMultiSelect": False,
    "options": [
      "A hard iteration ceiling and loop break that escalates to human support when max turns are reached.",
      "A rule in the system prompt telling Claude never to call the same search tool more than once per user session.",
      "A client configuration setting max_tokens to 10 so the model physically cannot generate further tool calls.",
      "An automated switch that drops sampling temperature to zero whenever a duplicate query string is detected."
    ],
    "correctIndices": [0],
    "rationales": {
      "correct": "Option A is correct. Autonomous agent loops must always have an explicit turn counter and maximum iteration ceiling in the execution harness to halt recursion and escalate to a human or fallback workflow.",
      "distractors": [
        "Option B is incorrect because a prompt instruction cannot physically enforce loop termination if the model gets caught in an edge case.",
        "Option C is incorrect because restricting max_tokens to 10 will truncate valid tool arguments and break the schema parsing.",
        "Option D is incorrect because lowering temperature does not stop repetitive search patterns once a reasoning loop has started."
      ]
    },
    "keyInsight": "Always bound agent loops with an explicit iteration ceiling and circuit breaker in code."
  },
  {
    "id": 4,
    "domainId": 1,
    "domainName": "Agents and Workflows",
    "subSkill": "Agent Patterns and Frameworks",
    "module": "Module 2 (Agent Memory and Skills)",
    "scenario": "An engineering team is evaluating whether to adopt an agent framework (such as LangGraph or PydanticAI) versus writing a native loop with the Claude Agent SDK for a document review workflow. Which condition most strongly justifies adopting LangGraph?",
    "isMultiSelect": False,
    "options": [
      "The workflow requires stateful cyclical graph execution with persistent checkpoints and human-approval pauses.",
      "The workflow consists solely of streaming text tokens to a single client over standard Server-Sent Events.",
      "The application only needs to invoke a single external calculator tool and return the computed numerical answer.",
      "The project requires reducing per-token inference pricing by bypassing the Anthropic Messages API gateway."
    ],
    "correctIndices": [0],
    "rationales": {
      "correct": "Option A is correct. Frameworks like LangGraph earn their complexity when workflows require explicit state graphs, multi-step branching, cyclical routing, and checkpointed state for human pauses.",
      "distractors": [
        "Option B is incorrect because simple SSE streaming is natively supported by the Anthropic SDK with minimal code.",
        "Option C is incorrect because a single tool call does not justify an entire graph abstraction framework.",
        "Option D is incorrect because agent frameworks do not reduce API pricing or bypass the API gateway."
      ]
    },
    "keyInsight": "Adopt agent frameworks when you need checkpointed state graphs and complex human-in-the-loop branching; use native loops when simple."
  },
  {
    "id": 5,
    "domainId": 1,
    "domainName": "Agents and Workflows",
    "subSkill": "Agent Architecture",
    "module": "Module 2 (Agent Construction)",
    "scenario": "A financial data processor needs to extract tables from 200 PDF files, calculate totals, format a standardized spreadsheet, and email the report. The sequence of actions is strictly linear and never branches. Why is a deterministic code pipeline preferred over an autonomous agent?",
    "isMultiSelect": False,
    "options": [
      "A deterministic pipeline eliminates prompt non-determinism, reduces token overhead, and guarantees execution order.",
      "Autonomous agents are legally prohibited from parsing financial table structures under SOC2 and HIPAA guidelines.",
      "A code pipeline allows Claude to dynamically generate new tool schemas during runtime execution without validation.",
      "Deterministic pipelines automatically qualify for a 90% discount on Claude Messages API input and output tokens."
    ],
    "correctIndices": [0],
    "rationales": {
      "correct": "Option A is correct. When steps are deterministic and sequential, standard code orchestration is cheaper, lower latency, and 100% predictable compared to an autonomous agent loop.",
      "distractors": [
        "Option B is incorrect because SOC2/HIPAA does not forbid autonomous agents, but architecture should fit the problem.",
        "Option C is incorrect because pipelines do not dynamically invent schemas at runtime.",
        "Option D is incorrect because pipelines do not receive automated 90% discounts."
      ]
    },
    "keyInsight": "Decide workflow vs agent before writing the loop. Deterministic steps should be orchestrated with code."
  },
  {
    "id": 6,
    "domainId": 1,
    "domainName": "Agents and Workflows",
    "subSkill": "Agent Construction with Claude",
    "module": "Module 2 (Agent Construction)",
    "scenario": "In an agentic harness, an external weather API tool call fails due to a network connection timeout. What is the most resilient way for the client harness to report this failure to Claude in the tool_use loop?",
    "isMultiSelect": False,
    "options": [
      "Return a tool_result with is_error=True and an explanatory error message so Claude can retry or explain the issue.",
      "Crash the client application process immediately so that Kubernetes can reschedule the pod on another node.",
      "Omit the tool_result message completely from the conversation history and resend the user's initial query.",
      "Fabricate plausible average weather statistics and return them as valid tool data to avoid model confusion."
    ],
    "correctIndices": [0],
    "rationales": {
      "correct": "Option A is correct. Tool execution errors should be returned to Claude inside a tool_result block with is_error: true and a clear message, enabling Claude to reason about the failure, retry, or inform the user.",
      "distractors": [
        "Option B is incorrect because crashing the process on a routine network timeout breaks user sessions.",
        "Option C is incorrect because omitting tool_result breaks the mandatory tool_use alternation contract.",
        "Option D is incorrect because hallucinating/faking data corrupts application integrity."
      ]
    },
    "keyInsight": "Return tool failures explicitly to Claude using is_error: true so the model can self-correct or report."
  },
  {
    "id": 7,
    "domainId": 1,
    "domainName": "Agents and Workflows",
    "subSkill": "Agent Patterns and Frameworks",
    "module": "Module 2 (Agent Memory and Skills)",
    "scenario": "A support agent interacts with enterprise clients across multi-day troubleshooting sessions. The context window approaches its limit on Day 3. What is the recommended context engineering pattern to maintain continuity without losing critical facts?",
    "isMultiSelect": False,
    "options": [
      "Periodically summarize older conversational turns into a structured state block while pruning raw tool payloads.",
      "Increase the max_tokens parameter to 500,000 to expand the physical hardware context window of the model.",
      "Concatenate the entire raw log into the system prompt of every subagent launched during the active session.",
      "Delete all assistant messages while keeping user messages to preserve token budget without losing context."
    ],
    "correctIndices": [0],
    "rationales": {
      "correct": "Option A is correct. Effective context engineering uses compaction and summarization: condense historical turns into an updated state summary and prune verbose tool outputs before sending subsequent requests.",
      "distractors": [
        "Option B is incorrect because max_tokens limits generation length, not the input context window, and context windows are fixed budgets.",
        "Option C is incorrect because concatenating raw logs wastes tokens and accelerates context window exhaustion.",
        "Option D is incorrect because deleting assistant turns violates message alternation and removes the model's reasoning trace."
      ]
    },
    "keyInsight": "Compact conversation history and prune verbose tool outputs to keep multi-session agents within token budget."
  },
  {
    "id": 8,
    "domainId": 1,
    "domainName": "Agents and Workflows",
    "subSkill": "Agent Architecture",
    "module": "Module 4 (Cost, Latency, Reliability)",
    "scenario": "A development team splits an interconnected database refactoring task across five parallel subagents coordinated by a supervisor. The monthly token bill increases roughly fifteen-fold, while task completion quality remains unchanged compared to a single-agent run. What is the most proportionate architectural change?",
    "isMultiSelect": False,
    "options": [
      "Revert to a single agent with curated context, reserving fan-out for independent parallel tasks.",
      "Increase the per-turn token limit for each subagent to accelerate task resolution speed.",
      "Add three specialized subagents to divide the refactoring tasks into even smaller slices.",
      "Enable output streaming on the supervisor agent to reduce perceived end-to-end task latency."
    ],
    "correctIndices": [0],
    "rationales": {
      "correct": "Option A is correct. Multi-agent fan-out multiplies token costs (~15x) and only delivers value when work splits into truly independent parallel streams. On tightly coupled refactorings where subtasks depend on shared state, a single agent with good context engineering is more effective and far cheaper.",
      "distractors": [
        "Option B is incorrect because raising subagent token limits further inflates token spend on tasks that are already failing to benefit from fan-out.",
        "Option C is incorrect because adding more subagents to a coupled task compounds coordination friction and multiplies token consumption.",
        "Option D is incorrect because streaming alters perceived latency for a human observer but does not address the underlying token multiplier or architecture flaw."
      ]
    },
    "keyInsight": "Fan-out only pays when the task splits into independent parallel parts. On coupled tasks, orchestrator-worker patterns cause roughly 15x token multiplication with flat quality."
  }
]

print(f"Loaded {len(questions)} Domain 1 questions for Exam 2.")
