from azure.cli.testsdk.scenario_tests import (
    RecordingProcessor
)
from azure.cli.testsdk.scenario_tests.utilities import is_text_payload
import json

MOCK_ACR_TOKEN = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
MOCK_SAS_URI = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"


class AcrTokenReplacer(RecordingProcessor):
    def process_response(self, response):
        ACR_TOKEN = "acrToken"
        if is_text_payload(response) and response["body"]["string"]:
            try:
                response_body = json.loads(response["body"]["string"])
                if ACR_TOKEN in response_body:
                    response_body[ACR_TOKEN] = MOCK_ACR_TOKEN
                response["body"]["string"] = json.dumps(response_body)
            except TypeError:
                pass
        return response


class SasUriReplacer(RecordingProcessor):
    def process_response(self, response):
        CONTAINER_CREDENTIALS = "containerCredentials"
        CONTAINER_SAS_URI = "containerSasUri"
        if not (is_text_payload(response) and response["body"]["string"]):
            return response

        response_body = json.loads(response["body"]["string"])
        try:
            if CONTAINER_CREDENTIALS not in response_body:
                return response

            credentials_list = response_body[CONTAINER_CREDENTIALS]
            new_credentials_list = []

            for credential in credentials_list:
                if CONTAINER_SAS_URI in credential:
                    credential[CONTAINER_SAS_URI] = MOCK_SAS_URI
                new_credentials_list.append(credential)

            response_body[CONTAINER_CREDENTIALS] = new_credentials_list
            response["body"]["string"] = json.dumps(response_body)
        except TypeError:
            pass

        return response
