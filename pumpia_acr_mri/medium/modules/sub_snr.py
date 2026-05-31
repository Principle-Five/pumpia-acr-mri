"""
Subtraction SNR module for ACR MRI phantom
"""
from pumpia_acr_mri.bases.modules.sub_snr import ACRMRISubSNR

from pumpia_acr_mri.medium.acr_mri_context import MedACRContextManager


class MedACRSubSNR(ACRMRISubSNR):
    """
    Module for subtraction method SNR on ACR MRI phantom.
    """
    context_manager = MedACRContextManager()
