"""
Subtraction SNR module for ACR MRI phantom
"""
from pumpia_acr_mri.bases.modules.sub_snr import ACRMRISubSNR

from pumpia_acr_mri.large.acr_mri_context import LargeACRContextManager


class LargeACRSubSNR(ACRMRISubSNR):
    """
    Module for subtraction method SNR on ACR MRI phantom.
    """
    context_manager = LargeACRContextManager()
