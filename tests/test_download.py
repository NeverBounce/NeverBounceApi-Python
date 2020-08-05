"""Test the API endpoints located at /jobs"""
from __future__ import unicode_literals
import json

import pytest
import responses

import neverbounce_sdk
from neverbounce_sdk import urlforversion, GeneralException


@pytest.fixture
def client():
    api_key = 'secret key'
    return neverbounce_sdk.client(api_key=api_key)


@pytest.fixture
def tempfile(tmpdir):
    return tmpdir.join('test.csv')


@responses.activate
def test_download_defaults(client, tempfile):
    responses.add(responses.POST,
                  urlforversion('v4.2', 'jobs', 'download'),
                  body=r'data\ndata',
                  status=200,
                  content_type='application/octet-stream')

    client.jobs_download(123, tempfile, line_feed_type='LINEFEED_0A')
    assert tempfile.read() == r'data\ndata'

    called_with = json.loads(responses.calls[0].request.body.decode('UTF-8'))
    default_args = {
        'line_feed_type': 'LINEFEED_0A',
        'binary_operators_type': 'BIN_1_0',
        'valids': 1,
        'invalids': 1,
        'catchalls': 1,
        'unknowns': 1,
        'job_id': 123
    }

    for k, v in default_args.items():
        assert called_with[k] == v


@responses.activate
def test_download_upstream_error(client, tempfile):
    responses.add(responses.POST,
                  urlforversion('v4.2', 'jobs', 'download'),
                  status=200,
                  json={'status': 'general_failure',
                        'message': 'Something went wrong'})

    with pytest.raises(GeneralException):
        client.jobs_download(123, tempfile)


def test_malformed_download_options(client, tempfile):
    with pytest.raises(ValueError):
        client.jobs_download(123, tempfile, segmentation=('not an opt',))
    with pytest.raises(ValueError):
        client.jobs_download(123, tempfile, appends=('not an opt',))
    with pytest.raises(ValueError):
        client.jobs_download(123, tempfile, yes_no_representation='frowns')
    with pytest.raises(ValueError):
        client.jobs_download(123, tempfile, line_feed_type='emojis')
