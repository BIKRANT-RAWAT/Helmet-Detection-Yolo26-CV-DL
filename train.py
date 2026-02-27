import os
from dotenv import load_dotenv
from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataPreprocessing
from src.model_trainer import ModelTrainer
from src.utils import load_yaml


if __name__ == "__main__":

    # Load .env file
    load_dotenv()

    # Get API key from environment
    ROBOFLOW_API_KEY = os.getenv("ROBOFLOW_API_KEY")

    if ROBOFLOW_API_KEY is None:
        raise ValueError("ROBOFLOW_API_KEY not found in .env file")

    # Load config
    config = load_yaml("config/config.yaml")

    # ---------------------
    # Data Ingestion
    # ---------------------
    ingestion = DataIngestion(config, ROBOFLOW_API_KEY)
    dataset_path = ingestion.download_dataset()

    # ---------------------
    # Data Preprocessing
    # ---------------------
    preprocessing = DataPreprocessing(dataset_path)
    preprocessing.process_labels()
    preprocessing.update_yaml()

    # ---------------------
    # Model Training
    # ---------------------
    trainer = ModelTrainer(config)
    trainer.train(os.path.join(dataset_path, "data.yaml"))
    trainer.save_best_model()