"""
Integral uniformity module for ACR MRI phantom
"""
from pumpia_acr_mri.bases.modules.uniformity import ACRMRIUniformity

from pumpia_acr_mri.medium.acr_mri_context import MedACRContextManager


class MedACRUniformity(ACRMRIUniformity):
    """
    Integral uniformity module for ACR MRI phantom.
    """
    context_manager = MedACRContextManager()
