# Documentation Compliance Agent

A Python-based automation tool that compares software documentation against a live website UI and generates compliance reports. The pipeline parses documentation, extracts UI structure from a website, compares the two, and produces HTML reports with an AI-assisted summary and a deterministic fallback when AI output is unavailable.

## Overview

This project is designed to help teams validate whether product documentation matches the actual experience of a web application. It combines:

- PDF documentation parsing
- Browser-based UI extraction
- Semantic and fuzzy matching
- AI-based comparison via Groq
- HTML report generation and dashboard output

## Features

- Extracts structured content from a documentation PDF
- Crawls and captures UI elements from a website
- Compares documentation text with live UI content
- Generates page-level compliance reports
- Produces an HTML dashboard overview
- Supports a fuzzy-matching fallback when AI response validation fails

## Project Structure

- app/ai/ - AI prompting, comparison, fuzzy matching, and validation logic
- app/extractor/ - Browser automation, login, crawling, and DOM extraction
- app/parser/ - PDF parsing and documentation structure extraction
- app/report/ - Report and dashboard generation
- tests/ - Entry points for parsing, crawling, and reporting stages
- data/ - Input PDFs, extracted JSON data, screenshots, and generated reports

## Setup Instructions

### 1. Prerequisites

- Python 3.10+
- pip
- A browser-compatible environment for Playwright

### 2. Clone the repository

```bash
git clone <your-repo-url>
cd documentation-compliance-agent
```

### 3. Create and activate a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Install Playwright browsers

```bash
playwright install
```

### 6. Configure environment variables

Create a `.env` file in the project root with the following values:

```env
GROQ_API_KEY=your_groq_api_key
BASE_URL=https://your-app-url
EMAIL=your_login_email
PASSWORD=your_login_password
```

### 7. Prepare the documentation input

Place your documentation PDF at:

```text
data/guidelines/WaiverPro-User-Guidelines.pdf
```

If needed, update the path in the parser and test scripts.

## How to Run Each Stage

### Option A: Run the full workflow through the Streamlit UI

This is the easiest way to run the full process end to end.

```bash
streamlit run app.py
```

Then:

1. Enter the website URL
2. Upload the documentation PDF
3. Provide your Groq API key
4. Click "Run Compliance Check"

The app will run the parsing, crawling, and comparison stages and then generate downloadable HTML reports.

### Option B: Run each stage manually

#### 1. Parse the documentation PDF

```bash
python -m tests.test_parser
```

This step extracts text from the PDF and prepares structured documentation content.

#### 2. Crawl the website and extract UI content

```bash
python -m tests.test_crawler
```

This stage launches a browser, logs in, navigates the site, and saves extracted UI JSON data.

#### 3. Generate compliance reports

```bash
python -m tests.test_dashboard
```

This step compares the documentation and extracted UI content and generates HTML reports in the reports folder.

## Architectural Decisions and Tool Selection

### Pipeline design

The project follows a modular three-stage pipeline:

1. Parse documentation
2. Extract UI structure from the target website
3. Compare and generate reports

This separation makes each stage easier to test and debug independently.

### Why Playwright

Playwright was chosen for browser automation because it is reliable for modern web applications, supports login flows, waiting for dynamic content, and captures DOM-based UI structure accurately.

### Why Groq

Groq is used for AI-assisted comparison because it provides fast LLM inference for summarizing and validating documentation-to-UI compliance. The LLM is used to produce richer structured insights.

### Why fuzzy matching is included

The fuzzy-matching layer acts as a deterministic fallback. If the AI request fails or returns invalid output, the system can still produce a useful compliance score and issue list based on string similarity and component comparison.

### Why Streamlit

Streamlit provides a lightweight interface for uploading a PDF, entering credentials and API details, and viewing generated reports without needing a separate frontend.

## Known Limitations

- The project currently relies on a fixed documentation PDF path and a specific login flow.
- It expects the target website to have a predictable DOM structure and login behavior.
- The login automation uses selectors that may need updates if the application UI changes.
- AI-based comparison depends on a valid Groq API key and network access.
- Report quality may vary depending on the quality of the documentation PDF and the website structure.
- The system is best suited for structured documentation review, not fully generalized automated QA.

## What I Would Improve Next

- Make the configuration fully file-driven instead of relying on hardcoded paths and selectors
- Add more robust error handling and retry logic for browser and AI failures
- Improve the crawling strategy to handle dynamic pages and complex navigation more reliably
- Add a database or artifact store for caching extracted data and previous reports
- Strengthen test coverage for parser, crawler, matcher, and report generation
- Add a background job mode so large compliance runs can execute asynchronously
- Improve the UI and reporting experience with more detailed insights and visual analytics

