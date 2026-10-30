<!-- SPDX-FileCopyrightText: 2026 roolrz -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# HypeR workspace manifest

```sh
mkdir workspace && cd workspace
repo init -u https://github.com/HypeR-Proj/manifest -b feat/fuchsia-f2fs
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
The workspace-root `Makefile`, `project.py`, `.vscode` and `.clang-format` are
manifest-generated links; all implementation and policy stay in their source repositories. Modules may provide an
independent Kconfig, and each module can be built from its own checkout. See the
[build contract](https://hyper-proj.github.io/build/docs/module-builds.html).

The [module documentation catalog](modules.md) is generated from this manifest at
documentation publication time. Adding a project adds its documentation entry
without editing HypeR's generic documentation. `integration.repositories` in
`component.json` lists management-only repositories such as HypeR; CI checks them
when needed without adding them to a user's source workspace.

Related PRs share one `topic:` label and use manually dispatched system verification.
Working feature manifests may select same-named branches instead of `main`.
I/O VM packages and Pi5 image publication remain separate from system acceptance.

See [product configuration](docs/configuration.md) for deployment and board policy.

## F2FS working checkout

This experimental manifest is not intended to merge. It selects the shared
`feat/fuchsia-f2fs` branch for `build`, `svc`, `ci`, `system-tests`, `lib-fs-f2fs` and `fs-f2fs`;
all other projects follow `main`. The build and service catalogs register the optional library and worker.
Each Rust repository owns its Cargo workspace and lockfile. The build branch
also supplies stable content checksums for timestamp-varying upstream archives. Shared Native compiler selection
is on main. The CI branch adds preserved-license validation; the
disposable-image acceptance case belongs to `system-tests`.

To switch an existing clean workspace, use `repo init -u
https://github.com/HypeR-Proj/manifest -b feat/fuchsia-f2fs`, then `repo sync`.
The `-b` option belongs to `repo init`. No duplicate manifest checkout or
source-side workspace files are needed: `make prepare` generates the build view
under `OUT`.

Follow [the acceptance guide](https://github.com/HypeR-Proj/system-tests/blob/feat/fuchsia-f2fs/fs-f2fs/README.md)
to test a cloned disposable disk. Normal `/data` images are not reformatted.
To return to the rolling system, initialize the manifest with `-b main` and
run `repo sync` again.
