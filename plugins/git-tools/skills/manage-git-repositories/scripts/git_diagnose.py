#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


TOKEN_KEYS = {
    "access_token",
    "api_key",
    "apikey",
    "auth",
    "key",
    "password",
    "signature",
    "token",
}


def git(repo: pathlib.Path, *args: str, timeout: int = 20) -> tuple[int, str, str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError:
        return 127, "", "git executable not found"
    except subprocess.TimeoutExpired:
        return 124, "", "git command timed out"
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def redact_url(value: str) -> str:
    if re.match(r"^[^/@\s]+@[^:\s]+:.+$", value):
        user_host, path = value.split(":", 1)
        user, host = user_host.split("@", 1)
        return f"{user}@{host}:{path}"
    try:
        parts = urlsplit(value)
    except ValueError:
        return "[invalid remote URL]"
    if not parts.scheme or not parts.netloc:
        return value
    host = parts.hostname or ""
    if parts.port:
        host = f"{host}:{parts.port}"
    query = []
    for key, item in parse_qsl(parts.query, keep_blank_values=True):
        query.append((key, "[REDACTED]" if key.lower() in TOKEN_KEYS else item))
    return urlunsplit((parts.scheme, host, parts.path, urlencode(query), parts.fragment))


def get(repo: pathlib.Path, *args: str) -> str | None:
    code, out, _ = git(repo, *args)
    return out if code == 0 and out else None


def parse_status(text: str) -> dict[str, int]:
    result = {"staged": 0, "modified": 0, "untracked": 0, "conflicted": 0}
    conflict_codes = {"DD", "AU", "UD", "UA", "DU", "AA", "UU"}
    for line in text.splitlines():
        if len(line) < 2:
            continue
        code = line[:2]
        if code == "??":
            result["untracked"] += 1
            continue
        if code in conflict_codes:
            result["conflicted"] += 1
        if code[0] not in {" ", "?"}:
            result["staged"] += 1
        if code[1] not in {" ", "?"}:
            result["modified"] += 1
    return result


def diagnose(repo: pathlib.Path, check_remotes: bool) -> dict[str, object]:
    repo = repo.resolve()
    code, root, error = git(repo, "rev-parse", "--show-toplevel")
    if code != 0:
        return {"ok": False, "path": str(repo), "error": error or "not a Git repository"}

    root_path = pathlib.Path(root)
    status_text = get(root_path, "status", "--porcelain=v1", "--untracked-files=all") or ""
    branch = get(root_path, "branch", "--show-current")
    detached = get(root_path, "rev-parse", "--short", "HEAD") if not branch else None
    upstream = get(root_path, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}")

    ahead = behind = None
    if upstream:
        counts = get(root_path, "rev-list", "--left-right", "--count", f"HEAD...{upstream}")
        if counts:
            left, right = counts.split()
            ahead, behind = int(left), int(right)

    remotes: list[dict[str, object]] = []
    for name in (get(root_path, "remote") or "").splitlines():
        url = get(root_path, "remote", "get-url", name) or ""
        item: dict[str, object] = {"name": name, "url": redact_url(url)}
        if check_remotes:
            remote_code, _, remote_error = git(
                root_path, "ls-remote", "--exit-code", "--heads", name, timeout=30
            )
            item["reachable"] = remote_code == 0
            if remote_code != 0:
                item["error"] = re.sub(
                    r"(?i)(password|token|authorization)[^\s]*",
                    "[REDACTED]",
                    remote_error[:300],
                )
        remotes.append(item)

    return {
        "ok": True,
        "root": str(root_path),
        "branch": branch or f"detached@{detached or 'unknown'}",
        "head": get(root_path, "rev-parse", "HEAD"),
        "upstream": upstream,
        "ahead": ahead,
        "behind": behind,
        "status": parse_status(status_text),
        "author": {
            "name": get(root_path, "config", "--get", "user.name"),
            "email": get(root_path, "config", "--get", "user.email"),
        },
        "remotes": remotes,
        "last_commit": get(root_path, "log", "-1", "--format=%h %ad %s", "--date=iso-strict"),
    }


def render_human(report: dict[str, object]) -> str:
    if not report.get("ok"):
        return f"Git diagnosis failed: {report.get('error')} ({report.get('path')})"
    lines = [
        f"Repository: {report['root']}",
        f"Branch: {report['branch']}",
        f"HEAD: {report.get('head')}",
        f"Upstream: {report.get('upstream') or '-'}",
        f"Ahead/behind: {report.get('ahead')}/{report.get('behind')}",
    ]
    status = report["status"]
    lines.append(
        "Changes: staged={staged}, modified={modified}, untracked={untracked}, "
        "conflicted={conflicted}".format(**status)
    )
    author = report["author"]
    lines.append(
        f"Author: {author.get('name') or '[unset]'} <{author.get('email') or '[unset]'}>"
    )
    lines.append("Remotes:")
    for remote in report["remotes"]:
        suffix = ""
        if "reachable" in remote:
            suffix = " reachable" if remote["reachable"] else " unreachable"
        lines.append(f"  - {remote['name']}: {remote['url']}{suffix}")
    lines.append(f"Last commit: {report.get('last_commit') or '-'}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only Git repository diagnostics.")
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--check-remotes", action="store_true")
    args = parser.parse_args()

    report = diagnose(pathlib.Path(args.path), args.check_remotes)
    print(json.dumps(report, ensure_ascii=False, indent=2) if args.as_json else render_human(report))
    return 0 if report.get("ok") else 2


if __name__ == "__main__":
    raise SystemExit(main())
