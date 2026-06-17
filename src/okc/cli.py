import argparse
import sys
from urllib.parse import urlparse

from okc import __version__ as version


def main() -> None:
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
        help="Database URL (e.g. sqlite:///path/to/db, postgresql://user@host/db)",
    )
    introspect_parser.add_argument(
        "--out",
        default="./okf-bundle",
        help="Output directory for the OKF bundle (default: ./okf-bundle)",
    )

    args = parser.parse_args()

    if args.command == "introspect":
        _handle_introspect(args)
    else:
        parser.print_help()


def _handle_introspect(args: argparse.Namespace) -> None:
    source = _create_source(args.url)
    if source is None:
        print(
            f"Error: Unsupported database URL scheme.\n"
            f"  URL: {args.url}\n"
            f"  Supported schemes: sqlite, postgresql, postgres\n"
            f"  Example: okc introspect sqlite:///path/to/db --out ./bundle",
            file=sys.stderr,
        )
        sys.exit(1)

    from okc.bundle.generator import generate_bundle

    print(f"Introspecting {args.url}...")
    try:
        concepts = source.list_concepts()
        table_count = sum(1 for c in concepts if c.kind == "table")
        view_count = sum(1 for c in concepts if c.kind in ("view", "materialized_view"))
        print(f"  Found {table_count} tables, {view_count} views")

        generate_bundle(source, args.out)

        import os
        file_count = sum(len(files) for _, _, files in os.walk(args.out))
        print(f"  Written {file_count} files to {args.out}")
        print("Done.")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


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
