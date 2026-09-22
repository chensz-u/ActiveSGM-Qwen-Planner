import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock


class RuntimePathTests(unittest.TestCase):
    def test_model_path_uses_environment_override(self):
        from src.llm.runtime_paths import resolve_qwen_model_path

        with tempfile.TemporaryDirectory() as temp_dir:
            with mock.patch.dict(os.environ, {"QWEN_PLANNER_MODEL_PATH": temp_dir}):
                self.assertEqual(Path(temp_dir).resolve(), resolve_qwen_model_path())

    def test_model_path_defaults_to_repository_models_directory(self):
        from src.llm import runtime_paths

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            expected = root / "models/Qwen2.5-1.5B-Instruct"
            expected.mkdir(parents=True)
            with mock.patch.object(runtime_paths, "REPO_ROOT", root), mock.patch.dict(
                os.environ, {}, clear=True
            ):
                self.assertEqual(expected.resolve(), runtime_paths.resolve_qwen_model_path())

    def test_missing_model_path_has_actionable_error(self):
        from src.llm import runtime_paths

        with tempfile.TemporaryDirectory() as temp_dir:
            with mock.patch.object(runtime_paths, "REPO_ROOT", Path(temp_dir)), mock.patch.dict(
                os.environ, {}, clear=True
            ):
                with self.assertRaisesRegex(FileNotFoundError, "download_qwen.py"):
                    runtime_paths.resolve_qwen_model_path()


class DownloadSafetyTests(unittest.TestCase):
    def test_nonempty_download_directory_requires_force(self):
        from scripts.setup.download_qwen import prepare_download_target

        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir)
            (target / "existing.txt").write_text("keep", encoding="utf-8")
            with self.assertRaisesRegex(FileExistsError, "--force"):
                prepare_download_target(target, force=False)

    def test_force_allows_reusing_nonempty_directory_without_deleting_it(self):
        from scripts.setup.download_qwen import prepare_download_target

        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir)
            existing = target / "existing.txt"
            existing.write_text("keep", encoding="utf-8")
            self.assertEqual(target.resolve(), prepare_download_target(target, force=True))
            self.assertEqual("keep", existing.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
