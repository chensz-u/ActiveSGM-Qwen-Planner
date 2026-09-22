import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class EnvironmentContractTests(unittest.TestCase):
    def test_supported_environment_has_compatible_core_versions(self):
        environment = (ROOT / "envs/environment-cu117.yml").read_text(encoding="utf-8")
        requirements = (ROOT / "envs/requirements-repro.txt").read_text(encoding="utf-8")
        installer = (ROOT / "scripts/setup/install_environment.sh").read_text(encoding="utf-8")
        combined = "\n".join((environment, requirements, installer))

        expected = (
            "python=3.8",
            "torch==1.13.1+cu117",
            "torchvision==0.14.1+cu117",
            "torchaudio==0.13.1+cu117",
            "mmcv-full==1.6.0",
            "mmdet==2.25.3",
            "mmsegmentation==0.26.0",
            "transformers==4.45.2",
        )
        for pin in expected:
            self.assertIn(pin, combined)
        self.assertNotIn("mmcv==2.0.0", combined)

    def test_installer_is_fail_fast_and_has_no_machine_specific_networking(self):
        installer = (ROOT / "scripts/setup/install_environment.sh").read_text(encoding="utf-8")
        self.assertIn("set -Eeuo pipefail", installer)
        self.assertNotRegex(installer, r"/home/[^/$\s]+")
        self.assertNotRegex(installer, r"https?_proxy=")


if __name__ == "__main__":
    unittest.main()
