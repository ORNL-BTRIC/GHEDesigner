import os
from datetime import datetime

from ghedesigner.manager import run_manager_from_cli_worker
from ghedesigner.tests.ghe_base_case import GHEBaseTest


class TestDemoFiles(GHEBaseTest):

    def test_demo_files(self):

        time_str = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")

        for _, _, files in os.walk(self.demos_path):
            for f in files:
                try:
                    demo_file_path = self.demos_path / f
                    out_dir = self.demo_output_parent_dir / time_str / f.replace('.json', '')
                    os.makedirs(out_dir)
                    run_manager_from_cli_worker(input_file_path=demo_file_path, output_directory=out_dir)
                except:
                    print(f"Demo file failed: {f}")
                    exit(1)
