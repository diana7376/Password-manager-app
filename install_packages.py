import subprocess


def install_packages():
    packages = [
        "django",
        "djangorestframework",
        "django-filter",
        "django-cors-headers",
        "django-no-last-login",
        "mysqlclient",
        "cryptography",
        "drf-nested-routers",
        "djangorestframework-simplejwt"
    ]

    for package in packages:
        subprocess.check_call(["pip", "install", package])


if __name__ == "__main__":
    install_packages()
