#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

from touying.exporter import to_html

CONFIG = {
    "file": "Tutorial.typ",
    "output": None,
    "root": None,
    "start_page": 1,
    "count": None,
    "silent": False,
}


def main():
    parser = argparse.ArgumentParser(
        description="Export Touying presentation to HTML",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s presentation.typ
  %(prog)s presentation.typ -o output.html
  %(prog)s presentation.typ --start-page 2 --count 5
  
You can also configure the file path directly in this script by setting CONFIG["file"].
        """
    )
    
    parser.add_argument(
        "input",
        nargs="?",
        help="Input typst file"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Output HTML file (default: input.html)",
        default=None
    )
    
    parser.add_argument(
        "--root",
        help="Root directory for typst file",
        default=None
    )
    
    parser.add_argument(
        "--font-paths",
        nargs="*",
        help="Paths to custom fonts",
        default=[]
    )
    
    parser.add_argument(
        "--start-page",
        type=int,
        help="Page to start from (default: 1)",
        default=1
    )
    
    parser.add_argument(
        "--count",
        type=int,
        help="Number of pages to convert (default: all)",
        default=None
    )
    
    parser.add_argument(
        "--silent",
        action="store_true",
        help="Run silently without output"
    )
    
    parser.add_argument(
        "--sys-inputs",
        help="JSON string to pass to typst's sys.inputs",
        default="{}"
    )
    
    args = parser.parse_args()
    
    input_file = args.input or CONFIG["file"]
    output_file = args.output or CONFIG["output"]
    root_dir = args.root or CONFIG["root"]
    start_page = CONFIG["start_page"]
    page_count = CONFIG["count"]
    silent_mode = CONFIG["silent"]
    
    if not input_file:
        print("Error: No input file specified.")
        print("\nPlease set CONFIG['file'] in this script or provide a file as argument.")
        print("\nUsage: python export.py <input.typ> [options]")
        print("\nUse --help for more options.")
        sys.exit(1)
    
    input_path = Path(input_file)
    if not input_path.is_absolute():
        input_path = Path.cwd() / input_path
    input_file = str(input_path)
    
    if not input_path.exists():
        print(f"Error: File not found: {input_file}")
        print(f"Current directory: {Path.cwd()}")
        sys.exit(1)
    
    try:
        import json
        sys_inputs = json.loads(args.sys_inputs)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in --sys-inputs: {args.sys_inputs}")
        sys.exit(1)
    
    try:
        to_html(
            input=input_file,
            root=root_dir,
            font_paths=args.font_paths,
            output=output_file,
            start_page=start_page,
            count=page_count,
            silent=silent_mode,
            sys_inputs=sys_inputs
        )
        
        if not silent_mode:
            output = output_file or Path(input_file).with_suffix(".html")
            print(f"Successfully exported to {output}")
            
    except PermissionError as e:
        print(f"Error: Access denied - the file may be open in another program.")
        print(f"File: {input_file}")
        print(f"Please close any programs that might be using this file and try again.")
        print(f"Details: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
