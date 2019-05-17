# coding: utf-8
# server.py
import math
import grpc
import time
from concurrent import futures

import pi_pb2
import pi_pb2_grpc


# 圆周率计算服务实现类
class PiCalculatorServicer(pi_pb2_grpc.PiCalculatorServicer):

    def Calc(self, request, ctx):
        # 计算圆周率的逻辑在这里
        s = 0.0
        for i in range(request.n):
            s += 1.0/(2*i+1)/(2*i+1)
        # 注意返回的是一个响应对象
        return pi_pb2.PiResponse(value=math.sqrt(8*s))


def main():
    # 多线程服务器
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # 实例化圆周率服务类
    servicer = PiCalculatorServicer()
    # 注册本地服务
    pi_pb2_grpc.add_PiCalculatorServicer_to_server(servicer, server)
    # 监听端口
    server.add_insecure_port('127.0.0.1:8080')
    # 开始接收请求进行服务
    server.start()
    # 使用 ctrl+c 可以退出服务
    try:
        time.sleep(1000)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    main()
