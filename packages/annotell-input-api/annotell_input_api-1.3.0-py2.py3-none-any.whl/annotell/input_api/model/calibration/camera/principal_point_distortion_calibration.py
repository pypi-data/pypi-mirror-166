from annotell.input_api.model.calibration.camera.common import BaseCameraCalibration
from annotell.input_api.model.calibration.common import CalibrationType
from annotell.input_api.model.base_serializer import BaseSerializer


class PrincipalPointDistortionCoefficients(BaseSerializer):
    k1: float
    k2: float


class PrincipalPoint(BaseSerializer):
    x: float
    y: float


class DistortionCenter(BaseSerializer):
    x: float
    y: float


class PrincipalPointDistortionCalibration(BaseCameraCalibration):
    calibration_type = CalibrationType.PRINCIPALPOINTDIST.value
    distortion_coefficients: PrincipalPointDistortionCoefficients
    distortion_center: DistortionCenter
    principal_point: PrincipalPoint