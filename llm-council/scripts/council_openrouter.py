#!/usr/bin/env python3
"""
council_openrouter.py — cross-vendor LLM Council (faithful to karpathy/llm-council).

Fans out a question to real different model providers via OpenRouter, then runs a
blind peer-review + ranking round across them. Stdlib only (urllib + threads).

Stage 1: each COUNCIL_MODEL answers the question independently, in parallel.
Stage 2: each model sees ALL answers anonymized (Response A..N), evaluates them,
         and returns a FINAL RANKING. Run in parallel.
Output : a single JSON blob on stdout — answers (labeled + de-anonymized),
         reviews, and the aggregate ranking. The caller (Claude, as Chairman)
         does Stage 3 synthesis.

Usage:
    python3 council_openrouter.py "your question"
    echo "your question" | python3 council_openrouter.py
    python3 council_openrouter.py --models "openai/gpt-5.1,x-ai/grok-4" "question"

Reads OPENROUTER_API_KEY from the environment or a .env in CWD / ~/.claude/.
"""

import json
import os
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

# --- The original Karpathy council. Edit these slugs to taste. ----------------
# If a slug 404s on OpenRouter, that member is dropped and noted; the rest run.
COUNCIL_MODELS = [
    "openai/gpt-5.5",
    "google/gemini-3.1-pro-preview",
    "anthropic/claude-opus-4.8",
    "x-ai/grok-4.3",
]

API_URL = "https://openrouter.ai/api/v1/chat/completions"
TIMEOUT = 300  # seconds per call; these models can be slow
LABELS = [chr(ord("A") + i) for i in range(26)]  # Response A, B, C, ...


def load_api_key():
    key = os.environ.get("OPENROUTER_API_KEY")
    if key:
        return key.strip()
    for path in (os.path.join(os.getcwd(), ".env"),
                 os.path.expanduser("~/.claude/.env")):
        try:
            with open(path) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("OPENROUTER_API_KEY="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
        except OSError:
            continue
    return None


def call_model(api_key, model, prompt):
    """Return (content, error). Exactly one is non-None."""
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
    }).encode()
    req = urllib.request.Request(API_URL, data=body, method="POST")
    req.add_header("Authorization", f"Bearer {api_key}")
    req.add_header("Content-Type", "application/json")
    req.add_header("HTTP-Referer", "https://github.com/karpathy/llm-council")
    req.add_header("X-Title", "llm-council skill")
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            data = json.load(resp)
        return data["choices"][0]["message"]["content"], None
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:500]
        return None, f"HTTP {e.code}: {detail}"
    except Exception as e:  # noqa: BLE001 — surface anything to the caller
        return None, f"{type(e).__name__}: {e}"


STAGE1_PROMPT = """You are one member of an expert council answering a question \
independently. Give your genuine best answer.

Question: {question}

Give a direct, well-reasoned answer. State your key assumptions and the strongest \
objection to your own position. Be specific and concise — no preamble, no hedging.
Return only your answer."""

STAGE2_PROMPT = """You are evaluating anonymized answers to this question:

Question: {question}

{block}

Your task:
1. Evaluate each response individually — what it does well, what it does poorly — \
judging on accuracy and insight only, not style or length.
2. Then give a final ranking, best to worst.

Format the ranking EXACTLY like this at the very end (labels only, no extra text):

FINAL RANKING:
1. Response X
2. Response Y
..."""


def run(question, models, api_key):
    # --- Stage 1: independent answers, in parallel ---------------------------
    with ThreadPoolExecutor(max_workers=len(models)) as ex:
        results = list(ex.map(
            lambda m: (m, *call_model(api_key, m, STAGE1_PROMPT.format(question=question))),
            models,
        ))

    members = []  # successful answers, in label order
    failures = []
    for model, content, err in results:
        if err:
            failures.append({"model": model, "error": err})
        else:
            members.append({"model": model, "answer": content})

    if len(members) < 2:
        return {
            "error": "Fewer than 2 council members answered — cannot run a council.",
            "failures": failures,
        }

    for i, m in enumerate(members):
        m["label"] = f"Response {LABELS[i]}"

    # --- Stage 2: blind peer review + ranking, in parallel -------------------
    block = "\n\n".join(f"{m['label']}:\n{m['answer']}" for m in members)
    review_prompt = STAGE2_PROMPT.format(question=question, block=block)
    with ThreadPoolExecutor(max_workers=len(members)) as ex:
        review_results = list(ex.map(
            lambda m: (m["model"], *call_model(api_key, m["model"], review_prompt)),
            members,
        ))

    reviews = []
    for model, content, err in review_results:
        reviews.append({"reviewer_model": model,
                        "review": content if content else f"[review failed] {err}"})

    # --- Aggregate rankings by average position ------------------------------
    positions = {m["label"]: [] for m in members}
    for r in reviews:
        if not r["review"].startswith("[review failed]"):
            for pos, label in parse_ranking(r["review"], positions.keys()):
                positions[label].append(pos)

    aggregate = []
    for m in members:
        ranks = positions[m["label"]]
        avg = sum(ranks) / len(ranks) if ranks else None
        aggregate.append({"label": m["label"], "model": m["model"],
                          "avg_rank": avg, "votes": len(ranks)})
    aggregate.sort(key=lambda x: (x["avg_rank"] is None, x["avg_rank"] or 0))

    return {
        "question": question,
        "members": members,            # label -> model -> answer (de-anonymized)
        "reviews": reviews,
        "aggregate_ranking": aggregate,  # best first
        "failures": failures,
    }


def parse_ranking(review_text, valid_labels):
    """Yield (position, 'Response X') pairs from the FINAL RANKING block."""
    valid = set(valid_labels)
    lines = review_text.splitlines()
    idx = next((i for i, l in enumerate(lines)
                if "FINAL RANKING" in l.upper()), None)
    if idx is None:
        return
    pos = 0
    for line in lines[idx + 1:]:
        for label in valid:
            if label in line:
                pos += 1
                yield pos, label
                break


def main():
    argv = sys.argv[1:]
    models = COUNCIL_MODELS
    if argv and argv[0] == "--models":
        models = [m.strip() for m in argv[1].split(",") if m.strip()]
        argv = argv[2:]
    question = " ".join(argv).strip() or sys.stdin.read().strip()
    if not question:
        print(json.dumps({"error": "No question provided."}))
        sys.exit(1)

    api_key = load_api_key()
    if not api_key:
        print(json.dumps({"error": "OPENROUTER_API_KEY not found in env or .env. "
                                   "Add it to the project .env to use cross-vendor mode."}))
        sys.exit(1)

    print(json.dumps(run(question, models, api_key), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
