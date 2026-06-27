import streamlit as st
import subprocess
import os

st.set_page_config(
    page_title="AI Documentation Compliance Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Documentation Compliance Agent")

st.write(
    "Automatically compare documentation with the live website."
)

st.divider()

website = st.text_input(
    "Website URL",
    value="https://white-cliff-0bca3ed00.1.azurestaticapps.net"
)

groq = st.text_input(
    "Groq API Key",
    type="password"
)

pdf = st.file_uploader(
    "Upload Documentation PDF",
    type="pdf"
)

st.divider()

if st.button("🚀 Run Compliance Check"):

    st.info("Starting project...")

    if pdf is not None:

        os.makedirs("data", exist_ok=True)

        with open(
            "data/documentation.pdf",
            "wb"
        ) as f:

            f.write(pdf.read())

    steps = [

        ("Extract PDF", "python -m tests.test_parser"),

        ("Login", "python -m tests.test_login"),

        ("Crawl Website", "python -m tests.test_crawler"),

        ("Generate Reports", "python -m tests.test_dashboard")

    ]

    progress = st.progress(0)

    for i, (title, command) in enumerate(steps):

        st.write(f"### {title}")

        subprocess.run(command, shell=True)

        progress.progress((i + 1) / len(steps))

    st.success("Completed!")

    st.write("Reports generated inside the reports folder.")