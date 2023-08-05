import time

import configparser
import json
import logging
import queue
import requests
import threading
import traceback
from logging.handlers import RotatingFileHandler
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# create logger
logger = logging.getLogger('logiqai')
logger.setLevel(logging.INFO)

# create console handler and set level to debug
ch = RotatingFileHandler("/var/log/logiqaidstsyslogng", mode='a', maxBytes=1024 * 1024, backupCount=2)
ch.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter('%(asctime)s %(name)s {%(filename)s:%(lineno)d} %(levelname)s %(message)s',
                              datefmt='%m/%d/%Y %I:%M:%S %p')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


class AtomicInteger():
    def __init__(self, value=0):
        self._value = int(value)
        self._lock = threading.Lock()

    def inc(self, d=1):
        with self._lock:
            self._value += int(d)
            return self._value

    def dec(self, d=1):
        return self.inc(-d)

    @property
    def value(self):
        with self._lock:
            return self._value

    @value.setter
    def value(self, v):
        with self._lock:
            self._value = int(v)
            return self._value

class LogDestination(object):
    def open(self):
        """Open a connection to the target service

        Should return False if opening fails"""
        return True

    def close(self):
        """Close the connection to the target service"""
        pass

    def is_opened(self):
        """Check if the connection to the target is able to receive messages"""
        try:
            alive_url = "{0}/v1/json_batch".format(self.url)
            logger.debug("Checking if destination is alive:%s",alive_url)
            r = requests.head(alive_url,timeout=1, verify=False)
            logger.debug("Destination returned: %d", r.status_code)
            return r.status_code == 405
        except Exception as e:
            logger.debug("Got exception: %s", str(e))
            raise(e)

    def _periodic_stats_reset(self):
        self.periodic_stats_counter_events.value = 0
        self.periodic_static_counter_bytes.value = 0

    def _periodic_stats_increment(self, events, bytes):
        self.periodic_stats_counter_events.inc(events)
        self.periodic_static_counter_bytes.inc(bytes)

    def _periodic_stats_publisher(self):
        logger.info("Starting periodic stats publisher")
        while True:
            time.sleep(60)
            logger.info("Stats since last publish, Bytes:%d, Events:%d",
                        self.periodic_static_counter_bytes.value,
                        self.periodic_stats_counter_events.value)
            self._periodic_stats_reset()

    def init(self, options):
        try:
            logger.info("Starting LOGIQ.AI Syslog-ng destination driver")
            self.periodic_stats_counter_events = AtomicInteger(0)
            self.periodic_static_counter_bytes = AtomicInteger(0)
            threading.Thread(target=self._periodic_stats_publisher).start()
            return self._logiq_init(options)
        except:
            logger.error(traceback.format_exc())

    def _logiq_init(self, options):
        """This method is called at initialization time

        Should return false if initialization fails"""
        logger.debug(options)
        config = configparser.ConfigParser()
        if 'config' in options.keys():
            config.read(options['config'])
        else:
            config.read("/etc/syslog-ng/logiq.conf")

        if len(config.sections()) == 0:
            raise Exception("No sections in config or default config /etc/syslog-ng/logiq.conf")
        else:
            if 'logiq' in config.sections():
                if 'host' in config['logiq'].keys():
                    self.host = config['logiq']['host']
                else:
                    raise Exception("Missing host in config")

                if 'key' in config['logiq'].keys():
                    self.key = config['logiq']['key']
                    bt = "Bearer {0}".format(self.key)
                    self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': bt}
                    logger.debug("Key::%s", self.key)
                else:
                    self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

                if 'protocol' in config['logiq'].keys():
                    self.protocol = config['logiq']['protocol']
                else:
                    self.protocol = 'https'
            else:
                raise Exception("Missing 'logiq' configuration section")

        if 'workers' in options.keys():
            self.workers = int(options['workers'])
        else:
            self.workers = 1

        if 'worker_batch_lines' in options.keys():
            self.worker_batch_lines = int(options['worker_batch_lines'])
        elif 'worker-batch-lines' in options.keys():
            self.worker_batch_lines = int(options['worker-batch-lines'])
        else:
            self.worker_batch_lines = 25

        if 'application_key' in options.keys():
            self._is_app_key_override = True
            self.appkey = options['application_key']
        else:
            self._is_app_key_override = False

        if 'namespace_key' in options.keys():
            self._is_ns_key_override = True
            self.nskey = options['namespace_key']
        else:
            self._is_ns_key_override = False

        if 'cluster_key' in options.keys():
            self._is_cluster_key_override = True
            self.clusterkey = options['cluster_key']
        else:
            self._is_cluster_key_override = False

        if 'debug' in options.keys() and options['debug'] == 'true':
            self.debug = True
            logger.setLevel(logging.DEBUG)
            ch.setLevel(logging.DEBUG)
            logger.warning("!!!!!!! Debug is enabled")
        else:
            self.debug = False

        if 'loglevel' in options.keys():
            loglevelstr = options['loglevel']
            loglevel = logging.INFO
            if loglevelstr == "DEBUG" or loglevelstr == "debug":
                loglevel = logging.DEBUG
            elif loglevelstr == "INFO" or loglevelstr == "info":
                loglevel = logging.INFO
            elif loglevelstr == "WARN" or loglevelstr == "warn":
                loglevel = logging.WARN
            elif loglevelstr == "ERROR" or loglevelstr == "error":
                loglevel = logging.ERROR
            logger.setLevel(loglevel)
            ch.setLevel(loglevel)

        self.url = "{0}://{1}".format(self.protocol, self.host)

        logger.info("Host:%s", self.host)
        logger.info("Protocol:%s", self.protocol)
        logger.info("Workers:%d", self.workers)
        logger.info("Worker-batch-lines:%d", self.worker_batch_lines)
        logger.info("Url:%s", self.url)

        if self._is_ns_key_override == True:
            logger.info("Namespace key:%s", self.nskey)

        if self._is_app_key_override == True:
            logger.info("App key:%s", self.appkey)

        if self._is_cluster_key_override == True:
            logger.info("Cluster key:%s", self.appkey)

        self.worker_queues = dict()
        self.master_queue = queue.Queue()
        for i in range(self.workers):
            self.worker_queues[i] = queue.Queue()
        self.queued = 0
        return True

    def deinit(self):
        """This method is called at deinitialization time"""
        pass

    def send(self, msg):
        """Send a message to the target service

        It can return boolean. Since 3.20, it can return integer
        alternatively.
        Boolean: True to indicate success, False will suspend the
        destination for a period specified by the time-reopen() option.
        After that the same message is retried until retries() times.

        Integer:
        self.SUCCESS: message sending was successful (same as boolean True)
        self.ERROR: message sending was unsuccessful. Same message is retried.
            (same as boolean False)
        self.DROP: message cannot be sent, it should be dropped immediately.
        self.QUEUED: message is not sent immediately, it will be sent with the flush method.
        self.NOT_CONNECTED: message is put back to the queue, open method will be called until success.
        self.RETRY: message is put back to the queue, try to send again until 3 times, then fallback to self.NOT_CONNECTED."""
        logger.debug("Send:%s", msg)
        self.master_queue.put(msg)
        self.queued = self.queued + 1
        return self.QUEUED

    def _logiq_publish(self, eventlist):
        response = requests.post(
            "{0}/v1/json_batch".format(self.url),
            data=json.dumps(eventlist), headers=self.headers, verify=False)
        if response.status_code != 200:
            logger.error("Error posting to logiq: %s %s" % (response.status_code, response.text))
            return False
        else:
            logger.debug("Succesfully sent request to logiq: %s %s" % (response.status_code, response.text))
            return True

    def _bytes_handling(self, v):
        if isinstance(v, bytes):
            return v.decode()

    def _flush_worker_batch_map_to_logiq_fields(self, m):
        retval = dict()
        for k, v in m.items():
            if self._is_app_key_override == True:
                if k == self.appkey:
                    decodedv = self._bytes_handling(v)
                    retval["application"] = decodedv
                    retval[k] = decodedv
                    continue

            if self._is_ns_key_override == True:
                if k == self.nskey:
                    decodedv = self._bytes_handling(v)
                    retval["namespace"] = decodedv
                    retval[k] = decodedv
                    continue

            if self._is_cluster_key_override == True:
                if k == self.clusterkey:
                    decodedv = self._bytes_handling(v)
                    retval["cluster_id"] = decodedv
                    retval[k] = decodedv
                    continue

            if k == 'MESSAGE':
                retval['message'] = self._bytes_handling(v)
            elif k == 'PROGRAM':
                if self._is_app_key_override == False:
                    retval['application'] = self._bytes_handling(v)
                else:
                    retval['program'] = self._bytes_handling(v)
            elif k == 'PID':
                retval['proc_id'] = self._bytes_handling(v)
            elif k == 'FACILITY':
                retval['facility'] = self._bytes_handling(v)
            elif k == 'PRIORITY':
                retval['severity'] = self._bytes_handling(v)
            elif k == 'ISODATE':
                retval['timestamp'] = self._bytes_handling(v)
            elif k == 'HOST':
                retval['hostname'] = self._bytes_handling(v)
            elif k == 'DATE':
                continue
            else:
                retval[k] = self._bytes_handling(v)
        return retval

    def _flush_worker_batch(self, index, messages):
        if self.debug == True:
            for m in messages:
                logger.debug(str(m))
            # return True
        if len(messages) > 0:
            retries = 3
            while retries > 0:
                retpublish = self._logiq_publish(messages)
                if retpublish == True:
                    return True
                else:
                    retries = retries - 1

            logger.error("Retries exhausted, worker:%d", index)
            return False
        else:
            return True

    def _flush_worker(self, index, workerq, retvalq):
        logger.debug("Running worker:%s", index)
        messages = list()
        messages_to_publish = 0
        try:
            while True:
                m = workerq.get(False)
                logiq_fields_mapped_m = self._flush_worker_batch_map_to_logiq_fields(m)
                messages.append(logiq_fields_mapped_m)
                messages_to_publish = messages_to_publish + 1
                if messages_to_publish >= self.worker_batch_lines:
                    batchpublishret = self._flush_worker_batch(index, messages)
                    messages = list()
                    messages_to_publish = 0
                    if batchpublishret == False:
                        retvalq.put(False)
                        return
        except queue.Empty:
            retvalq.put(self._flush_worker_batch(index, messages))
            return
        else:
            logger.error("Else block, should not happen")
            retvalq.put(False)
            return

    def flush(self):
        """Flush the queued messages

        Since 3.20. It can return either a boolean or integer.
        Send needs to return with self.QUEUED in order to work.
        Boolean: True to indicate that the batch is successfully sent.
        False indicates error while sending the batch. The destination is suspended
        for time-reopen period. The messages in the batch are passed again to send, one by one.

        Integer:
        self.SUCCESS: batch sending was successful (same as boolean True)
        self.ERROR: batch sending was unsuccessful. (same as boolean False)
        self.DROP: batch cannot be sent, the messages should be dropped immediately.
        self.NOT_CONNECTED: the messages in the batch is put back to the queue,
            open method will be called until success.
        self.RETRY: message is put back to the queue, try to send again until 3 times, then fallback to self.NOT_CONNECTED."""

        logger.debug("Flush called. Queued:%d time:%s", self.queued, str(time.asctime()))
        thread_contexts = dict()
        thread_return_val_queues = dict()
        # Fill the worker queues
        worker_next = 0
        total_flush_events = 0
        total_flush_bytes = 0
        while True:
            try:
                m = self.master_queue.get(False)
                total_flush_events  = total_flush_events + 1
                total_flush_bytes = total_flush_bytes + len(m)
                self.worker_queues[worker_next].put(m)
                worker_next = (worker_next + 1) % self.workers
            except queue.Empty:
                break
        # Debug
        if self.debug == "true":
            for i in range(self.workers):
                logger.debug("Worker q size:%d", self.worker_queues[i].qsize())

        self._periodic_stats_increment(total_flush_events, total_flush_bytes)

        # Start the worker threads
        for i in range(self.workers):
            thread_return_val_queues[i] = queue.Queue()
            thread_contexts[i] = threading.Thread(target=self._flush_worker, args=(i, self.worker_queues[i],
                                                                                   thread_return_val_queues[i]))
            thread_contexts[i].start()

        for i in range(self.workers):
            thread_contexts[i].join()
            thread_return = thread_return_val_queues[i].get()
            logger.debug("Retval worker:%d %s", i, str(thread_return))
            if thread_return == False:
                return self.ERROR

        logger.debug("Flush completed")
        self.queued = 0
        return self.SUCCESS
