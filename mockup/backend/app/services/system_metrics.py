from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass

import psutil


@dataclass
class GpuMetrics:
    gpu_util_pct: float | None
    memory_util_pct: float | None
    power_w: float | None


def _read_gpu_metrics() -> GpuMetrics:
    if shutil.which("nvidia-smi") is None:
        return GpuMetrics(gpu_util_pct=None, memory_util_pct=None, power_w=None)

    cmd = [
        "nvidia-smi",
        "--query-gpu=utilization.gpu,utilization.memory,power.draw",
        "--format=csv,noheader,nounits",
    ]

    try:
        # In some shared GPU hosts nvidia-smi can be slower; avoid dropping values too aggressively.
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=5)
    except Exception:
        return GpuMetrics(gpu_util_pct=None, memory_util_pct=None, power_w=None)

    line = (result.stdout or "").strip().splitlines()
    if not line:
        return GpuMetrics(gpu_util_pct=None, memory_util_pct=None, power_w=None)

    first = line[0].split(",")
    if len(first) < 3:
        return GpuMetrics(gpu_util_pct=None, memory_util_pct=None, power_w=None)

    def to_float(value: str) -> float | None:
        raw = value.strip()
        if not raw or raw.lower() in {"n/a", "nan"}:
            return None
        try:
            return float(raw)
        except ValueError:
            return None

    return GpuMetrics(
        gpu_util_pct=to_float(first[0]),
        memory_util_pct=to_float(first[1]),
        power_w=to_float(first[2]),
    )


def collect_system_metrics() -> dict:
    vm = psutil.virtual_memory()
    gpu = _read_gpu_metrics()
    return {
        "cpu_pct": psutil.cpu_percent(interval=0.0),
        "ram_pct": vm.percent,
        "ram_used_mb": round(vm.used / (1024 * 1024), 2),
        "ram_total_mb": round(vm.total / (1024 * 1024), 2),
        "gpu_util_pct": gpu.gpu_util_pct,
        "gpu_mem_util_pct": gpu.memory_util_pct,
        "gpu_power_w": gpu.power_w,
    }
