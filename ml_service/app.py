from fastapi import FastAPI
from pydantic import BaseModel

from summarizer import summarize_text

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