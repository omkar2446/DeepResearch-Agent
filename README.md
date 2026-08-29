# DeepResearch Agent

An autonomous multi-agent research system that investigates questions, gathers evidence, challenges its own conclusions, generates evidence-backed reports, and continuously monitors topics for meaningful changes.

**Tagline:** Research questions the way a senior analyst would—deeply, methodically, and critically.

---

## Phase 1: Research Manager Agent & Research Planning

This is the Phase 1 implementation. It demonstrates:

1. **Google ADK + Gemini Integration** – Direct connection to Google's Gemini API
2. **Research Manager Agent** – Orchestrates research workflows
3. **Research Planning** – Creates structured research plans with subquestions
4. **Minimal Runnable Application** – Complete Python implementation

### Architecture

```
User Research Question
        ↓
Research Manager Agent
        ↓
Gemini 2.0 Flash
        ↓
Structured Research Plan
(complexity, goals, subquestions, sources, timeline, strategy)
```

---

## Setup Instructions

### 1. Get a Google API Key

You must have a Google Gemini API key to run this project.

**Steps:**

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Get API Key" or "Create API Key"
3. Copy your API key

**Important:** Your API key is sensitive. Never commit it to version control.

### 2. Clone / Download the Project

```bash
cd d:\DeepResearch Agent
```

### 3. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment

Copy `.env.example` to `.env`:

```bash
copy .env.example .env
```

Edit `.env` and add your Google API key:

```env
GOOGLE_API_KEY=your_actual_api_key_here
GEMINI_MODEL=gemini-2.0-flash
```

### 6. Run the Application

```bash
python -m backend.main
```

---

## Expected Output

When you run the application, you'll see:

```
================================================================================
DeepResearch Agent - Phase 1: Research Planning
================================================================================
[INFO] Configuration loaded successfully
[INFO] Research Manager Agent initialized
[INFO] Creating research plan for: Will AI replace software developers by 2030?

================================================================================
RESEARCH QUESTION: Will AI replace software developers by 2030?
================================================================================

████████████████████████████████████████████████████████████████████████████████
RESEARCH PLAN
████████████████████████████████████████████████████████████████████████████████

QUESTION:
  Will AI replace software developers by 2030?

COMPLEXITY: COMPLEX

RESEARCH GOALS:
  1. Understand current capabilities of AI coding systems
  2. Analyze employment trends and market demand for developers
  3. Assess technical limitations and barriers
  ...

SUBQUESTIONS:
  1. What can current AI coding systems actually do?
  2. What evidence exists regarding developer productivity?
  3. What are the limitations of AI coding systems?
  ...

EXPECTED SOURCES:
  • Academic papers on AI and machine learning
  • Industry analyst reports
  • Technical documentation
  ...

ESTIMATED TIMELINE: 3-4 weeks

RESEARCH STRATEGY:
  Multi-phase analysis combining...

SUCCESS CRITERIA:
  1. Collect at least 50 reliable sources
  2. Identify both supporting and conflicting evidence
  ...

████████████████████████████████████████████████████████████████████████████████
```

The system will also generate a `research_agent.log` file with detailed logs.

---

## Project Structure

```
DeepResearch Agent/
├── backend/
│   ├── __pycache__/
│   ├── agents/
│   │   └── manager.py              # Research Manager Agent
│   ├── models/
│   │   └── research.py             # Data models (ResearchPlan, ResearchProject)
│   ├── main.py                     # Entry point
│   └── config.py                   # Configuration management
├── .env                            # Your secrets (DO NOT commit)
├── .env.example                    # Template
├── .gitignore
├── requirements.txt
└── README.md
```

---

## How It Works (Phase 1)

### 1. Configuration Loading
- Reads `GOOGLE_API_KEY` from `.env`
- Validates that required environment variables are set

### 2. Research Manager Agent Initialization
- Creates a `ResearchManagerAgent` instance
- Configures connection to Google Gemini API

### 3. Research Plan Creation
- Takes a research question as input
- Sends a detailed prompt to Gemini
- Gemini analyzes the question and returns:
  - **Complexity Level**: simple, moderate, or complex
  - **Research Goals**: 3-5 specific goals
  - **Subquestions**: 5-8 researchable subquestions
  - **Expected Sources**: Types of sources to search
  - **Timeline**: Estimated research duration
  - **Strategy**: Research approach
  - **Success Criteria**: 4-6 criteria for evaluating results

