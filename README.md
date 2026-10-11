# LearnMate AI Starter

Based on the uploaded AI-Powered Learning Companion for School Children problem statement.

## Windows / VS Code
1. Extract this ZIP and open `learnmate_ai_starter` in VS Code.
2. Open Terminal > New Terminal.
3. Run `python -m venv .venv`
4. Activate: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` then ` .\.venv\Scripts\Activate.ps1`
5. Install: `python -m pip install --upgrade pip`
6. Install packages: `python -m pip install -r requirements.txt`
7. Create `.env`: `Copy-Item .env.example .env`
8. Get your own key at https://aistudio.google.com/app/apikey and put it in `.env`. Never share or commit `.env`.
9. Run: `python -m streamlit run app.py`
10. Open the local URL shown (usually http://localhost:8501).

If `python` is not found, install Python 3.11/3.12 and check Add Python to PATH. If port 8501 is busy, use `python -m streamlit run app.py --server.port 8502`. If Gemini returns 401/403, check key/API access; if 404, update `GEMINI_MODEL` to a currently available model ID.

## Limitations
Prototype only. It is not fine-tuned and does not yet include voice input/output, permanent database, cross-student leaderboard, offline mode, or deployment. AI may make mistakes; students should verify answers with teachers/textbooks. Do not enter sensitive personal data.
