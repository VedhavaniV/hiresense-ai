import React, { useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import { ArrowRight, BrainCircuit, CheckCircle2, FileUp, Github, Loader2, Target, XCircle } from "lucide-react";
import "./styles.css";

type Analysis = {
  score: number;
  skill_score: number;
  semantic_score: number;
  scoring_method: string;
  matched_skills: string[];
  missing_skills: string[];
  resume_skills: string[];
  job_skills: string[];
  roadmap: string[];
};

const sampleResume = `AI & Data Science graduate with projects in Python, SQL, FastAPI, machine learning, pandas, Docker, and GitHub Actions. Built REST API services and worked with model evaluation.`;

const sampleJob = `We are hiring an AI Engineer with Python, SQL, FastAPI, Docker, Kubernetes, MLflow, AWS, CI/CD, machine learning, and data pipeline experience.`;

function App() {
  const [resumeText, setResumeText] = useState(sampleResume);
  const [jobDescription, setJobDescription] = useState(sampleJob);
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const apiUrl = useMemo(() => import.meta.env.VITE_API_URL || "http://localhost:8000", []);

  async function analyzeFit() {
    setIsLoading(true);
    setError("");

    try {
      const response = resumeFile ? await analyzeResumeFile() : await analyzeResumeText();

      if (!response.ok) {
        const message = await readErrorMessage(response);
        throw new Error(message);
      }

      const data = (await response.json()) as Analysis;
      setAnalysis(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setIsLoading(false);
    }
  }

  async function analyzeResumeText() {
    return fetch(`${apiUrl}/api/v1/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ resume_text: resumeText, job_description: jobDescription }),
    });
  }

  async function analyzeResumeFile() {
    const formData = new FormData();
    formData.append("resume_file", resumeFile as File);
    formData.append("job_description", jobDescription);

    return fetch(`${apiUrl}/api/v1/analyze-resume-file`, {
      method: "POST",
      body: formData,
    });
  }

  async function readErrorMessage(response: Response) {
    try {
      const payload = (await response.json()) as { detail?: string };
      return payload.detail || "Unable to analyze. Check that the backend is running.";
    } catch {
      return "Unable to analyze. Check that the backend is running.";
    }
  }

  return (
    <main className="app-shell">
      <section className="workspace">
        <aside className="sidebar">
          <div className="brand-row">
            <div className="brand-mark">
              <BrainCircuit size={23} aria-hidden="true" />
            </div>
            <div>
              <p className="eyebrow">Open-source AI career platform</p>
              <h1>HireSense AI</h1>
            </div>
          </div>

          <div className="metric-panel">
            <span className="metric-label">Overall Fit</span>
            <strong>{analysis ? `${analysis.score}%` : "--"}</strong>
            <div className="score-track">
              <span style={{ width: `${analysis?.score ?? 0}%` }} />
            </div>
          </div>

          <nav className="nav-list" aria-label="Project areas">
            <a href="#analyzer">Analyzer</a>
            <a href="#skills">Skill Gap</a>
            <a href="#roadmap">Roadmap</a>
            <a href="https://github.com" target="_blank" rel="noreferrer">
              <Github size={16} aria-hidden="true" /> GitHub
            </a>
          </nav>
        </aside>

        <section className="content">
          <header className="topbar">
            <div>
              <p className="eyebrow">MVP 0.1</p>
              <h2>Resume-to-job intelligence dashboard</h2>
            </div>
            <button className="primary-button" onClick={analyzeFit} disabled={isLoading}>
              {isLoading ? <Loader2 className="spin" size={18} /> : <Target size={18} />}
              Analyze Fit
            </button>
          </header>

          <section className="input-grid" id="analyzer">
            <label>
              <span>Resume Text</span>
              <textarea value={resumeText} onChange={(event) => setResumeText(event.target.value)} />
            </label>
            <label>
              <span>Job Description</span>
              <textarea value={jobDescription} onChange={(event) => setJobDescription(event.target.value)} />
            </label>
          </section>

          <section className="upload-panel">
            <div>
              <div className="section-title compact">
                <h3>Resume PDF Upload</h3>
                <FileUp size={18} aria-hidden="true" />
              </div>
              <p>{resumeFile ? resumeFile.name : "Pasted resume text mode"}</p>
            </div>
            <input
              type="file"
              accept="application/pdf"
              onChange={(event) => setResumeFile(event.target.files?.[0] ?? null)}
            />
            {resumeFile && (
              <button className="secondary-button" onClick={() => setResumeFile(null)} type="button">
                Clear PDF
              </button>
            )}
          </section>

          {error && <div className="error-box">{error}</div>}

          <section className="score-grid">
            <ScoreCard label="Skill Score" value={analysis?.skill_score} />
            <ScoreCard label="Semantic Score" value={analysis?.semantic_score} />
            <ScoreCard label="Overall Score" value={analysis?.score} />
          </section>

          <section className="results-grid" id="skills">
            <ResultPanel
              title="Matched Skills"
              icon={<CheckCircle2 size={18} />}
              items={analysis?.matched_skills ?? []}
              empty="Run analysis to see aligned skills."
              tone="positive"
            />
            <ResultPanel
              title="Missing Skills"
              icon={<XCircle size={18} />}
              items={analysis?.missing_skills ?? []}
              empty="Run analysis to see skill gaps."
              tone="warning"
            />
          </section>

          <section className="roadmap-panel" id="roadmap">
            <div className="section-title">
              <h3>Learning Roadmap</h3>
              <ArrowRight size={18} aria-hidden="true" />
            </div>
            <ul>
              {(analysis?.roadmap ?? ["Run an analysis to generate a focused learning roadmap."]).map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </section>
        </section>
      </section>
    </main>
  );
}

function ScoreCard({ label, value }: { label: string; value?: number }) {
  return (
    <article className="score-card">
      <span>{label}</span>
      <strong>{value === undefined ? "--" : `${value}%`}</strong>
    </article>
  );
}

function ResultPanel({
  title,
  icon,
  items,
  empty,
  tone,
}: {
  title: string;
  icon: React.ReactNode;
  items: string[];
  empty: string;
  tone: "positive" | "warning";
}) {
  return (
    <article className={`result-panel ${tone}`}>
      <div className="section-title">
        <h3>{title}</h3>
        {icon}
      </div>
      {items.length ? (
        <div className="chip-list">
          {items.map((item) => (
            <span key={item}>{item}</span>
          ))}
        </div>
      ) : (
        <p className="empty-state">{empty}</p>
      )}
    </article>
  );
}

createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
