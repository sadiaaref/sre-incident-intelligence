from ..adapters.json_io import result_to_dict
import json

def print_result(result, json_output=False):
    if json_output:
        print(json.dumps(result_to_dict(result), indent=2))
    else:
        print(result.report)
