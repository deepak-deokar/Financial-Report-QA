from app.pipelines.tatqa_ingestion_pipeline import ingest_tatqa_dataset
from app import config

if __name__ == "__main__":
    ingest_tatqa_dataset(config.TATQA_FILE)