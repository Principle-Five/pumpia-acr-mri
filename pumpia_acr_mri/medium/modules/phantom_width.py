"""
Phantom width of ACR MRI phantom
"""
from pumpia_acr_mri.bases.modules.phantom_width import ACRMRIPhantomWidth

from pumpia_acr_mri.medium.acr_mri_context import MedACRContextManager


class MedACRPhantomWidth(ACRMRIPhantomWidth):
    """
    Calculates ACR MRI phantom width
    """
    HALF_LINE_LENGTH = 100
    PHANTOM_WIDTH = 165

    context_manager = MedACRContextManager()
