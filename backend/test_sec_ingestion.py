# test_tatqa_ingestion.py

from app.pipelines.tatqa_ingestion_pipeline import ingest_tatqa_dataset

if __name__ == "__main__":
    file_path = "../datasets/tatqa/tatqa_dataset_train.json"
    ingest_tatqa_dataset(file_path)