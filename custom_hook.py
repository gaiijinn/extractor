import subprocess


def run_custom_hook():

    result_black = subprocess.run(["black", "--verbose", "."], capture_output=True, text=True)
    print(result_black.stdout)
    if result_black.stderr:
        print(result_black.stderr)

    result_flake8 = subprocess.run(["flake8", "--verbose", "."], capture_output=True, text=True)
    print(result_flake8.stdout)
    if result_flake8.stderr:
        print(result_flake8.stderr)


if __name__ == "__main__":
    run_custom_hook()
