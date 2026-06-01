"""
Calculates the contrast of the 1 mm resolution insert.
"""
from pumpia_acr_mri.bases.modules.resolution import ACRMRIResolution

from pumpia_acr_mri.medium.acr_mri_context import MedACRContextManager


class MedACRResolution(ACRMRIResolution):
    """
    Calculates the contrast of the 1mm resolution insert.
    """
    BOX_Y_OFFSET = 28
    BOX_X_OFFSET = -5
    context_manager = MedACRContextManager()
