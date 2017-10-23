"""TVM stats"""

# stdlib imports
import datetime
import logging
from datetime import timedelta
import os
import subprocess
import sys
import platform

# non-stdlib imports
import dateutil.tz
import psutil
import time
from applicationinsights import TelemetryClient


# global defines
_IS_PLATFORM_WINDOWS = platform.system() == 'Windows'

telemetryClient = TelemetryClient(os.environ["APP_INSIGHT_KEY"])

class NodeStatsUtils:
    @staticmethod
    def check_required_python_version():
        """Checks to see if we have the minimum required version of Python
        Parameters:
            None
        Returns:
            If the python interpreter version suffices
        Raises:
            Nothing
        """
        return sys.version_info >= (3, 4)

    @staticmethod
    def python_environment():  # pragma: no cover
        """Get the python interpreter information
        Parameters:
            None
        Returns:
            python interpreter information
        Raises:
            Nothing
        """
        return ' '.join(
            [platform.python_implementation(), platform.python_version()])

    @staticmethod
    def os_environment():
        """Get the OS environment
        Parameters:
            None
        Returns:
            operating system information
        Raises:
            Nothing
        """
        return platform.platform()

    @staticmethod
    def system():
        """Get the system environment
        Parameters:
            None
        Returns:
            platform system
        Raises
            Nothing
        """
        return platform.system()

    @staticmethod
    def on_windows():
        """If system environment is Windows
        Parameters:
            None
        Returns:
            True if running on Windows
        Raises
            Nothing
        """
        return _IS_PLATFORM_WINDOWS

    @staticmethod
    def node():
        """Get the platform node
        Parameters:
            None
        Returns:
            platform node
        Raises
            Nothing
        """
        return platform.node()

    @staticmethod
    def distribution():  # pragma: no cover
        """Get the OS distribution
        Parameters:
            None
        Returns:
            operating system distribution
        Raises:
            Nothing
        """
        dist = NodeStatsUtils.system()
        if dist == 'Linux':
            dist = ' '.join(platform.linux_distribution())
        elif dist == 'Darwin':
            dist = ' '.join(platform.mac_ver())
        elif dist == 'Windows':
            dist = ' '.join(platform.win32_ver())
        return dist

    @staticmethod
    def encode_utf8(value):
        """Encodes a value as utf-8
        Parameters:
            value - value to encode
        Returns:
            Encoded string as utf-8
        Raises:
            Nothing
        """
        if isinstance(value, str):
            return value.encode('utf8')
        return str(value).encode('utf8')

    @staticmethod
    def decode_utf8(value):
        """Decodes a string encoded as utf-8
        Parameters:
            value - value to decode
        Returns:
            Decoded string
        Raises:
            Nothing
        """
        return value.decode('utf8')

    @staticmethod
    def encode_utf16le(value):
        """Encodes a value as utf-16le (UCS-2)
        Parameters:
            value - value to encode
        Returns:
            Encoded string as utf-16le
        Raises:
            Nothing
        """
        if isinstance(value, str):
            return value.encode('utf-16le')
        return str(value).encode('utf-16le')

    @staticmethod
    def decode_utf16le(value):
        """Decodes a string encoded as utf-16le (UCS-2)
        Parameters:
            value - value to decode
        Returns:
            Decoded string
        Raises:
            Nothing
        """
        return value.decode('utf-16le')

    @staticmethod
    def decode_hex(value):
        """Decodes a string with hex encoding to bytes
        Parameters:
            value - value to decode
        Returns:
            Decoded string
        Raises:
            Nothing
        """
        return bytes.fromhex(value)

    @staticmethod
    def datetime_utcnow():
        """Returns a datetime now with UTC timezone
        Parameters:
            None
        Returns:
            datetime object representing now with UTC timezone
        Raises:
            Nothing
        """
        return datetime.datetime.now(dateutil.tz.tzutc())

    @staticmethod
    def datetime_now(tz=None):
        """Returns a datetime now with specified timezone
        Parameters:
            tz - timezone for returned datetime object, default is tzlocal
        Returns:
            datetime object representing now with specified timezone
        Raises:
            Nothing
        """
        if tz is None:
            tz = dateutil.tz.tzlocal()
        return datetime.datetime.now(tz)

    @staticmethod
    def diff_datetimes_as_ticks(t1, t2):
        """Compute the difference between two datetimes (t2 - t1) in
        Windows ticks
        Parameters:
            t1 - time1
            t2 - time2
        Returns:
            (t2 - t1) in ticks
        Raises:
            No special exception handling
        """
        return int(10e6 * (t2 - t1).total_seconds())

    @staticmethod
    def convert_datetime_to_ticks(dtvalue, nanoseconds=None):
        """Convert a datetime object to a .NET ticks value. Note that the python
        datetime objects only support precision to microseconds. Truncation will
        occur at that precision if nanoseconds parameter is not supplied.

        :param datetime.datetime dtvalue: datetime object
        :param int nanoseconds: nanoseconds
        :rtype: int
        :return: ticks value with a precision up to hundreds of nanoseconds
        :raises ValueError: if dtvalue is not a datetime object or nanoseconds
            is not an int
        """
        if not isinstance(dtvalue, datetime.datetime):
            raise ValueError('dtvalue type {} is not a datetime'.format(
                type(dtvalue)))
        if nanoseconds is not None and not isinstance(nanoseconds, int):
            raise ValueError('nanoseconds type {} is not integral'.format(
                type(nanoseconds)))
        delta = dtvalue - \
            datetime.datetime(1, 1, 1, tzinfo=dateutil.tz.tzutc())
        return NodeStatsUtils.convert_timedelta_to_timeinterval(
            delta, nanoseconds, checkparams=False)

    @staticmethod
    def convert_timedelta_to_timeinterval(
            timedelta, nanoseconds=None, checkparams=True):
        """Convert a timedelta object to a time interval value. Note that
        the python datetime objects only support precision to microseconds.
        Truncation will occur at that precision if nanoseconds parameter is
        not supplied.

        :param datetime.timedelta timedelta: datetime.timedelta object
        :param int nanoseconds: nanoseconds
        :param bool checkparams: check parameters
        :rtype: int
        :return: Time interval value with precision up to hundreds of nanoseconds
        :raises ValueError: if timedelta is not a datetime.timedelta object or
            nanoseconds is not an int
        """
        if checkparams:
            if not isinstance(timedelta, datetime.timedelta):
                raise ValueError('timedelta type {} is not a datetime.timedelta'.
                                 format(type(timedelta)))
            if nanoseconds is not None and not isinstance(nanoseconds, int):
                raise ValueError('nanoseconds type {} is not integral'.format(
                    type(nanoseconds)))
        total_sec = int(timedelta.total_seconds() * 10e6)
        neg = False
        if total_sec < 0:
            neg = True
            total_sec = -total_sec
        delta = total_sec // 10 * 10
        if neg:
            delta = -delta
        if nanoseconds is not None:
            # convert nanoseconds to "ticks" and add to delta
            if nanoseconds < 0:
                nanoseconds = abs(nanoseconds) // 100
                delta += -nanoseconds
            else:
                delta += nanoseconds // 100
        return delta


