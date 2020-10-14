#!/usr/bin/env python

"""Tests for `broto3` package."""

import pytest


from broto3 import broto3


def test_simulated_errors():
    session = broto3.BrokeSession(error_rate=1.0)

    with pytest.raises(Exception) as e_info:
        session.client("s3").list_objects(
            Bucket='string',
            Delimiter='string',
            EncodingType='url',
            Marker='string',
            MaxKeys=123,
            Prefix='string',
            RequestPayer='requester',
            ExpectedBucketOwner='string'
        )
    assert str(e_info.value).split(":")[-1].strip() == broto3.BrokeSession.error_message


def test_real_errors():
    session = broto3.BrokeSession(error_rate=0.0)

    with pytest.raises(Exception) as e_info:
        session.client("s3").list_objects(
            Bucket='string',
            Delimiter='string',
            EncodingType='url',
            Marker='string',
            MaxKeys=123,
            Prefix='string',
            RequestPayer='requester',
            ExpectedBucketOwner='string'
        )
    assert str(e_info.value).split(":")[-1].strip() != broto3.BrokeSession.error_message
