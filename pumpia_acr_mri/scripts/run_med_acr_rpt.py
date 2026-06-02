# command line "python -m nuitka .\pumpia_acr_mri\scripts\run_med_acr_rpt.py"

# tk-inter is needed for tkinter to work with nuitka
# nuitka documentation suggests it is not explicitly needed/found automatically but this is wrong
# (possibly due to inclusion of matplotlib)

# nuitka-project: --enable-plugin=tk-inter
# nuitka-project: --mode=onefile
# nuitka-project: --windows-console-mode=disable
# nuitka-project: --user-package-configuration-file=dicoms.nuitka-package.config.yml

from pumpia_acr_mri.medium.acr_mri_rpt_collection import MedACRrptCollection


def run_med_acr():
    MedACRrptCollection.run()


if __name__ == "__main__":
    run_med_acr()
