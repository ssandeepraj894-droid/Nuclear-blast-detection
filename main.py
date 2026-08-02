#!/usr/bin/env python3
"""
Root execution entry point for Nuclear Blast Detector application.
"""

import sys
from nuclear_blast_detector.cli import cli_main

if __name__ == "__main__":
    cli_main(sys.argv[1:])
