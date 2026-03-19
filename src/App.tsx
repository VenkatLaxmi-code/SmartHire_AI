/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { Download, Terminal, FileCode2, Play } from 'lucide-react';

export default function App() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans p-8">
      <div className="max-w-4xl mx-auto">
        <header className="mb-12 text-center">
          <h1 className="text-4xl font-bold tracking-tight text-slate-900 mb-4">
            AI Resume Screener Generated
          </h1>
          <p className="text-lg text-slate-600">
            Your Python Flask application has been successfully generated according to your specifications.
          </p>
        </header>

        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden mb-8">
          <div className="p-6 border-b border-slate-100 bg-slate-50/50 flex items-center gap-3">
            <FileCode2 className="w-6 h-6 text-indigo-600" />
            <h2 className="text-xl font-semibold">Project Structure</h2>
          </div>
          <div className="p-6 bg-slate-900 text-slate-300 font-mono text-sm overflow-x-auto">
            <pre>
{`AI_Resume_Screener/
├── app.py                 # Main Flask application
├── resume_parser.py       # PDF and DOCX text extraction
├── skill_extractor.py     # NLP-based skill extraction (spaCy)
├── ranking.py             # TF-IDF and Cosine Similarity logic
├── requirements.txt       # Python dependencies
├── templates/
│   ├── index.html         # Upload dashboard
│   └── results.html       # Ranking and analysis results
└── static/
    └── style.css          # Professional blue/white theme`}
            </pre>
          </div>
        </div>

        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden mb-8">
          <div className="p-6 border-b border-slate-100 bg-slate-50/50 flex items-center gap-3">
            <Terminal className="w-6 h-6 text-indigo-600" />
            <h2 className="text-xl font-semibold">How to Run Locally</h2>
          </div>
          <div className="p-6 space-y-6">
            <div className="space-y-2">
              <h3 className="font-medium text-slate-900 flex items-center gap-2">
                <span className="flex items-center justify-center w-6 h-6 rounded-full bg-indigo-100 text-indigo-700 text-sm font-bold">1</span>
                Download the Project
              </h3>
              <p className="text-slate-600 pl-8">
                Click the <strong className="text-slate-900">Export</strong> button in the top right corner of AI Studio and select <strong className="text-slate-900">Download ZIP</strong>. Extract the ZIP file on your computer.
              </p>
            </div>

            <div className="space-y-2">
              <h3 className="font-medium text-slate-900 flex items-center gap-2">
                <span className="flex items-center justify-center w-6 h-6 rounded-full bg-indigo-100 text-indigo-700 text-sm font-bold">2</span>
                Navigate to the Directory
              </h3>
              <div className="pl-8">
                <code className="block bg-slate-100 p-3 rounded-lg text-sm font-mono text-slate-800">
                  cd path/to/extracted/folder/AI_Resume_Screener
                </code>
              </div>
            </div>

            <div className="space-y-2">
              <h3 className="font-medium text-slate-900 flex items-center gap-2">
                <span className="flex items-center justify-center w-6 h-6 rounded-full bg-indigo-100 text-indigo-700 text-sm font-bold">3</span>
                Install Dependencies
              </h3>
              <p className="text-slate-600 pl-8 mb-2">It is recommended to use a virtual environment:</p>
              <div className="pl-8">
                <code className="block bg-slate-100 p-3 rounded-lg text-sm font-mono text-slate-800">
                  python -m venv venv<br/>
                  source venv/bin/activate  # On Windows use: venv\Scripts\activate<br/>
                  pip install -r requirements.txt<br/>
                  python -m spacy download en_core_web_sm
                </code>
              </div>
            </div>

            <div className="space-y-2">
              <h3 className="font-medium text-slate-900 flex items-center gap-2">
                <span className="flex items-center justify-center w-6 h-6 rounded-full bg-indigo-100 text-indigo-700 text-sm font-bold">4</span>
                Configure Email Settings (Optional)
              </h3>
              <p className="text-slate-600 pl-8">
                To enable the "Send Improvements to All Candidates" feature, open <code className="bg-slate-100 px-1 py-0.5 rounded text-sm font-mono">app.py</code> and update the SMTP settings with your email credentials. By default, it runs in simulation mode.
              </p>
            </div>

            <div className="space-y-2">
              <h3 className="font-medium text-slate-900 flex items-center gap-2">
                <span className="flex items-center justify-center w-6 h-6 rounded-full bg-indigo-100 text-indigo-700 text-sm font-bold">5</span>
                Run the Application
              </h3>
              <div className="pl-8">
                <code className="block bg-slate-100 p-3 rounded-lg text-sm font-mono text-slate-800">
                  python app.py
                </code>
                <p className="text-slate-600 mt-2">
                  Open your browser and navigate to <a href="http://localhost:5000" className="text-indigo-600 hover:underline" target="_blank" rel="noreferrer">http://localhost:5000</a>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
