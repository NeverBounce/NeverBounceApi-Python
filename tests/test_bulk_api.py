"""Test the API endpoints located at /jobs (except /jobs/download)"""
from __future__ import unicode_literals
import json

import pytest
import responses

import neverbounce_sdk
from neverbounce_sdk import urlforversion
from neverbounce_sdk.bulk import _job_status


@pytest.fixture
def client():
    api_key = 'secret key'
    return neverbounce_sdk.client(api_key=api_key)


def test_search(client, monkeypatch):
    # Tests that the iteration wrapper works and that client.search correctly
    # calls client.raw_search
    expected_results = [{'data': val} for val in 'abc123']

    def _search(**kwargs):
        kwargs.update(dict(job_id=None, filename=None, job_status=None,
                      page=0, items_per_page=10))
        return dict(results=expected_results,
                    total_pages=1,
                    total_results=1,
                    query=kwargs)

    monkeypatch.setattr(client, 'raw_search', _search)
    results = client.jobs_search()
    for res, exp in zip(iter(results), expected_results):
        assert res == exp


def test_results(client, monkeypatch):
    # Tests that the iteration wrapper works and that client.results correctly
    # calls client.raw_results
    expected_results = [{'data': val} for val in 'abc123']

    def _results(job_id=0, **kwargs):
        kwargs.update(dict(filename=None, show_only=None,
                      page=0, items_per_page=10))
        return dict(results=expected_results,
                    total_pages=1,
                    total_results=1,
                    query=kwargs)

    monkeypatch.setattr(client, 'raw_results', _results)
    results = client.jobs_results(0)
    for res, exp in zip(iter(results), expected_results):
        assert res == exp


@responses.activate
def test_raw_result_interface(client):
    responses.add(responses.GET,
                  urlforversion('v4.2', 'jobs', 'results'),
                  status=200,
                  json={'status': 'success'})

    client.raw_results(123)
    for arg in ('job_id=123', 'page=1', 'items_per_page=10'):
        assert arg in responses.calls[0].request.url


@responses.activate
def test_raw_search_interface(client):
    responses.add(responses.GET,
                  urlforversion('v4.2', 'jobs', 'search'),
                  status=200,
                  json={'status': 'success'})

    # defaults
    client.raw_search()
    request_url = responses.calls[0].request.url
    for arg in ('job_id', 'filename') + tuple(_job_status):
        assert arg not in request_url
    for arg in ('page=1', 'items_per_page=10'):
        assert arg in request_url

    client.raw_search(job_id=123, filename='test.csv', job_status='complete')
    request_url = responses.calls[1].request.url
    for arg in ('page=1', 'items_per_page=10', 'job_id=123',
                'filename=test.csv', 'job_status=complete'):
        assert arg in request_url

    with pytest.raises(ValueError):
        client.raw_search(job_status='some unknown value OH NO')


@responses.activate
def test_create(client):
    responses.add(responses.POST,
                  urlforversion('v4.2', 'jobs', 'create'),
                  json={'status': 'success'},
                  status=200)

    raw_args = dict(input=['test@example.com'],
                    input_location='supplied',
                    auto_parse=0, auto_start=0, run_sample=0)

    client.jobs_create(['test@example.com'])
    called_with = json.loads(responses.calls[0].request.body.decode('UTF-8'))
    assert 'filename' not in called_with
    for k, v in raw_args.items():
        assert called_with[k] == v

    new_raw_args = raw_args.copy()
    new_raw_args['filename'] = 'testfile.csv'
    client.jobs_create(['test@example.com'], filename='testfile.csv')
    called_with = json.loads(responses.calls[1].request.body.decode('UTF-8'))
    for k, v in raw_args.items():
        assert called_with[k] == v


@responses.activate
def test_parse(client):
    responses.add(responses.POST,
                  urlforversion('v4.2', 'jobs', 'parse'),
                  json={'status': 'success'},
                  status=200)

    client.jobs_parse(123)
    called_with = json.loads(responses.calls[0].request.body.decode('UTF-8'))
    expected_args = dict(job_id=123, auto_start=0)
    for k, v in expected_args.items():
        assert called_with[k] == v


@responses.activate
def test_start(client):
    responses.add(responses.POST,
                  urlforversion('v4.2', 'jobs', 'start'),
                  json={'status': 'success'},
                  status=200)

    client.jobs_start(123)
    called_with = json.loads(responses.calls[0].request.body.decode('UTF-8'))
    expected_args = dict(job_id=123, run_sample=0)
    for k, v in expected_args.items():
        assert called_with[k] == v


@responses.activate
def test_status(client):
    responses.add(responses.GET,
                  urlforversion('v4.2', 'jobs', 'status'),
                  json={'status': 'success'},
                  status=200)

    client.jobs_status(123)
    assert 'job_id=123' in responses.calls[0].request.url


@responses.activate
def test_delete(client):
    responses.add(responses.GET,
                  urlforversion('v4.2', 'jobs', 'delete'),
                  json={'status': 'success'},
                  status=200)

    client.jobs_delete(123)
    assert 'job_id=123' in responses.calls[0].request.url
