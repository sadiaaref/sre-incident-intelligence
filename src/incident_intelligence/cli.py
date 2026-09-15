import argparse
from .adapters.json_io import load_incident
from .engine.analyzer import IncidentAnalyzer
from .reporting.console import print_result

def main():
    parser=argparse.ArgumentParser(description="Explainable SRE incident intelligence")
    parser.add_argument("incident", help="path to incident JSON")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args=parser.parse_args()
    result=IncidentAnalyzer().analyze(load_incident(args.incident))
    print_result(result, args.json)

if __name__ == "__main__": main()
