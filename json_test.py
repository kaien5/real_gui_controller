import json

hvc_settings = {"ip address": "192.10.10.105", "connection name 1": "Nozzle", "connection name 2": "V2", "connection name 3": "V1",
                "connection name 4": "Anode", "connection name 5": "V3", "connection name 6": "MCP", "module name 1": "HV06", "module name 2": "HV05",
                "module name 3": "HV04", "module name 4": "HV03", "module name 5": "HV02", "module name 6": "HV01", "min voltage 1": "250",
                "min voltage 2": "250", "min voltage 3": "250", "min voltage 4": "250", "min voltage 5": "150", "min voltage 6": "150",
                "max voltage 1": "5000", "max voltage 2": "5000", "max voltage 3": "5000", "max voltage 4": "5000", "max voltage 5": "3000",
                "max voltage 6": "3000", "voltage set 1": 0, "voltage set 2": 0, "voltage set 3": 0, "voltage set 4": 0, "voltage set 5": 0,
                "voltage set 6": 0, "delta V/s 1": 100, "delta V/s 2": 100, "delta V/s 3": 100, "delta V/s 4": 50, "delta V/s 5": 50,
                "delta V/s 6": 25}

with open('hvc_settings.json', 'w') as f:
    json.dump(hvc_settings, f)
    print(hvc_settings)

