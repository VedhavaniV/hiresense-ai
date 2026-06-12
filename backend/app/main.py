from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.matcher import analyze_match
from app.pdf_parser import PdfExtractionError, extract_text_from_pdf


class AnalyzeRequest(BaseModel):
    resume_text: str = Field(..., min_length=10)
    job_description: str = Field(..., min_length=10)


class AnalyzeResponse(BaseModel):
    score: int
    matched_skills: list[str]
    missing_skills: list[str]
    resume_skills: list[str]
    job_skills: list[str]
    roadmap: list[str]


app = FastAPI(
    title="HireSense AI",
    description="Open-source resume intelligence and job matching API.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/v1/analyze", response_model=AnalyzeResponse)
def analyze(payload: AnalyzeRequest) -> AnalyzeResponse:
    report = analyze_match(payload.resume_text, payload.job_description)
    return AnalyzeResponse(**report.__dict__)


@app.post("/api/v1/analyze-resume-file", response_model=AnalyzeResponse)
async def analyze_resume_file(
    resume_file: UploadFile = File(...),
    job_description: str = Form(..., min_length=10),
) -> AnalyzeResponse:
    if resume_file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF resume uploads are supported.")

    file_bytes = await resume_file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded PDF is empty.")

    try:
        resume_text = extract_text_from_pdf(file_bytes)
    except PdfExtractionError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    report = analyze_match(resume_text, job_description)
    return AnalyzeResponse(**report.__dict__)
