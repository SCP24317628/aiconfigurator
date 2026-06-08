# SPDX-FileCopyrightText: Copyright (c) 2025-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

import os

from aiconfigurator.sdk import common
from aiconfigurator.sdk.perf_database import get_supported_databases, get_systems_paths
from aiconfigurator.sdk.task import ESTIMATE_DATABASE_VERSION


def _system_yaml_exists(system_name: str) -> bool:
    return any(
        os.path.isfile(os.path.join(systems_root, f"{system_name}.yaml"))
        for systems_root in get_systems_paths()
    )


def get_webapp_supported_databases() -> dict[str, dict[str, list[str]]]:
    """Return real databases plus estimate-only systems known by the SDK."""
    supported_databases = {
        system: {backend: list(versions) for backend, versions in backend_versions.items()}
        for system, backend_versions in get_supported_databases().items()
    }

    estimate_only_backends = {backend.value: [ESTIMATE_DATABASE_VERSION] for backend in common.BackendName}
    for system_name in sorted(common.SupportedSystems):
        if system_name not in supported_databases and _system_yaml_exists(system_name):
            supported_databases[system_name] = estimate_only_backends.copy()

    return supported_databases


def get_webapp_system_choices() -> list[str]:
    return sorted(get_webapp_supported_databases())


def get_webapp_backend_choices(system_name: str, *, reverse: bool = False) -> list[str]:
    supported_databases = get_webapp_supported_databases()
    return sorted(supported_databases.get(system_name, {}).keys(), reverse=reverse)


def get_webapp_version_choices(system_name: str, backend_name: str, *, reverse: bool = False) -> list[str]:
    supported_databases = get_webapp_supported_databases()
    return sorted(supported_databases.get(system_name, {}).get(backend_name, []), reverse=reverse)


def get_estimate_quant_mode_choices() -> tuple[list[str], list[str], list[str], list[str]]:
    return (
        [common.GEMMQuantMode.float16.name],
        [common.KVCacheQuantMode.float16.name],
        [common.FMHAQuantMode.float16.name],
        [common.MoEQuantMode.float16.name],
    )
