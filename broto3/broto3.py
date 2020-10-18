"""Main module."""

import botocore
import boto3
import random
import time

from http import HTTPStatus


class BrokeSession(boto3.Session):
    error_message = "Simulated error from Broto3"
    def __init__(self, *args, latency=5, error_rate=0.2, latency_rate=0.1, **kwargs):
        super(BrokeSession, self).__init__(*args, **kwargs)

        self.latency = latency
        self.latency_rate = latency_rate
        self.error_rate = error_rate

    def client(self, *args, **kwargs):
        c = super(BrokeSession, self).client(*args, **kwargs)

        original_method = c._make_api_call

        def _make_api_call(operation_name, api_params):
            latency = (random.random() * self.latency) * \
                (random.random() < self.latency_rate)
            time.sleep(latency)

            if random.random() < self.error_rate:
                error_code = random.choice([s for s in HTTPStatus if s >= 400])
                error_class = c.exceptions.from_code(error_code)

                parsed_response = {
                    "Error": {
                        "Code": error_code,
                        "Message": BrokeSession.error_message
                    }
                }
                raise error_class(parsed_response, operation_name)
            else:
                return original_method(operation_name, api_params)

        c._make_api_call = _make_api_call
        return c
