#!/usr/bin/env python3
import pytest

import helpers.keeper_utils as keeper_utils
from helpers.cluster import ClickHouseCluster

cluster = ClickHouseCluster(__file__)
node1 = cluster.add_instance(
    "node1",
    main_configs=["configs/enable_keeper1.xml", "configs/use_keeper.xml"],
    stay_alive=True,
)
node2 = cluster.add_instance(
    "node2",
    main_configs=["configs/enable_keeper2.xml", "configs/use_keeper.xml"],
    stay_alive=True,
)
node3 = cluster.add_instance(
    "node3",
    main_configs=["configs/enable_keeper3.xml", "configs/use_keeper.xml"],
    stay_alive=True,
)


def wait_nodes():
    keeper_utils.wait_nodes(cluster, [node1, node2, node3])


@pytest.fixture(scope="module")
def started_cluster():
    try:
        cluster.start()
        wait_nodes()

        yield cluster

    finally:
        cluster.shutdown()


def get_fake_zk(nodename, timeout=30.0):
    return keeper_utils.get_fake_zk(cluster, nodename, timeout=timeout)


def stop_zk(zk):
    try:
        if zk:
            zk.stop()
            zk.close()
    except:
        pass


def test_restart_multinode(started_cluster):
    try:
        node1_zk = node2_zk = node3_zk = None

        node1_zk = get_fake_zk("node1")
        node2_zk = get_fake_zk("node2")
        node3_zk = get_fake_zk("node3")

        for i in range(100):
            node1_zk.create(
                "/test_read_write_multinode_node" + str(i),
                ("somedata" + str(i)).encode(),
            )

        for i in range(100):
            if i % 10 == 0:
                node1_zk.delete("/test_read_write_multinode_node" + str(i))

        node2_zk.sync("/test_read_write_multinode_node0")
        node3_zk.sync("/test_read_write_multinode_node0")

        for i in range(100):
            if i % 10 != 0:
                assert (
                    node2_zk.get("/test_read_write_multinode_node" + str(i))[0]
                    == ("somedata" + str(i)).encode()
                )
                assert (
                    node3_zk.get("/test_read_write_multinode_node" + str(i))[0]
                    == ("somedata" + str(i)).encode()
                )
            else:
                assert (
                    node2_zk.exists("/test_read_write_multinode_node" + str(i)) is None
                )
                assert (
                    node3_zk.exists("/test_read_write_multinode_node" + str(i)) is None
                )

    finally:
        for zk in [node1_zk, node2_zk, node3_zk]:
            stop_zk(zk)

    node1.restart_clickhouse(kill=True)
    node2.restart_clickhouse(kill=True)
    node3.restart_clickhouse(kill=True)
    wait_nodes()

    for i in range(100):
        try:
            node1_zk = get_fake_zk("node1")
            node2_zk = get_fake_zk("node2")
            node3_zk = get_fake_zk("node3")
            for i in range(100):
                if i % 10 != 0:
                    assert (
                        node1_zk.get("/test_read_write_multinode_node" + str(i))[0]
                        == ("somedata" + str(i)).encode()
                    )
                    assert (
                        node2_zk.get("/test_read_write_multinode_node" + str(i))[0]
                        == ("somedata" + str(i)).encode()
                    )
                    assert (
                        node3_zk.get("/test_read_write_multinode_node" + str(i))[0]
                        == ("somedata" + str(i)).encode()
                    )
                else:
                    assert (
                        node1_zk.exists("/test_read_write_multinode_node" + str(i))
                        is None
                    )
                    assert (
                        node2_zk.exists("/test_read_write_multinode_node" + str(i))
                        is None
                    )
                    assert (
                        node3_zk.exists("/test_read_write_multinode_node" + str(i))
                        is None
                    )
            break
        except Exception as ex:
            print("Got exception as ex", ex)
        finally:
            for i in range(100):
                if node1_zk.exists("/test_read_write_multinode_node" + str(i)):
                    node1_zk.delete("/test_read_write_multinode_node" + str(i))
            for zk in [node1_zk, node2_zk, node3_zk]:
                stop_zk(zk)
