import json
import os
import sys

# Add parent directory to path so we can import contracts module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from contracts.family_insurance_contract import get_contract_artifacts


def main():
    artifacts = get_contract_artifacts()

    build_dir = os.path.join(os.path.dirname(__file__), "..", "build")
    os.makedirs(build_dir, exist_ok=True)

    with open(os.path.join(build_dir, "approval.teal"), "w", encoding="utf-8") as f:
        f.write(artifacts["approval"])

    with open(os.path.join(build_dir, "clear.teal"), "w", encoding="utf-8") as f:
        f.write(artifacts["clear"])

    with open(os.path.join(build_dir, "contract.json"), "w", encoding="utf-8") as f:
        json.dump(artifacts["abi"], f, indent=2)

    print("Contract artifacts generated in blockchain/build")


if __name__ == "__main__":
    main()