def setup_logger():
    # logger defines
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s.%(msecs)03dZ %(levelname)s %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

logger = setup_logger()

# global defines
_DEFAULT_STATS_UPDATE_INTERVAL = 5
if NodeStatsUtils.on_windows():
    _USER_DISK = 'C:\\'
else:
    _USER_DISK = '/mnt/resources'
    if not os.path.exists(_USER_DISK):
        _USER_DISK = '/mnt'
_MEGABYTE = 1048576


class NodeStats:
    class Properties:
        """Property names"""
        SampleTime = 'SampleTime'
        BootTime = 'Sys_BootTime'
        NumConnectedUsers = 'Sys_NumConnectedUsers'
        NumProcesses = 'Sys_NumProcesses'
        CpuCount = 'Sys_CpuCount'
        CpuPercentages = 'Sys_CpuPercentages'
        MemTotalMiB = 'Sys_MemTotalMiB'
        MemAvailableMiB = 'Sys_MemAvailableMiB'
        SwapTotalMiB = 'Sys_SwapTotalMiB'
        SwapAvailableMiB = 'Sys_SwapAvailableMiB'
        DiskTotalMiB = 'Sys_DiskTotalMiB'
        DiskAvailableMiB = 'Sys_DiskAvailableMiB'
        DiskReadOperations = 'Sys_DiskReadOperations'
        DiskWriteOperations = 'Sys_DiskWriteOperations'
        DiskReadMiB = 'Sys_DiskReadMiB'
        DiskWriteMiB = 'Sys_DiskWriteMiB'
        DiskReadTimeSeconds = 'Sys_DiskReadTimeSeconds'
        DiskWriteTimeSeconds = 'Sys_DiskWriteTimeSeconds'
        NetReadPackets = 'Sys_NetReadPackets'
        NetWritePackets = 'Sys_NetWritePackets'
        NetReadMiB = 'Sys_NetReadMiB'
        NetWriteMiB = 'Sys_NetWriteMiB'
        NetReadPacketsDropped = 'Sys_NetReadPacketsDropped'
        NetWritePacketsDropped = 'Sys_NetWritePacketsDropped'
        NetReadErrors = 'Sys_NetReadErrors'
        NetWriteErrors = 'Sys_NetWriteErrors'

    """Persistent Task Stats class"""

    def __init__(self):
        """Ctor for Task Stats
        Parameters:
        Returns:
            Nothing
        Raises:
            Nothing
        """
        self.sys_boot_time = None
        self.sys_num_connected_users = 0
        self.sys_num_pids = 0
        self.sys_cpu_count = 0
        self.sys_cpu_percent = None
        self.sys_mem_total = 0
        self.sys_mem_avail = 0
        self.sys_swap_total = 0
        self.sys_swap_avail = 0
        self.sys_disk_total = 0
        self.sys_disk_avail = 0
        self.sys_disk_read_ops = 0
        self.sys_disk_write_ops = 0
        self.sys_disk_read_xfer = 0
        self.sys_disk_write_xfer = 0
        self.sys_disk_read_time = 0
        self.sys_disk_write_time = 0
        self.sys_net_read_packets = 0
        self.sys_net_write_packets = 0
        self.sys_net_read_xfer = 0
        self.sys_net_write_xfer = 0
        self.sys_net_read_packets_dropped = 0
        self.sys_net_write_packets_dropped = 0
        self.sys_net_read_errors = 0
        self.sys_net_write_errors = 0
        self.timestamp = NodeStatsUtils.datetime_utcnow()


