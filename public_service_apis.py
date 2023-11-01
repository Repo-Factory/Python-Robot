""" 
    @Strix Elixel 
    Generic ROS2 Client API to help make function calls
    Basically to integrate with any service we write, you would have to figure out how to properly make
    the service call and also pass the appropriate parameters. Instead, each service can be shipped with 
    the appropriate client code so someone can use one public function to integrate with another package.
    Every package that needs to interface with another module could import this central module
"""


import rclpy


###################################################################################################################


""" 
    GENERIC ROS2 SERVICE CALL CODE  
    This will wrap validation and temp node spinning to process callback.
    This always has to do be done no matter the service call, so we can write it once and leave boilerplate out of main code
"""


def validate_service(client) -> bool:
        while not client.wait_for_service(10):
            if not rclpy.ok():
                return False
        return True


def make_service_call(node, client, future): # Each call will need a temp node with a client attached.
    if not validate_service(client):
        return None
    rclpy.spin_until_future_complete(node, future, timeout_sec=0.1)
    return future.result()


################################################################################################################### 

class ServiceAPIs():
    """ 
        Important static class will have all public functions that we can use on the robot to integrate with other people's code
    """
    def SendFrame(self, node, client, request) -> int:
        future = client.call_async(request)
        return make_service_call(node, client, future)
