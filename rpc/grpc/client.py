# coding: utf-8
# client.py

import grpc

import pi_pb2
import pi_pb2_grpc


def main():
    channel = grpc.insecure_channel('localhost:8080')
    # 使用 stub
    client = pi_pb2_grpc.PiCalculatorStub(channel)
    # 调用吧
    for i in range(1, 1000):
        print "pi(%d) =" % i, client.Calc(pi_pb2.PiRequest(n=i)).value


if __name__ == '__main__':
    main()
