"""
Legal AI Platform — Hearing Summarizer
Takes TranscriptionResult (or raw text) → extracts structured legal intelligence.

LLM backend: Gemini API (default) | swap for Mistral/Ollama easily.
"""

import os
import json
import re
from dataclasses import dataclass, asdict, field
from typing import Optional
from datetime import datetime


# ─── Data Models ──────────────────────────────────────────────────────────────

@dataclass
class ActionItem:
    task: str                          # What must be done
    assigned_to: str                   # "Defendant Lawyer", "Plaintiff", "Judge", etc.
    deadline: Optional[str] = None     # "14 days", "2024-03-15", "Next hearing", etc.
    priority: str = "medium"           # low | medium | high | critical
    source_quote: Optional[str] = None # Original line that triggered this


@dataclass
class KeyDecision:
    decision: str
    made_by: str                       # "Judge", "Both parties", etc.
    timestamp_hint: Optional[str] = None


@dataclass
class HearingSummary:
    case_id: Optional[str]
    hearing_date: Optional[str]
    court: Optional[str]
    parties: list[str]                 # ["Plaintiff: XYZ Corp", "Defendant: ABC Ltd"]
    judges: list[str]
    lawyers: list[str]

    # Core intelligence
    summary: str                       # 3-5 sentence plain English summary
    key_decisions: list[KeyDecision]
    action_items: list[ActionItem]
    next_hearing_date: Optional[str]
    next_hearing_court: Optional[str]

    # Risk signals
    risk_flags: list[str]              # ["Missing evidence mentioned", "Contempt warning issued"]
    legal_sections_cited: list[str]    # ["IPC 302", "CrPC 164", "Article 21"]

    # Meta
    sentiment: str                     # "Favorable for plaintiff" | "Neutral" | "Contentious"
    generated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


# ─── Prompt Builder ───────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are an expert Indian legal AI assistant embedded in a court hearing intelligence platform.
You analyze court hearing transcripts and extract structured legal intelligence.
Always respond ONLY with valid JSON. No markdown, no explanation, no preamble.
Be precise. Use plain English in summaries. Infer speaker roles from context."""

def build_extraction_prompt(transcript_text: str, case_context: dict = None) -> str:
    context_block = ""
    if case_context:
        context_block = f"\nCase Context:\n{json.dumps(case_context, indent=2)}\n"

    return f"""Analyze this court hearing transcript and extract structured legal intelligence.
{context_block}
TRANSCRIPT:
\"\"\"
{transcript_text[:12000]}
\"\"\"

