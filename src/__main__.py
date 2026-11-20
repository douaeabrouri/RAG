import fire
from src.commands import CLI


def main():
    fire.Fire(CLI)


if __name__ == "__main__":

    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"An error occurred: {e}")
