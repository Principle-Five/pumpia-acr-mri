import sys
from pathlib import Path

if str(Path(__file__).resolve().parent.parent) not in sys.path:
    sys.path.append(str(Path(__file__).resolve().parent.parent))

from pumpia_acr_mri.scripts.run_med_acr_rpt import run_med_acr

run_med_acr()
