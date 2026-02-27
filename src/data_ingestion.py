from roboflow import Roboflow
import yaml
import os


class DataIngestion:
    def __init__(self, config, api_key):
        self.config = config
        self.api_key = api_key

    def download_dataset(self):
        rf = Roboflow(api_key=self.api_key)

        project = rf.workspace(
            self.config["roboflow"]["workspace"]
        ).project(self.config["roboflow"]["project"])

        version = project.version(self.config["roboflow"]["version"])

        dataset = version.download(
            self.config["roboflow"]["format"],
            location=self.config["paths"]["dataset_root"]
        )

        print("Dataset downloaded successfully!")
        return dataset.location