# producto-core

Free software core of the product.

## License

This project is licensed under the GNU Affero General Public License, version 3 only.

SPDX-License-Identifier: AGPL-3.0-only

See [LICENSE](LICENSE) for the full text and [NOTICE](NOTICE) for the copyright notice. The choice is **`AGPL-3.0-only`**, not `AGPL-3.0-or-later`; do not mix the two expressions. Every source file carries an SPDX header ([docs/licensing.md](docs/licensing.md#spdx-headers)).

The AGPL allows commercial use. The business around this project sells operational convenience, availability, support and services; it does not claim an exclusivity the license does not grant.

## Network use and Corresponding Source (AGPL section 13)

If you run a **modified** version of this program and let users interact with it over a network, section 13 of the license requires you to offer those users the **Corresponding Source** of the version you run, at no charge, through a standard means of software copying. The Corresponding Source includes the scripts needed to build, install and run the program; it never includes customer data or credentials.

How this project meets that obligation, and what a deployment must do:

- **"Source" link.** Every network-facing interface of the application must show a visible **Source** link (for example in the footer and in *About*) and APIs must expose it too. The link points to the source **of the deployed version**, not just to the main branch: `https://github.com/erlen-frontier/producto-core/tree/<commit>` or the release's source archive.
- **Build metadata.** The release flow produces `SOURCE.json` (repository, tag, commit, archive name and SHA-256). The application reads it at build time to render the link. There is no application code in this repository yet; when it is added, it must include the link and a test that fails if the link is missing or does not match the deployed commit.
- **Self-hosters** who modify the program must point the link to *their* modified source.

Details: [docs/licensing.md](docs/licensing.md#corresponding-source-and-the-source-link).

## Reproducible source archive

Anyone can rebuild the release source archive without access to any secret:

```bash
git clone https://github.com/erlen-frontier/producto-core.git
cd producto-core
scripts/source-archive.sh v1.2.3 dist v1.2.3   # <ref> <output dir> [<label>]
sha256sum dist/*.tar.gz                        # compare with the release's SHA256SUMS
```

The archive is produced with `git archive` + `gzip -n`, so the same commit gives byte-identical output with the same git and gzip versions. Each release links commit, archive, SBOM and build provenance ([docs/releasing.md](docs/releasing.md)).

## Development checks

```bash
python3 scripts/check_compliance.py        # LICENSE, SPDX headers, required files
python3 -m unittest discover -s tests -v   # tests of the scripts
```

Pull requests run these checks plus `dco` (Signed-off-by on every commit) and `convencion` without any credentials. The release flow is a separate workflow that only runs on `v*` tags.

## Contributing

Contributions are welcome under the [Developer Certificate of Origin](CONTRIBUTING.md#developer-certificate-of-origin-dco) (`git commit -s`); there is no CLA. AI-assisted contributions follow the same standard as any other, with human review and sign-off ([CONTRIBUTING.md](CONTRIBUTING.md#ai-generated-code)). Please follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Security

Please report vulnerabilities privately through GitHub's "Report a vulnerability" option in the Security tab. Do not open public issues for security problems. See [SECURITY.md](SECURITY.md).

## Trademarks

The license covers the code, not the names or logos of the project or of the managed service. See [docs/licensing.md](docs/licensing.md#trademarks).
