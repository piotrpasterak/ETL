"""Tiny module for supporting installation process. Mainly uses Gecko driver downloader.
"""
from webdriverdownloader import GeckoDriverDownloader


def install():
    dd = GeckoDriverDownloader()
    dd.download_and_install()


if __name__ == '__main__':
    install()
