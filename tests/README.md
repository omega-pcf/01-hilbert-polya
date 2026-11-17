# Tests

Canonical entrypoint (verified, exit 0): `uv run python tests/verify_t_star.py` — the same command as `pnpm run verify:py`.

This repo verifies numerically with a script, not pytest: there is no `test_*.py` suite, so pytest is not a dependency and `pyproject.toml` carries no `[tool.pytest.ini_options]` (a bare `uv run pytest` fails with `Failed to spawn: pytest`). When pytest tests are added, follow the family form used by `05-kk-golden-throat`: `[dependency-groups] dev = ["pytest>=8.0"]` plus `[tool.pytest.ini_options] testpaths = ["tests"]`, run as `uv run pytest tests/ -q`.
