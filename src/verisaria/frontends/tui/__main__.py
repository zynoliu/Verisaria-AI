"""Entry point: ``python -m verisaria.frontends.tui <pack> [--llm ...] [--save-dir ...]``."""
from __future__ import annotations

import argparse

from verisaria.protocol.engine_session import EngineSession
from verisaria.frontends.tui.app import VerisariaApp


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="verisaria-tui", description="Verisaria TUI")
    parser.add_argument("content_pack", help="Path to content pack JSON")
    parser.add_argument(
        "--llm", default="fake",
        choices=["fake", "ollama", "openai", "minimax"], help="LLM backend",
    )
    parser.add_argument("--save-dir", default="saves", help="Save directory")
    args = parser.parse_args(argv)

    engine = EngineSession.start(
        args.content_pack, save_dir=args.save_dir, llm_backend=args.llm
    )
    VerisariaApp(engine).run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
