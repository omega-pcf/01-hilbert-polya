# Project Documentation

This directory contains all the technical documentation for the project, including usage guides, architecture, specifications, and research queries.

## Structure

```
docs/
├── README.md              # This file
├── usage.md               # Release pipeline usage guide
├── architecture.md        # Release system architecture
├── style/                 # Style guides and editorial principles
└── archive/               # Archived research and specifications
```

## Main Documentation

### Usage Guides

- **usage.md**: Full guide for using the release pipeline.
  - Development workflow with LaTeX Workshop.
  - Conventional Commits and automatic changelog generation.
  - Build and release commands.
  - Installation and requirements.

### Architecture

- **architecture.md**: Architecture of the release system.
  - Tech stack (release-it, plugins, Docker).
  - Full execution flow.
  - Reproducibility measures.
  - Scripts structure and metadata.

### Style Guide

- **style/STYLE_GUIDE.md**: Internal formal coherence guidelines.
  - Voice and tone.
  - Unified notation.
  - Definition and theorem structures.
  - Content verification protocols.

## Archived Documentation

The `archive/` directory contains documentation that is no longer part of the main active set but is preserved for historical reference or context.

- **archive/perplexity/**: Detailed queries and research responses on specific technical problems.
- **archive/specs/**: Formal technical specifications for legacy configurations.

## Conventions

### Conventional Commits

All commits must follow the [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <description>
```

**Common Types:**
- `feat`: New functionality.
- `fix`: Bug fix.
- `docs`: Documentation changes.
- `refactor`: Code refactoring.
- `chore`: Maintenance tasks.
