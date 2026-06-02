# command line "python -m nuitka .\pumpia_acr_mri\scripts\run_large_acr_rpt_old.py"

# tk-inter is needed for tkinter to work with nuitka
# nuitka documentation suggests it is not explicitly needed/found automatically but this is wrong
# (possibly due to inclusion of matplotlib)

# nuitka-project: --enable-plugin=tk-inter
# nuitka-project: --mode=onefile
# nuitka-project: --windows-console-mode=disable
# nuitka-project: --user-package-configuration-file=dicoms.nuitka-package.config.yml

from pumpia_acr_mri.large_old.acr_mri_rpt_collection import LargeACRrptCollection


def run_large_acr():
    LargeACRrptCollection.run()


if __name__ == "__main__":
    run_large_acr()
