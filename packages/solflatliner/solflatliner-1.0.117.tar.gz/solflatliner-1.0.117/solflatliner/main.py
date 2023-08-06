#!/usr/bin/env python3
import argparse
import os
import re
import sys
from os.path import exists
from re import Pattern

DESCRIPTION = """
Source Verification Unfolds.\n
Unfolds all local imports in a solidity file to generate a flat solidity file.\n
Put the output file into out/ folders.
"""

pattern_contract = r"^contract.\S.[a-zA-Z0-9]+"
pattern_abstract_contract = r"^abstract\scontract.\S.[a-zA-Z0-9]+"
pattern_library = r"^library.\S.[a-zA-Z0-9]+"
pattern_interface = r"^interface.\S.[a-zA-Z0-9]+"


def parse_arguments():
    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "file", type=str, metavar="*.sol",
        help="target filename with imports")

    parser.add_argument(
        "version", type=str, metavar="*.*.*",
        help="solidity compiler version e.g. 0.4.24")

    parser.add_argument(
        "-o", "--output", type=str, metavar="*.sol",
        help="output filename (default: flat.sol)")

    parser.add_argument(
        "-d", "--ofolder", type=str, metavar="*",
        help="output folder (default: verify)",
        default="verify")

    parser.add_argument(
        "-lib", "--library", type=str, metavar="*",
        help="Reference library folder path (default: lib)",
        default="lib")

    parser.add_argument(
        "-l", "--license", type=str, metavar="*",
        help="Licensing identifier. Please check from https://spdx.org/licenses/ for detail (default: AGPL-3.0)",
        default="AGPL-3.0")

    args = parser.parse_args()
    return args


def is_sol_valid(infile, s):
    if ".sol" != infile[-4:]:
        print("{} file is not a solidity file!!!".format(s))
        sys.exit(-2)


def check_signatures(line: str, signatures: list, p: str) -> int:
    if re.search(p, line):
        res = re.findall(p, line)[0]
        if res in signatures:
            print(f"dup signature:: {res}")
            return 2
        else:
            signatures.append(res)
            return 1
    else:
        return 0


def unfold_imports(library_folder: str, imports: list, signatures: list, infile: str, importline: str = ""):
    buffer = []

    if infile not in imports:

        found = exists(infile)

        if not found:
            if importline == "":
                print(f"There is no file found from the given path {infile}")
                sys.exit(-5)
            else:
                infile = os.path.join(library_folder, importline)

        try:
            with open(infile, "r+") as f:
                signature_count = 0
                skipline = False
                for line in f:
                    # Remove the pragma line in all imports
                    if "pragma" in line[:6]:
                        continue
                    # Remove the LICENSE line in all imports
                    if "//" in line[:2] and "SPDX-License-Identifier:" in line:
                        continue

                    g11 = check_signatures(line, signatures, pattern_contract)

                    if g11 == 1:
                        signature_count += g11

                    if g11 == 2:
                        skipline = True

                    g12 = check_signatures(line, signatures, pattern_abstract_contract)

                    if g12 == 1:
                        signature_count += g12

                    if g12 == 2:
                        skipline = True

                    g2 = check_signatures(line, signatures, pattern_interface)

                    if g2 == 1:
                        signature_count += g2

                    if g2 == 2:
                        skipline = True

                    g3 = check_signatures(line, signatures, pattern_library)

                    if g3 == 1:
                        signature_count += g3

                    if g3 == 2:
                        skipline = True

                    # Read the imports
                    if "import" in line[:6]:
                        match = re.search(r".*[\'|\"](.*)[\'|\"]", line)
                        if match:
                            dirname = os.path.dirname(infile)
                            importline = match.group(1)
                            file = os.path.join(dirname, importline)
                            absfile = os.path.abspath(file)
                            buffer.append(unfold_imports(library_folder, imports, signatures, absfile, importline))
                            imports.append(absfile)
                        else:
                            print("There's syntax error of import in {}".format(infile))
                            sys.exit(-3)

                        continue

                    if skipline is False:
                        buffer.append(line)

                    if "}" in line[:1]:
                        skipline = False

                if signature_count > 1:
                    print("there are more than 1 class primitive in this file.")

        except FileNotFoundError:
            print(f"There is no file found from the given path {infile}")
            sys.exit(-5)

    return ''.join(buffer)


def main():
    # Read arguments
    args = parse_arguments()
    # Check if the solidity compiler version format is valid
    match = re.search(r"\d+\.\d+\.\d+", args.version)
    if not match:
        print("Compiler version is not a valid format")
        sys.exit(-1)
    # Check if the input solidity filename is valid
    is_sol_valid(args.file, "Input")
    dirname = os.path.dirname(os.path.abspath(args.file))
    basename = os.path.basename(os.path.abspath(args.file))
    # Check if the output solidity filename is valid
    if not args.output:
        args.output = basename[:-4] + "-flat.sol"
    is_sol_valid(args.output, "Output")

    # arguments configurations
    LICENSE = args.license
    OUTPUT_FOLDER = f"{args.ofolder}/"
    VERSION = args.version
    INFILE = args.file

    # Make output folder
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    outfile = os.path.join(OUTPUT_FOLDER, args.output)
    # output file and input file
    imports = []
    signatures = []
    with open(outfile, "w+") as f:
        f.write("pragma solidity ^{};\n".format(VERSION))
        f.write("// SPDX-License-Identifier: {}\n".format(LICENSE))
        f.write("// Please do not edit this file as this is generated file \n")
        f.write(unfold_imports(args.library, imports, signatures, os.path.abspath(INFILE)))

    print("🥡 Success! Output: {} in the {} folder".format(os.path.basename(outfile), OUTPUT_FOLDER))


def checker():
    version = "0.8.13"
    infile = "/Users/hesdx/Documents/piplines/solidity-flatliner/example/test.sol"
    outfile = "/Users/hesdx/Documents/piplines/solidity-flatliner/example/atest.sol"
    lib = "lib"
    imports = []
    signatures = []
    with open(outfile, "w+") as f:
        f.write("pragma solidity ^{};\n".format(version))
        f.write("// SPDX-License-Identifier: agpl-3.0\n")
        f.write(unfold_imports(lib, imports, signatures, os.path.abspath(infile)))

    print(f"after test imports: {imports}")
    print(f"after test signatures: {signatures}")


if __name__ == "__main__":
    main()
