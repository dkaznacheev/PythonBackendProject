import futures3
import grpc
from collections import defaultdict

import postcount_pb2 as grpc_post_msg
import postcount_pb2_grpc as grpc_post


class PostCountServicer(grpc_post.PostCounterServicer):
    def __init__(self):
        self.post_counts = defaultdict(int)

    def GetPostCount(self, request, context):
        if request.username:
            count = self.post_counts[request.username]
        else:
            count = 0
            for _, post_count in self.post_counts.items():
                count += post_count
        return grpc_post_msg.PostCountResponse(count=count)

    def PostMessage(self, request, context):
        self.post_counts[request.username] += 1
        print(self.post_counts)
        return grpc_post_msg.Ok()


if __name__ == '__main__':
    server = grpc.server(futures3.ThreadPoolExecutor(max_workers=10))
    grpc_post.add_PostCounterServicer_to_server(PostCountServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()
