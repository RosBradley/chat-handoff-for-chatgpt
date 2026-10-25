"""Regression checks for installation, validation and distribution boundaries."""
import hashlib
import json
import secrets
import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from install_skill import install, inventory
from repo_tools import build, source_files, validate, write_zip


class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.source = self.base / "source"
        shutil.copytree(ROOT / "skills/chat-handoff", self.source)
        self.target = self.base / "project/.agents/skills/chat-handoff"

    def test_install_and_idempotency(self):
        self.assertEqual(install(self.source, self.target), ("Installed", None))
        self.assertEqual(inventory(self.source), inventory(self.target))
        self.assertEqual(install(self.source, self.target), ("Already current", None))

    def test_refuses_changed_installation_without_replacement(self):
        install(self.source, self.target)
        (self.target / "SKILL.md").write_text("user changes", encoding="utf-8")
        with self.assertRaises(ValueError):
            install(self.source, self.target)
        self.assertEqual((self.target / "SKILL.md").read_text(), "user changes")

    def test_replacement_preserves_backup_outside_discovery(self):
        install(self.source, self.target)
        (self.target / "SKILL.md").write_text("user changes", encoding="utf-8")
        _, backup = install(self.source, self.target, replace=True)
        self.assertIsNotNone(backup)
        self.assertFalse(backup.is_relative_to(self.target.parent))
        self.assertEqual((backup / "SKILL.md").read_text(), "user changes")
        self.assertEqual(inventory(self.source), inventory(self.target))

    def test_refuses_source_overlap(self):
        nested = self.source / "chat-handoff"
        with self.assertRaises(ValueError):
            install(self.source, nested)

    def test_refuses_source_symlink_entry(self):
        try:
            (self.source / "external").symlink_to(self.base / "unrelated")
        except (OSError, NotImplementedError):
            self.skipTest("Symlinks unavailable")
        with self.assertRaises(ValueError):
            install(self.source, self.target)

    def test_missing_skill_fails_without_creating_target(self):
        (self.source / "SKILL.md").unlink()
        with self.assertRaises(ValueError):
            install(self.source, self.target)
        self.assertFalse(self.target.exists())


class RepositoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()

    def clone_source(self):
        dest = self.base / "repo"
        for p in source_files(ROOT):
            target = dest / p.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, target)
        return dest

    def test_repository_validates(self):
        self.assertEqual(validate(ROOT)["skill"], "chat-handoff")

    def test_version_drift_rejected(self):
        root = self.clone_source()
        p = root / ".codex-plugin/plugin.json"
        value = json.loads(p.read_text())
        value["version"] = "9.9.9"
        p.write_text(json.dumps(value))
        with self.assertRaisesRegex(ValueError, "manifests disagree"):
            validate(root)

    def test_broken_link_rejected(self):
        root = self.clone_source()
        p = root / "README.md"
        p.write_text(p.read_text() + "\n[Missing](docs/no-such-file.md)\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Broken link"):
            validate(root)

    def test_malformed_yaml_rejected(self):
        root = self.clone_source()
        p = root / "skills/chat-handoff/agents/openai.yaml"
        p.write_text("interface: []\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "UI metadata"):
            validate(root)

    def test_build_contains_only_plugin_and_checksum(self):
        paths = build(self.base / "dist", ROOT)
        version = validate(ROOT)["version"]
        self.assertEqual([p.name for p in paths], [f"chat-handoff-plugin-{version}.zip", "SHA256SUMS.txt"])
        self.assertEqual(set(paths[0].parent.iterdir()), set(paths))
        with zipfile.ZipFile(paths[0]) as z:
            expected = {f"chat-handoff/{p.relative_to(ROOT).as_posix()}" for p in (ROOT / "skills").rglob("*") if p.is_file()}
            expected.update(f"chat-handoff/{name}" for name in ("plugin.json", ".codex-plugin/plugin.json", "LICENSE", "NOTICE.md"))
            self.assertEqual(set(z.namelist()), expected)
            for name in ("LICENSE", "NOTICE.md"):
                self.assertEqual(z.read(f"chat-handoff/{name}"), (ROOT / name).read_bytes())
        lines = paths[1].read_text().splitlines()
        self.assertEqual(lines, [f"{hashlib.sha256(paths[0].read_bytes()).hexdigest()}  {paths[0].name}"])

    def test_build_reproducible_and_checksums_match(self):
        first = build(self.base / "one", ROOT)
        second = build(self.base / "two", ROOT)
        self.assertEqual([p.read_bytes() for p in first], [p.read_bytes() for p in second])
        for line in first[-1].read_text().splitlines():
            digest, name = line.split("  ", 1)
            self.assertEqual(digest, hashlib.sha256((first[-1].parent / name).read_bytes()).hexdigest())

    def test_private_root_files_excluded(self):
        root = self.clone_source()
        private_value = secrets.token_hex(32)
        for relative in ("handoffs/private.md", ".git/config", ".env", ".agents/skills/local/SKILL.md"):
            p = root / relative
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(private_value)
        paths = build(self.base / "out", root)
        for path in paths[:-1]:
            with zipfile.ZipFile(path) as z:
                self.assertTrue(all(private_value.encode() not in z.read(n) for n in z.namelist()))

    def test_unsafe_and_duplicate_archive_paths_rejected(self):
        unsafe_names = (
            "../escape", "nested/../../escape", "/absolute", "//server/share",
            "C:/absolute", "C:relative", "\\absolute", "nested\\file",
        )
        cases = [[(name, b"x")] for name in unsafe_names]
        cases.append([("A.md", b"x"), ("a.md", b"y")])
        for entries in cases:
            with self.subTest(entries=entries):
                with self.assertRaises(ValueError):
                    write_zip(self.base / "bad.zip", entries)

    def test_case_collision_in_source_rejected(self):
        root = self.clone_source()
        (root / "docs/SETUP.md").write_text("collision", encoding="utf-8")
        if (root / "docs/setup.md").read_text(encoding="utf-8") == "collision":
            self.skipTest("Case-insensitive filesystem")
        with self.assertRaisesRegex(ValueError, "collision"):
            source_files(root)


if __name__ == "__main__":
    unittest.main()
