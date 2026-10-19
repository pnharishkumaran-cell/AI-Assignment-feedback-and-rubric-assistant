
import json

import streamlit as st

from backend import evaluate_assignment

st.set_page_config(
    page_title="AI Rubric Assistant",
    page_icon="📝",
    layout="wide",
)

st.title("📝 AI Assignment Feedback & Rubric Assistant")
st.caption(
    "Evaluate assignments against a weighted rubric and generate feedback."
)

with st.sidebar:
    st.header("Evaluation Settings")

    max_marks = st.number_input(
        "Maximum marks",
        min_value=1,
        max_value=1000,
        value=20,
    )

    st.subheader("Rubric Weights (%)")

    accuracy = st.slider("Accuracy", 0, 100, 40)
    completeness = st.slider("Completeness", 0, 100, 30)
    clarity = st.slider("Clarity", 0, 100, 20)
    originality = st.slider("Originality", 0, 100, 10)

    weights = {
        "Accuracy": accuracy,
        "Completeness": completeness,
        "Clarity": clarity,
        "Originality": originality,
    }

    weight_total = sum(weights.values())
    st.write(f"Total weight: **{weight_total}%**")

    if weight_total == 100:
        st.success("Weights are valid.")
    else:
        st.warning("Adjust the weights until they total 100%.")

st.header("Assignment Details")

title = st.text_input("Assignment title")
student_name = st.text_input("Student name (optional)")

submission = st.text_area(
    "Student submission",
    height=250,
    placeholder="Paste the student's assignment here...",
)

extra_instructions = st.text_area(
    "Assignment requirements or extra instructions (optional)",
    placeholder="Explain what the assignment was expected to cover...",
)

if st.button("Evaluate Assignment", type="primary", use_container_width=True):
    if weight_total != 100:
        st.error("Rubric weights must total 100%.")
    elif not title.strip():
        st.error("Enter an assignment title.")
    elif not submission.strip():
        st.error("Paste the student's submission.")
    else:
        try:
            with st.spinner("Evaluating assignment with Gemini..."):
                report = evaluate_assignment(
                    title=title,
                    submission=submission,
                    weights=weights,
                    max_marks=max_marks,
                    student_name=student_name,
                    extra_instructions=extra_instructions,
                )

            st.session_state["evaluation_report"] = report

        except Exception as exc:
            st.error(f"Evaluation failed: {exc}")

report = st.session_state.get("evaluation_report")

if report:
    st.divider()
    st.header("Evaluation Results")

    col1, col2 = st.columns(2)

    col1.metric(
        "Final Score",
        f'{report["total_score"]} / {report["maximum_marks"]}',
    )
    col2.metric("Percentage", f'{report["percentage"]}%')

    st.subheader("Criterion-wise Feedback")

    for name, details in report["criteria"].items():
        with st.expander(name, expanded=True):
            st.write(f'**Evaluation:** {details["percentage"]}%')
            st.write(f'**Weight:** {details["weight"]}%')
            st.write(f'**Marks:** {details["marks"]}')
            st.write(f'**Reason:** {details["reason"]}')

    st.subheader("Strengths")
    for item in report["strengths"]:
        st.markdown(f"- {item}")

    st.subheader("Areas to Improve")
    for item in report["improvements"]:
        st.markdown(f"- {item}")

    st.subheader("Overall Feedback")
    st.write(report["overall_feedback"])

    st.info(report["review_notice"])

    st.download_button(
        "Download Evaluation Report (JSON)",
        data=json.dumps(report, indent=2, ensure_ascii=False),
        file_name="assignment_evaluation.json",
        mime="application/json",
    )
