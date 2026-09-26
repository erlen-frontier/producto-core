# Security policy

## Reporting a vulnerability

Please report vulnerabilities **privately** through GitHub's private vulnerability reporting:

1. Go to the repository's **Security** tab.
2. Click **Report a vulnerability** (direct link: <https://github.com/erlen-frontier/producto-core/security/advisories/new>).

**Do not** open public issues, pull requests or discussions about security problems, and do not publish details before a fix is available.

Please include, when you can:

- the affected version, tag or commit;
- the component and configuration (self-hosted or managed service);
- steps to reproduce or a proof of concept;
- the impact you observed or expect.

Do not include real personal data, credentials or customer data in the report. Test only against your own installation; do not access, modify or delete data that is not yours, and do not degrade the managed service.

## What happens next

- We acknowledge the report, investigate and keep you informed through the private advisory.
- We coordinate a fix **before** publishing details that could facilitate attacks, then publish a GitHub Security Advisory (and request a CVE when appropriate), crediting you unless you prefer otherwise.
- This is a young project maintained by a small team: we handle reports as quickly as we can, but **we do not offer a guaranteed response time** yet. There is no bug bounty program.

## Supported versions

The project has not published a stable release yet. Security fixes are made on `main` and included in the next release. Once releases exist, only the latest release receives fixes unless stated otherwise here.

## Scope

In scope: the code in this repository and its release artifacts (source archive, SBOM, provenance). Issues in third-party dependencies should also be reported upstream; tell us too if they affect this project.

A formal safe-harbor statement is pending legal review.
