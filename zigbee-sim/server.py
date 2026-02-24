from flask import Flask, jsonify, request

app = Flask(__name__)

devices = {
    "zb_light_1": {"id": "zb_light_1", "type": "light", "state": "OFF"},
    "zb_light_2": {"id": "zb_light_2", "type": "light", "state": "OFF"},
    "zb_plug_1":  {"id": "zb_plug_1",  "type": "plug",  "state": "OFF", "power": 0.0},
}


@app.get("/devices")
def get_devices():
    return jsonify(list(devices.values()))


@app.get("/devices/<dev_id>")
def get_device(dev_id):
    dev = devices.get(dev_id)
    if not dev:
        return jsonify({"error": "not_found"}), 404
    return jsonify(dev)


@app.post("/devices/<dev_id>")
def set_device(dev_id):
    dev = devices.get(dev_id)
    if not dev:
        return jsonify({"error": "not_found"}), 404

    data = request.get_json(silent=True) or {}
    state = data.get("state")
    if state in ("ON", "OFF"):
        dev["state"] = state
        if dev["type"] == "plug":
            dev["power"] = 50.0 if state == "ON" else 0.0
    return jsonify(dev)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

