import importlib.util
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
import uuid


spec = importlib.util.spec_from_file_location(
    "asan_verify", Path(__file__).resolve().parents[1] / "verify.py"
)
verify = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verify)


class VerificationTests(unittest.TestCase):
    def evidence_dir(self):
        directory = Path.cwd() / "work" / "asan-unit-tests" / uuid.uuid4().hex
        directory.mkdir(parents=True)
        return directory

    def error_result(self):
        return {
            "returncode": 86, "timed_out": False, "stdout": "",
            "stderr": (
                "ERROR: AddressSanitizer: heap-buffer-overflow\n"
                "#0 in main /opt/asan-check/cases.c:15:12\n"
                "SUMMARY: AddressSanitizer: heap-buffer-overflow\n"
            ),
        }

    def test_expected_report_passes(self):
        self.assertTrue(verify.valid_error(self.error_result(), "heap-buffer-overflow"))

    def test_unrelated_crash_fails(self):
        result = self.error_result()
        result["returncode"] = 139
        self.assertFalse(verify.valid_error(result, "heap-buffer-overflow"))

    def test_wrong_category_fails(self):
        self.assertFalse(verify.valid_error(self.error_result(), "heap-use-after-free"))

    def test_missing_source_location_fails(self):
        result = self.error_result()
        result["stderr"] = result["stderr"].replace("cases.c:15:12", "0x12345")
        self.assertFalse(verify.valid_error(result, "heap-buffer-overflow"))

    def test_timeout_is_not_a_detection(self):
        result = self.error_result()
        result["timed_out"] = True
        self.assertFalse(verify.valid_error(result, "heap-buffer-overflow"))

    def test_normal_output_is_checked(self):
        result = {"returncode": 0, "timed_out": False, "stdout": "OK 7\n", "stderr": ""}
        self.assertTrue(verify.valid_normal(result))
        result["stdout"] = "wrong answer"
        self.assertFalse(verify.valid_normal(result))

    def test_normal_stderr_fails(self):
        result = {"returncode": 0, "timed_out": False, "stdout": "OK 7\n", "stderr": "error"}
        self.assertFalse(verify.valid_normal(result))

    def test_missing_command_is_logged(self):
        output = self.evidence_dir()
        result = verify.run_logged(
            output, "missing", ["asan-test-command-that-does-not-exist"]
        )
        self.assertIsNone(result["returncode"])
        self.assertTrue((output / "missing.json").is_file())

    def test_timeout_is_logged(self):
        result = verify.run_logged(
            self.evidence_dir(), "timeout",
            [sys.executable, "-c", "import time; time.sleep(2)"], timeout=0.05,
        )
        self.assertTrue(result["timed_out"])

    def test_log_cannot_be_overwritten(self):
        path = self.evidence_dir() / "result.json"
        verify.write_json(path, {"status": "failed"})
        with self.assertRaises(FileExistsError):
            verify.write_json(path, {"status": "passed"})

    def test_bounded_resources_pass(self):
        with patch.object(Path, "read_text", side_effect=["2147483648", "128", "200000 100000"]):
            self.assertEqual(verify.require_limits()["memory.max"], "2147483648")

    def test_unlimited_memory_fails(self):
        with patch.object(Path, "read_text", side_effect=["max", "128", "200000 100000"]):
            with self.assertRaises(RuntimeError):
                verify.require_limits()

    def test_unlimited_cpu_fails(self):
        with patch.object(Path, "read_text", side_effect=["2147483648", "128", "max 100000"]):
            with self.assertRaises(RuntimeError):
                verify.require_limits()

    def test_excessive_process_limit_fails(self):
        with patch.object(Path, "read_text", side_effect=["2147483648", "512", "200000 100000"]):
            with self.assertRaises(RuntimeError):
                verify.require_limits()


if __name__ == "__main__":
    unittest.main()
