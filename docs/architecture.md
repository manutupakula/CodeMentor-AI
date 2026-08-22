# CodeMentor AI - System Architecture & Engineering Specifications

## 1. Executive Summary

**CodeMentor AI** is an adaptive, pedagogically driven programming tutor designed to foster algorithmic problem-solving and deep concept comprehension rather than passive answer consumption.

The system is built on the foundational educational principle:
> **"Don't immediately solve the student's problem. First help the student discover the solution."**

---

## 2. High-Level Architecture

```mermaid
graph TD
    subgraph Client ["Frontend Layer (React 18 + Vite + Tailwind + Monaco)"]
        UI_Dash[Dashboard & Analytics]
        UI_Quiz[Knowledge Check Wizard]
        UI_Editor[Monaco Coding Workspace]
        UI_Hints[3-Tier Progressive Hints Drawer]
        UI_Chat[Contextual AI Tutor Chat]
        UI_Revise[Revise My Mistakes Hub]
    end

    subgraph API_Gateway ["Backend Gateway (FastAPI Async)"]
        Router_Auth["/api/auth"]
        Router_Profile["/api/profile"]
        Router_Assess["/api/assessment"]
        Router_Prob["/api/problems"]
        Router_Sess["/api/sessions"]
        Router_Tutor["/api/tutor"]
        Router_Learner["/api/learner"]
    end

    subgraph Core_Services ["Service & Business Logic Layer"]
        AuthSvc[Auth & JWT Security Service]
        AssessSvc[Assessment & Deterministic Baseline Engine]
        ProfileSvc[Learner Profile & Mastery Engine]
        RecomSvc[Multi-Factor Recommendation Engine]
        TutorSvc[Tutor Orchestrator & State Machine]
        Runner[Safe Sandbox Code Execution Engine]
    end

    subgraph AI_Layer ["Pedagogical AI Layer (Gemini 3.7 Flash)"]
        GeminiClient[Official google-genai SDK]
        StructuredOutput[Strict Pydantic Output Schemas]
        SystemPrompt[Pedagogical System Directives]
        ContextBuilder[Compact Student Context Builder]
        FallbackEngine[Deterministic Fallback Diagnostics]
    end

    subgraph Database ["Persistence Layer (PyMongo Async / MongoDB Atlas)"]
        Col_Users[(users)]
        Col_Probs[(problems)]
        Col_Assess[(assessments & assessment_bank)]
        Col_Sess[(learning_sessions)]
        Col_Attempts[(attempts)]
        Col_Profiles[(learner_profiles)]
        Col_Convs[(conversations)]
    end

    Client <-->|REST / JSON| API_Gateway
    API_Gateway --> Core_Services
    Core_Services --> Database
    TutorSvc --> Runner
    TutorSvc --> AI_Layer
    AssessSvc --> AI_Layer
    RecomSvc --> ProfileSvc
    ProfileSvc --> Database
```

---

## 3. Server-Side Answer Locking Protocol

To guarantee that students cannot bypass the pedagogical discovery loop, answer locking is strictly enforced **server-side**:

1. **Problem Endpoint Masking**:
   - `GET /api/problems` and `GET /api/problems/{id}` unconditionally omit the fields `solution`, `explanation`, `better_approach`, `time_complexity`, and `space_complexity`.
2. **Session Attempt Guard**:
   - Every session starts with `solution_unlocked = false`, `attempts_allowed = 3`, and `attempts_used = 0`.
3. **Strict 403 Solution Endpoint**:
   - `GET /api/sessions/{session_id}/solution` executes an authorization check. If `solution_unlocked == false`, the server immediately responds with `403 Forbidden` (`SolutionLockedError`).
4. **Unlocking Conditions**:
   - **Independent / Hint Solve**: The student submits code passing all automated test cases (`solution_unlocked = true`, status = `solved_independently` or `solved_with_hints`).
   - **Exhausted Attempts**: The student utilizes all allowed attempts (`attempts_used >= attempts_allowed`), whereupon the backend transitions `solution_unlocked = true` and status = `exhausted`.

---

## 4. 3-Tier Progressive Hint State Machine

```mermaid
stateDiagram-v2
    [*] --> Attempt1_Incorrect: Submit 1st Wrong Code
    Attempt1_Incorrect --> HintLevel1: Generate Socratic Hint
    note right of HintLevel1
        Hint Level 1: Socratic Discovery
        - Probing question
        - Asks what happens at boundaries
        - Solution remains LOCKED
    end note

    HintLevel1 --> Attempt2_Incorrect: Submit 2nd Wrong Code
    Attempt2_Incorrect --> HintLevel2: Generate Conceptual Hint
    note right of HintLevel2
        Hint Level 2: Conceptual Mechanism
        - Explains underlying data/control flow
        - Solution remains LOCKED
    end note

    HintLevel2 --> Attempt3_Incorrect: Submit 3rd Wrong Code
    Attempt3_Incorrect --> SolutionUnlocked: Max Attempts Exhausted
    note right of SolutionUnlocked
        Hint Level 3 + Full Unlock
        - Code guidance
        - Reference Python solution
        - Time & Space complexity
        - Optimization & learning tips
    end note

    Attempt1_Incorrect --> Solved: Correct Code
    Attempt2_Incorrect --> Solved: Correct Code
    Attempt3_Incorrect --> Solved: Correct Code
    Solved --> SolutionUnlocked: Full Explanations Revealed
```

---

## 5. Deterministic Learner Profile & Mastery Algorithm

Concept mastery is computed deterministically to guarantee transparency, explainability, and reproducibility across student cohorts:

$$\text{Raw Mastery}(c) = 0.40 \cdot \text{Assessment}(c) + 0.30 \cdot \text{SuccessRate}(c) + 0.20 \cdot \text{IndSolveRate}(c) + 0.10 \cdot \text{RecentPerf}(c)$$

$$\text{Final Mastery}(c) = \max\Big(0.05, \min\big(0.99, \text{Raw Mastery}(c) - \text{MistakePenalty} - \text{HintPenalty}\big)\Big)$$

Where:
- $\text{MistakePenalty} = \min(0.20, \text{recurring\_mistakes}[c] \times 0.05)$
- $\text{HintPenalty} = \min(0.15, \frac{\text{hints\_used}}{\max(1, \text{attempts})} \times 0.05)$
- **Strong Topics**: $\text{Final Mastery}(c) \ge 0.70$
- **Weak Topics (Needs Practice)**: $\text{Final Mastery}(c) < 0.60$
