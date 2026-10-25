"""Repository validation and reproducible packaging."""
from __future__ import annotations
import hashlib
import json
import re
import zipfile
from pathlib import Path, PurePosixPath
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
NAME = "chat-handoff"
SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
SOURCE_ROOTS = ("skills", "scripts", "tests", "docs", "examples", "templates", ".github", ".codex-plugin")
ROOT_FILES = ("README.md", "AGENTS.md", "CHANGELOG.md", "LICENSE", "NOTICE.md", "CONTRIBUTING.md", ".gitignore", ".gitattributes", "requirements-dev.txt", "plugin.json")
SKIP = {"__pycache__", ".pytest_cache", ".DS_Store"}


def source_files(root: Path) -> list[Path]:
    result = []
    for name in ROOT_FILES:
        p = root / name
        if not p.is_file():
            raise ValueError(f"Required file missing: {name}")
        result.append(p)
    for name in SOURCE_ROOTS:
        base = root / name
        if base.is_symlink() or not base.is_dir():
            raise ValueError(f"Invalid source directory: {name}")
        for p in sorted(base.rglob("*")):
            if p.is_symlink():
                raise ValueError(f"Source symlink not allowed: {p}")
            if p.is_file() and not any(part in SKIP for part in p.parts) and p.suffix != ".pyc":
                if p.name.startswith("._") or p.name.startswith(".env"):
                    raise ValueError(f"Unwanted source file: {p}")
                result.append(p)
    seen = set()
    for p in result:
        if p.is_symlink():
            raise ValueError(f"Source symlink not allowed: {p}")
        key = p.relative_to(root).as_posix().casefold()
        if key in seen:
            raise ValueError(f"Case-insensitive path collision: {p}")
        seen.add(key)
    return sorted(result)


