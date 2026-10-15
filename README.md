# EvaLoop extension: code ↔ tests loop

Fork: <https://github.com/tiva710/EvaLoop_Extension>

Standard  loop turns each round's code into an English summary. I thought it would be interesting to turn it into Python `assert` statements instead, and the next round's code is generated from those asserts (plus the original prompt's assert line).

## Changes + Why

 `config.py` adds a `--loop` option (also in `cli.py` and `evaluator.py`), because the loop was hardcoded, plus the new `code_generation_tests` loop, and treats `maas` model names as API models so Vertex AI models can run. `tasks/__init__.py` imports the new task, `tasks/test_writing.py` to register it.

## Reqs

- Linux or Linux container 
- Google Cloud CLI (`gcloud`) w/Vertex AI enabled
- Models: `qwen/qwen3-coder-480b-a35b-instruct-maas` and `qwen/qwen3-235b-a22b-instruct-2507-maas` on Vertex AI, `global` region

## To run

```bash
gcloud auth application-default login
gcloud services enable aiplatform.googleapis.com
export OPENAI_BASE_URL="https://aiplatform.googleapis.com/v1/projects/PROJECT_ID_HERE/locations/global/endpoints/openapi"
export OPENAI_API_KEY=$(gcloud auth print-access-token)

# both takes a couple hours
evaloop evaluate --model qwen/qwen3-coder-480b-a35b-instruct-maas --loop code_generation_tests \
  --experiment_name tests_qwen3-coder-480b
evaloop evaluate --model qwen/qwen3-235b-a22b-instruct-2507-maas --loop code_generation_tests \
  --experiment_name tests_qwen3-235b
```

runs write: `results/<experiment_name>_code_generation_summarization_results.json`

## Reproducing the numbers

run this on each results file:

```bash
evaloop analyze --results_path results/tests_qwen3-coder-480b_code_generation_summarization_results.json \
  --metrics "ASL_pow,ASL_bias,pass@1,pass_drop"
```

**Baseline scores:** same formulas, applied to each task's `successful_cycles` in the data package (`loops/<model_id>.json`). For Qwen3 235B this gives 7.712

**Failure analysis:** for each round in the results files, I ran the model's asserts against the code it wrote that round and against the next round's code.
