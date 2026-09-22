import tempfile
import unittest
from pathlib import Path


class EnvironmentToolTests(unittest.TestCase):
    def test_exact_version_comparison(self):
        from scripts.repro.check_environment import version_matches

        self.assertTrue(version_matches("1.13.1+cu117", "1.13.1+cu117"))
        self.assertFalse(version_matches("1.13.1+cu116", "1.13.1+cu117"))

    def test_import_check_reports_missing_module_without_raising(self):
        from scripts.repro.check_environment import check_import

        result = check_import("module_that_cannot_exist_42")
        self.assertEqual("FAIL", result.status)
        self.assertIn("not importable", result.detail)


class SecurityScannerTests(unittest.TestCase):
    def test_scanner_detects_sensitive_patterns_without_echoing_secret(self):
        from scripts.repro.security_scan import scan_paths

        secret = "hf_" + "ABCDEFGHIJKLMNOPQRSTUVWXYZ123456"
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "unsafe.txt"
            path.write_text(
                "token=" + secret + "\n-----BEGIN " + "OPENSSH PRIVATE KEY-----\n",
                encoding="utf-8",
            )
            findings = scan_paths([path])
        self.assertGreaterEqual(len(findings), 2)
        self.assertNotIn(secret, "\n".join(item.message for item in findings))

    def test_scanner_detects_personal_absolute_paths(self):
        from scripts.repro.security_scan import scan_paths

        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "path.txt"
            path.write_text("/data/run01/" + "scxj889/project", encoding="utf-8")
            findings = scan_paths([path])
        self.assertTrue(any(item.kind == "personal-path" for item in findings))

    def test_scanner_rejects_large_files(self):
        from scripts.repro.security_scan import scan_paths

        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "large.bin"
            path.write_bytes(b"0" * 33)
            findings = scan_paths([path], max_bytes=32)
        self.assertEqual("large-file", findings[0].kind)

    def test_scanner_accepts_harmless_text(self):
        from scripts.repro.security_scan import scan_paths

        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "safe.txt"
            path.write_text("QWEN_PLANNER_MODEL_PATH=/srv/models/qwen", encoding="utf-8")
            self.assertEqual([], scan_paths([path]))


if __name__ == "__main__":
    unittest.main()
