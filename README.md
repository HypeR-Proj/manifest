<!-- SPDX-FileCopyrightText: 2026 roolrz -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# HypeR workspace manifest

```sh
mkdir workspace && cd workspace
repo init -u https://github.com/HypeR-Proj/manifest -b main
repo sync
make prepare
make rebuild ARCH=aarch64
```

`default.xml` owns repository names, source paths and revisions. Normal projects
track `main`; no manual revision-advance commits are needed. The build tools
occupy `build/system/`; the workspace root has no Git repository. The independent
FIT tool lives at `build/tools/fit-pack`; Pi5 image distribution lives at
`build/pi5-images/`. The app and service catalogs use `build/app/` and
`build/svc/`, beside `build/system/` without nesting Git repositories. The manifest itself has one checkout in
`.repo/manifests`; there is no second `.workspace` project and no top-level HypeR
checkout. Edit manifest policy and `products/` board descriptions here.

`make prepare` reads repository-owned `component.json` descriptions and generates
build contexts, configurations, editor settings and execution views under OUT.
The workspace-root `README.md`, `Makefile`, `project.py`, `.vscode` and `.clang-format` are
manifest-generated links; all implementation and policy stay in their source repositories. Modules may provide an
independent Kconfig, and each module can be built from its own checkout. See the
[build contract](https://hyper-proj.github.io/build/docs/module-builds.html).

The root README is a thin entry page owned by the docs repository. It links to
HypeR's generic documentation and the generated module catalog, without adding
a root Git repository or another HypeR checkout.

The [module documentation catalog](https://hyper-proj.github.io/manifest/modules.html) is generated from this manifest at
documentation publication time. Adding a project adds its documentation entry
without editing HypeR's generic documentation. `integration.repositories` in
`component.json` lists management-only repositories such as HypeR; CI checks them
when needed without adding them to a user's source workspace.

Related PRs share one `topic:` label and use manually dispatched system verification.
Working feature manifests may select same-named branches instead of `main`.
I/O VM packages and Pi5 image publication remain separate from system acceptance.

See [product configuration](docs/configuration.md) for deployment and board policy.
