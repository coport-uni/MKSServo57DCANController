from mks_motor import MKSMotor
import threading

# Two motors on separate USB2CAN adapters (port 0 and 1).
# Hardware-level CAN sync (0x4B broadcast) requires a shared
# bus, so threading is used instead for parallel operation.
motor_a = MKSMotor.open(port=0)
motor_b = MKSMotor.open(port=1)

# --- Initialization in parallel ---
# Homing is slow (~seconds); running both concurrently
# halves total startup time.
t_init_a = threading.Thread(target=lambda: (motor_a.setup(), motor_a.home()))
t_init_b = threading.Thread(target=lambda: (motor_b.setup(), motor_b.home()))
t_init_a.start()
t_init_b.start()
t_init_a.join()
t_init_b.join()

try:
    MKSMotor.run_sync([motor_a, motor_b], [(50, 25, 10)])
finally:
    motor_a.close()
    motor_b.close()
