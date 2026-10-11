import os
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

ROOT = Path(__file__).parent
load_dotenv(ROOT / ".env")
st.set_page_config(page_title="LearnMate AI", page_icon="📚", layout="wide")

def ai_call(prompt, image_bytes=None, mime_type=None):
    key = os.getenv("GEMINI_API_KEY", "").strip()
    if not key or key == "PASTE_YOUR_API_KEY_HERE":
        return None, "Gemini API key missing. Add it to .env beside app.py, save, and restart."
    model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip()
    try:
        client = genai.Client(api_key=key)
        content = [prompt]
        if image_bytes:
            content.append(types.Part.from_bytes(data=image_bytes, mime_type=mime_type or "image/jpeg"))
        response = client.models.generate_content(model=model, contents=content)
        return response.text or "The AI returned an empty response.", None
    except Exception as exc:
        return None, f"Gemini request failed: {exc}"

def tutor_prompt(subject, grade, language, pace, task, question, performance=""):
    return f"""You are LearnMate AI, a patient school tutor. Teach, do not merely give answers.
Grade: {grade}; Subject: {subject}; Language: {language}; Explanation style: {pace}.
Task: {task}; Student request: {question}; Recent performance: {performance or 'Not supplied'}.
Respond in {language} and adapt to the grade. For problems, show numbered steps, define formulas/symbols, and check the final answer.
For concepts, include a simple explanation, a worked example, common mistake, and real-world connection.
If an image/question is unclear, say so and ask for clarification. End with one short check-your-understanding question.
"""

def show_ai(prompt, image_bytes=None, mime_type=None):
    with st.spinner("LearnMate is thinking..."):
        answer, error = ai_call(prompt, image_bytes, mime_type)
    if error:
        st.error(error)
    else:
        st.markdown(answer)
        st.session_state["last_answer"] = answer

st.title("📚 LearnMate AI")
st.caption("Your personalized learning companion for Mathematics, Physics, and Chemistry")
st.info("Prototype for learning support. AI can make mistakes; verify important answers with your teacher or textbook. Do not enter private personal information.")

with st.sidebar:
    st.header("Your learning profile")
    nickname = st.text_input("Nickname (optional)")
    grade = st.selectbox("Class / grade", ["Class 6", "Class 7", "Class 8", "Class 9", "Class 10", "Class 11", "Class 12"])
    subject = st.selectbox("Subject", ["Mathematics", "Physics", "Chemistry", "General Science"])
    language = st.selectbox("Preferred language", ["English", "Telugu", "Hindi", "Kannada", "Tamil"])
    pace = st.selectbox("Explanation style", ["Simple and slow", "Balanced", "Detailed / challenge me"])

tabs = st.tabs(["Ask the Tutor", "Solve from Image", "Practice Quiz", "My Progress", "Study Plan"])

with tabs[0]:
    st.subheader("Ask a learning question")
    task = st.radio("What do you need?", ["Explain a concept", "Solve step by step", "Give an example", "Explain my mistake"], horizontal=True)
    question = st.text_area("Type your question", placeholder="Example: Explain Newton's second law with a simple example.")
    if st.button("Ask LearnMate", type="primary", key="ask"):
        if question.strip():
            show_ai(tutor_prompt(subject, grade, language, pace, task, question, st.session_state.get("performance", "")))
        else:
            st.warning("Type a question first.")

with tabs[1]:
    st.subheader("Read a handwritten question or diagram")
    image_file = st.file_uploader("Upload image", type=["png", "jpg", "jpeg", "webp"], key="image")
    image_question = st.text_area("What should the tutor do?", placeholder="Transcribe the question, then solve it step by step.")
    if image_file:
        st.image(image_file, caption="Uploaded image", use_container_width=True)
    if st.button("Read and explain image", type="primary", key="imgbtn"):
        if image_file:
            prompt = tutor_prompt(subject, grade, language, pace, "Image-based tutoring. Read visible text first, then explain.", image_question or "Transcribe and solve the question shown in the image.")
            show_ai(prompt, image_file.getvalue(), image_file.type or "image/jpeg")
        else:
            st.warning("Upload an image first.")

with tabs[2]:
    st.subheader("Practice quiz")
    topic = st.text_input("Quiz topic", placeholder="e.g., Linear equations, motion, acids and bases")
    count = st.slider("Number of questions", 3, 10, 5)
    difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Challenging"])
    if st.button("Generate quiz", type="primary", key="quiz"):
        if topic.strip():
            show_ai(f"Create a {count}-question {difficulty} multiple-choice quiz for {grade}, {subject}, topic {topic}. Respond in {language}. Four options per question. Put answer key and brief explanations after all questions. Verify calculations.")
        else:
            st.warning("Enter a topic.")
    st.markdown("#### Review answers")
    answers = st.text_area("Enter answers (example: 1-B, 2-D, 3-A)")
    if st.button("Review my answers", key="review"):
        if answers.strip():
            show_ai(f"Help review these quiz answers for {grade}, {subject}, in {language}: {answers}. If the questions and answer key are not available, ask the student to paste them; do not guess.")
        else:
            st.warning("Enter your answers first.")

with tabs[3]:
    st.subheader("Progress and rewards")
    if "topics" not in st.session_state:
        st.session_state["topics"] = []
    if "points" not in st.session_state:
        st.session_state["points"] = 0
    done = st.text_input("Topic you completed", placeholder="e.g., Fractions")
    if st.button("Mark complete", key="done"):
        if done.strip() and done.strip() not in st.session_state["topics"]:
            st.session_state["topics"].append(done.strip())
            st.session_state["points"] += 10
            st.success("Completed! +10 points")
    st.metric("Learning points", st.session_state["points"])
    if st.session_state["points"] >= 50:
        st.success("🏅 Curious Learner badge unlocked!")
    elif st.session_state["points"] >= 20:
        st.success("⭐ Practice Star badge unlocked!")
    else:
        st.info("Complete topics to earn points and badges.")
    for item in st.session_state["topics"]:
        st.write("✅", item)
    st.session_state["performance"] = st.text_area("Optional recent performance", placeholder="e.g., 4/5 correct; fractions are difficult.")

with tabs[4]:
    st.subheader("Personalized study plan")
    goal = st.text_input("Topic or exam goal", placeholder="e.g., Class 10 quadratic equations")
    days = st.slider("Plan length (days)", 3, 30, 7)
    minutes = st.slider("Study time per day (minutes)", 10, 120, 30, step=10)
    weak = st.text_area("Topics you find difficult (optional)")
    if st.button("Create study plan", type="primary", key="plan"):
        if goal.strip():
            show_ai(f"Create a realistic {days}-day study plan for {grade}, subject {subject}, in {language}. Goal: {goal}. Daily time: {minutes} minutes. Weak areas: {weak or 'not specified'}. Include daily goals, short activities, practice, revision checkpoints, and final self-assessment. Adapt to {pace}.")
        else:
            st.warning("Enter a goal.")

with st.expander("Included features and limitations"):
    st.markdown("""
**Included:** Gemini tutor, image question reading, grade/pace/language personalization, quiz generation, session-only points/badges, study plans.

**Not yet included:** speech-to-text, text-to-speech, permanent database, cross-student leaderboard, fine-tuned model, offline mode, and deployment. This uses a hosted Gemini model and is not fine-tuned. Verify important answers with a teacher/textbook.
""")
