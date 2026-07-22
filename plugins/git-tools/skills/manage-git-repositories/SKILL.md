---
name: manage-git-repositories
description: Safely inspect, initialize, publish, synchronize, and troubleshoot Git repositories across local Git, Gitea, GitHub, GitLab, and generic SSH or HTTPS remotes. Use when the user asks about repository status, commits, branches, remotes, clone or push failures, SSH keys, Git credentials, publishing a project, configuring a primary remote plus a mirror, or recovering from Git conflicts without losing local work.
---

# Manage Git Repositories

Operate conservatively. Preserve local work, verify exact targets, and show evidence before changing repository state.

## Safety Rules

- Never display, commit, log, or transmit passwords, access tokens, private keys, cookies, or credential-bearing URLs.
- Redact URL user information, token query parameters, and authorization headers.
- Treat existing modified, staged, and untracked files as user-owned work.
- Do not run `reset --hard`, forced checkout, clean, history rewriting, force push, recursive deletion, or branch deletion unless the user explicitly requests the exact destructive operation.
- Before a merge, rebase, cherry-pick, remote replacement, or branch rewrite, inspect status and explain the impact.
- Prefer non-interactive Git commands and explicit repository paths.
- Do not create commits, tags, releases, pull requests, or remote repositories unless the user requested publication or a change.

## Start With Diagnosis

Run the bundled read-only diagnostic script:

```bash
python <skill-dir>/scripts/git_diagnose.py <repository-path>
```

Use `--json` for structured output. Use `--check-remotes` only when remote network access is relevant because it can trigger authentication.

Then confirm:

1. Repository root and current branch.
2. Modified, staged, untracked, conflicted, ahead, and behind counts.
3. Upstream branch and every remote URL after redaction.
4. Git author configuration.
5. Whether the intended remote is reachable.

## Initialize Or Publish

For an ordinary new repository:

1. Inspect the directory for secrets, generated files, and existing user work.
2. Create or review `.gitignore`.
3. Initialize Git only when no repository exists.
4. Configure commit identity only with user-approved values.
5. Review the exact staged diff.
6. Commit with a specific message.
7. Add the requested remote.
8. Fetch the remote before the first push when it already contains commits.
9. Merge unrelated initial content carefully instead of overwriting it.
10. Push without force and verify the remote commit hash.

## Configure Gitea And GitHub Mirrors

Prefer clear remote roles:

```text
gitea   primary customer-accessible repository
origin  GitHub or another public mirror
```

Before synchronizing:

- Verify both remotes point to the intended repositories.
- Fetch both remotes.
- Compare local `HEAD` with each remote branch.
- Push to the primary first, verify it, then push the identical commit to the mirror.
- Report partial success when one remote is unavailable.

Do not silently force two divergent histories to match.

## Troubleshoot Clone And Push

Diagnose in layers:

1. DNS resolution.
2. TCP connectivity to HTTPS 443 or SSH port.
3. TLS certificate and hostname.
4. Git client and proxy configuration.
5. SSH config, selected identity, and host key.
6. Repository existence.
7. User or team permission.
8. Branch protection and non-fast-forward rejection.

Interpret common failures:

- `connection reset`: network path, proxy, CDN, or remote endpoint.
- `permission denied (publickey)`: wrong key, wrong SSH client, missing account key, or `IdentitiesOnly` mismatch.
- `authentication failed`: expired token, wrong credential helper entry, or insufficient scope.
- `repository not found`: wrong owner/path or no read permission.
- `non-fast-forward`: remote contains commits not present locally; fetch and integrate.
- `unrelated histories`: remote and local were initialized independently; preserve both and merge deliberately.

## Commit And Review

Before committing:

- Run `git diff --check`.
- Review `git status --short`.
- Review staged paths and staged diff.
- Scan staged content for likely credentials.
- Avoid mixing unrelated user changes into the commit.

After pushing:

- Compare local and remote branch hashes.
- Report the branch and commit hash.
- State which remotes succeeded.

## Output

Return:

1. Current repository state.
2. Actions taken.
3. Remote and branch results.
4. Remaining risk or user action.

Do not claim a push, mirror, or authentication succeeded without a command result proving it.
