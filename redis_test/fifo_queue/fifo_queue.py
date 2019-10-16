# _*_ encoding:utf-8 _*_
__author__ = 'zhl'
__date__ = '2019/10/16 10:43'

from redis import Redis


class FIFOqueue:
    """ 创建 FIFO 队列，先进先出 """

    def __init__(self, client, key):
        self.client = client
        self.key = key

    def enqueue(self, item):
        """
        将给定元素放入队列，然后返回队列当前包含的元素数量作为结果。
        """
        return self.client.rpush(self.key, item)

    def dequeue(self):
        """
        移除并返回队列目前入队时间最长的元素。
        """
        return self.client.lpop(self.key)


if __name__ == "__main__":
    client = Redis(host="192.168.120.201", password="123456", decode_responses=True)
    q = FIFOqueue(client, "buy-request")
    q.enqueue("peter-buy-milk")
    q.enqueue("john-buy-rice")
    q.enqueue("david-buy-keyboard")
    print(q.dequeue())
    print(q.dequeue())
    print(q.dequeue())
