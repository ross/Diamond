
from diamond import *
import diamond.collector
import re
import subprocess
import os

class VarnishCollector(diamond.collector.Collector):
    """VarnishCollector grabs stats from Varnish and submits them the Graphite
    """
    _RE = re.compile("^(?P<stat>[\w_\(\)\.,]*)\s+(?P<psa>\d*)\s+"
                   "(?P<psan>[\d.]*)\s(?P<desc>[\w\., /]*)$", re.M)
    _CMD = '/usr/bin/varnishstat'
    _KEYS = ['client_conn', 'client_drop', 'client_req', 'cache_hit',
             'cache_hitpass', 'cache_miss', 'backend_conn', 'backend_unhealthy',
             'backend_busy', 'backend_fail', 'backend_reuse', 'backend_toolate',
             'backend_recycle', 'backend_retry', 'fetch_head', 'fetch_length',
             'fetch_chunked', 'fetch_eof', 'fetch_bad', 'fetch_close',
             'fetch_oldhttp', 'fetch_zero', 'fetch_failed', 'n_sess_mem',
             'n_sess', 'n_object', 'n_vampireobject', 'n_objectcore',
             'n_objecthead', 'n_waitinglist', 'n_vbc', 'n_wrk', 'n_wrk_create',
             'n_wrk_failed', 'n_wrk_max', 'n_wrk_lqueue', 'n_wrk_queued',
             'n_wrk_drop', 'n_backend', 'n_expired', 'n_lru_nuked',
             'n_lru_moved', 'losthdr', 'n_objsendfile', 'n_objwrite',
             'n_objoverflow', 's_sess', 's_req', 's_pipe', 's_pass', 's_fetch',
             's_hdrbytes', 's_bodybytes', 'sess_closed', 'sess_pipeline',
             'sess_readahead', 'sess_linger', 'sess_herd', 'shm_records',
             'shm_writes', 'shm_flushes', 'shm_cont', 'shm_cycles', 'sms_nreq',
             'sms_nobj', 'sms_nbytes', 'sms_balloc', 'sms_bfree', 'backend_req',
             'n_vcl', 'n_vcl_avail', 'n_vcl_discard', 'n_ban', 'n_ban_add',
             'n_ban_retire', 'n_ban_obj_test', 'n_ban_re_test', 'n_ban_dups',
             'hcb_nolock', 'hcb_lock', 'hcb_insert', 'accept_fail',
             'client_drop_late', 'uptime', 'dir_dns_lookups', 'dir_dns_failed',
             'dir_dns_hit', 'dir_dns_cache_full']

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        return {
            'path':     'varnish'
        }

    def collect(self):
        data = self.poll()
        for key in data:
            self.publish(key, int(data[key]))

    def poll(self):
        data = {}
        if not os.access(self._CMD, os.X_OK):
            return data
        output = subprocess.Popen([self._CMD, '-1'], stdout=subprocess.PIPE).communicate()[0]
        matches = self._RE.findall(output)
        for line in matches:
            if line[0] in self._KEYS:
                data[line[0]] = line[1]
        return data
