pkgname = "bootupd"
pkgver = "0.2.21"
pkgrel = 0
build_style = "cargo"
hostmakedepends = [
    "cargo-auditable",
    "openssl-devel",
    "pkgconf",
]
pkgdesc = "Distro-agnostic bootloader updater"
maintainer = "Aster Boese <asterboese@mailbox.org>"
license = "Apache-2.0"
url = "https://github.com/coreos/bootupd"
source = f"{url}/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "969150dc61faad1051c359ee31a60c9d3deb3d2310160e5a1c1a77fad7153160"
# tests fail with "creation time is not available on this platform currently"
options = ["!check"]


def post_install(self):
    self.install_license("COPYRIGHT")
