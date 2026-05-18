"""
Legal AI Platform — Court Hearing Transcriber
Uses OpenAI Whisper for audio transcription with speaker diarization support.
"""

import os
import json
import whisper
import tempfile
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional
import warnings
warnings.filterwarnings("ignore")


# ─── Data Models ──────────────────────────────────────────────────────────────

@dataclass
class TranscriptSegment:
    start: float          # seconds
    end: float            # seconds
    text: str
    speaker: Optional[str] = None   # filled if diarization enabled


@dataclass
class TranscriptionResult:
    file_name: str
    language: str
    duration: float       # seconds
    full_text: str
    segments: list[TranscriptSegment]
    model_used: str


# ─── Transcriber ──────────────────────────────────────────────────────────────

class LegalTranscriber:
    """
    Wraps OpenAI Whisper for legal audio transcription.
    Supports: mp3, mp4, wav, m4a, ogg, flac, webm
    """

    SUPPORTED_FORMATS = {".mp3", ".mp4", ".wav", ".m4a", ".ogg", ".flac", ".webm"}

    def __init__(self, model_size: str = "base"):
        """
        model_size options:
          tiny   — fastest, least accurate (~1GB VRAM)
          base   — good balance (default)
          small  — better accuracy
          medium — high accuracy
          large  — best accuracy, slowest
        """
        print(f"[Transcriber] Loading Whisper model: {model_size}")
        self.model = whisper.load_model(model_size)
        self.model_size = model_size
        print(f"[Transcriber] Model ready.")

    def transcribe(
        self,
        audio_path: str,
        language: str = None,        # None = auto-detect; "en", "hi", etc.
        translate_to_english: bool = False,
    ) -> TranscriptionResult:
        """
        Transcribe audio file. Returns structured TranscriptionResult.

        Args:
            audio_path: Path to audio file
            language: Force language (None = auto-detect)
            translate_to_english: Translate non-English audio to English
        """
        path = Path(audio_path)

        if not path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        if path.suffix.lower() not in self.SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported format: {path.suffix}. "
                f"Supported: {self.SUPPORTED_FORMATS}"
            )

        print(f"[Transcriber] Transcribing: {path.name}")

        # Whisper options
        options = {
            "word_timestamps": False,
            "verbose": False,
        }
        if language:
            options["language"] = language
        if translate_to_english:
            options["task"] = "translate"

        result = self.model.transcribe(str(path), **options)

        # Build segments
        segments = []
        for seg in result.get("segments", []):
            segments.append(TranscriptSegment(
                start=round(seg["start"], 2),
                end=round(seg["end"], 2),
                text=seg["text"].strip(),
            ))

        # Compute duration from last segment
        duration = segments[-1].end if segments else 0.0

        return TranscriptionResult(
            file_name=path.name,
            language=result.get("language", "unknown"),
            duration=duration,
            full_text=result["text"].strip(),
            segments=segments,
            model_used=self.model_size,
        )

    def transcribe_with_speakers(
        self,
        audio_path: str,
        speaker_labels: dict[str, str] = None,
        language: str = None,
    ) -> TranscriptionResult:
        """
        Transcribe + assign speaker labels based on time ranges.

        speaker_labels format:
        {
            "Judge":    [(0, 120), (300, 450)],     # (start_sec, end_sec)
            "Lawyer1":  [(120, 300)],
            "Lawyer2":  [(450, 600)],
        }

        If speaker_labels is None, segments won't have speaker tags.
        """
        result = self.transcribe(audio_path, language=language)

        if speaker_labels:
            result.segments = self._assign_speakers(result.segments, speaker_labels)

        return result

    def _assign_speakers(
        self,
        segments: list[TranscriptSegment],
        speaker_labels: dict[str, list[tuple]],
    ) -> list[TranscriptSegment]:
        """Map speaker names onto segments by time overlap."""
        for seg in segments:
            seg_mid = (seg.start + seg.end) / 2
            for speaker, ranges in speaker_labels.items():
                for (start, end) in ranges:
                    if start <= seg_mid <= end:
                        seg.speaker = speaker
                        break
        return segments

    def to_json(self, result: TranscriptionResult, output_path: str = None) -> str:
        """Export TranscriptionResult to JSON string (and optionally save file)."""
        data = asdict(result)
        json_str = json.dumps(data, indent=2, ensure_ascii=False)

        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(json_str)
            print(f"[Transcriber] Saved JSON: {output_path}")

        return json_str

    def to_text(self, result: TranscriptionResult, output_path: str = None) -> str:
        """Export readable transcript with speaker labels and timestamps."""
        lines = []
        lines.append(f"=== LEGAL HEARING TRANSCRIPT ===")
        lines.append(f"File     : {result.file_name}")
        lines.append(f"Language : {result.language}")
        lines.append(f"Duration : {result.duration:.1f}s ({result.duration/60:.1f} min)")
        lines.append(f"Model    : {result.model_used}")
        lines.append("=" * 40)
        lines.append("")

        for seg in result.segments:
            timestamp = f"[{self._fmt_time(seg.start)} → {self._fmt_time(seg.end)}]"
            speaker = f"{seg.speaker}: " if seg.speaker else ""
            lines.append(f"{timestamp} {speaker}{seg.text}")

        text = "\n".join(lines)

        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"[Transcriber] Saved transcript: {output_path}")

        return text

    @staticmethod
    def _fmt_time(seconds: float) -> str:
        m, s = divmod(int(seconds), 60)
        return f"{m:02d}:{s:02d}"


