# Quickstart: Orisha

**Date**: 2026-01-31
**Branch**: `001-system-doc-generator`

## Prerequisites

### Required

- Python 3.11+
- Git

### Optional (for full functionality)

- **Syft** - SBOM generation ([install guide](https://github.com/anchore/syft#installation))
- **Terravision** - Terraform diagrams ([install guide](https://github.com/patrickchugh/terravision))
- **Graphviz** - Required by Terravision for diagram rendering

### LLM Backend (choose one, optional)

- **Claude**: Requires `ANTHROPIC_API_KEY`
- **Gemini**: Requires `GOOGLE_API_KEY`
- **Ollama**: Local installation at http://localhost:11434

---

## Installation

```bash
# Install from PyPI (when published)
pip install orisha

# Or install from source
git clone https://github.com/your-org/orisha.git
cd orisha
pip install -e .
```

---

## Basic Usage

### 1. Initialize configuration

```bash
cd /path/to/your/repo
orisha init
```

This creates `.orisha/config.yaml` with default settings.

### 2. Write documentation

```bash
orisha write
```

Output: `./docs/system.md` (or as configured in YAML)

### 3. Write in CI/CD

```bash
orisha write --ci
```

All settings (LLM, tools, output path) come from `.orisha/config.yaml`.

---

## Verify Tool Availability

```bash
orisha check
```

Example output:
```
✓ git: 2.43.0
✓ syft: 1.0.0
✓ terravision: 2.0.0
✓ graphviz: 9.0.0

All tools available. Ready to generate documentation.
```

---

## Configuration

All settings are managed in `.orisha/config.yaml`. CLI flags are minimal and only for per-run overrides.

### Initialize configuration file

```bash
orisha init
```

Creates `.orisha/config.yaml` with default settings.

### Example configuration

```yaml
# Output settings
output:
  path: "./docs/system.md"
  format: "markdown"

# Tool selection (auto-skipped if not applicable)
tools:
  sbom: "syft"              # or: trivy
  diagrams: "terravision"   # default

# Human content sections (Principle VI)
# Add your own content to merge with generated docs
sections:
  overview:
    file: ".orisha/sections/overview.md"
    strategy: "prepend"     # prepend | append | replace
  security:
    file: ".orisha/sections/security.md"
    strategy: "append"

# LLM settings (optional - works without LLM)
llm:
  provider: "claude"         # or: gemini, ollama
  model: "claude-3-5-sonnet-20241022"
  api_key: "${ANTHROPIC_API_KEY}"
  temperature: 0             # required for reproducibility
```

---

## Custom Templates

### Use a custom Jinja2 template

Add to `.orisha/config.yaml`:

```yaml
template:
  path: "./my-template.md.j2"
```

Then run `orisha write` as usual.

### Available template variables

| Variable | Type | Description |
|----------|------|-------------|
| `repository` | object | Repository metadata |
| `technology_stack` | object | Languages, frameworks, dependencies |
| `sbom` | object | Software Bill of Materials |
| `architecture_diagram` | object | Terraform diagram info |
| `source_analysis` | object | Code structure analysis |
| `version_history` | list | Document version history |
| `generated_at` | datetime | Generation timestamp |

---

## CI/CD Integration

Configuration is committed to the repo in `.orisha/config.yaml`. CI just runs `orisha write --ci`.

### GitHub Actions

```yaml
name: Write Documentation
on:
  push:
    branches: [main]

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Orisha
        run: pip install orisha

      - name: Install Syft
        run: |
          curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin

      - name: Write documentation
        run: orisha write --ci
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}

      - name: Commit documentation
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add docs/
          git diff --staged --quiet || git commit -m "docs: update system documentation"
          git push
```

### GitLab CI

```yaml
write-docs:
  image: python:3.11
  script:
    - pip install orisha
    - orisha write --ci
  artifacts:
    paths:
      - docs/
  only:
    - main
```

---

## Troubleshooting

### "Syft not found" warning

Orisha continues without SBOM. Install Syft for dependency scanning:
```bash
curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin
```

### "Terravision not found" warning

Orisha continues without architecture diagrams. Install Terravision if you have Terraform files:
```bash
pip install terravision
```

### "LLM request failed"

Documentation is written with placeholder text for LLM sections. Check your API key and network connectivity. Orisha works without LLM—you'll just get deterministic analysis only.

### Large repository performance

For repositories over 100k lines, use verbose mode to monitor progress:
```bash
orisha write --verbose
```

---

## Next Steps

- Read the [CLI Reference](contracts/cli.md) for all commands and options
- Review the [Data Model](data-model.md) to understand output structure
- Customize the default template for your organization's standards
