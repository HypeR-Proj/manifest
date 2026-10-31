<!--
SPDX-FileCopyrightText: 2026 roolrz
SPDX-License-Identifier: Apache-2.0
-->

# Workspace development

The manifest defines project paths and revisions. `repo sync` follows
component `main` branches. Revisions are recorded when testing or publishing;
contributors do not maintain internal version pins.

Build tools occupy the workspace root. Module repositories stay independently
editable. The manifest owns board/product descriptions; repositories own their
Cargo declarations, optional Kconfig and test commands. `make prepare` generates
an execution view and all configuration/build files under OUT. The manifest
itself stays in `.repo/manifests`, without a duplicate source checkout.

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

Run `make prepare` and build the Native SDK with `make sdk ARCH=aarch64`.
Open `out/HypeR-aarch64.code-workspace` in VS Code. Generated editor settings
resolve the prepared Cargo workspaces and the architecture's SDK in OUT;
source edits still update their owning Git checkout.

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

## Module validation

`python3 project.py test manifest` checks the source layout and product policy.
Build-module tests validate generated Cargo workspaces and dependency boundaries
using `scripts/check-workspace.py`. Neither check needs a whole-system boot.
Changes to a module's tests belong in its own `component.json`; runtime cases
belong to `system-tests`, while reusable harness code belongs to `test-framework`.
