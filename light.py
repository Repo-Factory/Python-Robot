#!/usr/bin/env python3

import rclpy
from public_service_apis import ServiceAPIs
from rclpy.node import Node
from scion_types.srv import SendFrame

APIS = ServiceAPIs()

class LightNode(Node):
    def __init__(self):
        super().__init__('light_node')
        self.can_node = Node("light_can_temp")
        self.can_client = self.can_node.create_client(SendFrame, 'send_can_raw')
        self.timer = self.create_timer(.01, self.turn_on_light)


    def turn_on_light(self):
        request = SendFrame.Request()
        request.can_id = 0x04
        request.can_dlc = 5
        request.can_data = [0x04, 0x00, 0x04, 0x00, 0x01, 0x00, 0x00, 0x00]
        APIS.SendFrame(self.can_node, self.can_client, request)


def main(args=None):
    rclpy.init(args=args)
    light_node = LightNode()
    rclpy.spin(light_node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()