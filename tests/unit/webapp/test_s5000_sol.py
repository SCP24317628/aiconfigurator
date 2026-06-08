# SPDX-FileCopyrightText: Copyright (c) 2025-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from aiconfigurator.sdk import common
from aiconfigurator.sdk.task import ESTIMATE_DATABASE_VERSION
from aiconfigurator.webapp.database_options import (
    get_webapp_backend_choices,
    get_webapp_system_choices,
    get_webapp_version_choices,
)
from aiconfigurator.webapp.events.event_fn import EventFn, _load_database_for_mode


def test_s5000_is_available_as_estimate_only_webapp_system():
    assert "s5000" in get_webapp_system_choices()
    assert set(get_webapp_backend_choices("s5000")) == {backend.value for backend in common.BackendName}
    assert get_webapp_version_choices("s5000", "trtllm") == [ESTIMATE_DATABASE_VERSION]


def test_s5000_webapp_dropdown_events_return_estimate_version():
    backend_update, version_reset_update = EventFn.update_backend_choices("s5000")
    assert "trtllm" in backend_update["choices"]
    assert version_reset_update["choices"] is None

    version_update = EventFn.update_version_choices("s5000", "trtllm")
    assert version_update["choices"] == [ESTIMATE_DATABASE_VERSION]

    quant_updates = EventFn.update_quant_mode_choices(
        "Qwen/Qwen3-32B",
        "s5000",
        "trtllm",
        ESTIMATE_DATABASE_VERSION,
        False,
    )
    assert quant_updates[0]["choices"] == [common.GEMMQuantMode.float16.name]
    assert quant_updates[1]["choices"] == [common.KVCacheQuantMode.float16.name]
    assert quant_updates[2]["choices"] == [common.FMHAQuantMode.float16.name]
    assert quant_updates[3]["choices"] == [common.MoEQuantMode.float16.name]


def test_s5000_webapp_sol_loader_uses_system_yaml_without_perf_tables():
    database = _load_database_for_mode("s5000", "trtllm", ESTIMATE_DATABASE_VERSION, common.DatabaseMode.SOL.name)

    assert database.system == "s5000"
    assert database.backend == "trtllm"
    assert database.version == ESTIMATE_DATABASE_VERSION
    assert database.get_default_database_mode() == common.DatabaseMode.SOL
