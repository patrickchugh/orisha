# Contract: Code Explanation API

**Date**: 2026-02-01
**Branch**: `001-system-doc-generator`

## Overview

Defines the internal API for generating code behavior explanations using LLM. This supplements the existing section summarization with function-level and class-level explanations.

---

## Input: Function Context

The explanation API receives function metadata extracted from AST parsing.

### FunctionContext (input to LLM)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | str | Yes | Function name |
| file | str | Yes | Source file path |
| parameters | list[str] | Yes | Parameter names |
| return_type | str | No | Return type annotation if available |
| docstring | str | No | Extracted docstring (Python """, JSDoc /**, Go //) |
| source_snippet | str | No | First 5 lines of function body |
| language | str | Yes | Source language (python, javascript, go, java, etc.) |

### ClassContext (input to LLM)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | str | Yes | Class name |
| file | str | Yes | Source file path |
| methods | list[str] | Yes | Method names |
| bases | list[str] | Yes | Base class names |
| docstring | str | No | Extracted class docstring |
| language | str | Yes | Source language |

---

## Output: Explanations

### FunctionExplanation

| Field | Type | Description |
|-------|------|-------------|
| name | str | Function name (matches input) |
| description | str | 1-2 sentence explanation of what the function does |
| error | str | None | Error message if explanation failed |

### ClassExplanation

| Field | Type | Description |
|-------|------|-------------|
| name | str | Class name (matches input) |
| description | str | 1-2 sentence explanation of class responsibility |
| error | str | None | Error message if explanation failed |

---

## Batching Strategy

To manage token limits and API costs, functions are batched for explanation.

### Batch Parameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| max_batch_size | 20 | Keeps prompt under ~4000 tokens |
| group_by | file | Functions from same file share context |
| include_docstring | Yes | Primary source of intent |
| include_snippet | Yes | First 5 lines only |
| max_snippet_lines | 5 | Limits token usage per function |

### Token Budget (per function)

| Component | Typical Tokens |
|-----------|---------------|
| Function name + signature | 10-20 |
| Docstring (if exists) | 20-100 |
| First 5 lines of body | 30-80 |
| **Total per function** | ~50-200 |

### Response Budget

| Component | Typical Tokens |
|-----------|---------------|
| Explanation per function | ~30-60 |
| Batch of 20 functions | ~600-1200 |

---

## Prompt Template

### System Prompt

```
You are documenting a codebase for enterprise IT documentation. Your explanations must be:
- Specific and technical, using actual names from the code
- Factual, never speculative (avoid "appears to", "seems to", "probably")
- Concise (1-2 sentences per function)
```

### User Prompt Template

```
For each function below, provide a 1-2 sentence technical explanation of:
- What the function does
- Its primary purpose in the system

Functions to explain:

1. {function_name}({parameters})
   File: {file}
   Docstring: {docstring or "None"}
   Code:
   ```{language}
   {source_snippet}
   ```

2. ...

Respond in this exact format:
1. [explanation]
2. [explanation]
```

---

## Response Parsing

### Expected Format

Numbered list matching input order:

```
1. Validates API rate limits for the given client ID against DynamoDB counters.
2. Increments the usage counter for a client in the rate limiting table.
3. Returns the current timestamp formatted for CloudWatch metrics.
```

### Parsing Rules

1. Split response by newline
2. Match lines starting with number + period
3. Extract text after the number
4. Map by position to input function list
5. Handle mismatches gracefully (log warning, use placeholder)

### Error Handling

| Scenario | Action |
|----------|--------|
| LLM returns fewer explanations | Use placeholder for missing |
| LLM returns malformed response | Parse what's possible, placeholder rest |
| LLM call fails entirely | Use placeholder for all in batch |
| Rate limit | Retry with exponential backoff |

---

## Integration Points

### AST Parser → Explanation API

```python
# After AST parsing extracts functions
functions: list[CanonicalFunction]  # Includes docstring, snippet

# Explanation API processes batches
explanations = await generate_function_explanations(functions, llm_client)

# Results stored back in canonical model
for func, explanation in zip(functions, explanations):
    func.description = explanation.description
```

### Explanation API → Template

```jinja2
### Function Reference

{% for file, functions in functions_by_file.items() %}
#### {{ file }}

{% for func in functions %}
**{{ func.name }}({{ func.parameters | join(', ') }})**
{{ func.description or "*No explanation available*" }}

{% endfor %}
{% endfor %}
```

---

## Configuration

### LLM Settings (from config.yaml)

The explanation API uses the same LLM configuration as section summarization:

```yaml
llm:
  provider: "claude"
  model: "claude-3-5-sonnet-20241022"
  api_key: "${ANTHROPIC_API_KEY}"
  temperature: 0  # Required for reproducibility
```

### Explanation-Specific Options

| Option | Default | Description |
|--------|---------|-------------|
| skip_explanations | false | Skip function explanation generation |
| max_functions_per_batch | 20 | Batch size for LLM calls |
| snippet_lines | 5 | Lines of function body to include |

---

## Determinism (Principle II)

- Temperature fixed at 0 for greedy decoding
- Same function + docstring + snippet = same explanation
- Minor variations in punctuation/phrasing accepted per SC-005
- Batch order is deterministic (sorted by file, then line number)

---

## Performance Targets

| Metric | Target | Notes |
|--------|--------|-------|
| Functions per batch | 20 | Balances latency vs token cost |
| Batches in parallel | 3-5 | Respects rate limits |
| Total time for 500 functions | <60s | ~25 batches, parallelized |
