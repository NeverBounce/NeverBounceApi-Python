from .utils import urlforversion

__all__ = ['JobRunnerMixin']

_segmentation_options = {
    'valids',
    'invalids',
    'catchalls',
    'unknowns',
    'disposables',
    'include_duplicates',
    'only_duplicates',
    'only_bad_syntax'
}

_appends_options = {
    'bad_syntax',
    'free_email_host',
    'role_account',
    'addr',
    'alias',
    'host',
    'subdomain',
    'domain',
    'tld',
    'fqdn',
    'network',
    'has_dns_info',
    'has_mail_server',
    'mail_server_reachable',
    'email_status_int',
    'email_status'
}

_job_status = {
    'under_review',
    'queued',
    'failed',
    'complete',
    'running',
    'parsing',
    'waiting',
    'parsing',
    'uploading'
}


class ResultIter(object):
    """Utility class for iterating through a paginated API. """
    page_end = object()

    def __init__(self, method, *args, **kwargs):
        self._method = method
        self.data = method(*args, **kwargs)
        self._update()

    def _update(self):
        self._results = iter(self.data['results'])
        self.page = int(self.data['query']['page'])
        self.total_pages = int(self.data['total_pages'])
        self.total_results = int(self.data['total_results'])

    def get_next_page(self):
        query = {}
        for key, val in self.data['query'].items():
            if key in _job_status or key in ('page', 'items_per_page'):
                query[key] = int(val)
            else:
                query[key] = val

        query['page'] += 1
        self.data = self._method(**query)
        self._update()

    def __next__(self):
        # traverse pages
        rval = next(self._results, self.page_end)
        if rval is self.page_end:
            self.get_next_page()
            # if this raises StopIteration, then we're done
            return next(self._results)
        return rval

    # Python 2 COMPAT
    next = __next__

    def __iter__(self):
        return self


