# Contributing to producto-core

Thank you for contributing. This project is free software under **`AGPL-3.0-only`**; by contributing you agree that your contribution is licensed under the same license.

## Quick checklist

1. Open an issue first for large changes, so we can agree on the approach.
2. Work on a branch in your fork; never on `main`.
3. Add SPDX headers to new source files ([docs/licensing.md](docs/licensing.md#spdx-headers)).
4. Run the checks locally:
   ```bash
   python3 scripts/check_compliance.py
   python3 -m unittest discover -s tests -v
   ```
5. Sign off every commit (`git commit -s`), see below.
6. Open a pull request. Title in English with [Conventional Commits](https://www.conventionalcommits.org/) (`feat: ...`, `fix: ...`, `docs: ...`), and a `## Testing` section with the commands you ran and their real result.

Pull requests from forks run the test flow **without any credentials or deployment secrets**, and first-time contributors' workflows need a maintainer's approval before they run. Changes to `.github/` (workflows, templates, CODEOWNERS) receive extra review.

## Developer Certificate of Origin (DCO)

We use the DCO instead of a CLA. The DCO documents that you have the right to submit your contribution; it does **not** transfer your copyright to anyone and does not grant a proprietary license.

Add a `Signed-off-by` line matching the commit author to **every** commit:

```bash
git commit -s -m "fix: handle empty input"
# Signed-off-by: Your Name <you@example.com>
```

Forgot? Fix the whole branch and force-push it (only your branch, never `main`):

```bash
git rebase --signoff origin/main
git push --force-with-lease
```

The `dco` check fails if any non-merge commit in the pull request lacks a `Signed-off-by` whose e-mail matches the commit author. By signing off you certify the following:

```text
Developer Certificate of Origin
Version 1.1

Copyright (C) 2004, 2006 The Linux Foundation and its contributors.

Everyone is permitted to copy and distribute verbatim copies of this
license document, but changing it is not allowed.


Developer's Certificate of Origin 1.1

By making a contribution to this project, I certify that:

(a) The contribution was created in whole or in part by me and I
    have the right to submit it under the open source license
    indicated in the file; or

(b) The contribution is based upon previous work that, to the best
    of my knowledge, is covered under an appropriate open source
    license and I have the right under that license to submit that
    work with modifications, whether created in whole or in part
    by me, under the same open source license (unless I am
    permitted to submit under a different license), as indicated
    in the file; or

(c) The contribution was provided directly to me by some other
    person who certified (a), (b) or (c) and I have not modified
    it.

(d) I understand and agree that this project and the contribution
    are public and that a record of the contribution (including all
    personal information I submit with it, including my sign-off) is
    maintained indefinitely and may be redistributed consistent with
    this project or the open source license(s) involved.
```

Your sign-off is public and permanent. You may use a GitHub `noreply` address.

## AI-generated code

AI-assisted contributions are welcome and held to **exactly the same standard** as any other contribution:

- **Human review is required** for every change, its tests and the provenance of any new dependency. A human who understands the change submits it and answers for it.
- **"The model generated it" is not evidence** of originality, security, correctness or ownership. You remain responsible for making sure the output does not reproduce code you have no right to submit under `AGPL-3.0-only`.
- **Only humans sign off.** An AI agent must never add a `Signed-off-by` line: the DCO is a certification that only a person can make. The human who reviewed the change adds the sign-off (`git commit -s` or `git rebase --signoff`).
- **Disclose the assistance** with commit trailers, for example:
  ```text
  Agent: claude
  Agent-Model: <exact model id>
  ```
- Tests must be real: do not claim results you did not run.
- No secrets, credentials, customer data or personal data in code, tests, fixtures, prompts or logs.

## Third-party code

Do not paste code from other projects unless its license is compatible with `AGPL-3.0-only` and you follow the [third-party policy](docs/licensing.md#third-party-code-and-dependencies) (vendored under `third_party/`, original license kept, listed in `NOTICE`). New dependencies must be justified in the pull request and appear in the lock file.

## Security issues

Never report vulnerabilities in public issues or pull requests. Use private reporting as described in [SECURITY.md](SECURITY.md).

## Code of Conduct

Participation is governed by the [Code of Conduct](CODE_OF_CONDUCT.md).
