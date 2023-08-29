"""main file"""
import argparse
from rubeus.version import VERSION


def main():
    """Main function"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=f"rubeus {VERSION}",
        help="Print version and exit.",
    )

    _ = parser.parse_args()


if __name__ == "__main__":
    main()
