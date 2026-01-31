# Research: Orisha - Automated System Documentation Generator

**Date**: 2026-01-31
**Branch**: `001-system-doc-generator`

## 1. CLI Framework: Click vs Typer

### Decision: **Typer** with typer-config extension

### Rationale:
- Built on Click, providing all of Click's power with less boilerplate
- Type hints-based argument parsing reduces code duplication
- Supports subcommands via `@app.command()` decorators
- `typer-config` extension provides `@use_yaml_config`, `@use_toml_config` decorators for configuration file support
- No built-in "CI mode" but easy to implement via `--ci` flag or `CI=true` env var check
- Inherits Click's excellent error handling

### Alternatives Considered:
- **Click**: More mature but requires more boilerplate code
- **argparse**: Standard library but verbose and lacks built-in subcommand groups

---

## 2. Multi-Language AST Parsing

### Decision: **tree-sitter-language-pack** + **tree-sitter**

### Rationale:
- `tree-sitter-language-pack` is the actively maintained successor to `tree-sitter-languages`
- Bundles 100+ languages with pre-built wheels (no compilation needed)
- Supports Python 3.10+ and tree-sitter 0.25.x
- Zero GPL dependencies - all bundled languages use permissive licenses
- Full typing support for IDE integration

### Usage Pattern:
```python
from tree_sitter_language_pack import get_language, get_parser

python_parser = get_parser("python")
js_parser = get_parser("javascript")
go_parser = get_parser("go")
java_parser = get_parser("java")

tree = python_parser.parse(bytes(source_code, "utf8"))
```

### Alternatives Considered:
- **Individual language packages**: More granular but requires managing multiple dependencies
- **tree-sitter-languages**: Now unmaintained; avoid for new projects

---

## 3. Unified LLM Access

### Decision: **LiteLLM**

### Rationale:
- Confirmed support for all required providers:
  - Claude (Anthropic): `anthropic/claude-3-5-sonnet-20241022`
  - Gemini (Google): `gemini/gemini-pro`
  - Ollama (local): `ollama/llama2` with `api_base="http://localhost:11434"`
- Unified `completion()` API across 100+ providers
- Built-in cost tracking, retries, fallbacks, and logging

### Deterministic Output Configuration:
```python
import litellm

response = litellm.completion(
    model="anthropic/claude-3-5-sonnet-20241022",
    messages=[{"role": "user", "content": prompt}],
    temperature=0,  # Greedy decoding - most deterministic
    seed=42,        # Optional - only matters if temperature > 0
)
```

### Important Caveat:
Temperature=0 is necessary but not sufficient for perfect determinism. Design the application to be robust to minor output variations rather than expecting bit-perfect reproducibility. This aligns with SC-005 which exempts punctuation and filler words from reproducibility requirements.

### Alternatives Considered:
- **Direct SDKs** (anthropic, google-generativeai, ollama): More control but requires maintaining multiple integrations
- **LangChain**: Heavier framework; overkill for this use case

---

## 4. SBOM Generation: Syft Integration

### Decision: **Invoke Syft via subprocess.run() with JSON output**

### Rationale:
- Industry-standard SBOM generator from Anchore
- Runs client-side with no cloud dependencies
- Supports multiple output formats (Syft JSON, CycloneDX, SPDX)
- Comprehensive scanning across multiple package ecosystems

### Integration Pattern:
```python
import subprocess
import json

def generate_sbom(target: str, format: str = "json") -> dict:
    result = subprocess.run(
        ["syft", target, "-o", format, "-q"],
        capture_output=True,
        text=True,
        check=True,
        timeout=300
    )
    return json.loads(result.stdout)
```

### Output Formats:
| Format | Flag | Use Case |
|--------|------|----------|
| Syft JSON | `-o json` | Most comprehensive |
| CycloneDX JSON | `-o cyclonedx-json` | Security-focused standard |
| SPDX JSON | `-o spdx-json` | Compliance-focused standard |

### Alternatives Considered:
- **Syft Go library**: Would require CGO bindings; subprocess is simpler
- **Python-native tools** (pip-licenses, pipdeptree): Less comprehensive

---

## 5. Terraform Diagram Generation: Terravision Integration

### Decision: **Invoke Terravision via subprocess.run()**

### Rationale:
- Purpose-built for CI/CD pipeline integration ("Docs as Code")
- Client-side only - no Terraform or cloud access required
- Multi-cloud support: AWS, Google Cloud, Azure
- Can read directly from Git repositories

### Prerequisites:
- Python 3.10+
- Graphviz (for diagram rendering)
- Git (for remote repos)

### Integration Pattern:
```python
import subprocess
from pathlib import Path

def generate_terraform_diagram(source: str, output_file: str = "architecture.png") -> Path:
    cmd = ["terravision", "draw", "--source", source, "--output", output_file]
    subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=120)
    return Path(output_file)
```

### Alternatives Considered:
- **terraform graph**: Native to Terraform but produces raw DOT format requiring manual processing
- **Pluralith**: Commercial alternative with more features but requires account/API access
- **Inframap**: Open-source but less actively maintained

---

## Summary: Technology Stack

| Component | Choice | Package/Tool |
|-----------|--------|--------------|
| CLI Framework | Typer | `typer`, `typer-config` |
| AST Parsing | tree-sitter | `tree-sitter`, `tree-sitter-language-pack` |
| LLM Access | LiteLLM | `litellm` |
| SBOM Generation | Syft | External CLI tool |
| Terraform Diagrams | Terravision | External CLI tool |
| Templating | Jinja2 | `jinja2` |

## Resolved Clarifications

| Item | Resolution |
|------|------------|
| CLI Framework | Typer (not Click) |
| AST Library | tree-sitter-language-pack |
| LLM Determinism | temperature=0, accept minor variations per SC-005 |