# ─── FastAPI Endpoint (plug into your backend) ─────────────────────────────────

def create_fastapi_router():
    """
    Returns a FastAPI router with /transcribe endpoint.
    Partner can mount this in main FastAPI app.
    """
    try:
        from fastapi import APIRouter, UploadFile, File, Form, HTTPException
        from fastapi.responses import JSONResponse
    except ImportError:
        print("FastAPI not installed. Run: pip install fastapi")
        return None

    router = APIRouter(prefix="/api/ai", tags=["transcription"])
    transcriber = LegalTranscriber(model_size="base")

    @router.post("/transcribe")
    async def transcribe_audio(
        file: UploadFile = File(...),
        language: str = Form(default=None),
        translate_to_english: bool = Form(default=False),
    ):
        """
        Upload audio file → get transcript JSON back.
        Accepts: mp3, wav, m4a, mp4, ogg, flac, webm
        """
        suffix = Path(file.filename).suffix.lower()
        if suffix not in LegalTranscriber.SUPPORTED_FORMATS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported format: {suffix}"
            )

        # Save upload to temp file
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        try:
            result = transcriber.transcribe(
                tmp_path,
                language=language,
                translate_to_english=translate_to_english,
            )
            return JSONResponse(content={
                "status": "success",
                "data": {
                    "file_name": result.file_name,
                    "language": result.language,
                    "duration": result.duration,
                    "full_text": result.full_text,
                    "segments": [
                        {
                            "start": s.start,
                            "end": s.end,
                            "text": s.text,
                            "speaker": s.speaker,
                        }
                        for s in result.segments
                    ],
                    "model_used": result.model_used,
                }
            })
        finally:
            os.unlink(tmp_path)

    return router

    # ─── Simple Wrapper Function ──────────────────────────────────────────────────

def transcribe_audio(file_path: str) -> str:
    """
    Simple interface required by external modules.

    Input:
        file_path (str) -> path to audio file

    Returns:
        str -> full transcript text
    """

    transcriber = LegalTranscriber(
        model_size="base"
    )

    result = transcriber.transcribe(file_path)

    # IMPORTANT:
    # Return STRING only
    # Do NOT print anything
    return result.full_text


# ─── Quick Test ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python transcriber.py <audio_file>")
        print("Example: python transcriber.py hearing.mp3")
        sys.exit(1)

    audio_file = sys.argv[1]
    model = sys.argv[2] if len(sys.argv) > 2 else "base"

    t = LegalTranscriber(model_size=model)
    result = t.transcribe(audio_file)

    # Print readable transcript
    print(t.to_text(result))

    # Save JSON
    out_json = audio_file.rsplit(".", 1)[0] + "_transcript.json"
    t.to_json(result, output_path=out_json)
    print(f"\nJSON saved: {out_json}")