def validate(root: Path = ROOT) -> dict:
    try:
        import yaml
    except ImportError as exc:
        raise ValueError("Run: python3 -m pip install -r requirements-dev.txt") from exc
    m = json.loads((root / "plugin.json").read_text(encoding="utf-8"))
    c = json.loads((root / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    if m.get("$schema") != SCHEMA or m.get("name") != NAME:
        raise ValueError("Invalid portable plugin schema/name")
    version = m.get("version", "")
    if not re.fullmatch(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)", version):
        raise ValueError("Use a stable major.minor.patch version")
    if c.get("name") != NAME or c.get("version") != version or c.get("skills", "").rstrip("/") != "./skills":
        raise ValueError("Portable and Codex manifests disagree")
    interface = m["extensions"]["com.openai"]["interface"]
    if c.get("interface") != interface:
        raise ValueError("Plugin presentation metadata differs")
    if not 1 <= len(interface["shortDescription"]) <= 30:
        raise ValueError("Plugin subtitle must be 1–30 characters")
    if interface["category"] != "Productivity" or not isinstance(interface["capabilities"], list):
        raise ValueError("Invalid category/capabilities")
    if m.get("license") != "MIT":
        raise ValueError("MIT license metadata is missing")
    if (root / ".app.json").exists() or (root / "mcp.json").exists():
        raise ValueError("Unexpected app/server file in skills-only distribution")
    skill = root / "skills" / NAME
    text = (skill / "SKILL.md").read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must begin with YAML frontmatter")
    front = yaml.safe_load(text.split("---", 2)[1])
    if not isinstance(front, dict) or set(front) != {"name", "description"}:
        raise ValueError("Use skill name and description frontmatter only")
    if front["name"] != NAME or not isinstance(front["description"], str) or not front["description"].strip():
        raise ValueError("Invalid skill metadata")
    if len(text.encode("utf-8")) > 1024 * 1024 or f"Version: {version}\n" not in text:
        raise ValueError("Skill size/version is invalid")
    ui = yaml.safe_load((skill / "agents/openai.yaml").read_text(encoding="utf-8"))
    if not isinstance(ui, dict) or not isinstance(ui.get("interface"), dict):
        raise ValueError("Invalid OpenAI UI metadata")
    for key in ("display_name", "short_description", "default_prompt"):
        if not isinstance(ui["interface"].get(key), str) or not ui["interface"][key].strip():
            raise ValueError(f"Missing UI field: {key}")
    if "$chat-handoff" not in ui["interface"]["default_prompt"]:
        raise ValueError("Default prompt must mention $chat-handoff")
    files = source_files(root)
    allowed = {p.resolve() for p in files}
    for p in files:
        if p.suffix in {".yml", ".yaml"}:
            if not isinstance(yaml.safe_load(p.read_text(encoding="utf-8")), dict):
                raise ValueError(f"YAML must be an object: {p}")
        if p.suffix != ".md":
            continue
        body = re.sub(r"(?ms)^\x60{3}.*?^\x60{3}\s*$", "", p.read_text(encoding="utf-8"))
        for target in re.findall(r"\[[^\]]*\]\(([^)\s]+)\)", body):
            if re.match(r"[a-z][a-z0-9+.-]*:", target, re.I) or target.startswith("#"):
                continue
            linked = (p.parent / unquote(target.split("#", 1)[0])).resolve()
            if not linked.is_relative_to(root.resolve()) or not linked.exists():
                raise ValueError(f"Broken link in {p.name}: {target}")
            if linked.is_file() and linked not in allowed:
                raise ValueError(f"Link target not shipped: {target}")
    if f"## {version}" not in (root / "CHANGELOG.md").read_text(encoding="utf-8"):
        raise ValueError("Version missing from CHANGELOG.md")
    if f"Repository version: {version}." not in (root / "README.md").read_text(encoding="utf-8"):
        raise ValueError("Version missing from README.md")
    return {"version": version, "source_files": len(files), "skill": NAME}


def write_zip(output: Path, entries: list[tuple[str, bytes]]) -> None:
    names = [name for name, _ in entries]
    if len(names) != len({name.casefold() for name in names}):
        raise ValueError("Duplicate archive names")
    for name in names:
        # ZIP entry names use forward slashes regardless of the build host.
        p = PurePosixPath(name)
        if p.is_absolute() or ".." in p.parts or "\\" in name or re.match(r"^[A-Za-z]:", name):
            raise ValueError(f"Unsafe archive path: {name}")
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, data in sorted(entries):
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, data)
    with zipfile.ZipFile(output) as z:
        if z.testzip() is not None or set(z.namelist()) != set(names):
            raise ValueError(f"Archive verification failed: {output}")


def build(output: Path, root: Path = ROOT) -> list[Path]:
    version = validate(root)["version"]
    files = source_files(root)
    source = output / f"chat-handoff-for-chatgpt-{version}.zip"
    plugin = output / f"chat-handoff-plugin-{version}.zip"
    skill = output / f"chat-handoff-skill-{version}.zip"
    source_entries = [(f"chat-handoff-for-chatgpt/{p.relative_to(root).as_posix()}", p.read_bytes()) for p in files]
    plugin_files = [p for p in files if p.relative_to(root).parts[0] in {"skills", ".codex-plugin"} or (p.name in {"plugin.json", "LICENSE", "NOTICE.md"} and p.parent == root)]
    plugin_entries = [(f"chat-handoff/{p.relative_to(root).as_posix()}", p.read_bytes()) for p in plugin_files]
    skill_entries = [(f"chat-handoff/{p.relative_to(root / 'skills' / NAME).as_posix()}", p.read_bytes()) for p in files if p.is_relative_to(root / "skills" / NAME)]
    skill_entries += [(f"chat-handoff/{name}", (root / name).read_bytes()) for name in ("LICENSE", "NOTICE.md")]
    write_zip(source, source_entries)
    write_zip(plugin, plugin_entries)
    write_zip(skill, skill_entries)
    checksums = output / "SHA256SUMS.txt"
    checksums.write_text("".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n" for p in (source, plugin, skill)), encoding="utf-8")
    return [source, plugin, skill, checksums]
