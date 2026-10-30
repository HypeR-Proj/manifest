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
working = {'lib-fs-f2fs', 'ci', 'svc', 'system-tests', 'fs-f2fs', 'build'}
names, paths, links = set(), set(), set()
for project in root.findall('project'):
    name, path = project.get('name'), project.get('path')
    assert re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', name)
    assert name not in names and path not in paths
    assert not PurePosixPath(path).is_absolute() and '..' not in PurePosixPath(path).parts
    expected = 'refs/heads/feat/fuchsia-f2fs' if name in working else 'refs/heads/main'
    assert project.get('revision', 'refs/heads/main') == expected
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
assert next(p for p in root.findall('project') if p.get('name') == 'build').get('path') == 'build/system'
assert next(p for p in root.findall('project') if p.get('name') == 'fit-pack').get('path') == 'build/tools/fit-pack'
assert '.' not in paths, 'the workspace root must not be a Git project'
assert links == {'Makefile', 'project.py', '.vscode', '.clang-format'}
build = next(p for p in root.findall('project') if p.get('name') == 'build')
assert {(p.tag, p.get('src'), p.get('dest')) for p in build} == {
    ('linkfile', 'Makefile', 'Makefile'), ('linkfile', 'project.py', 'project.py'),
    ('linkfile', 'mk/workspace/.vscode', '.vscode'),
    ('linkfile', 'mk/workspace/.clang-format', '.clang-format')}
assert not {'HypeR', 'manifest'} & names, 'repo already owns the manifest; top-level docs are not build inputs'
print(f'validated {len(names)} rolling projects and {len(links)} workspace links')

assert {'build/app', 'build/svc', 'build/system', 'build/tools/fit-pack', 'build/pi5-images'} <= paths
for owner in ('build/app', 'build/svc', 'build/system', 'build/tools/fit-pack', 'build/pi5-images'):
    assert not any(owner != path and PurePosixPath(owner).is_relative_to(path) for path in paths), owner

assert working <= names
