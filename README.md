# 🔬 DeepResearch Agent

> **Research questions the way a senior analyst would — deeply, methodically, and critically.**

An autonomous multi-agent research system that investigates complex questions, gathers evidence, challenges its own conclusions, generates evidence-backed reports, and continuously monitors topics for meaningful changes.

**Phase 1 focuses on Research Planning using Google ADK + Gemini.**

---

## ✨ Phase 1 — What's Included

| Capability                         |   Status   |
| ---------------------------------- | :--------: |
| 🤖 Google ADK + Gemini Integration |      ✅     |
| 🧠 Research Manager Agent          |      ✅     |
| 📋 Structured Research Planning    |      ✅     |
| 🎯 Research Goals                  |      ✅     |
| ❓ Research Subquestions            |      ✅     |
| 📚 Expected Source Types           |      ✅     |
| ⏱️ Research Timeline Estimation    |      ✅     |
| 🏆 Success Criteria                |      ✅     |
| 🔎 Source Discovery                | 🔜 Phase 2 |
| 📑 Evidence Extraction             | 🔜 Phase 3 |
| 🧐 Critic / Verification Agent     | 🔜 Phase 4 |
| 📝 Report Generation               | 🔜 Phase 6 |
| ☁️ Firestore Persistence           | 🔜 Phase 7 |
| 💻 Frontend                        | 🔜 Phase 8 |
| 🔔 Continuous Monitoring           | 🔜 Phase 9 |

---

# 🏗️ Architecture

Phase 1 uses a simple research-planning pipeline:

```text
┌─────────────────────────┐
│  User Research Question │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│   Research Manager      │
│         Agent           │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│      Gemini 2.0 Flash   │
│       LLM Analysis      │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│   Structured Research   │
│          Plan           │
└─────────────────────────┘
```

The generated plan contains:

* **Complexity level**
* **Research goals**
* **Research subquestions**
* **Expected source types**
* **Estimated timeline**
* **Research strategy**
* **Success criteria**

---

# 🚀 Getting Started

## Prerequisites

Make sure you have:

* Python **3.10+**
* A Google Gemini API key
* Git
* pip

---

## 1. 🔑 Get a Google Gemini API Key

Create a Gemini API key from Google AI Studio:

