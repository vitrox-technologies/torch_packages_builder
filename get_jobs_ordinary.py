import json
import os


LINUX_X64 = "ubuntu-22.04"
WINDOWS_X64 = "windows-2022"
MACOS_X64 = "macos-13"
MACOS_ARM64 = "macos-14"

# Standard Python versions to support
DEFAULT_PYTHON_VERSIONS = ("3.9", "3.10", "3.11", "3.12", "3.13")
# Standard numpy versions to support
DEFAULT_NUMPY_VERSIONS = ("1.24.0", "1.26.0", "2.0.0")


def add_os(oses_list: list, os_name: str, os_env_var: str):
    if os.environ[os_env_var] == "true":
        oses_list.append(os_name)


def main():
    limit_python = os.environ.get("LIMIT_PYTHON")
    if limit_python:
        python_versions = limit_python.split(",")
    else:
        python_versions = DEFAULT_PYTHON_VERSIONS
    
    numpy_version = os.environ.get("NUMPY_VERSION")
    if numpy_version:
        numpy_versions = numpy_version.split(",")
    else:
        numpy_versions = DEFAULT_NUMPY_VERSIONS

    oses_names = []
    add_os(oses_names, LINUX_X64, "LINUX_WHEELS")
    add_os(oses_names, WINDOWS_X64, "WINDOWS_WHEELS")
    add_os(oses_names, MACOS_X64, "MACOS_WHEELS")
    add_os(oses_names, MACOS_ARM64, "MACOS_WHEELS")
    if not oses_names:
        raise RuntimeError("Select at least one OS")

    jobs = []
    for os_name in oses_names:
        for python_version in python_versions:
            for numpy_ver in numpy_versions:
                # Skip older Python versions on macOS ARM64
                pv = [int(x) for x in python_version.split(".")]
                if os_name == MACOS_ARM64 and pv[1] <= 9:
                    continue

                jobs.append({
                    "os": os_name,
                    "python-version": python_version,
                    "numpy-version": numpy_ver,
                })

    if not jobs:
        raise RuntimeError("No jobs to do")

    strategy_matrix = {"include": jobs}
    print(json.dumps(strategy_matrix))


if __name__ == "__main__":
    main()