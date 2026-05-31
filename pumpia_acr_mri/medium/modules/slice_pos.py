"""
Slice postition for Medium ACR Phantom.

Slice position is given in absolute offset, not the distance measured by the bars.
"""
from pumpia_acr_mri.bases.modules.slice_pos import ACRMRISlicePosition

from pumpia_acr_mri.medium.acr_mri_context import MedACRContextManager


class MedACRSlicePosition(ACRMRISlicePosition):
    """
    Calculates slice position for the ACR MRI phantom.

    Slice position is given in absolute offset, not the distance measured by the bars.
    """
    ROI_OFFSET = 55
    context_manager = MedACRContextManager()
