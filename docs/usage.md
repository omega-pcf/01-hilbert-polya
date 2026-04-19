# Release Pipeline Usage

## Development

**Template:** Preprint (`amsart.cls`). The paper is formatted using the standard AMS article class for a clean, vanilla preprint appearance suitable for arXiv and general distribution.

**Daily Workflow:** LaTeX Workshop (James Yu) in VS Code
- Automatically compiles to `build/main.pdf`.
- Real-time preview.

**Pre-release Verification:**
```bash
pnpm run build
sha256sum build/document-v*.pdf build/main.pdf  # They must match
```

## Commits and Changelog

**Conventional Commits:** All commits must follow the [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Common Types:**
- `feat`: New functionality.
- `fix`: Bug fix.
- `docs`: Documentation changes.
- `refactor`: Code refactoring.
- `chore`: Maintenance tasks (build, config, etc.).

**Examples:**
```bash
git commit -m "feat(release): add dotenv-cli to load GITHUB_TOKEN from .env"
git commit -m "fix(release): use automatic changelog from plugin"
git commit -m "refactor(scripts): remove legacy code and clean up unused utilities"
```

**Automatic Changelog:** The `@release-it/conventional-changelog` plugin automatically generates `CHANGELOG.md` based on conventional commits. The changelog is updated during each release with only the changes from the current version.

## Releases

**Independent Build:**
```bash
pnpm run build
```

**Full Release:**
```bash
pnpm run release
```

**Dry-run (no changes):**
```bash
pnpm run release:dry-run
```

## Installation

```bash
pnpm install
```

**Requirements:** Node.js 20+, pnpm 9+, Docker.
