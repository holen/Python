# coding: utf8

import json
from kazoo.client import KazooClient

zk = KazooClient(hosts="127.0.0.1:2181")
zk.start()
servers = set()
zk_root = '/demo'
# 获取子节点名称
for child in zk.get_children(zk_root):
    # 获取子节点 value
    node = zk.get(zk_root + "/" + child)
    print node
    addr = json.loads(node[0])
    servers.add("%s:%d" % (addr["host"], addr["port"]))

# 专成列表
servers = list(servers)

print servers
