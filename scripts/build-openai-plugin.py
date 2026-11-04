#!/usr/bin/env python3

import argparse
import hashlib
import io
import json
import re
import zipfile
from pathlib import Path

ZIP_TIMESTAMP = (2026, 10, 19, 21, 5, 2)


def collect_files(root: Path) -> tuple[str, dict[str, Path]]:
    plugin = root / "plugins/falconer"
    files = {
        "LICENSE": root / "LICENSE",
        "README.md": plugin / "README.openai.md",
        "TRADEMARKS.md": root / "TRADEMARKS.md",
        "assets/logo.svg": plugin / "assets/logo.svg",
        "mcp.json": plugin / "mcp.openai.json",
        "plugin.json": plugin / ".openai-plugin/plugin.json",
        "skills/falconer-knowledge/SKILL.md": plugin
        / "skills/falconer-knowledge/SKILL.md",
    }
    for source in files.values():
        if source.is_symlink() or not source.is_file():
            raise ValueError(f"Missing or unsupported package source: {source}")

    manifest = json.loads(files["plugin.json"].read_text())
    version = manifest["version"]
    if not isinstance(version, str) or not re.fullmatch(
        r"[0-9]+\.[0-9]+\.[0-9]+", version
    ):
        raise ValueError("The OpenAI manifest must declare a release version")

    cases = manifest["extensions"]["com.openai"]["review"]["test_cases"]
    for kind, count in (("positive", 5), ("negative", 3)):
        if not isinstance(cases[kind], list) or len(cases[kind]) != count:
            raise ValueError(f"Expected exactly {count} {kind} review cases")
        required = ["description", "prompt", "expected_behavior"]
        if kind == "positive":
            required.append("tools_triggered")
        for case in cases[kind]:
            if not isinstance(case, dict) or any(
                not isinstance(case.get(key), str) or not case[key].strip()
                for key in required
            ):
                raise ValueError(f"Incomplete {kind} review case")

    servers = json.loads(files["mcp.json"].read_text())["mcpServers"]
    if not isinstance(servers, dict) or len(servers) != 1:
        raise ValueError("Plugin-level review cases require exactly one MCP server")
    return version, files


def build_archive(files: dict[str, Path]) -> bytes:
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, source in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=ZIP_TIMESTAMP)
            info.create_system = 3
            mode = 0o100755 if source.stat().st_mode & 0o111 else 0o100644
            info.external_attr = mode << 16
            archive.writestr(
                info,
                source.read_bytes(),
                compress_type=zipfile.ZIP_DEFLATED,
                compresslevel=9,
            )
    return output.getvalue()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build the OpenAI plugin from maintained source"
    )
    parser.add_argument(
        "--archive",
        action="store_true",
        help="Also create immutable ZIP and manifest snapshots under submissions",
    )
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    try:
        version, files = collect_files(root)
        contents = build_archive(files)
        filename = f"falconer-openai-plugin-{version}.zip"
        snapshots = {}
        if args.archive:
            release = root / "submissions/openai/plugins" / f"v{version}"
            snapshots = {
                release / filename: contents,
                release / "plugin.json": files["plugin.json"].read_bytes(),
            }
            for target, data in snapshots.items():
                if target.exists() and target.read_bytes() != data:
                    raise ValueError(
                        f"Archived {version} differs from source; bump the package version before archiving"
                    )

        destination = root / "dist" / filename
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(contents)
        for target, data in snapshots.items():
            target.parent.mkdir(parents=True, exist_ok=True)
            try:
                with target.open("xb") as snapshot:
                    snapshot.write(data)
            except FileExistsError:
                if target.read_bytes() != data:
                    raise ValueError(
                        f"Archived {version} differs from source; bump the package version before archiving"
                    )
        print(
            json.dumps(
                {
                    "version": version,
                    "archive": str(destination),
                    "sha256": hashlib.sha256(contents).hexdigest(),
                    "files": len(files),
                    "archived": args.archive,
                },
                indent=2,
            )
        )
    except (KeyError, OSError, ValueError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
