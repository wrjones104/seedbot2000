import asyncio
import argparse
import sys
from pathlib import Path

# Add the project root to the path to allow imports
# from the 'johnnydmad' package within this project
sys.path.insert(0, str(Path(__file__).resolve().parent))

from johnnydmad.johnnydmad import johnnydmad_webapp

def main():
    """
    Command-line wrapper to safely run the async johnnydmad_webapp function.
    """
    parser = argparse.ArgumentParser(description="Runs the johnnydmad music randomizer on an smc file.")
    parser.add_argument('--type', required=True, help="The type of randomization ('standard' or 'chaos').")
    parser.add_argument('--input', required=True, help="Absolute path to the input smc file.")
    parser.add_argument('--output', required=True, help="Absolute path for the output smc file.")
    parser.add_argument('--spoiler', required=True, help="Absolute path for the output spoiler log.")
    
    args = parser.parse_args()

    try:
        asyncio.run(johnnydmad_webapp(
            c=args.type,
            input_smc_path=args.input,
            output_smc_path=args.output,
            spoiler_log_path=args.spoiler
        ))
        print("Johnnydmad execution successful.")
    except Exception as e:
        print(f"An error occurred during johnnydmad execution: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()