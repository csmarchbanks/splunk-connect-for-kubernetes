import pytest
import time
import os
import logging
import json
from urllib.parse import urlparse
from ..common import check_events_from_splunk
from ..common import check_metrics_from_splunk


@pytest.mark.parametrize("metric,dimension", [
    #Aggregator Metrics
    ("kube.container.cpu.limit", "host"),
    ("kube.container.memory.request", "host"),
    ("kube.pod.cpu.limit", "host"),
    ("kube.pod.memory.request", "host"),
    ("kube.namespace.cpu.limit", "host"),
    ("kube.namespace.memory.request", "host"),
    ("kube.cluster.cpu.limit", "host"),
    ("kube.cluster.memory.request", "host"),
    ("kube.node.cpu.capacity", "host"),
    ("kube.node.memory.utilization", "host"),
    #Summary Metrics
    ("kube.node.cpu.usage", "host"),
    ("kube.node.memory.usage", "host"),
    ("kube.node.uptime", "host"),
    ("kube.node.network.rx_bytes", "host"),
    ("kube.node.fs.available_bytes", "host"),
    ("kube.node.imagefs.available_bytes", "host"),
    ("kube.node.runtime.imagefs.maxpid", "host"),
    ("kube.sys-container.cpu.usage", "host"),
    ("kube.sys-container.memory.usage_bytes", "host"),
    ("kube.sys-container.uptime", "host"),
    ("kube.pod.uptime", "host"),
    ("kube.pod.cpu.usage", "host"),
    ("kube.pod.memory.usage_bytes", "host"),
    ("kube.pod.network.rx_bytes", "host"),
    ("kube.pod.ephemeral-storage.available_bytes", "host"),
    ("kube.pod.volume.available_bytes", "host"),
    ("kube.container.uptime", "host"),
    ("kube.container.cpu.usage", "host"),
    ("kube.container.memory.usage_bytes", "host"),
    ("kube.container.rootfs.available_bytes", "host"),
    ("kube.container.logs.used_bytes", "host"),
    #Stats Metrics
    ("kube.node.cpu.cfs.periods", "host"),
    ("kube.node.diskio.io_service_bytes.stats.Read", "host"),
    ("kube.node.filesystem.available", "host"),
    ("kube.node.memory.cache", "host"),
    ("kube.node.tasks_stats.nr_running", "host"),
    ("kube.node.network.*.rx_bytes", "host"),
    #Cadvisor Metrics
    ("kube.container.cpu.load.average.10s", "host"),
    ("kube.container.fs.inodes.free", "host"),
    ("kube.container.last.seen", "host"),
    ("kube.container.memory.usage.bytes", "host"),
    ("kube.container.network.receive.bytes.total", "host"),
    ("kube.container.spec.cpu.period", "host"),
    ("kube.container.tasks.state", "host")
])
def test_metric_name(setup, metric, dimension):
    '''
    This test covers one metric from each endpoint that the metrics plugin covers
    '''
    logging.info("testing for presence of metric={0}".format(metric))

    events = check_metrics_from_splunk(start_time="-24h@h",
                                  end_time="now",
                                  url=setup["splunkd_url"],
                                  user=setup["splunk_user"],
                                  password=setup["splunk_password"],
                                  index="circleci_metrics",
                                  metric_name=metric,
                                  dimension=dimension)
    logging.info("Splunk received %s events in the last minute",
                         len(events))
    assert len(events) > 0


@pytest.mark.parametrize("metric,dimension", [    
    ("kube.container.cpu.limit", "cluster_name")
])
def test_metric_cluster_name(setup, metric, dimension):
    '''
    This test verifies the presence of the target cluster name - circleci-k8s-cluster-metrics
    '''
    counter == 0

    logging.info("testing for presence of metric={0}".format(metric))

    events = check_metrics_from_splunk(start_time="-24h@h",
                                  end_time="now",
                                  url=setup["splunkd_url"],
                                  user=setup["splunk_user"],
                                  password=setup["splunk_password"],
                                  index="circleci_metrics",
                                  metric_name=metric,
                                  dimension=dimension)
    logging.info("Splunk received %s events in the last minute",
                         len(events))
    
    #for (i=0; i<len(events); i++):
    for x in events:
        if x.name == "circleci-k8s-cluster-metrics":
            counter += 1

    assert counter > 0