👉 **[Google AI Studio — Get API Key](https://aistudio.google.com/app/apikey)**

> ⚠️ **Security:** Never commit your API key to Git or expose it in source code.

---

## 2. 📥 Clone / Download the Project

Open your terminal and navigate to the project directory:

```bash
cd "d:\DeepResearch Agent"
```

If you're cloning from Git:

```bash
git clone <your-repository-url>
cd "DeepResearch Agent"
```

---

## 3. 🐍 Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 4. 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5. ⚙️ Configure Environment Variables

Copy the example environment file.

### Windows

```bash
copy .env.example .env
```

### macOS / Linux

```bash
cp .env.example .env
```

Then open `.env` and add your API key:

```env
GOOGLE_API_KEY=your_actual_api_key_here
GEMINI_MODEL=gemini-2.0-flash
```

### Example `.env.example`

```env
GOOGLE_API_KEY=your_actual_api_key_here
GEMINI_MODEL=gemini-2.0-flash
```

> 🔒 Make sure `.env` is included in `.gitignore`.

---

# ▶️ Running the Application

Start the Phase 1 research manager:

```bash
python -m backend.main
```

You should see output similar to:

```text
================================================================================
DeepResearch Agent - Phase 1: Research Planning
================================================================================

[INFO] Configuration loaded successfully
[INFO] Research Manager Agent initialized
[INFO] Creating research plan for:
       Will AI replace software developers by 2030?

================================================================================
RESEARCH QUESTION
================================================================================

Will AI replace software developers by 2030?

COMPLEXITY:
  COMPLEX

RESEARCH GOALS:

  1. Understand current capabilities of AI coding systems
  2. Analyze employment trends and market demand for developers
  3. Assess technical limitations and barriers
  4. Evaluate the economic impact of AI-assisted development

SUBQUESTIONS:

  1. What can current AI coding systems actually do?
  2. What evidence exists regarding developer productivity?
  3. What are the limitations of AI coding systems?
  4. How is AI changing software engineering roles?

EXPECTED SOURCES:

  • Academic papers
  • Industry analyst reports
  • Technical documentation
  • Developer surveys
  • Labor market data

ESTIMATED TIMELINE:

  3-4 weeks

RESEARCH STRATEGY:

  Multi-phase analysis combining technical,
  economic, labor-market, and industry evidence.

SUCCESS CRITERIA:

  1. Collect at least 50 reliable sources
  2. Identify supporting and conflicting evidence
  3. Separate facts from forecasts
  4. Assess uncertainty explicitly

================================================================================
```

A detailed log file will also be created:

```text
research_agent.log
```

---

# 📁 Project Structure

```text
DeepResearch Agent/
│
├── backend/
│   │
│   ├── agents/
│   │   └── manager.py
│   │       └── Research Manager Agent
│   │
│   ├── models/
│   │   └── research.py
│   │       └── ResearchPlan & ResearchProject
│   │
│   ├── main.py
│   │   └── Application entry point
│   │
│   └── config.py
│       └── Configuration management
│
├── .env
│   └── Local secrets — DO NOT COMMIT
│
├── .env.example
│   └── Environment configuration template
│
├── .gitignore
│
├── requirements.txt
│
├── research_agent.log
│   └── Runtime logs
│
└── README.md
```

---

# 🧠 How It Works

## 1. Configuration Loading

The application:

* Loads environment variables from `.env`
* Reads `GOOGLE_API_KEY`
* Reads the configured Gemini model
* Validates required configuration
* Initializes application logging

---

## 2. Research Manager Initialization

The `ResearchManagerAgent` is responsible for coordinating the research workflow.

```python
manager = ResearchManagerAgent()
```

The manager connects to Gemini and prepares the research-planning prompt.

---

## 3. Research Plan Creation

A research question is passed to the manager:

```python
plan = manager.create_research_plan(question)
```

Gemini analyzes the question and generates a structured plan.

The plan includes:

```text
Research Question
       │
       ├── Complexity
       │
       ├── Research Goals
       │
       ├── Subquestions
       │
       ├── Expected Sources
       │
       ├── Timeline
       │
       ├── Research Strategy
       │
       └── Success Criteria
```

---

## 4. Research Project Creation

The manager creates a research project containing:

* Unique research ID
* Research question
* Research plan
* Creation timestamp
* Initial project status
* Monitoring configuration

The initial status is:

```text
planning
```

---

# 🧩 Core Components

## `ResearchManagerAgent`

Located at:

```text
backend/agents/manager.py
```

The main orchestrator for the system.

### Main methods

```python
create_research_plan(question)
```

Creates a structured research plan using Gemini.

```python
create_research_project(question, plan)
```

Creates the research project metadata.

---

## `ResearchPlan`

Located at:

```text
backend/models/research.py
```

A Pydantic model representing the structured research plan.

It contains information such as:

* Question
* Complexity
* Goals
* Subquestions
* Expected sources
* Timeline
* Strategy
* Success criteria

---

## `ResearchProject`

Represents the research project's metadata and lifecycle.

It tracks:

* Research ID
* Question
* Status
* Timestamps
* Research plan
* Monitoring settings

Firestore persistence will be introduced in a later phase.

---

# 🧪 Testing

You can test the system by changing the research question in:

```text
backend/main.py
```

For example:

```python
research_question = "Will AI replace software developers by 2030?"
```

### Suggested research questions

#### 🤖 AI & Software

```text
Will AI replace software developers by 2030?
```

#### 🔋 Energy Technology

```text
Are solid-state batteries commercially viable by 2030?
```

#### ⚛️ Quantum Computing

```text
What are the biggest barriers to practical quantum computing?
```

---

# 📊 Example Research Plan

For the question:

> **Will AI replace software developers by 2030?**

The system may generate:

| Category         | Example                                                         |
| ---------------- | --------------------------------------------------------------- |
| Complexity       | Complex                                                         |
| Goals            | Understand AI capabilities, labor trends, technical limitations |
| Subquestions     | 5–8 focused research questions                                  |
| Sources          | Academic papers, industry reports, technical documentation      |
| Timeline         | 3–4 weeks                                                       |
| Strategy         | Multi-phase technical + economic + labor analysis               |
| Success Criteria | Reliable evidence, conflicting viewpoints, uncertainty analysis |

---

# 📝 Logging

DeepResearch Agent writes detailed runtime information to:

```text
research_agent.log
```

To monitor logs:

### Windows PowerShell

```powershell
Get-Content research_agent.log -Wait
```

### macOS / Linux

```bash
tail -f research_agent.log
```

Logs include:

* Configuration status
* Agent initialization
* Research questions
* Gemini requests
* Response parsing
* Errors
* Research plan generation

---

# 🛠️ Troubleshooting

<details>
<summary><strong>❌ GOOGLE_API_KEY environment variable is required</strong></summary>

Make sure you have created a `.env` file:

```bash
copy .env.example .env
```

Then add:

```env
GOOGLE_API_KEY=your_actual_api_key_here
```

</details>

<details>
<summary><strong>❌ Failed to parse Gemini response as JSON</strong></summary>

Gemini may have returned an unexpected response format.

Check:

```text
research_agent.log
```

for the generated response and parsing error.

</details>

<details>
<summary><strong>❌ 429 Too Many Requests</strong></summary>

You may have reached the Gemini API rate limit.

Wait for the limit to reset and try again.

</details>

<details>
<summary><strong>❌ No output after running the application</strong></summary>

Check:

```text
research_agent.log
```

for configuration or runtime errors.

Also verify that your virtual environment is activated.

</details>

---

# 🔐 Security

API keys are sensitive credentials.

### Never do this ❌

```python
GOOGLE_API_KEY = "AIzaSy..."
```

### Do this instead ✅

```env
GOOGLE_API_KEY=your_actual_api_key_here
```

And access it through environment configuration.

### Security checklist

* [x] Store secrets in `.env`
* [x] Keep `.env` in `.gitignore`
* [x] Use `.env.example` for configuration templates
* [x] Never hard-code API keys
* [ ] Use Google Cloud Secret Manager in production

---

# 🗺️ Roadmap

DeepResearch Agent is designed to evolve into a complete autonomous research platform.

```text
                    ┌────────────────────┐
                    │ Research Question  │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Research Manager   │
                    │      Phase 1       │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Source Discovery   │
                    │      Phase 2       │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Evidence Agent     │
                    │      Phase 3       │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Critic / Verify    │
                    │      Phase 4       │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Report Generation  │
                    │      Phase 6       │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Firestore Storage  │
                    │      Phase 7       │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Frontend / UI      │
                    │      Phase 8       │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Continuous         │
                    │ Monitoring Phase 9 │
                    └────────────────────┘
```

---

# 🔎 Phase 2 — Source Discovery

The next phase introduces the **Source Discovery Agent**.

It will:

* 🔍 Find relevant sources
* ⭐ Prioritize sources by quality
* ♻️ Detect and remove duplicates
* 🏷️ Capture source metadata
* 📊 Assign relevance scores
* 🔗 Store source URLs and references

The workflow becomes:

```text
Research Plan
      ↓
Source Discovery Agent
      ↓
Source Prioritization
      ↓
Duplicate Detection
      ↓
Found Sources
      ↓
Evidence Agent
```

---

# ☁️ Future Google Cloud Architecture

The long-term architecture is designed around Google Cloud:

```text
┌──────────────────────────────┐
│      React / Next.js         │
│          Frontend            │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│          Cloud Run           │
│             API              │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       Google ADK             │
│      Agent Orchestration     │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       Gemini / Vertex AI     │
│        LLM Backbone          │
└──────────────┬───────────────┘
               │
        ┌──────┴──────┐
        ▼             ▼
┌─────────────┐ ┌─────────────┐
│  Firestore  │ │   Pub/Sub   │
│ Persistence │ │ Background  │
│             │ │   Tasks     │
└─────────────┘ └─────────────┘
```

---

# 🧰 Technology Stack

| Technology         | Purpose                          |
| ------------------ | -------------------------------- |
| 🐍 Python 3.10+    | Application runtime              |
| 🤖 Google Gemini   | LLM backbone                     |
| 🧩 Google ADK      | Agent orchestration              |
| 📦 Pydantic        | Data validation                  |
| ☁️ Google Cloud    | Future production infrastructure |
| 🔥 Firestore       | Future persistent storage        |
| 📡 Pub/Sub         | Future background processing     |
| ⚛️ React / Next.js | Future frontend                  |

---

# 🎯 Project Goals

DeepResearch Agent aims to move beyond simple LLM question answering.

The long-term goal is an agent that can:

```text
ASK
 ↓
PLAN
 ↓
SEARCH
 ↓
COLLECT
 ↓
VERIFY
 ↓
CHALLENGE
 ↓
SYNTHESIZE
 ↓
REPORT
 ↓
MONITOR
```

Instead of simply generating an answer, the system should build an **auditable chain of evidence** behind its conclusions.

---

# 📚 Research Philosophy

DeepResearch Agent is designed around several principles:

### 1. Evidence over confidence

A confident answer is not necessarily a correct answer.

### 2. Multiple perspectives

The system should actively search for supporting **and conflicting** evidence.

### 3. Source quality matters

Not every webpage or document should receive equal weight.

### 4. Claims should be traceable

Important conclusions should eventually be connected to the evidence supporting them.

### 5. Uncertainty should be explicit

When evidence is incomplete or contradictory, the system should say so.

### 6. Research should be reproducible

A research project should retain enough metadata and evidence to understand how its conclusions were reached.

---

# 👨‍💻 Authors & Attribution

Built for an **agentic AI hackathon**.

### Uses

* Google Gemini 2.0 Flash
* Google Generative AI SDK
* Google ADK
* Pydantic
* Python 3.10+

---

# 📄 License

This project is licensed under the **MIT License**.

---

# ⭐ Contributing

Contributions, ideas, and improvements are welcome.

The project is currently in **Phase 1**, so the architecture is expected to evolve significantly as additional research agents are introduced.

---

<div align="center">

### 🔬 DeepResearch Agent

**Research deeply. Verify critically. Report with evidence.**

Built for the next generation of agentic research.

</div>
