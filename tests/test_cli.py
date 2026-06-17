import json
import os
import tempfile
import time
from unittest.mock import MagicMock, patch

import pytest

from okc import cli
from okc.console import console


@pytest.fixture(autouse=True)
def reset_console_state():
    console.quiet = False
    yield


class MockConcept:
    def __init__(self, kind, name):
        self.kind = kind
        self.id = [name]


@pytest.fixture
def mock_source():
    source = MagicMock()
    source.list_concepts.return_value = [
        MockConcept("table", "users"),
        MockConcept("table", "orders"),
        MockConcept("view", "active_orders"),
    ]
    return source


def make_args(url="sqlite:///test.db", out=None, quiet=False, json=False):
    args = MagicMock(spec=[])
    args.url = url
    args.out = out
    args.quiet = quiet
    args.json = json
    return args


class TestStyledOutput:
    def test_success_styled_output(self, capsys, mock_source):
        with (
            patch("okc.cli._create_source", return_value=mock_source),
            patch("okc.bundle.generator.generate_bundle"),
            tempfile.TemporaryDirectory() as tmpdir,
        ):
            args = make_args(out=tmpdir)
            cli._handle_introspect(args)

        captured = capsys.readouterr()
        assert "Found 2 tables, 1 views" in captured.out
        assert "Written 0 files" in captured.out
        assert "Done in" in captured.out

    def test_error_unsupported_scheme(self, capsys):
        args = make_args(url="mysql:///test")

        with pytest.raises(SystemExit) as exc_info:
            cli._handle_introspect(args)

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Unsupported database URL scheme" in captured.err

    def test_no_ansi_when_not_tty(self, capsys, mock_source):
        with (
            patch("okc.cli._create_source", return_value=mock_source),
            patch("okc.bundle.generator.generate_bundle"),
            tempfile.TemporaryDirectory() as tmpdir,
        ):
            args = make_args(out=tmpdir)
            cli._handle_introspect(args)

        captured = capsys.readouterr()
        assert "\x1b[" not in captured.out


class TestQuietFlag:
    def test_quiet_suppresses_stdout(self, capsys, mock_source):
        with (
            patch("okc.cli._create_source", return_value=mock_source),
            patch("okc.bundle.generator.generate_bundle"),
            tempfile.TemporaryDirectory() as tmpdir,
        ):
            args = make_args(out=tmpdir, quiet=True)
            cli._handle_introspect(args)

        captured = capsys.readouterr()
        assert captured.out == ""

    def test_quiet_preserves_stderr(self, capsys):
        args = make_args(url="mysql:///test", quiet=True)

        with pytest.raises(SystemExit):
            cli._handle_introspect(args)

        captured = capsys.readouterr()
        assert captured.out == ""
        assert "Unsupported database URL scheme" in captured.err


class TestJsonFlag:
    def test_json_success_output(self, capsys, mock_source):
        with (
            patch("okc.cli._create_source", return_value=mock_source),
            patch("okc.bundle.generator.generate_bundle"),
            tempfile.TemporaryDirectory() as tmpdir,
        ):
            args = make_args(out=tmpdir, json=True)
            cli._handle_introspect(args)

        captured = capsys.readouterr()
        data = json.loads(captured.out.strip())
        assert data["status"] == "ok"
        assert data["url"] == "sqlite:///test.db"
        assert data["tables"] == 2
        assert data["views"] == 1
        assert data["files"] == 0
        assert data["output_dir"] == tmpdir
        assert isinstance(data["elapsed_ms"], int)
        assert data["elapsed_ms"] >= 0

    def test_json_error_output(self, capsys):
        args = make_args(url="mysql:///test", json=True)

        with pytest.raises(SystemExit) as exc_info:
            cli._handle_introspect(args)

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        data = json.loads(captured.out.strip())
        assert data["status"] == "error"
        assert "Unsupported database URL scheme" in data["message"]

    def test_quiet_json_precedence(self, capsys, mock_source):
        with (
            patch("okc.cli._create_source", return_value=mock_source),
            patch("okc.bundle.generator.generate_bundle"),
            tempfile.TemporaryDirectory() as tmpdir,
        ):
            args = make_args(out=tmpdir, quiet=True, json=True)
            cli._handle_introspect(args)

        captured = capsys.readouterr()
        data = json.loads(captured.out.strip())
        assert data["status"] == "ok"
