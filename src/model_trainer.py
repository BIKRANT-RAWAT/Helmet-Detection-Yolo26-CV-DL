from ultralytics import YOLO
import os
from src.utils import create_directories, file_exists, copy_file


class ModelTrainer:
    def __init__(self, config):
        self.config = config

    def train(self, data_yaml_path):
        model = YOLO("yolo26s.pt")

        results = model.train(
            data=data_yaml_path,
            epochs=self.config["training"]["epochs"],
            imgsz=self.config["training"]["imgsz"],
            batch=self.config["training"]["batch"],
            optimizer=self.config["training"]["optimizer"],
            lr0=self.config["training"]["lr0"],
            patience=self.config["training"]["patience"],
            amp=self.config["training"]["amp"],
            close_mosaic=self.config["training"]["close_mosaic"],
            project="runs",
            name=self.config["paths"]["project_name"],
            exist_ok=True
        )

        print("Training completed!")
        return results

    def save_best_model(self):
        best_path = os.path.join(
            "runs",
            self.config["paths"]["project_name"],
            "weights",
            "best.pt"
        )
    
        create_directories([self.config["paths"]["artifacts"]])
    
        save_path = os.path.join(
            self.config["paths"]["artifacts"],
            "best_helmet_model.pt"
        )
    
        if file_exists(best_path):
            copy_file(best_path, save_path)
            print(f"Best model saved at: {save_path}")
        else:
            print("best.pt not found!")