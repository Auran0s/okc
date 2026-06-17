import argparse
import json
import sys
import time
from urllib.parse import urlparse

from okc import __version__ as version
from okc.console import console, error, success, status


def main() -> None:
    from rich.traceback import install as install_traceback

    install_traceback(show_locals=True)

    parser = argparse.ArgumentParser(
        prog="okc",
        description="Open Knowledge CLI - introspect databases and generate OKF bundles.",
        epilog=(
            "Supported backends:\n"
            "  sqlite:///path/to/db      SQLite database\n"
            "  postgresql://user@host/db  PostgreSQL database\n"
            "\n"
            "OKF (Open Knowledge Format) is a markdown-based format for\n"
            "describing database schemas as cross-linked concept documents."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"okc {version}",
    )

    subparsers = parser.add_subparsers(dest="command")
    introspect_parser = subparsers.add_parser(
        "introspect",
        help="Introspect a database and generate an OKF bundle",
        description="Connect to a database, introspect its schema, and write an OKF v0.1 bundle.",
    )
    introspect_parser.add_argument(
        "url",
        help=(
            "Database URL (e.g. sqlite:///path/to/db, postgresql://user@host/db). "
            "For PostgreSQL, use the PGPASSWORD environment variable "
            "instead of embedding credentials in the URL."
        ),
    )
    introspect_parser.add_argument(
        "--out",
        default="./okf-bundle",
        help="Output directory for the OKF bundle (default: ./okf-bundle)",
    )
    introspect_parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress stdout output (stderr still flows)",
    )
    introspect_parser.add_argument(
        "--json",
        action="store_true",
        help="Output structured JSON instead of styled terminal output",
    )

    args = parser.parse_args()

    if args.command == "introspect":
        _handle_introspect(args)
    else:
        parser.print_help()


def _handle_introspect(args: argparse.Namespace) -> None:
    source = _create_source(args.url)
    if source is None:
        _report_error(
            args,
            "Unsupported database URL scheme.\n"
            f"  URL: {args.url}\n"
            "  Supported schemes: sqlite, postgresql, postgres\n"
            '  Example: okc introspect sqlite:///path/to/db --out ./bundle',
        )
        sys.exit(1)

    from okc.bundle.generator import generate_bundle

    use_json = args.json
    if use_json:
        pass
    elif args.quiet:
        console.quiet = True

    show_spinner = not use_json and not args.quiet

    start = time.monotonic()

    try:
        if show_spinner:
            with status(f"Introspecting {args.url}..."):
                concepts = source.list_concepts()
        else:
            concepts = source.list_concepts()

        table_count = sum(1 for c in concepts if c.kind == "table")
        view_count = sum(1 for c in concepts if c.kind in ("view", "materialized_view"))

        if not use_json:
            success(f"Found {table_count} tables, {view_count} views")

        if show_spinner:
            with status("Generating OKF bundle..."):
                generate_bundle(source, args.out)
        else:
            generate_bundle(source, args.out)

        import os

        file_count = sum(len(files) for _, _, files in os.walk(args.out))
        elapsed = time.monotonic() - start

        if use_json:
            print(
                json.dumps(
                    {
                        "status": "ok",
                        "url": args.url,
                        "tables": table_count,
                        "views": view_count,
                        "files": file_count,
                        "output_dir": args.out,
                        "elapsed_ms": int(elapsed * 1000),
                    }
                )
            )
        else:
            success(f"Written {file_count} files to {args.out}")
            success(f"Done in {elapsed:.1f}s")
    except Exception as e:
        if use_json:
            print(json.dumps({"status": "error", "message": str(e)}))
        else:
            error("Introspection failed. Use --json for detailed error output.")
        sys.exit(1)


def _report_error(args: argparse.Namespace, message: str) -> None:
    if args.json:
        print(json.dumps({"status": "error", "message": message}))
    else:
        error(message)


def _create_source(url: str):
    parsed = urlparse(url)
    scheme = parsed.scheme

    if scheme == "sqlite":
        from okc.sources.sqlite import SQLiteSource
        return SQLiteSource(url)
    elif scheme in ("postgresql", "postgres"):
        from okc.sources.postgres import PostgresSource
        return PostgresSource(url)
    else:
        return None