### 4. Research Project Creation
- Generates a unique `research_id`
- Creates a `ResearchProject` document
- Records creation timestamp
- Sets initial status to "planning"

### 5. Output
- Prints formatted research plan to console
- Creates detailed logs in `research_agent.log`

---

## Key Components

### ResearchManagerAgent (`backend/agents/manager.py`)

The orchestrator that:
- Analyzes research questions
- Creates structured research plans
- In later phases, will delegate to specialized agents

**Main Methods:**
- `create_research_plan(question)` – Creates research plan
- `create_research_project(question, plan)` – Creates project document

### Data Models (`backend/models/research.py`)

**ResearchPlan:**
- Stores the structured research plan
- Includes question, complexity, goals, subquestions, etc.
- Uses Pydantic for validation

**ResearchProject:**
- Stores the research project metadata
- Tracks status, timestamps, monitoring settings
- Will be persisted to Firestore in later phases

### Configuration (`backend/config.py`)

- Manages environment variables
- Validates required settings
- Provides centralized access to configuration

---

## Testing

Test the system with different research questions by editing `backend/main.py`:

```python
research_question = "Your custom research question here?"
```

Try these test questions:

1. **"Will AI replace software developers by 2030?"**
   - Complex question requiring multiple angles

2. **"Are solid-state batteries commercially viable by 2030?"**
   - Technical question with clear evaluation criteria

3. **"What are the biggest barriers to practical quantum computing?"**
   - Technical question requiring synthesis of multiple barriers

---

## Current Limitations (Phase 1)

- ✗ No source discovery (added in Phase 2)
- ✗ No evidence extraction (added in Phase 3)
- ✗ No critic/verification (added in Phase 4)
- ✗ No report generation (added in Phase 6)
- ✗ No Firestore persistence (added in Phase 7)
- ✗ No frontend (added in Phase 8)
- ✗ No continuous monitoring (added in Phase 9)

---

## Next Phase (Phase 2): Source Discovery Agent

Phase 2 will add:

- **Source Discovery Agent** – Finds relevant sources
- **Source Prioritization** – Ranks sources by quality
- **Duplicate Detection** – Removes duplicate sources
- **Source Metadata** – Captures title, URL, type, relevance score

The workflow will become:

```
Research Plan → Source Discovery Agent → Found Sources → Evidence Agent (Phase 3)
```

---

## Troubleshooting

### Error: "GOOGLE_API_KEY environment variable is required"

**Solution:** You haven't set up `.env` file. See Setup Instructions step 5.

### Error: "Failed to parse Gemini response as JSON"

**Solution:** This might indicate Gemini is responding with an unexpected format. Check logs in `research_agent.log`.

### Error: "429 Too Many Requests"

**Solution:** You've hit the Gemini API rate limit. Wait a few minutes before trying again.

### No output after running the script

**Solution:** Check `research_agent.log` for error details.

---

## Security Notes

- **Never commit `.env`** – It contains your API key
- Use `.env.example` as a template for team members
- Store API keys in environment variables, not in code
- For production, use Google Cloud Secret Manager

---

## Google Cloud Architecture (Future Phases)

Phase 1 uses direct Gemini API calls. Future phases will add:

```
Frontend (React/Next.js)
    ↓
Cloud Run (API)
    ↓
Google ADK + Agents
    ↓
Gemini / Vertex AI
    ↓
Firestore (Persistent Storage)
    ↓
Pub/Sub (Background Tasks)
```

---

## Authors & Attribution

Built for an agentic AI hackathon.

Uses:
- **Google Gemini 2.0 Flash** – LLM backbone
- **Google Generative AI SDK** – API client
- **Pydantic** – Data validation
- **Python 3.10+**

---

## License

MIT

---

## Questions?

Check the logs:

```bash
tail -f research_agent.log
```

All major operations log their status. The logs should provide context for any issues.

---

**Ready for Phase 2?** Let me know when you want to add the Source Discovery Agent!
#   D e e p R e s e a r c h - A g e n t  
 