Return ONLY this JSON structure (no markdown, no extra text):
{{
  "case_id": "string or null",
  "hearing_date": "YYYY-MM-DD or descriptive string or null",
  "court": "court name or null",
  "parties": ["Plaintiff: Name", "Defendant: Name"],
  "judges": ["Judge name"],
  "lawyers": ["Lawyer name - side"],
  "summary": "3-5 sentence plain English summary of what happened in this hearing",
  "key_decisions": [
    {{
      "decision": "What was decided",
      "made_by": "Who decided",
      "timestamp_hint": "approximate time in transcript or null"
    }}
  ],
  "action_items": [
    {{
      "task": "Specific action required",
      "assigned_to": "Who must do it",
      "deadline": "Deadline string or null",
      "priority": "low|medium|high|critical",
      "source_quote": "Exact or near-exact quote that triggered this"
    }}
  ],
  "next_hearing_date": "Date string or null",
  "next_hearing_court": "Court name or null",
  "risk_flags": ["Risk signal 1", "Risk signal 2"],
  "legal_sections_cited": ["IPC 302", "CrPC 164"],
  "sentiment": "Favorable for plaintiff|Favorable for defendant|Neutral|Contentious|Mixed"
}}"""


# ─── LLM Backend ──────────────────────────────────────────────────────────────

# class GeminiBackend:
#     """Calls Google Gemini API."""

#     def __init__(self, api_key: str = None, model: str = "gemini-1.5-flash"):
#         try:
#             import google.generativeai as genai
#         except ImportError:
#             raise ImportError("Run: pip install google-generativeai")

#         self.genai = genai
#         key = api_key or os.environ.get("GEMINI_API_KEY")
#         if not key:
#             raise ValueError("GEMINI_API_KEY not set")
#         genai.configure(api_key=key)
#         self.model = genai.GenerativeModel(
#             model_name=model,
#             system_instruction=SYSTEM_PROMPT,
#         )

#     def complete(self, prompt: str) -> str:
#         response = self.model.generate_content(prompt)
#         return response.text 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
class GeminiBackend:
    def __init__(self, api_key: str = None, model: str = "gemini-2.0-flash"):
        try:
            from google import genai
        except ImportError:
            raise ImportError("Run: pip install google-genai")

        key = api_key or os.environ.get("GEMINI_API_KEY")
        if not key:
            raise ValueError("GEMINI_API_KEY not set")
        self.client = genai.Client(api_key=key)
        self.model = model

    def complete(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=SYSTEM_PROMPT + "\n\n" + prompt,
        )
        return response.text

class OllamaBackend:
    """
    Local Ollama backend (free, no API key).
    Run: ollama pull mistral  OR  ollama pull llama3
    """

    def __init__(self, model: str = "mistral", base_url: str = "http://localhost:11434"):
        try:
            import requests
            self.requests = requests
        except ImportError:
            raise ImportError("Run: pip install requests")
        self.model = model
        self.base_url = base_url

    def complete(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            "stream": False,
            "format": "json",  # force JSON output
        }
        resp = self.requests.post(
            f"{self.base_url}/api/chat",
            json=payload,
            timeout=120,
        )
        resp.raise_for_status()
        return resp.json()["message"]["content"]


class OpenAIBackend:
    """OpenAI / any OpenAI-compatible API (Together, Groq, etc.)."""

    def __init__(
        self,
        api_key: str = None,
        model: str = "gpt-4o-mini",
        base_url: str = None,  # Override for Together/Groq/etc.
    ):
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("Run: pip install openai")

        key = api_key or os.environ.get("OPENAI_API_KEY")
        kwargs = {"api_key": key}
        if base_url:
            kwargs["base_url"] = base_url
        self.client = OpenAI(**kwargs)
        self.model = model

    def complete(self, prompt: str) -> str:
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.1,
        )
        return resp.choices[0].message.content


# ─── Main Summarizer ──────────────────────────────────────────────────────────

class LegalSummarizer:
    """
    Orchestrates: transcript text → HearingSummary.

    Usage:
        summarizer = LegalSummarizer(backend="gemini")
        summary = summarizer.summarize(transcript_text)
        print(summary.action_items)
    """

    BACKENDS = {
        "gemini": GeminiBackend,
        "ollama": OllamaBackend,
        "openai": OpenAIBackend,
    }

    def __init__(self, backend: str = "gemini", **backend_kwargs):
        if backend not in self.BACKENDS:
            raise ValueError(f"backend must be one of: {list(self.BACKENDS.keys())}")
        print(f"[Summarizer] Using backend: {backend}")
        self.llm = self.BACKENDS[backend](**backend_kwargs)

    def summarize(
        self,
        transcript_text: str,
        case_context: dict = None,
    ) -> HearingSummary:
        """
        Main method. Pass raw transcript string.

        case_context (optional): dict with known info to help LLM
        {
            "case_id": "CRL/2024/001",
            "case_title": "State vs. Ravi Kumar",
            "court": "Delhi High Court",
        }
        """
        prompt = build_extraction_prompt(transcript_text, case_context)

        print("[Summarizer] Sending to LLM...")
        raw = self.llm.complete(prompt)

        data = self._parse_json(raw)
        return self._build_summary(data)

    def summarize_from_segments(
        self,
        segments: list,          # list of TranscriptSegment (from transcriber.py)
        case_context: dict = None,
    ) -> HearingSummary:
        """
        Accepts segments from TranscriptionResult directly.
        Formats with speaker labels before sending to LLM.
        """
        lines = []
        for seg in segments:
            speaker = f"{seg.speaker}: " if getattr(seg, "speaker", None) else ""
            time = f"[{seg.start:.0f}s] "
            lines.append(f"{time}{speaker}{seg.text}")
        transcript_text = "\n".join(lines)
        return self.summarize(transcript_text, case_context)

    def _parse_json(self, raw: str) -> dict:
        """Robust JSON parser — strips markdown fences if LLM disobeys."""
        text = raw.strip()
        # Strip ```json ... ``` fences
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise ValueError(f"LLM returned invalid JSON: {e}\nRaw:\n{raw[:500]}")

    def _build_summary(self, data: dict) -> HearingSummary:
        """Map raw dict → typed HearingSummary dataclass."""
        key_decisions = [
            KeyDecision(**kd) for kd in data.get("key_decisions", [])
        ]
        action_items = [
            ActionItem(**ai) for ai in data.get("action_items", [])
        ]
        return HearingSummary(
            case_id=data.get("case_id"),
            hearing_date=data.get("hearing_date"),
            court=data.get("court"),
            parties=data.get("parties", []),
            judges=data.get("judges", []),
            lawyers=data.get("lawyers", []),
            summary=data.get("summary", ""),
            key_decisions=key_decisions,
            action_items=action_items,
            next_hearing_date=data.get("next_hearing_date"),
            next_hearing_court=data.get("next_hearing_court"),
            risk_flags=data.get("risk_flags", []),
            legal_sections_cited=data.get("legal_sections_cited", []),
            sentiment=data.get("sentiment", "Neutral"),
        )

    def to_json(self, summary: HearingSummary, output_path: str = None) -> str:
        json_str = json.dumps(asdict(summary), indent=2, ensure_ascii=False)
        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(json_str)
            print(f"[Summarizer] Saved: {output_path}")
        return json_str

    def to_text(self, summary: HearingSummary) -> str:
        """Human-readable summary report."""
        lines = [
            "=" * 50,
            "  LEGAL HEARING INTELLIGENCE REPORT",
            "=" * 50,
            f"Case ID      : {summary.case_id or 'Unknown'}",
            f"Date         : {summary.hearing_date or 'Unknown'}",
            f"Court        : {summary.court or 'Unknown'}",
            f"Parties      : {', '.join(summary.parties) or 'Unknown'}",
            f"Judge(s)     : {', '.join(summary.judges) or 'Unknown'}",
            f"Sentiment    : {summary.sentiment}",
            "",
            "── SUMMARY ─────────────────────────────────",
            summary.summary,
            "",
            "── KEY DECISIONS ───────────────────────────",
        ]
        for i, kd in enumerate(summary.key_decisions, 1):
            lines.append(f"  {i}. [{kd.made_by}] {kd.decision}")

        lines += ["", "── ACTION ITEMS ────────────────────────────"]
        for i, ai in enumerate(summary.action_items, 1):
            deadline = f" | Due: {ai.deadline}" if ai.deadline else ""
            lines.append(f"  {i}. [{ai.priority.upper()}] {ai.task}")
            lines.append(f"     → Assigned: {ai.assigned_to}{deadline}")
            if ai.source_quote:
                lines.append(f"     → Source: \"{ai.source_quote}\"")

        lines += ["", "── RISK FLAGS ──────────────────────────────"]
        for flag in summary.risk_flags:
            lines.append(f"  ⚠ {flag}")

        lines += ["", "── LEGAL SECTIONS CITED ────────────────────"]
        lines.append("  " + ", ".join(summary.legal_sections_cited) if summary.legal_sections_cited else "  None detected")

        if summary.next_hearing_date:
            lines += [
                "",
                "── NEXT HEARING ────────────────────────────",
                f"  Date  : {summary.next_hearing_date}",
                f"  Court : {summary.next_hearing_court or 'Same court'}",
            ]

        lines.append("=" * 50)
        return "\n".join(lines)


# ─── FastAPI Router ───────────────────────────────────────────────────────────

def create_fastapi_router(backend: str = "gemini", **backend_kwargs):
    """Mount this in your main FastAPI app alongside transcriber router."""
    try:
        from fastapi import APIRouter, HTTPException
        from fastapi.responses import JSONResponse
        from pydantic import BaseModel
    except ImportError:
        print("FastAPI not installed.")
        return None

    router = APIRouter(prefix="/api/ai", tags=["summarization"])
    summarizer = LegalSummarizer(backend=backend, **backend_kwargs)

    class SummarizeRequest(BaseModel):
        transcript_text: str
        case_context: dict = None

    @router.post("/summarize")
    async def summarize_hearing(req: SummarizeRequest):
        """
        POST /api/ai/summarize
        Body: { "transcript_text": "...", "case_context": {...} }
        Returns: HearingSummary JSON
        """
        if len(req.transcript_text.strip()) < 50:
            raise HTTPException(status_code=400, detail="Transcript too short")

        try:
            summary = summarizer.summarize(req.transcript_text, req.case_context)
            return JSONResponse(content={
                "status": "success",
                "data": asdict(summary),
            })
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return router


# ─── Pipeline: Transcribe → Summarize ────────────────────────────────────────

def transcribe_and_summarize(
    audio_path: str,
    llm_backend: str = "gemini",
    whisper_model: str = "base",
    case_context: dict = None,
    **backend_kwargs,
) -> tuple:
    """
    Full pipeline: audio file → (TranscriptionResult, HearingSummary)

    Example:
        transcript, summary = transcribe_and_summarize(
            "hearing.mp3",
            llm_backend="gemini",
            case_context={"case_id": "CRL/2024/001"}
        )
    """
    # Import here to avoid circular dependency
    from transcriber import LegalTranscriber

    t = LegalTranscriber(model_size=whisper_model)
    transcript = t.transcribe(audio_path)

    s = LegalSummarizer(backend=llm_backend, **backend_kwargs)
    summary = s.summarize_from_segments(transcript.segments, case_context)

    return transcript, summary


# ─── Quick Test ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    # Test with mock transcript if no audio file given
    MOCK_TRANSCRIPT = """
    [0s] Judge: This is the hearing for case CRL 2024 slash 112, State versus Mehta.
    [15s] Judge: Mr. Sharma, your client must submit all financial documents within 14 days.
    [30s] Lawyer Sharma: Understood, Your Honour. We will comply.
    [45s] Judge: The prosecution must also file the charge sheet by next Friday.
    [60s] Prosecutor: We note that, Your Honour. The charge sheet will be filed under IPC Section 420.
    [75s] Judge: I am also noting that the defense has not submitted the bail application yet. This is a serious concern.
    [90s] Lawyer Sharma: We will file the bail application by tomorrow, Your Honour.
    [105s] Judge: Very well. Next hearing is scheduled for March 15, 2024 at this court only. Court adjourned.
    """

    backend = sys.argv[1] if len(sys.argv) > 1 else "gemini"

    summarizer = LegalSummarizer(backend=backend)
    summary = summarizer.summarize(MOCK_TRANSCRIPT, case_context={
        "case_id": "CRL/2024/112",
        "case_title": "State vs. Mehta",
    })

    print(summarizer.to_text(summary))
    summarizer.to_json(summary, "hearing_summary.json")
    print("\nJSON saved: hearing_summary.json")