class JobRunnerMixin(object):
    """
    Mixin class that exposes methods of interacting with the NeverBounce
    bulk API endpoints.
    """

    def raw_search(self,
                   job_id=None, filename=None, job_status=None,
                   page=1, items_per_page=10, **extra_query):
        """Direct interface to the jobs/search endpoint. See the documentation
        for :py:class:``search`` for more."""
        data = dict(page=page, items_per_page=items_per_page)

        if job_id:
            data['job_id'] = job_id

        if filename:
            data['filename'] = filename

        if job_status:
            if job_status not in _job_status:
                msg = ('unknown argument {} for `job_status` in `search`; '
                       'must be one of {}'.format(job_status, _job_status))
                raise ValueError(msg)
            data['job_status'] = job_status

        data.update(extra_query)

        endpoint = urlforversion(self.api_version, 'jobs', 'search')
        resp = self._make_request('GET', endpoint, params=data)
        self._check_response(resp)
        return resp.json()

    def raw_results(self, job_id, page=1, items_per_page=10, **extra_query):
        """Direct interface to the jobs/results endpoint. See the documentation
        fro ``results`` for more."""
        data = dict(job_id=job_id,
                    page=page,
                    items_per_page=items_per_page)

        data.update(extra_query)

        endpoint = urlforversion(self.api_version, 'jobs', 'results')
        resp = self._make_request('GET', endpoint, params=data)
        self._check_response(resp)
        return resp.json()

    def jobs_search(self, **kwargs):
        """
        This function wraps the ``raw_search`` method in a custom results
        iterator.  Iteration is over the items of the ``results`` object
        returned by the API.  The iterator object will automatically fetch
        consecutive pages from the API; the page to start with and page size
        may be controlled by the ``page`` and ``items_per_page`` keyword-only
        arguments, which are passed directly to ``raw_search``.

        Keyword Arguments:
            job_id (int):
                If given, match search results against this job id. Default is
                None.

            filename (str):
                If given, return all results with exactly this filename.
                Default is None.

            job_status (str):
                If given, filter the results to only include the category of
                job given by ``show_only``.  Allowable categories are:

                    under_review
                    queued
                    failed
                    complete
                    running
                    parsing
                    waiting
                    parsing
                    uploading


                Default is ``None`` (perform no category filtering).

            page (int):
                The search results page to start from.

            items_per_page (int):
                How many items to include per page of results.

        Returns:
            An instance of ``_result_iter``

        See Also:
            https://developers.neverbounce.com/v4.0/reference#jobs-search
        """
        return ResultIter(self.raw_search, **kwargs)

    def jobs_results(self, job_id, **kwargs):
        """
        This function wraps the ``raw_results`` method in a custom results
        iterator.  Iteration is over the items of the ``results`` object
        returned by the API.  The iterator object will automatically fetch
        consecutive pages from the API; the page to start with and page size
        may be controlled by the ``page`` and ``items_per_page`` keyword-only
        arguments, which are passed directly to ``raw_results``.

        Arguments:
            job_id (int):
                The numeric id of the job to get results for.

        Returns:
            An instance of ``_result_iter``

        See Also:
            https://developers.neverbounce.com/v4.0/reference#jobs-results
        """
        return ResultIter(self.raw_results, job_id, **kwargs)

    def jobs_create(self, input, from_url=False, filename=None,
                    auto_parse=False, auto_start=False, as_sample=False,
                    historical_data=True, allow_manual_review=None,
                    callback_url=None, callback_headers=None):
        """
        Creates a bulk job.

        Arguments:
            input (str or list):
                The input may be either a string URL to a remote location from
                which to read input objects, or a list of mappings denoting
                emails.  Each mapping should contain an ``email`` key and may
                contain arbitrary other keys as metadata.

            from_url (bool):
                If ``True``, consider ``input`` a remote URL. Default is
                ``False``.

            filename (str):
                If given, will be associated with the job as metadata. Default
                is ``None``.

            auto_parse (bool):
                If ``True``, begin parsing the job immediately upon receipt.
                Default is ``False``.

            auto_start (bool):
                If ``True``, begin processing the job immediately upon parsing.
                Default is ``False``.

            as_sample (bool):
                If ``True``, run only a sample of the given input and return an
                estimation of the job's total bounce rate.

            historical_data (bool): If ``True``, return historical data.
                Default is ``True``.

            allow_manual_review (bool):
                If ``True``, allows job to fall to manual review.
                Default is ``None``.

            callback_url (str):
                If given, callbacks will be send to the specified URL. Default
                is ``None``.

            callback_headers (dict):
                If given, callbacks with headers will be send to the URL
                specified in "callback_url".
                Default is ``None``.

        Returns:
            A ``dict`` with keys ``status``, ``job_id``, and
            ``execution_time``.

        See Also:
            https://developers.neverbounce.com/v4.0/reference#jobs-create
        """
        endpoint = urlforversion(self.api_version, 'jobs', 'create')

        data = dict(input=input,
                    auto_parse=int(auto_parse),
                    auto_start=int(auto_start),
                    run_sample=int(as_sample))

        data['request_meta_data'] = {
            'leverage_historical_data': int(historical_data)
        }

        data['input_location'] = 'remote_url' if from_url else 'supplied'
        if filename is not None:
            data['filename'] = filename

        if allow_manual_review is not None:
            data['allow_manual_review'] = int(allow_manual_review)

        if callback_url is not None:
            data['callback_url'] = callback_url

        if callback_headers is not None:
            data['callback_headers'] = callback_headers

        resp = self._make_request('POST', endpoint, json=data)
        self._check_response(resp)

        return resp.json()

    def jobs_parse(self, job_id, auto_start=False):
        """
        This endpoint allows you to parse a job created with auto_parse
        disabled. You cannot reparse a list once it's been parsed.

        Arguments:
            job_id (int):
                the job's numeric ID

            auto_start (bool):
                Whether or not to begin immediately processing the job
                following parsing.

        Returns:
            A ``dict`` with keys ``status``, ``queue_id``, and
            ``execution_time``.

        See Also:
            https://developers.neverbounce.com/v4.0/reference#jobs-parse
        """
        endpoint = urlforversion(self.api_version, 'jobs', 'parse')
        data = dict(job_id=job_id, auto_start=int(auto_start))
        resp = self._make_request('POST', endpoint, json=data)
        self._check_response(resp)
        return resp.json()

    def jobs_start(self, job_id, run_sample=False, allow_manual_review=None):
        """
        This endpoint allows you to start a job created or parsed with
        auto_start disabled. Once the list has been started the credits will be
        deducted and the process cannot be stopped or restarted.

        Arguments:
            job_id (int):
                the job's numeric ID

            run_sample (bool):
                Whether or not to run a sample of this job's contents and
                return an estimate of the job's bounce rate

            allow_manual_review (bool):
                If ``True``, allows job to fall to manual review.
                Default is ``None``.

        Returns:
            A ``dict`` with keys ``status``, ``queue_id``, and
            ``execution_time``.

        See Also:
            https://developers.neverbounce.com/v4.0/reference#jobs-start
        """
        endpoint = urlforversion(self.api_version, 'jobs', 'start')
        data = dict(job_id=job_id, run_sample=int(run_sample))

        if allow_manual_review is not None:
            data['allow_manual_review'] = int(allow_manual_review)

        resp = self._make_request('POST', endpoint, json=data)
        self._check_response(resp)
        return resp.json()

    def jobs_status(self, job_id):
        """
        Returns a status object (a dict) with a number of keys relevant to the
        status of the job given by ``job_id``.

        Arguments:
            job_id (int): the job's numeric id

        Returns:
            A ``dict`` with keys indicating various aspects of the job's
            progression.

        See also:
            https://developers.neverbounce.com/v4.0/reference#jobs-status
        """
        endpoint = urlforversion(self.api_version, 'jobs', 'status')
        resp = self._make_request('GET', endpoint, params=dict(job_id=job_id))
        self._check_response(resp)
        return resp.json()

    def jobs_download(self, job_id, fd,
                      segmentation=('valids', 'invalids',
                                    'catchalls', 'unknowns'),
                      appends=(),
                      yes_no_representation='int',
                      line_feed_type='unix'):
        r"""
        Download the full results of job ``job_id`` as a CSV file into the
        file-like object given by ``fd``.

        Arguments:

            job_id (int):
                the integer ID of the job to download

            fd (file):
                an open file or file-like object to write the download to

            segmentation (list[str]):
                A list of string values declaring what subset of the full
                results to download. Possible values are:

                   * valids
                   * invalids
                   * catchalls
                   * unknowns
                   * disposables
                   * include_duplicates
                   * only_duplicates
                   * only_bad_syntax

            appends (list[str]):
                A list of fields to append to the downloaded CSV. Valid options
                are:

                   * bad_syntax
                   * free_email_host
                   * role_account
                   * addr
                   * alias
                   * host
                   * subdomain
                   * domain
                   * tld
                   * fqdn
                   * network
                   * has_dns_info
                   * has_mail_server
                   * mail_server_reachable
                   * email_status_int
                   * email_status

            yes_no_representation (str):
                Sets the characters used to represent Boolean values in the
                generated CSV file. The following table gives each option's
                alias, the "raw" form actually sent in the request, and the
                meaning:

                .. table:: Boolean Value Representations
                   :widths: auto

                   =========== =============== ==========
                   Alias       Token           Meaning
                   =========== =============== ==========
                   int         BIN_1_0         1/0
                   upper       BIN_Y_N         Y/N
                   lower       BIN_y_n         y/n
                   lowercase   BIN_yes_no      yes/no
                   capitalcase BIN_Yes_No      Yes/No
                   bool        BIN_true_false  true/false
                   =========== =============== ==========

                You may use either the alias or the token as the setting, but
                only one setting may be given.

            line_feed_type (str):
                Sets the characters to use as line-ending in the generated CSV
                file. As with ``yes_no_representation``, you may use a
                convenience alias or the API's token, given in the following
                table:

                .. table:: Line Feed Characters
                   :widths: auto

                   =========== =============== ==========
                   Alias       Token           Meaning
                   =========== =============== ==========
                   unix        LINEFEED_0A     \n
                   windows     LINEFEED_0D0A   \r\n
                   appleII     LINEFEED_0D     \r
                   spooled     LINEFEED_0A     \n\r
                   =========== =============== ==========

        Returns:
            ``None``

        See Also:
            https://developers.neverbounce.com/v4.0/reference#jobs-download
        """
        data = dict(job_id=job_id)

        def add_opts(opts, allowable):
            # does a small bit of bookeeping to make sure we're returning
            # useful errors if an option is given with a typo
            for opt in opts:
                if opt not in allowable:
                    msg = ('{} is not a recognized option for the download'
                           'endpoint'.format(opt))
                    raise ValueError(msg)
                data[opt] = 1

        add_opts(segmentation, _segmentation_options)
        add_opts(appends, _appends_options)

        def set_setting(arg, argname, map_):
            # confer note on add_opts; these are just conveniences
            if arg in map_.values():
                data[argname] = arg
            else:
                try:
                    data[argname] = map_[arg]
                except KeyError:
                    msg = '{} is not a recognizable value for {}'.format(
                        arg, argname
                    )
                    raise ValueError(msg)

        set_setting(yes_no_representation, 'binary_operators_type', {
            'int': 'BIN_1_0',
            'upper': 'BIN_Y_N',
            'lower': 'BIN_y_n',
            'lowercase': 'BIN_yes_no',
            'capitalcase': 'BIN_Yes_No',
            'bool': 'BIN_true_false'
        })

        set_setting(line_feed_type, 'line_feed_type', {
            'unix': 'LINEFEED_0A',         # \n
            'windows': 'LINEFEED_0D0A',    # \r\n
            'appleII': 'LINEFEED_0D',      # \r
            'spooled': 'LINEFEED_0A'       # \n\r
        })

        endpoint = urlforversion(self.api_version, 'jobs', 'download')
        # the return val is (possibly) streaming; remember to set stream
        resp = self._make_request('POST', endpoint, json=data, stream=True)

        # returns json if there's an error, octet-stream if all is good
        if resp.headers['Content-Type'] == 'application/json':
            self._check_response(resp)

        # write the streaming csv file to fd
        for chunk in resp.iter_content(chunk_size=128):
            fd.write(chunk)

    def jobs_delete(self, job_id):
        """
        Permanently delete the job with id ``job_id``

        Arguments:
            job_id (int):  The job's numeric ID.

        Returns:
            A ``dict`` with keys ``status`` and ``execution_time``

        See Also:
            https://developers.neverbounce.com/v4.0/reference#jobs-delete
        """
        endpoint = urlforversion(self.api_version, 'jobs', 'delete')
        resp = self._make_request('GET', endpoint, params=dict(job_id=job_id))
        self._check_response(resp)
        return resp.json()
