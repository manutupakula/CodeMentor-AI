# CodeMentor AI - AI & LLM Architecture

## 1. AI Philosophy & Guiding Principles

CodeMentor AI utilizes Google's **Gemini 3.7 Flash** model (`gemini-3.7-flash`) accessed via the official `google-genai` Python SDK.

The core objective is **Pedagogical Discovery**:
- Rather than outputting direct code replacements, the model analyzes the student's conceptual model.
- It identifies fine-grained misconceptions (e.g. `missing_base_case`, `off_by_one`, `wrong_loop_boundary`).
- It generates targeted hints respecting the active hint level (1: Socratic $\rightarrow$ 2: Conceptual $\rightarrow$ 3: Code Guidance).
- Only when the session lock is released by the backend does the tutor provide full solutions and asymptotic complexity analysis.

---

## 2. Gemini Integration Pattern

```
┌─────────────────────────────────────────────────────────────┐
│ FastApi Tutor Service                                       │
│                                                             │
│ 1. Executes Student Code in Safe Sandbox                    │
│ 2. Extracts Test Case Pass/Fail & Stderr                    │
│ 3. Fetches Student Profile & Historical Mistakes            │
│ 4. Enforces Server-Side Attempt & Hint Lock State           │
└──────────────────────────────┬──────────────────────────────┘
                               │ Structured Context
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Gemini 3.7 Flash (`google-genai` SDK)                       │
│                                                             │
│ - System Prompt: Socratic & Pedagogical Directives          │
│ - Response Schema: Pydantic TutorAnalysis / Conversation    │
│ - Mode: response_mime_type="application/json"               │
│ - Temperature: 0.2 (deterministic, reliable diagnosis)      │
└──────────────────────────────┬──────────────────────────────┘
                               │ Pydantic Validated Object
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Response Processing & State Transition                      │
│                                                             │
│ - Validate Standardized Error Type                          │
│ - Record Attempt in MongoDB `attempts`                      │
│ - Increment Recurring Misconception Counter                 │
│ - Recalculate Deterministic Concept Mastery                 │
│ - Strip Solution Fields if `solution_unlocked == False`     │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Standardized Error Categories

Every diagnostic response is classified into one of the following validated categories:

| Error Category | Pedagogical Meaning | Example Scenario |
| :--- | :--- | :--- |
| `SYNTAX_ERROR` | Syntax violation or invalid formatting | Missing colon after `def`, unmatched brackets |
| `RUNTIME_ERROR` | Unhandled exception during execution | `RecursionError` (infinite recursion), `IndexError` |
| `LOGICAL_ERROR` | Code executes without crashing but returns incorrect value | Off-by-one loop boundary, incorrect math step |
| `ALGORITHM_ERROR` | Flawed fundamental algorithmic strategy | Using $O(n^2)$ search when binary search is needed |
| `EDGE_CASE_ERROR` | Solution works on general cases but fails on extremes | Empty list `[]`, negative numbers, 0 |
| `COMPLEXITY_ERROR` | Solution exceeds allowed time or memory limits | Naive Fibonacci recursion on $N=40$ |
| `CONCEPTUAL_MISUNDERSTANDING` | Misapplication of programming language semantics | Mutable default arguments in functions |
| `STYLE_ISSUE` | Non-idiomatic code structure | Manually indexing list instead of `enumerate()` |
| `CORRECT` | All test cases pass successfully | Optimal or correct solution |
| `UNKNOWN` | Uncategorized failure | Fallback categorization |

---

## 4. Multi-Turn Conversational Memory Architecture

- **Short-Term Memory**:
  - Live session dialogue stored in MongoDB collection `conversations`.
  - Injected as compact rolling chat history (last 6 turns) to provide smooth multi-turn follow-ups.
- **Long-Term Memory**:
  - Maintained in `learner_profiles`.
  - Tracks cross-problem concept mastery, recurring misconceptions, and independent vs. hint-assisted solve counts.
  - Injected into the prompt as a structured summary to prevent context bloating and ensure crisp, relevant responses.

---

## 5. Resilience & Fallback Safety Engine

- If the Gemini API experiences network interruption or rate limits, the system does **not** crash.
- The built-in deterministic pedagogical fallback engine parses test results and code structure, generates progressive hints, updates the learner profile, and preserves all user attempt state seamlessly.
