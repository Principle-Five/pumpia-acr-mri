"""
Slice width for Medium ACR Phantom
"""
from pumpia_acr_mri.bases.modules.slice_width import ACRMRISliceWidth

from pumpia_acr_mri.medium.acr_mri_context import MedACRContextManager


class MedACRSliceWidth(ACRMRISliceWidth):
    """
    Calculates slice width for the ACR MRI phantom by fitting to a flat top gaussian.

    Overall slice width is calculated by taking the geometric mean
    of the top and bottom ramp widths.
    """
    context_manager = MedACRContextManager()
