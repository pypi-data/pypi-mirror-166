#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : service
# @Time         : 2022/8/19 下午5:14
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


import grpc
from appzoo.grpc_app.utils import _options
from appzoo.grpc_app.protos.base_pb2 import Request, Response
from appzoo.grpc_app.protos.base_pb2_grpc import GrpcServiceServicer, GrpcServiceStub, add_GrpcServiceServicer_to_server

from meutils.pipe import *
from pickle import dumps, loads


class Service(GrpcServiceServicer):

    def __init__(self, debug=False, options=None):
        self.debug = debug
        self.options = options if options else _options

    def main(self, *args, **kwargs):
        raise NotImplementedError('Method not implemented!')

    @logger.catch()
    def _request(self, request, context):
        input = loads(request.data)
        if self.debug:
            logger.debug(input)

        output = dumps(self.main(input))
        return Response(data=output)

    def run(self, port=8000, max_workers=3, is_async=False):
        if is_async:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait([self.async_server()]))
            loop.close()

        server = grpc.server(ThreadPoolExecutor(max_workers), options=self.options)  # compression = None
        add_GrpcServiceServicer_to_server(self, server)
        server.add_insecure_port(f'[::]:{port}')

        logger.info("GrpcService Running ...")
        server.start()
        server.wait_for_termination()

    async def async_server(self, port=8000, max_workers=3):
        server = grpc.aio.server(ThreadPoolExecutor(max_workers), options=self.options)
        add_GrpcServiceServicer_to_server(self, server)
        server.add_insecure_port(f'[::]:{port}')

        logger.info("Async GrpcService Running ...")
        await server.start()
        await server.wait_for_termination()




if __name__ == '__main__':
    class MyService(Service):

        def main(self, data):
            time.sleep(1)
            return data


    MyService(debug=True).run(is_async=True)
