pkgname = "bootc"
pkgver = "0.1.15"
pkgrel = 0
build_style = "cargo"
# One test fails due to an issue with musl support in the libc crate
make_check_args = ["--", "--skip=command_run_ext"]
hostmakedepends = [
    "cargo-auditable",
    "pkgconf",
]
makedepends = [
    "glib-devel",
    "openssl-devel",
    "ostree-devel",
    "rust-std",
    "zstd-devel",
]
depends = [
    "bootupd"
]
pkgdesc = "Boot and upgrade via container images"
maintainer = "Aster Boese <asterboese@mailbox.org>"
license = "Apache-2.0 OR MIT"
url = "https://github.com/containers/bootc"
source = f"{url}/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "643242e9a5fe28e441fff7ddcb060a0829994b8f316f2977cbf256028257381e"


def post_patch(self):
    from cbuild.util import cargo

    cargo.clear_vendor_checksums(self, "ostree-ext")


def install(self):
    self.cargo.install(wrksrc="cli")
    self.install_license("LICENSE-APACHE")
    self.install_license("LICENSE-MIT")
