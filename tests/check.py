#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 roolrz
# SPDX-License-Identifier: Apache-2.0

"""Validate the rolling checkout layout and manifest-owned configuration."""

from pathlib import Path, PurePosixPath
import re
import xml.etree.ElementTree as ET

root = ET.parse(Path(__file__).resolve().parents[1] / 'default.xml').getroot()
assert root.find('default').get('revision') == 'refs/heads/main'
assert root.find('remote').get('fetch').rstrip('/') == 'https://github.com/HypeR-Proj'
names, paths, links = set(), set(), set()
for project in root.findall('project'):
    name, path = project.get('name'), project.get('path')
    assert re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', name)
    assert name not in names and path not in paths
    assert not PurePosixPath(path).is_absolute() and '..' not in PurePosixPath(path).parts
    assert project.get('revision', 'refs/heads/main') == 'refs/heads/main'
    names.add(name)
    paths.add(path)
    for link in project:
        assert link.tag in ('linkfile', 'copyfile')
        assert link.get('dest') not in links
        links.add(link.get('dest'))
        for value in (link.get('src'), link.get('dest')):
            p = PurePosixPath(value)
            assert not p.is_absolute() and not {'.git', '.repo', '..'} & set(p.parts)
        if name == 'manifest':
            assert (Path(__file__).resolve().parents[1] / link.get('src')).is_file()
assert {'test-framework', 'system-tests', 'kernel', 'abi', 'toolchain', 'lib-system', 'lib-rust', 'lib-rust-std',
        'build', 'ci', 'bootstrap', 'io-vm', 'pi5-images'} <= names
assert next(p for p in root.findall('project') if p.get('name') == 'build').get('path') == '.'
assert not links, 'make prepare owns the execution view, not repo linkfile'
assert not {'HypeR', 'manifest'} & names, 'repo already owns the manifest; top-level docs are not build inputs'
print(f'validated {len(names)} rolling projects and {len(links)} workspace links')
