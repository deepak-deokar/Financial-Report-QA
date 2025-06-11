from app.pipelines.sec_ingestion_pipeline_summary import ingest_sec_dataset

if __name__ == "__main__":
    root = "../datasets/sec_filings/raw/sec-edgar-filings/META"
    ingest_sec_dataset(root_folder=root, max_files=15)  # adjust as needed