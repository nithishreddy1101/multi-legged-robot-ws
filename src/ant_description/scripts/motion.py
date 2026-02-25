import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
import math


class AntWalkPosition(Node):
    def __init__(self):
        super().__init__('ant_walk_position')

        self.pub = self.create_publisher(
            Float64MultiArray,
            '/ant_controller/commands',
            10
        )

        self.timer = self.create_timer(0.05, self.update)  # 20 Hz
        self.t = 0.0

        # --- Tunable parameters ---
        self.hip_amp = 0.4        # forward/back swing
        self.step_height = 0.5    # knee lift
        self.ankle_angle = -0.2
        self.freq = 0.8           # walking speed

        # Tripod gait
        self.phases = [0, math.pi, 0, math.pi, 0, math.pi]

    def update(self):
        msg = Float64MultiArray()
        data = []

        omega = 2 * math.pi * self.freq

        for leg in range(6):
            phase = self.phases[leg]
            s = math.sin(omega * self.t + phase)

            # HIP swings forward/back
            hip = self.hip_amp * s

            # KNEE lifts leg when swinging forward
            knee = self.step_height * max(0.0, s)

            # ANKLE stabilizes foot
            ankle = self.ankle_angle

            data.extend([hip, knee, ankle])

        msg.data = data
        self.pub.publish(msg)
        self.t += 0.05


def main():
    rclpy.init()
    node = AntWalkPosition()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()