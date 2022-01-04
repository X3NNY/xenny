import subprocess


def is_sage():
    """Check if sage is installed and working"""
    try:
        sageversion = subprocess.check_output(["sage", "-v"], timeout=10)
    except OSError:
        return False

    if "SageMath version" in sageversion.decode("utf-8"):
        return True
    else:
        return False
