#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from src.llm.runtime_paths import resolve_qwen_model_path


def main() -> int:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    if not torch.cuda.is_available():
        raise RuntimeError("Qwen smoke test requires a visible CUDA GPU")

    model_path = resolve_qwen_model_path()
    tokenizer = AutoTokenizer.from_pretrained(
        str(model_path), local_files_only=True, trust_remote_code=True
    )
    model = AutoModelForCausalLM.from_pretrained(
        str(model_path),
        local_files_only=True,
        trust_remote_code=True,
        torch_dtype=torch.float16,
    ).to("cuda:0")
    prompt = 'Return only this JSON object: {"selected_candidate_id": 1}'
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda:0")
    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=32,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )
    generated = tokenizer.decode(
        output[0][inputs.input_ids.shape[-1] :], skip_special_tokens=True
    )
    match = re.search(r"\{.*?\}", generated, flags=re.DOTALL)
    if not match:
        raise RuntimeError("Model output did not contain a JSON object")
    parsed = json.loads(match.group(0))
    if "selected_candidate_id" not in parsed:
        raise RuntimeError("JSON output omitted selected_candidate_id")
    print("Qwen smoke test passed with a structured response.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
