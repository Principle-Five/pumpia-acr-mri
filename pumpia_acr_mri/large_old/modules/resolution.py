"""
Calculates the contrast of the 1 mm resolution insert.
"""
from pumpia_acr_mri.bases.modules.resolution import ACRMRIResolution

from pumpia_acr_mri.large_old.acr_mri_context import LargeACRContextManager


class LargeACRResolution(ACRMRIResolution):
    """
    Calculates the contrast of the 1mm resolution insert.
    """
    BOX_Y_OFFSET = 30
    BOX_X_OFFSET = 0
    context_manager = LargeACRContextManager()
