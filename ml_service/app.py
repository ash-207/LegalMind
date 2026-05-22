from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from summarizer import summarize_text
from transcriber import transcribe_audio


app = FastAPI()


class SummaryRequest(BaseModel):
    text: str


@app.post("/summarize")
def summarize(request: SummaryRequest):

    summary = summarize_text(
        request.text
    )

    return {
        "summary": summary
    }

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):

    # Save temporary audio file
    temp_path = f"temp_{file.filename}"

    with open(temp_path, "wb") as buffer:
        buffer.write(await file.read())

    # Transcribe audio
    transcription = transcribe_audio(temp_path)

    return {
        "transcription": transcription
    }