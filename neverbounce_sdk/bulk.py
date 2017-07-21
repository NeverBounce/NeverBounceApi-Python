from .utils import urlfor

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
    'completed',
    'processing',
    'indexing',
    'failed',
    'manual_review',
    'unpurchased'
}


class _result_iter(object):
    """ Utility class for iterating through a paginated API """

    def __init__(method, *args, **kwargs):
        self.method = method
        self._update(method(*args, **kwargs))

    def __next__(self):
        while True:
            if not self.results:
                return
            for res in self.results:
                yield res

            params = self.raw_results['query']
            params['page'] += 1
            self._update(self.method(**params))

    def _update(self, obj):
        self.raw_results = obj
        self.results = obj['results']
        self.page = obj['query']['page']
        self.total_pages = obj['total_pages']


class JobRunnerMixin(object):
    """
    Mixin class that exposes methods of interacting with the NeverBounce
    bulk API endpoints
    """

    def raw_search(self,
                   job_id=None, filename=None, show_only=None,
                   page=0, items_per_page=10):
        """Direct interface to the jobs/search endpoint. """
        data = dict(page=page, items_per_page=items_per_page)

        if job_id:
            data['job_id'] = job_id

        if filename:
            data['filename'] = filename

        if show_only:
            if show_only not in _job_status:
                msg = ('unknown argument {} for `show_only` in `search`; '
                       'must be one of {}'.format(show_only, _job_status))
                raise ValueError(msg)
            data[show_only] = 1

        endpoint = urlfor('jobs', 'search')
        resp = self._make_request('GET', endpoint, params=data)
        self._check_response(resp)
        return resp.json()

    def raw_results(self, job_id, page=0, items_per_page=10):
        """Direct interface to the jobs/results endpoint. """
        data = dict(job_id=job_id,
                    page=page,
                    items_per_page=items_per_page)

        endpoint = urlfor('jobs', 'results')
        resp = self._make_request('GET', endpoint, params=data)
        self._check_response(resp)
        return resp.json()

    def search(self, **kwargs):
        return _result_iter(self.raw_search, **kwargs)

    def results(self, job_id, **kwargs):
        return _result_iter(self.raw_results, job_id, **kwargs)

    def create(self, input, from_url=False, filename=None,
               auto_parse=False, auto_run=False, as_sameple=False):
        """
        Creates a bulk job
        """
        endpoint = urlfor('jobs', 'create')

        data = dict(input=input,
                    auto_parse=int(auto_parse),
                    auto_run=int(auto_run),
                    as_sameple=int(as_sameple))

        data['input_location'] = 'remote_url' if from_url else 'supplied'
        if filename is not None:
            data['filename'] = filename

        resp = self._make_request('POST', endpoint, json=data)
        self._check_response(resp)

        return resp.json()

    def parse(self, job_id, auto_start=True):
        """
        This endpoint allows you to parse a job created with auto_parse
        disabled. You cannot reparse a list once it's been parsed.
        """
        endpoint = urlfor('jobs', 'parse')
        data = dict(job_id=job_id, auto_start=int(auto_start))
        resp = self._make_request('POST', endpoint, json=data)
        self._check_response(resp)

        return resp.json()

    def start(self, job_id, run_sample=False):
        """
        This endpoint allows you to start a job created or parsed with
        auto_start disabled. Once the list has been started the credits will be
        deducted and the process cannot be stopped or restarted.
        """
        endpoint = urlfor('jobs', 'start')
        data = dict(job_id=job_id, run_sample=int(run_sample))
        resp = self._make_request('POST', endpoint, json=data)
        self._check_response(resp)

        return resp.json()

    def status(self, job_id):
        endpoint = urlfor('jobs', 'status')
        resp = self._make_request('GET', endpoint, params=dict(job_id=job_id))
        self._check_response(resp)
        # XXX Job handles (return here)
        return resp.json()

    def download(self, job_id, fd,
                 segmentation=('valids', 'invalids', 'catchalls', 'unknowns'),
                 appends=(),
                 yes_no_representation='int',
                 line_feed_type='unix'):
        """
        Download the full results of job ``job_id`` to a file-like object
        ``fd``.
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

        endpoint = urlfor('jobs', 'download')
        # the return val is (possibly) streaming; remember to set stream
        resp = self._make_request('POST', endpoint, json=data, stream=True)

        # returns json if there's an error, octet-stream if all is good
        if resp.headers['Content-Type'] == 'application/json':
            self._check_response(resp)

        # write the streaming csv file to fd
        for chunk in resp.iter_content(chunk_size=128):
            fd.write(chunk)

    def delete(self, job_id):
        """
        Permanently delete the job with id ``job_id``
        """
        endpoint = urlfor('jobs', 'delete')
        resp = self._make_request('POST', endpoint, data=dict(job_id=job_id))
        self._check_response(resp)
        return resp.json()
