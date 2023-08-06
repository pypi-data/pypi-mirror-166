# neuralmagic: no copyright
# flake8: noqa
__all__ = ["__version__", "version", "version_major", "version_minor", "version_bug", "version_build", "version_major_minor", "optimized", "is_release", "revision", "splash", "is_nightly", "build_date"]
__version__ = '1.2.0.20220903'

version = __version__
version_major, version_minor, version_bug, version_build = version.split(".") + (
    [None] if len(version.split(".")) < 4 else []
) # handle conditional for version being 3 parts or 4 
version_major_minor = f"{version_major}.{version_minor}"
optimized = 1
is_release = 0
is_nightly = 1
revision = '54fe9c4e'
splash = 'DeepSparse Engine, Copyright 2021-present / Neuralmagic, Inc. version: 1.2.0.20220903 COMMUNITY EDITION (54fe9c4e) (release) (optimized)'
build_date = '20220903'
