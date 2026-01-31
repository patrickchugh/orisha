# Feature Specification: Orisha - Automated System Documentation Generator

**Feature Branch**: `001-orisha-system-doc-generator`
**Created**: 2026-01-31
**Status**: Draft
**Input**: User description: "Create an automated system documentation generator for Enterprise IT audit, architecture, security and business stakeholders. Orisha runs in CI/CD pipelines to ensure documentation stays current as systems change. Uses deterministic analysis first (source code, Terraform, dependencies), then LLM to fill gaps and summarize sections in a template."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Generate Documentation from Repository (Priority: P1)

A DevOps engineer runs Orisha as part of their CI/CD pipeline to automatically generate up-to-date system documentation whenever code changes are merged.

**Why this priority**: This is the core value proposition - automatically generating documentation that stays current with system changes, eliminating manual documentation maintenance.

**Independent Test**: Can be fully tested by pointing Orisha at a sample repository and verifying it produces a complete documentation file with all detected components.

**Acceptance Scenarios**:

1. **Given** a git repository with source code, **When** the user runs Orisha CLI, **Then** a documentation file is generated containing detected components
2. **Given** a repository with Terraform files, **When** Orisha runs, **Then** the documentation includes cloud architecture diagrams
3. **Given** a repository with dependency files (package.json, requirements.txt, go.mod), **When** Orisha runs, **Then** the documentation includes a technology stack section
4. **Given** no LLM configuration is provided, **When** Orisha runs, **Then** deterministic analysis still produces useful documentation with placeholder summaries

---

### User Story 2 - Review Documentation for Audit Compliance (Priority: P2)

An IT auditor receives automatically generated system documentation that accurately describes the system architecture, dependencies, and technology stack to assess compliance.

**Why this priority**: Audit readiness is a primary enterprise use case that validates the accuracy and completeness of generated documentation.

**Independent Test**: Can be tested by generating documentation for a known system and verifying all security-relevant components (dependencies, infrastructure) are accurately documented.

**Acceptance Scenarios**:

1. **Given** generated documentation, **When** an auditor reviews it, **Then** all third-party dependencies are listed with version numbers
2. **Given** a system with cloud infrastructure, **When** documentation is generated, **Then** the architecture diagram accurately reflects the deployed resources
3. **Given** the same repository analyzed twice, **When** no changes occurred, **Then** the generated documentation is identical (reproducibility)

---

### User Story 3 - Configure LLM Backend for Summaries (Priority: P3)

A security-conscious enterprise configures Orisha to use a local LLM (Ollama) to ensure no source code is sent to external services while still getting intelligent summaries.

**Why this priority**: Enterprise security requirements often mandate local processing, making LLM backend flexibility essential for adoption.

**Independent Test**: Can be tested by configuring different LLM backends and verifying summaries are generated without external network calls when using local LLM.

**Acceptance Scenarios**:

1. **Given** Orisha configured with Ollama, **When** documentation is generated, **Then** no network requests are made to external LLM services
2. **Given** Orisha configured with Claude API, **When** documentation is generated, **Then** LLM summaries use the Claude service
3. **Given** Orisha configured with Gemini API, **When** documentation is generated, **Then** LLM summaries use the Gemini service
4. **Given** invalid LLM configuration, **When** Orisha runs, **Then** a clear error message indicates the configuration issue

---

### User Story 4 - Customize Documentation Template (Priority: P4)

A technical writer customizes the documentation template to match their organization's documentation standards before running Orisha.

**Why this priority**: Template customization enables enterprises to align generated documentation with their existing documentation standards.

**Independent Test**: Can be tested by providing a custom Jinja2 template and verifying the output matches the template structure.

**Acceptance Scenarios**:

1. **Given** a custom Jinja2 template, **When** Orisha runs, **Then** output follows the custom template structure
2. **Given** the default template, **When** Orisha runs, **Then** output follows the built-in template with all standard sections
3. **Given** a template with unsupported placeholders, **When** Orisha runs, **Then** unsupported placeholders remain visible with warnings

---

### User Story 5 - Export to Multiple Formats (Priority: P5)

A documentation manager exports generated documentation to different formats to publish on Confluence and SharePoint.

**Why this priority**: Multi-format export enables integration with existing enterprise documentation systems.

**Independent Test**: Can be tested by generating documentation and requesting different output formats, verifying each format is valid.

**Acceptance Scenarios**:

1. **Given** documentation content, **When** user requests Markdown output, **Then** valid Markdown file is produced
2. **Given** documentation content, **When** user requests Confluence-compatible format, **Then** output can be imported to Confluence
3. **Given** documentation content, **When** user requests HTML output, **Then** valid HTML file suitable for SharePoint is produced

---

### Edge Cases

