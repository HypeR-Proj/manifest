<!--
SPDX-FileCopyrightText: 2026 roolrz
SPDX-License-Identifier: Apache-2.0
-->

# HypeR source manifest

Initialize an empty working directory with:

```sh
repo init -u https://github.com/HypeR-Proj/manifest -b main
repo sync
```

The manifest is managed under `.repo/manifests`; source projects track `main`.
There are no manually advanced component revisions. Product configurations are
owned by `HypeR/products`; component Kconfig files belong to their repositories.
The build records the exact source inputs used for each output. A topic verifier
substitutes proposed changes only within its isolated checkout.
