"""
Ghosting module for medium ACR phantom.

This does not follow ACR guidelines
"""
from pumpia_acr_mri.bases.modules.ghosting import ACRMRIGhosting

from pumpia_acr_mri.large_old.acr_mri_context import LargeACRContextManager


class LargeACRGhosting(ACRMRIGhosting):
    """
    Ghosting module for large ACR phantom.
    """
    context_manager = LargeACRContextManager()
