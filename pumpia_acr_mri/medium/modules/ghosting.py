"""
Ghosting module for medium ACR phantom.

This does not follow ACR guidelines
"""
from pumpia_acr_mri.bases.modules.ghosting import ACRMRIGhosting

from pumpia_acr_mri.medium.acr_mri_context import MedACRContextManager


class MedACRGhosting(ACRMRIGhosting):
    """
    Ghosting module for medium ACR phantom.
    """
    context_manager = MedACRContextManager()
