import json
import sys
from .schemas import EmailInput
from .triage import classify

def main():
    raw = json.load(sys.stdin)
    print(classify(EmailInput.model_validate(raw)).model_dump_json(indent=2))

if __name__ == "__main__":
    main()
