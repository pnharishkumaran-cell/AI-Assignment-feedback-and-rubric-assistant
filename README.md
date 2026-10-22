📝 AI Assignment Feedback & Rubric Assistant

An AI-powered application that evaluates student assignments using Google Gemini and a customizable weighted rubric. Students can upload a PDF or enter their assignment text manually to receive scores, constructive feedback, strengths, and suggestions for improvement.

🚀 Features

- PDF Upload: Upload text-based PDF assignments.
- Text Extraction: Extract assignment text from PDFs using "pypdf".
- Manual Submission: Enter or paste assignment text directly.
- AI-Powered Evaluation: Generate assignment feedback using the Google Gemini API.
- Customizable Rubric: Adjust weights for Accuracy, Completeness, Clarity, and Originality.
- Weighted Scoring: Calculate marks based on rubric scores and weights.
- Detailed Feedback: Receive criterion-wise explanations, strengths, and improvement suggestions.
- JSON Export: Download the evaluation report as a JSON file.
- Input Validation: Validate assignment details, rubric weights, and AI-generated scores.

🛠️ Tech Stack

Technology| Purpose
Python| Application logic
Streamlit| Frontend and user interface
Google Gemini API| AI-based assignment evaluation
pypdf| Extract text from PDF files
python-dotenv| Load environment variables
JSON| Store and download evaluation reports

📂 Project Structure

Ai Assignment Feedback and Rubric Assistant/
│
├── app.py              # Streamlit frontend
├── backend.py          # Gemini API and evaluation logic
├── rubric.py           # Weighted rubric calculation
├── test_backend.py     # Offline backend tests
├── requirements.txt    # Python dependencies
├── .env                # Gemini API key (keep private)
├── .gitignore          # Files excluded from Git
└── README.md           # Project documentation

⚙️ Installation and Setup

1. Clone the repository

git clone <YOUR_GITHUB_REPOSITORY_URL>
cd "Ai Assignment Feedback and Rubric Assistant"

Alternatively, open your existing project folder in VS Code.

2. Create a virtual environment

For the Windows x64 Python environment used during development:

python -m venv .venv-x64

Activate it in PowerShell:

.\.venv-x64\Scripts\Activate.ps1

If PowerShell blocks activation, you can run the environment's Python executable directly instead.

3. Install dependencies

.\.venv-x64\Scripts\python.exe -m pip install -r requirements.txt

If the dependencies are not yet listed in "requirements.txt", install them with:

.\.venv-x64\Scripts\python.exe -m pip install streamlit google-genai python-dotenv pypdf

4. Configure the Gemini API key

Get an API key from "Google AI Studio" (https://aistudio.google.com/apikey).

Create a ".env" file in the project root:

GEMINI_API_KEY=your_actual_api_key

The application uses this key to authenticate requests to the Gemini API.

Security: Never commit your ".env" file or expose your API key publicly.

5. Run the application

.\.venv-x64\Scripts\python.exe -m streamlit run app.py

Streamlit will provide a local URL, usually:

http://localhost:8501

Open the URL in your browser to use the application.

📖 How to Use

1. Launch the application.
2. Enter the assignment title and optionally the student's name.
3. Set the maximum marks.
4. Configure the rubric weights.
5. Choose Upload PDF or Enter text manually.
6. If using a PDF, upload the file and review the extracted text.
7. Optionally provide additional evaluation instructions.
8. Click Evaluate Assignment.
9. Review the total score, criterion-wise marks, strengths, and improvement suggestions.
10. Download the report as a JSON file if needed.

📊 Evaluation Rubric

The default rubric contains four criteria:

Criterion| Default Weight
Accuracy| 40%
Completeness| 30%
Clarity| 20%
Originality| 10%
Total| 100%

The weights can be customized, but they must total exactly 100%.

Weighted Marks Formula

For each criterion:

Criterion Marks =
(Score Percentage / 100)
× (Rubric Weight / 100)
× Maximum Marks

The final score is the sum of the marks earned across all criteria.

🧪 Testing

Run the offline backend tests with:

.\.venv-x64\Scripts\python.exe test_backend.py

These tests can check application logic without making live Gemini API requests, depending on the test cases implemented in "test_backend.py".

For end-to-end testing, run the application and evaluate a sample assignment. This requires a valid API key and working Gemini API access.

⚠️ Limitations

- Scanned PDFs containing only images are not supported without OCR.
- PDF text extraction may not preserve complex tables, diagrams, mathematical notation, or formatting perfectly.
- Very long assignments may exceed the application's configured text limit.
- AI-generated scores and feedback may contain mistakes and should be reviewed by a human before official grading.
- The Originality score is an AI assessment, not proof of plagiarism or verified authorship.
- Gemini API access, model availability, rate limits, and charges depend on your Google AI Studio configuration and applicable terms.

🔮 Future Improvements

- OCR support for scanned PDFs.
- Support for additional file formats, such as DOCX.
- Assignment history and database integration.
- Student and teacher dashboards.
- Export reports to PDF.
- More flexible rubric criteria.
- Authentication and role-based access.
- Automated testing and deployment.

🔐 Security Notes

- Keep API keys in environment variables.
- Exclude ".env" and virtual environment folders from Git.
- Avoid uploading confidential student submissions without appropriate authorization.
- Review AI-generated feedback before using it for official academic decisions.

👨‍💻 Author

Hariz

Built as an AI and Data Science project to explore AI-powered academic evaluation, backend development, API integration, and rubric-based scoring.