class NodeStatsManager(object):
    """Node Stats Manager class"""

    def __init__(self, pool_id, node_id):
        self.pool_id = pool_id
        self.node_id = node_id
        self.enable_disk_perf = True
        self.cbhandle = None

    def initialize_perf_counters(self):
        # start cpu utilization monitoring, first value is ignored
        psutil.cpu_percent(interval=None, percpu=True)
        # if on windows, we may need to enable diskperf
        if NodeStatsUtils.on_windows():
            try:
                subprocess.check_call('diskperf -y', shell=True)
            except Exception as exc:
                logger.exception(exc)
                self.enable_disk_perf = False
        logger.debug('counters: enable_disk_perf={}'.format(
            self.enable_disk_perf))

    def _sample_stats(self):
        ns = NodeStats()
        logger.debug('node stats sample: pool={} node={} ts={}'.format(
            self.pool_id, self.node_id, ns.timestamp))
        # get system-wide counters
        ns.sys_cpu_count = psutil.cpu_count()
        ns.sys_boot_time = datetime.datetime.fromtimestamp(
            psutil.boot_time(), tz=dateutil.tz.tzutc())
        ns.sys_cpu_percent = psutil.cpu_percent(interval=None, percpu=True)
        ns.sys_swap_total, _, ns.sys_swap_avail, _, _, _ = psutil.swap_memory()
        try:
            ns.sys_disk_total, _, ns.sys_disk_avail, _ = psutil.disk_usage(
                _USER_DISK)
        except Exception:
            logger.error(
                'could not retrieve user disk stats: {}'.format(_USER_DISK))
        ns.sys_num_connected_users = len(psutil.users())
        ns.sys_num_pids = len(psutil.pids())
        mem = psutil.virtual_memory()
        ns.sys_mem_total = mem.total
        ns.sys_mem_avail = mem.available
        del mem
        diskio = psutil.disk_io_counters()
        ns.sys_disk_read_ops = diskio.read_count
        ns.sys_disk_write_ops = diskio.write_count
        ns.sys_disk_read_xfer = diskio.read_bytes
        ns.sys_disk_write_xfer = diskio.write_bytes
        ns.sys_disk_read_time = diskio.read_time
        ns.sys_disk_write_time = diskio.write_time
        del diskio
        netio = psutil.net_io_counters()
        ns.sys_net_read_packets = netio.packets_recv
        ns.sys_net_write_packets = netio.packets_sent
        ns.sys_net_read_xfer = netio.bytes_recv
        ns.sys_net_write_xfer = netio.bytes_sent
        ns.sys_net_read_packets_dropped = netio.dropin
        ns.sys_net_write_packets_dropped = netio.dropout
        ns.sys_net_read_errors = netio.errin
        ns.sys_net_write_errors = netio.errout
        del netio
        return ns

    def _create_stats_entity(self, ns):
        """Create stats entity

        :param NodeStats ns: node stats
        :rtype: dict
        :return: dictionary
        """
        if ns is None:
            return None
        # convert ns class into dict
        stats_dict = {}
        stats_dict[NodeStats.Properties.SampleTime] = \
            NodeStatsUtils.convert_datetime_to_ticks(ns.timestamp)
        stats_dict[NodeStats.Properties.BootTime] = \
            NodeStatsUtils.convert_datetime_to_ticks(ns.sys_boot_time)
        stats_dict[NodeStats.Properties.NumConnectedUsers] = \
            ns.sys_num_connected_users
        stats_dict[NodeStats.Properties.NumProcesses] = \
            ns.sys_num_pids
        stats_dict[NodeStats.Properties.CpuCount] = ns.sys_cpu_count
        if ns.sys_cpu_percent is not None:
            stats_dict[NodeStats.Properties.CpuPercentages] = \
                ' '.join(str(x) for x in ns.sys_cpu_percent)
        else:
            stats_dict[NodeStats.Properties.CpuPercentages] = ''
        stats_dict[NodeStats.Properties.MemTotalMiB] = \
            ns.sys_mem_total / _MEGABYTE
        stats_dict[NodeStats.Properties.MemAvailableMiB] = \
            ns.sys_mem_avail / _MEGABYTE
        stats_dict[NodeStats.Properties.SwapTotalMiB] = \
            ns.sys_swap_total / _MEGABYTE
        stats_dict[NodeStats.Properties.SwapAvailableMiB] = \
            ns.sys_swap_avail / _MEGABYTE
        stats_dict[NodeStats.Properties.DiskTotalMiB] = \
            ns.sys_swap_total / _MEGABYTE
        stats_dict[NodeStats.Properties.DiskAvailableMiB] = \
            ns.sys_swap_avail / _MEGABYTE
        stats_dict[NodeStats.Properties.DiskReadOperations] = \
            ns.sys_disk_read_ops
        stats_dict[NodeStats.Properties.DiskWriteOperations] = \
            ns.sys_disk_write_ops
        stats_dict[NodeStats.Properties.DiskReadMiB] = \
            ns.sys_disk_read_xfer / _MEGABYTE
        stats_dict[NodeStats.Properties.DiskWriteMiB] = \
            ns.sys_disk_write_xfer / _MEGABYTE
        stats_dict[NodeStats.Properties.DiskReadTimeSeconds] = \
            ns.sys_disk_read_time / 1000
        stats_dict[NodeStats.Properties.DiskWriteTimeSeconds] = \
            ns.sys_disk_write_time / 1000
        stats_dict[NodeStats.Properties.NetReadPackets] = \
            ns.sys_net_read_packets
        stats_dict[NodeStats.Properties.NetWritePackets] = \
            ns.sys_net_write_packets
        stats_dict[NodeStats.Properties.NetReadMiB] = \
            ns.sys_net_read_xfer / _MEGABYTE
        stats_dict[NodeStats.Properties.NetWriteMiB] = \
            ns.sys_net_write_xfer / _MEGABYTE
        stats_dict[NodeStats.Properties.NetReadPacketsDropped] = \
            ns.sys_net_read_packets_dropped
        stats_dict[NodeStats.Properties.NetWritePacketsDropped] = \
            ns.sys_net_write_packets_dropped
        stats_dict[NodeStats.Properties.NetReadErrors] = \
            ns.sys_net_read_errors
        stats_dict[NodeStats.Properties.NetWriteErrors] = \
            ns.sys_net_write_errors
        return stats_dict

    def periodic_sampler(self):
        while True:
            self._send_sample()
            time.sleep(5)

    def _send_sample(self):
        # collect stats
        stats = self._sample_stats()
        if stats is None:
            logger.error('could not sample node stats')

        # set a default interval
        interval = _DEFAULT_STATS_UPDATE_INTERVAL
        # convert nodestats to props
        props = self._create_stats_entity(stats)
        # upload to redis
        logger.debug('inserting node stats: {}'.format(props))
        telemetryClient.track_metric("Memeory used", stats.sys_mem_total - stats.sys_mem_avail)
        telemetryClient.track_metric("Memeory remaining", stats.sys_mem_avail)
        # self.redis.hmset('$node.stats:{}'.format(self.node_id), props)
        

    def register(self):
        logger.debug(
            'registering stats for pool={} node={}'.format(
                self.pool_id, self.node_id))
        # push self to pool set
        # self.redis.sadd('$pools', self.pool_id)
        print("Registering... $pools", self.pool_id)
        # push self to pool.node set
        print("Registering... $pools.nodes", self.pool_id, self.node_id)

        # self.redis.sadd('$pool.nodes:{}'.format(self.pool_id), self.node_id)
        # sample immediately and schedule for sampling
        self.periodic_sampler()

    def unregister(self, cleanup):
        logger.debug('unregistering stats for pool={} node={}'.format(
            self.pool_id, self.node_id))
        if cleanup:
            # remove self from node hash
            print("Unregister... $pools.stats", self.node_id)

            # self.redis.hdel('$node.stats:{}'.format(self.node_id))
            # remove self from pool.node set
            # self.redis.srem('$pool.nodes:{}'.format(
            #     self.pool_id), self.node_id)
            # if self.redis.scard('$pool.nodes:{}'.format(self.pool_id)) == 0:
            #     self.redis.srem('$pools', self.pool_id)
        # cancel periodic sampler
        if self.cbhandle is not None:
            try:
                logger.debug('attempting to cancel stats sampler')
                self.cbhandle.cancel()
                logger.info('stats sampler cancelled for')
            except Exception as exc:
                logger.exception(exc)
            self.cbhandle = None


