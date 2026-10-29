#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 roolrz
# SPDX-License-Identifier: Apache-2.0

"""Validate the rolling repo manifest without fetching component sources."""

from pathlib import Path
import re
import xml.etree.ElementTree as ET

root = ET.parse(Path(__file__).resolve().parents[1] / 'default.xml').getroot()
assert root.find('default').get('revision') == 'refs/heads/main'
assert root.find('remote').get('fetch').rstrip('/') == 'https://github.com/HypeR-Proj'
names = set()
for project in root.findall('project'):
    name = project.get('name')
    assert re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', name)
    assert name not in names and name != 'manifest'
    assert project.get('path') == name
    assert project.get('revision', 'refs/heads/main') == 'refs/heads/main'
    names.add(name)
assert {'HypeR', 'kernel', 'abi', 'toolchain', 'lib', 'rust-lib', 'rust-std', 'build', 'ci', 'bootstrap', 'io-vm', 'pi5-images'} <= names
print(f'validated {len(names)} rolling projects')
