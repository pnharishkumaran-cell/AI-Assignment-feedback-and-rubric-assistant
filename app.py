
import json
from io import BytesIO

import streamlit as st
from pypdf import PdfReader

from backend import evaluate_assignment


# --------------------------------------------------
# 1. Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Assignment Feedback Assistant",
    page_icon="📝",
    layout="wide"
)

st.title("📝 AI Assignment Feedback & Rubric Assistant")

st.write(
    "Upload an assignment PDF or enter your submission manually. "
    "The AI will evaluate it using your selected rubric."
)


# --------------------------------------------------
# 2. Sidebar settings
# --------------------------------------------------

st.sidebar.header("Evaluation Settings")

max_marks = st.sidebar.number_input(
    "Maximum marks",
    min_value=1,
    max_value=1000,
    value=20,
    step=1
)

st.sidebar.subheader("Rubric Weights")

accuracy_weight = st.sidebar.slider(
    "Accuracy (%)", 0, 100, 40
)

completeness_weight = st.sidebar.slider(
    "Completeness (%)", 0, 100, 30
)

clarity_weight = st.sidebar.slider(
    "Clarity (%)", 0, 100, 20
)

originality_weight = st.sidebar.slider(
    "Originality (%)", 0, 100, 10
)

weights = {
    "Accuracy": accuracy_weight,
    "Completeness": completeness_weight,
    "Clarity": clarity_weight,
    "Originality": originality_weight
}

total_weight = sum(weights.values())

st.sidebar.write(f"Total weight: **{total_weight}%**")

if total_weight != 100:
    st.sidebar.warning(
        "Adjust the weights so they total exactly 100%."
    )


# --------------------------------------------------
# 3. Assignment details
# --------------------------------------------------

st.header("Assignment Details")

student_name = st.text_input(
    "Student name (optional)"
)

title = st.text_input(
    "Assignment title",
    placeholder="Enter the assignment title"
)

st.subheader("Submit Your Assignment")

input_method = st.radio(
    "Choose submission method",
    ["Upload PDF", "Enter text manually"],
    horizontal=True
)


# --------------------------------------------------
# 4. PDF upload and text extraction
# --------------------------------------------------

submission = ""
pdf_error = None

if input_method == "Upload PDF":

    uploaded_pdf = st.file_uploader(
        "Choose your assignment PDF",
        type=["pdf"],
        help="Upload a text-based PDF containing your assignment."
    )

    if uploaded_pdf is not None:
        st.write(f"**Selected file:** {uploaded_pdf.name}")

        try:
            pdf_bytes = uploaded_pdf.getvalue()
            reader = PdfReader(BytesIO(pdf_bytes))

            if reader.is_encrypted:
                pdf_error = (
                    "This PDF is password-protected. "
                    "Please upload an unlocked PDF."
                )
            elif len(reader.pages) == 0:
                pdf_error = "The PDF contains no pages."
            else:
                submission = "\n".join(
                    page.extract_text() or ""
                    for page in reader.pages
                ).strip()

                if submission:
                    st.success(
                        f"Successfully extracted text from "
                        f"{len(reader.pages)} PDF page(s)."
                    )

                    with st.expander(
                        "Preview extracted assignment text"
                    ):
                        st.text_area(
                            "Extracted text",
                            value=submission,
                            height=250,
                            disabled=True,
                            key="pdf_text_preview"
                        )
                else:
                    pdf_error = (
                        "No readable text was found. "
                        "Your PDF may contain scanned images. "
                        "OCR support is not included in this version."
                    )

        except Exception as error:
            pdf_error = f"Could not read this PDF: {error}"

    if pdf_error:
        st.error(pdf_error)

else:

    submission = st.text_area(
        "Assignment submission",
        placeholder="Paste or type your assignment here...",
        height=250
    ).strip()


# --------------------------------------------------
# 5. Additional instructions
# --------------------------------------------------

extra_instructions = st.text_area(
    "Additional instructions (optional)",
    placeholder=(
        "Example: Focus on technical accuracy "
        "and provide constructive feedback."
    ),
    height=100
)


# --------------------------------------------------
# 6. Evaluate assignment
# --------------------------------------------------

st.divider()

if st.button(
    "Evaluate Assignment",
    type="primary",
    use_container_width=True
):

    if not title.strip():
        st.error("Please enter the assignment title.")

    elif total_weight != 100:
        st.error(
            "Rubric weights must total exactly 100%."
        )

    elif input_method == "Upload PDF" and uploaded_pdf is None:
        st.error("Please upload a PDF first.")

    elif pdf_error:
        st.error(
            "Please resolve the PDF issue before evaluating."
        )

    elif not submission:
        st.error(
            "No assignment text is available to evaluate."
        )

    else:
        try:
            with st.spinner(
                "Evaluating your assignment with Gemini..."
            ):
                report = evaluate_assignment(
                    title=title.strip(),
                    submission=submission,
                    weights=weights,
                    max_marks=max_marks,
                    student_name=student_name.strip(),
                    extra_instructions=extra_instructions.strip()
                )

            st.session_state["evaluation_report"] = report

        except Exception as error:
            st.error(
                f"Evaluation failed: {error}"
            )


# --------------------------------------------------
# 7. Display evaluation results
# --------------------------------------------------

report = st.session_state.get("evaluation_report")

if report:

    st.divider()
    st.header("📊 Evaluation Results")

    rubric_result = report.get("rubric", {})
    total_score = rubric_result.get("total_score", 0)
    maximum = rubric_result.get("maximum_marks", max_marks)

    percentage = (
        (total_score / maximum) * 100
        if maximum
        else 0
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Score",
        f"{total_score}/{maximum}"
    )

    col2.metric(
        "Percentage",
        f"{percentage:.1f}%"
    )

    col3.metric(
        "Criteria Evaluated",
        len(rubric_result.get("criteria", {}))
    )

    st.subheader("Rubric Breakdown")

    criteria = rubric_result.get("criteria", {})
    ai_scores = report.get("scores", {})
    reasons = report.get("reasons", {})

    for criterion, details in criteria.items():

        with st.expander(criterion):

            score = ai_scores.get(
                criterion,
                details.get("percentage", 0)
            )

            st.write(f"**AI score:** {score}%")
            st.write(
                f"**Rubric weight:** {details.get('weight', 0)}%"
            )
            st.write(
                f"**Marks earned:** {details.get('marks', 0)}"
            )

            reason = reasons.get(criterion)

            if reason:
                st.write(f"**Feedback:** {reason}")

    st.subheader("✅ Strengths")

    strengths = report.get("strengths", [])

    if strengths:
        for strength in strengths:
            st.markdown(f"- {strength}")
    else:
        st.write("No strengths were provided.")

    st.subheader("🎯 Areas for Improvement")

    improvements = report.get("improvements", [])

    if improvements:
        for improvement in improvements:
            st.markdown(f"- {improvement}")
    else:
        st.write("No improvement suggestions were provided.")

    st.subheader("📝 Overall Feedback")

    st.write(
        report.get(
            "overall_feedback",
            "No overall feedback was provided."
        )
    )

    st.info(
        "AI-generated scores and feedback should be reviewed "
        "by a human before being used for official grading."
    )

    # --------------------------------------------------
    # 8. Download JSON report
    # --------------------------------------------------

    st.subheader("Download Evaluation Report")

    json_report = json.dumps(
        report,
        indent=4,
        ensure_ascii=False
    )

    st.download_button(
        label="Download JSON Report",
        data=json_report,
        file_name="assignment_evaluation.json",
        mime="application/json",
        use_container_width=True
    )
