import typing
from collections import defaultdict

from mlflow.tracking._tracking_service.utils import _get_default_host_creds
from mlflow.utils.rest_utils import MlflowHostCreds, http_request_safe

from mlfoundry.monitoring.entities import ActualPacket, BasePacket, PredictionPacket
from mlfoundry.monitoring.store.repositories.dto import (
    ActualData,
    BatchInsertRequest,
    BatchUpdateActualRequest,
    ClassPrediction,
    Data,
    MlModelPrediction,
)
from mlfoundry.tracking.entities import AuthServerInfo


# TODO @nikp1172 add feature of autmatically serializing datetime object in \
#  mlflow.utils.rest_utils.http_request
class RestMonitoringStore:
    def __init__(self, host_uri: str):
        self.host_creds = _get_default_host_creds(store_uri=host_uri)

    def _insert_prediction(self, prediction_packets: typing.List[PredictionPacket]):
        if not prediction_packets:
            return
        items = [
            Data(
                data_id=packet.prediction.data_id,
                features=packet.prediction.features,
                prediction=MlModelPrediction(
                    value=packet.prediction.prediction_data.value,
                    probabilities=[
                        ClassPrediction(label=feature_name, score=score)
                        for feature_name, score in packet.prediction.prediction_data.probabilities.items()
                    ],
                    shap_values=packet.prediction.prediction_data.shap_values,
                    occurred_at=packet.prediction.occurred_at,
                ),
                raw_data=packet.prediction.raw_data,
            )
            for packet in prediction_packets
        ]
        batch_insert_request = BatchInsertRequest(
            model_version_id=prediction_packets[0].model_version_id,
            items=items,
        )

        response = http_request_safe(
            host_creds=self.host_creds,
            endpoint="/v1/data/batch-insert",
            method="post",
            json=batch_insert_request.to_json_dict(),
        )

    def _update_actuals(self, actual_packets: typing.List[ActualPacket]):
        if not actual_packets:
            return

        batch_update_request = BatchUpdateActualRequest(
            model_version_id=actual_packets[0].model_version_id,
            items=[
                ActualData(data_id=packet.actual.data_id, actual=packet.actual.value)
                for packet in actual_packets
            ],
        )
        response = http_request_safe(
            host_creds=self.host_creds,
            endpoint="/v1/data/batch-update-actual",
            method="post",
            json=batch_update_request.dict(),
        )

    def batch_log_inference(self, inference_packets: typing.List[BasePacket]):
        grouped_packets = defaultdict(list)
        for packet in inference_packets:
            grouped_packets[type(packet)].append(packet)

        # log predictions before actuals to avoid actuals getting logged before predictions
        if PredictionPacket in grouped_packets.keys():
            self._insert_prediction(grouped_packets[PredictionPacket])
        if ActualPacket in grouped_packets.keys():
            self._update_actuals(grouped_packets[ActualPacket])

    def enable_monitoring_if_not_enabled(self, model_version_id: str):
        response = http_request_safe(
            host_creds=self.host_creds,
            endpoint=f"/v1/model/enable",
            method="post",
            params={"model_version_id": model_version_id},
        )

    @staticmethod
    def get_auth_server_info(monitoring_uri: str) -> AuthServerInfo:
        response = http_request_safe(
            host_creds=MlflowHostCreds(host=monitoring_uri),
            endpoint="/v1/model/auth-server-info",
            method="get",
        )
        response = response.json()
        return AuthServerInfo.parse_obj(response)
