#!/usr/bin/env python3
"""Unit tests for Xiaohongshu guard cadence logic."""

import unittest
import sys
import tempfile
import os
from pathlib import Path
from datetime import datetime, timedelta, timezone

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from guard import check_cadence, record_post, CST


class TestXiaohongshuGuard(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.state_file = Path(self.tmp_dir.name) / "test_state.json"

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_midnight_blackout_blocked(self):
        # 03:30 AM CST (midnight blackout)
        test_dt = datetime(2026, 10, 12, 3, 30, tzinfo=CST)
        res = check_cadence(self.state_file, target_time=test_dt)
        self.assertFalse(res["allowed"])
        self.assertTrue(any("夜间禁发" in r for r in res["reasons"]))

    def test_golden_window_allowed_when_empty(self):
        # 12:30 PM CST (Golden window: 午休闲)
        test_dt = datetime(2026, 10, 12, 12, 30, tzinfo=CST)
        res = check_cadence(self.state_file, target_time=test_dt)
        self.assertTrue(res["allowed"])
        self.assertEqual(res["golden_window"], "午休闲")

    def test_minimum_gap_enforced(self):
        # Record post at 12:00 PM CST
        t1 = datetime(2026, 10, 12, 12, 0, tzinfo=CST)
        record_post(self.state_file, timestamp=t1.isoformat())

        # Check at 14:00 PM (2h later, under 6h growth min gap)
        t2 = datetime(2026, 10, 12, 14, 0, tzinfo=CST)
        res = check_cadence(self.state_file, target_time=t2)
        self.assertFalse(res["allowed"])
        self.assertTrue(any("距上一次发布不足" in r for r in res["reasons"]))

        # Check at 19:00 PM (7h later, exceeds 6h gap)
        t3 = datetime(2026, 10, 12, 19, 0, tzinfo=CST)
        res3 = check_cadence(self.state_file, target_time=t3)
        self.assertTrue(res3["allowed"])


if __name__ == "__main__":
    unittest.main()
