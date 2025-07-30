import os
import yaml
import json


def get_interfaces(base_dir="interfaces"):
    interfaces = []
    for interface in sorted(os.listdir(base_dir)):
        if interface.startswith("__"):
            continue
        interface_path = os.path.join(base_dir, interface)
        if not os.path.isdir(interface_path):
            continue
        for version in sorted(os.listdir(interface_path)):
            version_path = os.path.join(interface_path, version)
            if not os.path.isdir(version_path):
                continue
            interface_yaml_path = os.path.join(version_path, "interface.yaml")
            if os.path.exists(interface_yaml_path):
                with open(interface_yaml_path, "r") as f:
                    interface_yaml = yaml.safe_load(f)
                interface_details = {
                    "name": interface_yaml.get("name", interface),
                    "version": interface_yaml.get("version", version[1:]),
                }
                status = interface_yaml.get("status")
                interface_details["status"] = status
                if interface_details.get("status") in ["published", "draft"]:
                    interfaces.append(interface_details)

    interfaces.sort(key=lambda x: (x["name"], x["version"]))
    return interfaces


if __name__ == "__main__":
    interfaces = get_interfaces("interfaces")
    with open("index.json", "w") as f:
        json.dump(interfaces, f, indent=2)
