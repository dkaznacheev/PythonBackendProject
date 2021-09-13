import grpc
import postcount_pb2_grpc as post_grpc
import postcount_pb2 as post_grpc_msg

if __name__ == '__main__':
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = post_grpc.PostCounterStub(channel)
        count = stub.GetPostCount(post_grpc_msg.PostCountRequest())
        print(count.count)
