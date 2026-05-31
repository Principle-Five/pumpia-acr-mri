"""
Calculates the contrast of the 1 mm resolution insert.
"""
from pumpia_acr_mri.bases.modules.resolution import ACRMRIResolution

from pumpia_acr_mri.large.acr_mri_context import LargeACRContextManager


class LargeACRResolution(ACRMRIResolution):
    """
    Calculates the contrast of the 1mm resolution insert.
    """
    context_manager = LargeACRContextManager()
