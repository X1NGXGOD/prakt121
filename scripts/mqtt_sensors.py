import time
import random
import paho.mqtt.client as mqtt

BROKER_HOST = "mqtt"
BROKER_PORT = 1883

TOPIC_TEMP = "sensors/temp1/state"
TOPIC_HUM = "sensors/hum1/state"
TOPIC_MOTION = "sensors/motion1/state"


def main():
    client = mqtt.Client(client_id="mqtt-sensors")
    client.connect(BROKER_HOST, BROKER_PORT, 60)
    client.loop_start()

    motion_state = "OFF"
    last_motion_change = time.time()

    while True:
        temp = round(20 + random.uniform(-2, 2), 1)
        hum = round(50 + random.uniform(-10, 10), 1)

        client.publish(TOPIC_TEMP, payload=str(temp), qos=1, retain=False)
        client.publish(TOPIC_HUM, payload=str(hum), qos=1, retain=False)

        now = time.time()
        # держим текущее состояние motion около 60 секунд,
        # чтобы свет не мигал слишком часто
        if now - last_motion_change > 60:
            motion_state = "ON" if motion_state == "OFF" else "OFF"
            last_motion_change = now
        client.publish(TOPIC_MOTION, payload=motion_state, qos=1, retain=False)

        time.sleep(5)


if __name__ == "__main__":
    main()

