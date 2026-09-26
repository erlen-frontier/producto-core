# Licensing policy

This document is an engineering policy, not legal advice. Open questions are recorded at the end for legal review.

## License

- The project is licensed under **`AGPL-3.0-only`**. The full text is in [`LICENSE`](../LICENSE) (unmodified FSF text; `scripts/check_compliance.py` fails if it changes).
- Contributions are accepted under the same license (inbound = outbound) with the [DCO](../CONTRIBUTING.md#developer-certificate-of-origin-dco). The DCO documents that the contributor has the right to submit the work; it **does not** transfer copyright and does not grant any alternative proprietary license. There is no CLA.
- Changing the license of third-party contributions requires their permission. Nobody may relicense contributed code unilaterally.

## SPDX headers

Every first-party source file starts with two SPDX lines in the file's comment syntax (after a shebang line, if any):

```text
SPDX-FileCopyrightText: <year> producto-core contributors
SPDX-License-Identifier: AGPL-3.0-only
```

- Checked by `scripts/check_compliance.py` in CI for source extensions (`.py`, `.sh`, `.js`, `.mjs`, `.ts`, `.tsx`, `.css`, `.html`, `.sql`, `.go`, `.rs`, and more; see `CODE_EXTENSIONS` in the script). Documentation (`.md`), data (`.json`) and CI configuration (`.yml`) are covered by the repository-level license and do not need headers.
- The identifier must be exactly `AGPL-3.0-only`. `AGPL-3.0-or-later`, `GPL-3.0-*` or no identifier fail the check for first-party files.
- A contributor may add their own `SPDX-FileCopyrightText` line; do not remove existing ones.

## Third-party code and dependencies

- **Vendored code** lives only under `third_party/<name>/`, keeps its original license file and headers, and every file carries the upstream `SPDX-License-Identifier`. The check accepts only licenses in `COMPATIBLE_LICENSES` (see the script) for those files. Each vendored component is listed in `NOTICE` with name, version, source URL and license.
- **Dependencies** (packages installed by a manifest) are recorded through a lock file, appear in the release SBOM and are reviewed for license compatibility before being added. Compatible with `AGPL-3.0-only` in general: MIT, BSD-2-Clause, BSD-3-Clause, ISC, Apache-2.0, MPL-2.0 (unless marked "Incompatible With Secondary Licenses"), LGPL-2.1-or-later, LGPL-3.0, GPL-3.0, AGPL-3.0, Zlib, Unlicense, CC0-1.0. **Not compatible** unless legal review says otherwise: GPL-2.0-only, proprietary or "source available" licenses, licenses with field-of-use restrictions, and anything without a clear license.
- Evaluate dependency updates by tests, not by age. An urgent patch still needs a recovery path.
- Whether a separate module or service is part of the "program" depends on its real relationship with the program, **not** on it living in a different folder, repository or behind an API. When in doubt, record the question below instead of declaring it separable.

## Corresponding Source and the "Source" link

AGPL section 13 requires offering the Corresponding Source to every user who interacts with a modified version over a network.

- The application must show a **Source** link on every network-facing interface (footer and *About*), and APIs must expose it (for example a `/source` endpoint or a response header).
- The link targets the **deployed version**: `https://github.com/erlen-frontier/producto-core/tree/<commit>` or the release source archive. It is generated from the `SOURCE.json` produced by `scripts/source-archive.sh` during the release build, never hard-coded to `main`.
- The Corresponding Source includes build, install and run scripts, and excludes customer data, credentials and deployment secrets.
- Tests (once application code exists): the link is present on every page/API, resolves, and matches the deployed commit.
- Terms of service must not remove freedoms granted by the license. They may regulate hosting, quotas, support, acceptable use and brand.

## Releases

Each release relates **commit, source archive, SBOM and provenance**, and records who authorized it. See [releasing.md](releasing.md).

## Trademarks

The AGPL grants no trademark rights. The names and logos of the project and of the managed service may identify only the official project and service. Forks must use their own name when offered as a service. A formal trademark policy is pending legal review.

## Open questions for legal review

- Copyright holder wording in `NOTICE` once the company is incorporated.
- Formal trademark policy.
- Classification of any future private module that interacts with this program.
