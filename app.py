import streamlit as st
import subprocess
import os
import sys
import glob
from pathlib import Path

from app.report.zipper import ReportZipper

# ---------------------------------------------------
# UTF-8 Console
# ---------------------------------------------------

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# ---------------------------------------------------
# Streamlit Config
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Documentation Compliance Agent",
    page_icon="🤖",
    layout="wide"
)

# ---------------------------------------------------
# Session State
# ---------------------------------------------------

if "finished" not in st.session_state:
    st.session_state.finished = False

if "reports" not in st.session_state:
    st.session_state.reports = []

if "zip_file" not in st.session_state:
    st.session_state.zip_file = ""

# ---------------------------------------------------
# Header
# ---------------------------------------------------

st.title("🤖 AI Documentation Compliance Agent")

st.write(
    """
Automatically compare a software documentation PDF with the live website.

### Tech Stack
- 📄 PDF Parser
- 🌐 Playwright Automation
- 🤖 Groq LLM
- 📊 HTML Compliance Reports
- ⚡ Streamlit Dashboard
"""
)

st.divider()

# ---------------------------------------------------
# Inputs
# ---------------------------------------------------

website = st.text_input(
    "Website URL",
    value="https://white-cliff-0bca3ed00.1.azurestaticapps.net"
)

groq_key = st.text_input(
    "Groq API Key",
    type="password"
)

pdf = st.file_uploader(
    "Upload Documentation PDF",
    type="pdf"
)

st.divider()

# ---------------------------------------------------
# Run Button
# ---------------------------------------------------

if st.button("🚀 Run Compliance Check"):

    if pdf is None:
        st.error("Please upload the Documentation PDF.")
        st.stop()

    if groq_key == "":
        st.error("Please enter your Groq API Key.")
        st.stop()

    os.makedirs("data", exist_ok=True)

    with open("data/documentation.pdf", "wb") as f:
        f.write(pdf.read())

    os.environ["GROQ_API_KEY"] = groq_key
    os.environ["BASE_URL"] = website

    progress = st.progress(0)

    status = st.empty()

    console = st.empty()

    steps = [

        ("📄 Parsing Documentation", "python -m tests.test_parser"),

        ("🌐 Crawling Website", "python -m tests.test_crawler"),

        ("🤖 Comparing using AI", "python -m tests.test_dashboard")

    ]

    total = len(steps)

    for i, (title, command) in enumerate(steps):

        status.info(title)

        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )

        console.code(result.stdout)

        if result.returncode != 0:

            st.error("Project Execution Failed")

            st.code(result.stderr)

            st.stop()

        progress.progress((i + 1) / total)

    zipper = ReportZipper()

    zip_path = zipper.create_zip()

    st.session_state.finished = True

    st.session_state.zip_file = zip_path

    st.session_state.reports = sorted(
        glob.glob("reports/*.html")
    )

    st.rerun()

# ---------------------------------------------------
# Results
# ---------------------------------------------------

if st.session_state.finished:

    st.success("✅ Compliance Check Completed Successfully!")

    st.balloons()

    st.divider()

    reports = st.session_state.reports

    st.metric(
        "Reports Generated",
        len(reports)
    )

    st.download_button(
        label="📦 Download Complete Reports (ZIP)",
        data=open(st.session_state.zip_file, "rb"),
        file_name="Compliance_Reports.zip",
        mime="application/zip"
    )

    st.divider()

    st.header("📊 Individual Reports")

    for report in reports:

        report_name = Path(report).stem.replace("_", " ").title()

        with st.expander(report_name, expanded=False):

            with open(report, "r", encoding="utf-8") as f:

                html = f.read()

            st.components.v1.html(
                html,
                height=650,
                scrolling=True
            )

            with open(report, "rb") as f:

                st.download_button(
                    label=f"⬇ Download {report_name}",
                    data=f,
                    file_name=os.path.basename(report),
                    mime="text/html",
                    key=report
                )

    st.divider()

    st.info("🎉 Project Finished Successfully.")