- What happens when the repository contains no recognizable source code or dependency files? System produces minimal documentation with warning indicating no analyzable content found
- What happens when the user wants to augment the generated document to add clarity or insight for the LLM? The system needs to allow human changes to be inserted for specific sections and persist as part of the defualt Jinja2 template for future runs
- What happens when the human input content conflicts with what the LLM summary states? User should be alerted of meaninful differences and told to address the conflicts before generating final document
- How does the system handle corrupted or invalid dependency files? System skips invalid files with warnings, continues processing valid files
- What happens when Terraform parsing fails? System logs error, continues without architecture diagram, notes absence in documentation
- How does the system handle very large repositories? System processes incrementally without running out of memory, with progress indication
- What happens when the LLM service is unavailable? System completes with deterministic analysis, marks LLM sections as pending with clear notation
- How does the system handle binary files or non-text content? System skips binary files automatically without error
- What happens when source code contains syntax errors? System uses best-effort parsing, notes parsing issues in output without failing

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a command-line interface executable from CI/CD pipelines
- **FR-002**: System MUST read and analyze files from a local git repository
- **FR-003**: System MUST parse source code files using AST parsing for Python, JavaScript, Go, and Java
- **FR-004**: System MUST detect and parse dependency files (package.json, requirements.txt, go.mod, pom.xml, build.gradle)
- **FR-005**: System MUST invoke Syft for comprehensive dependency scanning and SBOM generation
- **FR-006**: System MUST detect Terraform files and invoke Terravision to generate architecture diagrams
- **FR-007**: System MUST embed generated architecture diagrams (PNG/SVG) in the documentation
- **FR-008**: System MUST render documentation using Jinja2 templates with defined placeholders
- **FR-009**: System MUST support multiple output formats (Markdown at minimum)
- **FR-010**: System MUST support configurable LLM backends (Claude, Gemini, Ollama)
- **FR-011**: System MUST use deterministic analysis before invoking LLM for any section
- **FR-012**: System MUST use temperature=0 and deterministic hyperparameters for LLM calls
- **FR-013**: System MUST produce identical output when run twice on an unchanged repository
- **FR-014**: System MUST provide clear error messages when external tools (Syft, Terravision) are unavailable
- **FR-015**: System MUST continue processing when individual components fail, documenting failures in output
- **FR-016**: System MUST support configuration via command-line arguments and/or configuration file
- **FR-017**: System MUST exit with appropriate exit codes for CI/CD integration (0 for success, non-zero for failure)


### Key Entities

- **Repository**: The source git repository being analyzed; contains source files, infrastructure code, and dependency manifests
- **Documentation Template**: A Jinja2 template defining the structure and sections of the output document; contains placeholders populated by analysis
- **Analysis Result**: Structured data collected from deterministic analysis tools (AST parsing, Syft, dependency parsing); serves as input to template rendering
- **LLM Configuration**: Settings specifying which LLM backend to use and connection parameters; includes provider type, API credentials, and model parameters
- **Architecture Diagram**: Visual representation of cloud infrastructure generated from Terraform; embedded as image in final documentation
- **Technology Stack**: Inventory of detected languages, frameworks, and dependencies; derived from dependency files and Syft scanning
- **Output Document**: The final rendered documentation in the specified format; contains all analyzed information and LLM-generated summaries

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Documentation generation completes within 5 minutes for repositories up to 100,000 lines of code
- **SC-002**: Generated documentation covers 100% of detected source code languages present in the repository
- **SC-003**: 100% of third-party dependencies are listed when dependency files are present and valid
- **SC-004**: Architecture diagrams are included whenever Terraform files are detected and Terravision is available
- **SC-005**: Two consecutive runs on the same unchanged repository produce near byte-identical output. Punctuation, or additional filler words like 'the' 'an' etc exempt. Meaning should be 100% the same.
- **SC-006**: System operates successfully in CI/CD pipelines without interactive prompts
- **SC-007**: Documentation is complete enough for technical and business stakeholders to understand system architecture without accessing source code
- **SC-008**: System handles missing external tools and checks for them at startup and exits gracefully saying required tools are not detected
- **SC-009**: Generated Markdown is valid and renders correctly in standard Markdown viewers
- **SC-010**: LLM-generated summaries accurately reflect the deterministic analysis data (no hallucinated components)
- **SC-011**: All documents generated must have a version history section, so it is clear when there are updates to it, along with a history so changes can be audited. Who made the change (Human or Orisha), on which date/time, pointing to which git repo to parse code from etc. should be clear with document template

## Assumptions

- Syft is available as an external tool and installed on the system where Orisha runs
- Terravision is available as an external tool for Terraform diagram generation
- Users have appropriate API keys configured when using cloud LLM services (Claude, Gemini)
- Ollama is running locally when configured as the LLM backend
- Git repositories are accessible and have read permissions
- Source code files use standard file extensions for their respective languages (.py, .js, .ts, .go, .java)
- Terraform files follow standard naming conventions (.tf extension)
- CI/CD environments provide sufficient resources (memory, CPU) for analysis operations
- Preflight check before running any tools ensures all these assumptions are met before it starts

## Out of Scope

- Direct publishing to Confluence or SharePoint (outputs formats suitable for import)
- Version control of generated documentation (handled by Git as documentation will be checked into Git repo along with code) - however, the document should contain version histroy as a section
- Interactive editing of generated documentation
- Support for programming languages beyond Python, JavaScript, Go, and Java
- Cloud infrastructure diagrams for non-Terraform infrastructure-as-code (CloudFormation, Pulumi, etc.)
- Automatic deployment of documentation to hosting platforms
