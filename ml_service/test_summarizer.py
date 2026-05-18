
from summarizer import LegalSummarizer

s = LegalSummarizer(
    backend="openai",
    api_key="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",    model="llama-3.1-8b-instant",
    base_url="https://api.groq.com/openai/v1"
)

summary = s.summarize(
    "The defendant must submit evidence within 14 days. "
    "Next hearing is March 15. Judge orders prosecution "
    "to file charge sheet under IPC 420."
)

print(s.to_text(summary))