from app.pipelines.finqa_ingestion_pipeline import ingest_finqa_dataset
from app import config

if __name__ == "__main__":
    ingest_finqa_dataset(config.FINQA_FILE)