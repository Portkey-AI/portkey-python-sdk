"""main file"""
import argparse
from .version import VERSION


def main():
    """Main function"""
    print("Comes here....")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=f"portkey {VERSION}",
        help="Print version and exit.",
    )

    _ = parser.parse_args()


if __name__ == "__main__":
    main()
