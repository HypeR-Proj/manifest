<!--
SPDX-FileCopyrightText: 2026 roolrz
SPDX-License-Identifier: Apache-2.0
-->

# HypeR workspace manifest

```sh
mkdir workspace && cd workspace
repo init -u https://github.com/HypeR-Proj/manifest -b main
repo sync
make native-initramfs ARCH=aarch64
```

`default.xml` owns repository paths and shared configuration links. Source projects
track `main`; no manual revision advances are required. Build tools occupy the
workspace root, and implementation repositories occupy `kernel`, `sdk`, `stdlib`,
`lib`, `app`, `svc`, `bootstrap` and `tests`. Library repository names start with
`lib`; their checkout paths follow their role in the workspace.

The manifest is checked out at `.workspace` as well as repo's `.repo/manifests`.
Edit `.workspace/default.xml` and `workspace/` configuration files in the manifest
repository. `linkfile` exposes shared Cargo, Kconfig, board and editor configuration
at their workspace paths. Component Kconfig files remain with their sources.

The documentation repository is checked out at `.project`. `io-vm` and
`pi5-images` retain their independent publication workflows. System CI consumes
qualified I/O VM packages; it does not rebuild the appliance for each test.

For related changes, use the same `topic:` label on each PR and manually dispatch
system verification in the CI repository. The verifier records exact revisions.