def main():
    """Main entry point for prism
    Parameters:
        Nothing
    Returns:
        Nothing
    Raises:
        Passes through exceptions except KeyboardInterrupt
    """
    ns = None
    try:
        # log basic info
        logger.info('python interpreter: {}'.format(
            NodeStatsUtils.python_environment()))
        logger.info('operating system: {}'.format(
            NodeStatsUtils.os_environment()))
        logger.info('distribution: {}'.format(NodeStatsUtils.distribution()))

        # extract account, pool, tvm from environment
        logger.debug('environment: {}'.format(os.environ))
        try:
            pool_id = os.environ['AZ_BATCH_POOL_ID']
            node_id = os.environ['AZ_BATCH_NODE_ID']
        except KeyError as ke:
            logger.exception(ke)
            # below is for local testing
            pool_id = '_test-pool-1'
            node_id = '_test-node-1'

        # get and set event loop mode
        logger.info('enabling event loop debug mode')

        # create node stats manager
        ns = NodeStatsManager(pool_id, node_id)
        ns.initialize_perf_counters()
        ns.register()

    except (KeyboardInterrupt, SystemExit):
        # TODO CTRL-C bug in Windows
        pass
    finally:
        if ns is not None:
            ns.unregister(True)


if __name__ == '__main__':
    main()
