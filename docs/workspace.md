<!--
SPDX-FileCopyrightText: 2026 roolrz
SPDX-License-Identifier: Apache-2.0
-->

# Workspace development

The manifest defines project paths and configuration links. `repo sync` follows
component `main` branches. Revisions are recorded when testing or publishing;
contributors do not maintain internal version pins.

Build tools occupy the workspace root. `kernel`, `sdk`, `stdlib`, `lib`, `app`,
`svc`, `bootstrap` and `tests` contain independent Git checkouts. Shared board,
Cargo, Kconfig and editor settings belong to this manifest repository; `linkfile`
places them at their workspace paths. Component Kconfig and test commands belong
to each component. No generated source tree or Cargo rewriting is involved.

```sh
repo start improve-top top
# Edit app/top/src/...
python3 project.py test top
make test-native ARCH=aarch64
cd app/top
git add src
git commit -s
git push hyper HEAD
```

Open the workspace root in VS Code and build the Native SDK with
`make sdk ARCH=aarch64`. The shared `.vscode` configuration locates the workspace
across nested Git repositories and resolves Native dependencies through the SDK.

For related changes, open one PR in each repository with the same `topic:name`
label. Module tests resolve that topic and run only the current repository's tests.
Rerun affected module checks after adding or changing peers. Manually dispatch
`System verification` in `HypeR-Proj/ci` with `topic:name`, `repository#number`, or
`main`. A run records exact source revisions and the qualified QEMU appliance
digest, and rejects a changed source combination before posting success.

GitHub cannot merge multiple repositories atomically. A topic proves the combined
candidate, while coordinated merges must preserve compatible intermediate states.
Administrator bypass is available only through PRs; it does not imply unrun tests
passed. Direct pushes and force pushes to default branches remain forbidden.

I/O VM qualification and package publication belong to `io-vm`. System tests use
its latest qualified package and do not compile the appliance. Pi5 distribution
is a separate manual pipeline and does not gate system verification. Each
repository independently publishes its documentation after a merge to `main`.
