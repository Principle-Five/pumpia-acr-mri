"""
Integral uniformity module for ACR MRI phantom
"""
from pumpia_acr_mri.bases.modules.uniformity import ACRMRIUniformity

from pumpia_acr_mri.large.acr_mri_context import LargeACRContextManager


class LargeACRUniformity(ACRMRIUniformity):
    """
    Integral uniformity module for ACR MRI phantom.
    """
    context_manager = LargeACRContextManager()
