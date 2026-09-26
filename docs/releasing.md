# Releasing

Releases are **separate from the pull request test flow**:

| Flow | Trigger | Credentials | What it does |
| --- | --- | --- | --- |
| Test flow (`checks`, `dco`, `convencion`) | pull request / push to `main` | none (`contents: read` or no permissions) | compliance checks, tests, reproducibility check, DCO, PR convention |
| Release flow (`release`) | push of a `v*` tag | no deployment secrets; `id-token`/`attestations` only in the attestation job | source archive, SBOM, provenance |

> **Status: draft.** The release workflow has not run yet. Review it before pushing the first tag.

## What a release produces

1. **Reproducible source archive** `producto-core-<tag>.tar.gz` built from the tagged commit with `scripts/source-archive.sh` (`git archive` + `gzip -n`). The build runs twice and fails if the two archives differ.
2. **`SOURCE.json`**: repository, tag, commit, archive name and SHA-256, and the source URL of that exact commit. The application uses it to render the **Source** link (AGPL section 13).
3. **SBOM** `producto-core-<tag>.spdx.json`, exported from GitHub's dependency graph (`GET /repos/{owner}/{repo}/dependency-graph/sbom`, SPDX 2.3).
4. **`SHA256SUMS`** for all files.
5. **Build provenance attestation** (SLSA, Sigstore) for all of the above, created by `actions/attest-build-provenance` in a job gated by the `produccion` environment: a human approves it, and GitHub records who authorized the release.

All files are uploaded as the workflow artifact `release-dist` (kept 90 days).

## Steps (human)

1. Make sure `main` is green and the changelog/notes are ready.
2. Create and push an annotated tag from `main`: `git tag -a v0.1.0 -m "v0.1.0" && git push origin v0.1.0`.
3. Approve the `attest` job in the `produccion` environment after checking the `build` job output.
4. Download `release-dist`, verify it, and publish a GitHub Release manually, attaching the files. The workflow does **not** publish releases or packages by itself.

## Verifying a release (anyone)

```bash
gh attestation verify producto-core-v0.1.0.tar.gz --repo erlen-frontier/producto-core
sha256sum -c SHA256SUMS
# Rebuild and compare:
git clone https://github.com/erlen-frontier/producto-core.git && cd producto-core
scripts/source-archive.sh v0.1.0 /tmp/rebuild v0.1.0 && sha256sum /tmp/rebuild/*.tar.gz
```

Signatures and attestations prove origin and integrity according to their implementation; they do not prove the absence of bugs.
