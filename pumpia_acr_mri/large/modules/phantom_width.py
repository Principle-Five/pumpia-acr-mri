"""
Phantom width of ACR MRI phantom
"""
from pumpia_acr_mri.bases.modules.phantom_width import ACRMRIPhantomWidth

from pumpia_acr_mri.large.acr_mri_context import LargeACRContextManager


class LargeACRPhantomWidth(ACRMRIPhantomWidth):
    """
    Calculates ACR MRI phantom width
    """
    HALF_LINE_LENGTH = 110
    PHANTOM_WIDTH = 190

    context_manager = LargeACRContextManager()
