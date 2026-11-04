import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


class PackageInputTests(unittest.TestCase):
    def test_local_private_files_are_not_packaged(self) -> None:
        repository = Path(__file__).resolve().parents[1]
        public_sources = [
            "LICENSE",
            "TRADEMARKS.md",
            "scripts/build-openai-plugin.py",
            "plugins/falconer/.openai-plugin/plugin.json",
            "plugins/falconer/README.openai.md",
            "plugins/falconer/mcp.openai.json",
            "plugins/falconer/assets/logo.svg",
            "plugins/falconer/skills/falconer-knowledge/SKILL.md",
        ]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in public_sources:
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(repository / name, target)
            for name in ["assets/.env", "skills/falconer-knowledge/local-debug.txt"]:
                (root / "plugins/falconer" / name).write_text("LOCAL_ONLY_BUILD_TEST")
            result = subprocess.run(
                [sys.executable, str(root / "scripts/build-openai-plugin.py")],
                check=True,
                capture_output=True,
                text=True,
            )
            archive_path = Path(json.loads(result.stdout)["archive"])
            with zipfile.ZipFile(archive_path) as archive:
                self.assertNotIn("assets/.env", archive.namelist())
                self.assertNotIn(
                    "skills/falconer-knowledge/local-debug.txt", archive.namelist()
                )
                self.assertEqual(
                    archive.read("skills/falconer-knowledge/SKILL.md"),
                    (
                        repository
                        / "plugins/falconer/skills/falconer-knowledge/SKILL.md"
                    ).read_bytes(),
                )


if __name__ == "__main__":
    unittest.main()
