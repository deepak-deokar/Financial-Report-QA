# backend/app/api.py

from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os

from app.services.hybrid_rag_pipeline import HybridRAGAgentPipeline
from app.services.insight_generator import InsightGenerator
from app.services.table_qa import run_table_qa
from app.utils.document_loader import ingest_document

# --- Initialize FastAPI Router ---
router = APIRouter()

# --- Initialize Pipelines ---
pipeline = HybridRAGAgentPipeline()
insight_generator = InsightGenerator(collection_name="default")   # << INIT ONCE

# --- Upload Endpoint ---
@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    upload_dir = "./uploads"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    print(f"[UPLOAD] File saved to {file_path}")

    # Ingest the document
    ingest_document(file_path)

    return JSONResponse({"message": "File uploaded and ingested successfully.", "file_path": file_path})

# --- Hybrid RAG QA Endpoint ---
class QARequest(BaseModel):
    question: str

@router.post("/hybrid_rag")
async def hybrid_rag_endpoint(request: QARequest):
    print(f"[API] Hybrid RAG question: {request.question}")

    response = pipeline.run(request.question)

    return JSONResponse({"question": request.question, "answer": response})

# --- Insights Endpoint ---
class InsightRequest(BaseModel):
    question: str

@router.post("/insights")
async def insights_endpoint(request: InsightRequest):
    print(f"[API] Insights question: {request.question}")

    # FIXED: use class method
    response = insight_generator.generate_insights(request.question)

    return JSONResponse({"question": request.question, "insights": response})

# --- Table QA Endpoint ---
class TableQARequest(BaseModel):
    file_path: str
    question: str

@router.post("/table_qa")
async def table_qa_endpoint(request: TableQARequest):
    print(f"[API] Table QA: {request.file_path}, Q: {request.question}")

    response = run_table_qa(request.file_path, request.question)

    return JSONResponse({"file_path": request.file_path, "question": request.question, "answer": response})