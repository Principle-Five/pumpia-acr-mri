"""
Slice postition for Medium ACR Phantom.

Slice position is given in absolute offset, not the distance measured by the bars.
"""
from pumpia_acr_mri.bases.modules.slice_pos import ACRMRISlicePosition

from pumpia_acr_mri.large_old.acr_mri_context import LargeACRContextManager


class LargeACRSlicePosition(ACRMRISlicePosition):
    """
    Calculates slice position for the ACR MRI phantom.

    Slice position is given in absolute offset, not the distance measured by the bars.
    """
    ROI_OFFSET = 65
    context_manager = LargeACRContextManager()
