#!/usr/bin/env python3
"""Xiaohongshu publishing cadence & risk guard.

Enforces account safety limits:
- Daily post caps (1 for cold start, 2 for growth, up to 4 for high-velocity)
- Minimum interval gap between posts (>=3h / >=6h)
- Midnight blackout (00:00 - 07:00 CST)
- Weekly post ceiling
- Abnormal risk cooldown (48h)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

CST = timezone(timedelta(hours=8))

DEFAULT_CONFIG = {
    "cold_start": {
        "max_daily": 1,
        "max_weekly": 7,
        "min_gap_hours": 20,
    },
    "growth": {
        "max_daily": 2,
        "max_weekly": 14,
        "min_gap_hours": 6,
    },
    "high_velocity": {
        "max_daily": 4,
        "max_weekly": 28,
        "min_gap_hours": 3,
    },
}

BLACKOUT_START = 0  # 00:00 CST
BLACKOUT_END = 7    # 07:00 CST

GOLDEN_WINDOWS = [
    (7, 30, 9, 15, "早通勤"),
    (11, 45, 14, 0, "午休闲"),
    (17, 30, 19, 30, "晚通勤"),
    (20, 30, 23, 0, "夜间黄金档"),
]


def get_default_state_path() -> Path:
    env_path = os.getenv("XHS_GUARD_STATE")
    if env_path:
        return Path(env_path)
    # Default to user home state or current directory
    home_dir = Path.home() / ".hermes" / "social_state"
    home_dir.mkdir(parents=True, exist_ok=True)
    return home_dir / "xhs_guard_state.json"


def load_state(state_file: Path) -> dict:
    if not state_file.exists():
        return {
            "mode": "growth",
            "notes": [],
            "interactions": [],
            "cooldown_until": None,
        }
    try:
        with open(state_file, encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = {}
    data.setdefault("mode", "growth")
    data.setdefault("notes", [])
    data.setdefault("interactions", [])
    data.setdefault("cooldown_until", None)
    return data


def save_state(state_file: Path, data: dict) -> None:
    state_file.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = state_file.with_suffix(".tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, state_file)


def dedupe_timestamps(stamps: list[str]) -> list[str]:
    seen: set[str] = set()
    res: list[str] = []
    for s in stamps:
        key = s.split(".")[0]
        if key not in seen:
            seen.add(key)
            res.append(s)
    return res


def parse_dt(s: str) -> datetime:
    dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=CST)
    return dt.astimezone(CST)


def check_cadence(state_file: Path, target_time: datetime | None = None) -> dict:
    now = target_time or datetime.now(CST)
    state = load_state(state_file)
    mode = state.get("mode", "growth")
    cfg = DEFAULT_CONFIG.get(mode, DEFAULT_CONFIG["growth"])

    reasons: list[str] = []
    wait_seconds = 0

    state["notes"] = dedupe_timestamps(state.get("notes", []))
    notes = [parse_dt(s) for s in state["notes"]]

    # 1. Check abnormal cooldown
    cd_str = state.get("cooldown_until")
    if cd_str:
        cd_dt = parse_dt(cd_str)
        if now < cd_dt:
            rem = int((cd_dt - now).total_seconds())
            reasons.append(f"账户安全冷却中，解禁时间: {cd_dt.strftime('%m-%d %H:%M')}")
            wait_seconds = max(wait_seconds, rem)

    # 2. Check midnight blackout window (00:00 - 07:00 CST)
    if BLACKOUT_START <= now.hour < BLACKOUT_END:
        resume = now.replace(hour=BLACKOUT_END, minute=0, second=0, microsecond=0)
        rem = int((resume - now).total_seconds())
        reasons.append(f"当前处于夜间禁发时段 (00:00-07:00)，预计 {resume.strftime('%H:%M')} 恢复")
        wait_seconds = max(wait_seconds, rem)

    # 3. Check daily limit
    today = now.date()
    todays = [n for n in notes if n.date() == today]
    if len(todays) >= cfg["max_daily"]:
        tomorrow = datetime.combine(today + timedelta(days=1), datetime.min.time(), CST) + timedelta(hours=BLACKOUT_END)
        rem = int((tomorrow - now).total_seconds())
        reasons.append(f"今日已发布 {len(todays)} 篇，达到阶段上限 ({cfg['max_daily']} 篇/天)")
        wait_seconds = max(wait_seconds, rem)

    # 4. Check minimum interval gap
    if notes:
        last = max(notes)
        gap_limit = timedelta(hours=cfg["min_gap_hours"])
        next_allowed = last + gap_limit
        if now < next_allowed:
            rem = int((next_allowed - now).total_seconds())
            reasons.append(f"距上一次发布不足 {cfg['min_gap_hours']} 小时 (上次: {last.strftime('%m-%d %H:%M')})，需等待至 {next_allowed.strftime('%m-%d %H:%M')}")
            wait_seconds = max(wait_seconds, rem)

    # 5. Check weekly limit
    week_start = today - timedelta(days=today.weekday())
    this_week = [n for n in notes if n.date() >= week_start]
    if len(this_week) >= cfg["max_weekly"]:
        reasons.append(f"本周已发布 {len(this_week)} 篇，达到周上限 ({cfg['max_weekly']} 篇/周)")

    # Find matching golden window
    current_golden = None
    for sh, sm, eh, em, label in GOLDEN_WINDOWS:
        start_time = now.replace(hour=sh, minute=sm, second=0)
        end_time = now.replace(hour=eh, minute=em, second=0)
        if start_time <= now <= end_time:
            current_golden = label
            break

    return {
        "allowed": len(reasons) == 0,
        "reasons": reasons,
        "wait_seconds": wait_seconds,
        "mode": mode,
        "today_count": len(todays),
        "week_count": len(this_week),
        "golden_window": current_golden,
        "checked_at": now.isoformat(),
    }


def record_post(state_file: Path, timestamp: str | None = None) -> dict:
    state = load_state(state_file)
    now = timestamp or datetime.now(CST).isoformat()
    state["notes"].append(now)
    state["notes"] = dedupe_timestamps(state["notes"])
    save_state(state_file, state)
    return {"status": "recorded", "timestamp": now, "total_notes": len(state["notes"])}


def main() -> int:
    parser = argparse.ArgumentParser(description="Xiaohongshu Cadence Guard")
    parser.add_argument("--state", type=Path, default=get_default_state_path(), help="State json file path")
    subparsers = parser.add_subparsers(dest="cmd")

    subparsers.add_parser("check", help="Check if publishing is currently allowed")
    record_parser = subparsers.add_parser("record-note", help="Record a note publish event")
    record_parser.add_argument("--time", help="ISO format timestamp (default: current time)")

    set_mode_parser = subparsers.add_parser("set-mode", help="Switch pacing mode")
    set_mode_parser.add_argument("mode", choices=["cold_start", "growth", "high_velocity"])

    cd_parser = subparsers.add_parser("set-cooldown", help="Set temporary risk cooldown (hours)")
    cd_parser.add_argument("hours", type=float, default=48.0)

    args = parser.parse_args()

    if args.cmd == "check" or not args.cmd:
        res = check_cadence(args.state)
        print("=" * 60)
        print(f" Xiaohongshu Cadence Check [Mode: {res['mode']}]")
        print("=" * 60)
        print(f"[*] 今日发布: {res['today_count']} 篇 | 本周发布: {res['week_count']} 篇")
        print(f"[*] 黄金时段: {res['golden_window'] or '非主力波峰时段'}")
        if res["allowed"]:
            print("\n[+] ALLOWED: 节奏正常，允许发布。")
            return 0
        else:
            print("\n[-] BLOCKED: 当前触发限频阻断：")
            for r in res["reasons"]:
                print(f"  - {r}")
            if res["wait_seconds"] > 0:
                mins = res["wait_seconds"] // 60
                print(f"\n[*] 建议等待睡眠时间: {res['wait_seconds']} 秒 (~{mins} 分钟)")
            return 1

    elif args.cmd == "record-note":
        res = record_post(args.state, args.time)
        print(f"[+] 记录成功: {res['timestamp']} (总记录: {res['total_notes']} 篇)")
        return 0

    elif args.cmd == "set-mode":
        state = load_state(args.state)
        state["mode"] = args.mode
        save_state(args.state, state)
        print(f"[+] 运行模式已更新为: {args.mode}")
        return 0

    elif args.cmd == "set-cooldown":
        state = load_state(args.state)
        cd_dt = datetime.now(CST) + timedelta(hours=args.hours)
        state["cooldown_until"] = cd_dt.isoformat()
        save_state(args.state, state)
        print(f"[!] 触发安全冷却直至: {cd_dt.strftime('%Y-%m-%d %H:%M:%S CST')}")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
