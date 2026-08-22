# CodeMentor AI - API Specification

Base URL: `http://localhost:8000/api`

All authenticated endpoints require standard HTTP Authorization header:
`Authorization: Bearer <access_token>`

---

## 1. Authentication & Users

### `POST /api/auth/register`
Creates a new learner account and initializes an empty learner profile.

**Request Body**:
```json
{
  "name": "Alex Mercer",
  "email": "alex@example.com",
  "password": "SecurePassword123!",
  "languages": ["python"],
  "self_declared_level": "intermediate",
  "selected_topics": ["Loops", "Arrays", "Recursion"]
}
```

**Response (201 Created)**:
```json
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer",
  "user": {
    "id": "u-12345",
    "name": "Alex Mercer",
    "email": "alex@example.com",
    "languages": ["python"],
    "self_declared_level": "intermediate",
    "selected_topics": ["Loops", "Arrays", "Recursion"],
    "knowledge_check_completed": false
  }
}
```

### `POST /api/auth/login`
Authenticates existing user and returns JWT token.

### `GET /api/auth/me`
Fetches current authenticated user details.

### `GET /api/profile` / `PUT /api/profile`
Retrieves or updates user language/skill preferences.

---

## 2. Knowledge Check Assessment

### `POST /api/assessment/start`
Starts a diagnostic Knowledge Check session, returning curated baseline questions (with answer keys securely stripped).

### `POST /api/assessment/submit`
Submits student answers, executes deterministic grading, updates user proficiency, and returns AI gap analysis comparing self-declared vs. actual scores.

**Request Body**:
```json
{
  "answers": [
    {"question_id": "q_loops_1", "selected_answer": "10"},
    {"question_id": "q_recursion_1", "selected_answer": "It causes infinite recursion..."}
  ]
}
```

**Response (200 OK)**:
```json
{
  "id": "assess-789",
  "score": 0.80,
  "score_percentage": 80,
  "self_declared_level": "intermediate",
  "calculated_level": "intermediate",
  "strong_topics": ["loops", "arrays"],
  "weak_topics": ["recursion"],
  "concept_scores": {
    "loops": 1.0,
    "arrays": 1.0,
    "recursion": 0.5
  },
  "gap_summary": "Your verified diagnostic score matches your intermediate self-assessment...",
  "detailed_feedback": "Solid foundation in loops..."
}
```

### `GET /api/assessment/latest`
Retrieves the most recent assessment results for the authenticated student.

---

## 3. Coding Problems & Catalogs

### `GET /api/problems`
Returns catalog of curated coding challenges.
- **Query Params**: `topic` (string), `difficulty` (string), `search` (string)
- **Security Note**: Solutions and explanations are omitted from this response.

### `GET /api/problems/{problem_id}`
Returns problem description, starter code, test case metadata, constraints, and examples.

---

## 4. Learning Sessions & Answer Locking

### `POST /api/sessions`
Initializes a tutoring session for a specific problem.

**Request Body**:
```json
{
  "problem_id": "prob_recursion_factorial"
}
```

**Response (201 Created)**:
```json
{
  "id": "sess-456",
  "user_id": "u-123",
  "problem_id": "prob_recursion_factorial",
  "topic": "Recursion",
  "attempts_allowed": 3,
  "attempts_used": 0,
  "attempts_remaining": 3,
  "hints_used": 0,
  "current_hint_level": 0,
  "solution_unlocked": false,
  "status": "in_progress"
}
```

### `POST /api/sessions/{session_id}/attempt`
Submits code for evaluation, executes test cases in isolated sandbox, invokes Gemini diagnosis, updates learner profile, and advances hint levels.

**Response (200 OK - Incorrect Attempt)**:
```json
{
  "attempt_id": "att-001",
  "session_id": "sess-456",
  "is_correct": false,
  "attempt_number": 1,
  "attempts_remaining": 2,
  "error_type": "RUNTIME_ERROR",
  "concept": "recursion",
  "subconcept": "base_case",
  "misconception": "missing_base_case",
  "analysis": "The recursive function continues calling itself without reaching a termination guard...",
  "hint": "What condition tells the recursive function to stop calling itself and return a base value?",
  "hint_level": 1,
  "solution_unlocked": false,
  "solution": null
}
```

### `POST /api/sessions/{session_id}/hint`
Requests the next progressive hint tier (Level 1 $\rightarrow$ Level 2 $\rightarrow$ Level 3).

### `GET /api/sessions/{session_id}/solution`
Fetches the official reference solution, conceptual breakdown, and time/space complexity.
- **Enforcement**: Returns `403 Forbidden` if `solution_unlocked == false`.

---

## 5. AI Tutor & Custom Problems

### `POST /api/tutor/chat`
Contextual multi-turn chat with CodeMentor AI during a problem session.

### `POST /api/tutor/custom-problem`
Analyzes arbitrary student-provided code and problem statements.

---

## 6. Learner Profile & Analytics

### `GET /api/learner/profile`
Returns concept mastery scores ($0.0 - 1.0$), strong topics, weak topics, and recurring misconception frequencies.

### `GET /api/learner/recommendations`
Returns personalized problem recommendations with natural-language pedagogical reasoning.

### `GET /api/learner/revise-mistakes`
Returns targeted revision cards matching recurring misconceptions with corrective advice and exercises.

### `GET /api/learner/history`
Returns learning session history log with attempt counts, hint metrics, and solve statuses.
