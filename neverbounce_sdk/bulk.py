from .utils import urlfor


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

_yes_no_repr = {
    'int': 'BIN_1_0',
    'upper': 'BIN_Y_N',
    'lower': 'BIN_y_n',
    'lowercase': 'BIN_yes_no',
    'capitalcase': 'BIN_Yes_No',
    'bool': 'BIN_true_false'
}

_linefeed_char_styles = {
    'unix': 'LINEFEED_0A',         # \n
    'windows': 'LINEFEED_0D0A',    # \r\n
    'appleII': 'LINEFEED_0D',      # \r
    'spooled': 'LINEFEED_0A'       # \n\r
}


class JobRunnerMixin(object):
    """
    Mixin class that exposes methods of interacting with the NeverBounce
    bulk API endpoints
    """

    def search(self):
        # TODO: needs pagination
        return NotImplemented

    def create(self, input, from_url=False,
               auto_parse=False, auto_run=False, as_sameple=False):
        """
        Creates a bulk job
        """
        endpoint = urlfor('jobs', 'create')
        # TODO: ask about the filename parameter
        data = dict(input=input,
                    auto_parse=int(auto_parse),
                    auto_run=int(auto_run),
                    as_sameple=int(as_sameple))
        data['input_location'] = 'remote_url' if from_url else 'supplied'
        resp = self._make_request('POST', endpoint, json=data)
        self._check_response(resp)
        # XXX Job handles (return here)
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
        # XXX Job handles (return here)
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
        # XXX Job handles (return here)
        return resp.json()

    def status(self, job_id):
        endpoint = urlfor('jobs', 'status')
        resp = self._make_request('GET', endpoint, params=dict(job_id=job_id))
        self._check_response(resp)
        # XXX Job handles (return here)
        return resp.json()

    def results(self):
        # TODO: needs pagination
        return NotImplemented

    def download(self, job_id, fname,
                 segmentation=('valids', 'invalids', 'catchalls', 'unknowns'),
                 appends=(),
                 yes_no_representation='int',
                 line_feed_type='unix'):
        """
        Download the full results of job ``job_id`` to a csv file ``fname``.
        """
        # construct this mass of options
        data = dict(job_id=job_id)

        data.update({key: 1
                     for key in segmentation
                     if key in _segmentation_options})

        data.update({key: 1
                     for key in appends
                     if key in _appends_options})

        # XXX: how are the settings sent, as json/form data? Assume so.
        if yes_no_representation.startswith('BIN'):
            data['binary_operators_type'] = yes_no_representation
        else:
            data['binary_operators_type'] = _yes_no_repr[yes_no_representation]

        if line_feed_type.startswith('LINEFEED'):
            data['line_feed_type'] = line_feed_type
        else:
            data['line_feed_type'] = _linefeed_char_styles[line_feed_type]

        endpoint = urlfor('jobs', 'download')
        # the return val is streaming; remember to set stream
        resp = self._make_request('POST', endpoint, json=data, stream=True)
        # cannot use self._check_response; this returns octets and hence
        # resp.json() (should) fail
        # we can still check for wire problems though
        resp.raise_for_status()
        # actually, TODO: how does this endpoint signal failure? The presence
        # of JSON response instead of application/octet-stream? There's no
        # actual error handling here yet

        # write the streaming csv file to fname
        with open(fname, 'wb') as fd:
            for chunk in resp.iter_content(chunk_size=128):
                fd.write(chunk)

    def delete(self, job_id):
        """
        Permanently delete the job with id ``job_id``
        """
        endpoint = urlfor('jobs', 'delete')
        resp = self._make_request('POST', endpoint, data=dict(job_id=job_id))
