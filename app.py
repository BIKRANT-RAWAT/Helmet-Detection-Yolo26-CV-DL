import os
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from src.inference import HelmetPredictor

app = FastAPI(title="Helmet Detection API 🚀")

MODEL_PATH = "artifacts/best_helmet_model.pt"
predictor = HelmetPredictor(MODEL_PATH)

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.get("/")
def home():
    return {"message": "Helmet Detection API Running 🚀"}


@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):

    input_path = os.path.join(UPLOAD_DIR, file.filename)
    output_path = os.path.join(OUTPUT_DIR, f"pred_{file.filename}")

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    predictor.predict_and_save(input_path, output_path)

    return FileResponse(output_path, media_type="image/jpeg")