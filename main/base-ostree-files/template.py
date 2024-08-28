pkgname = "base-ostree-files"
_iana_ver = "20240813"
pkgver = f"0.1.{_iana_ver}"
pkgrel = 1
provides = ["base-files"]
# highest priority dir owner
replaces_priority = 65535
pkgdesc = "Chimera Linux base system files"
maintainer = "q66 <q66@chimera-linux.org>"
license = "custom:meta"
url = "https://chimera-linux.org"
# no tests
options = ["!check", "bootstrap", "keepempty", "brokenlinks"]

def install(self):
    # base root dirs
    for d in [
        "boot",
        "dev",
        "etc",
        "media",
        "proc",
        "sys",
        "sysroot",
        "usr",
        "var",
    ]:
        self.install_dir(d)

    # /usr dirs
    for d in ["bin", "include", "lib", "share", "src"]:
        self.install_dir("usr/" + d)

    # apk exec dir
    self.install_dir("usr/lib/apk/exec")

    # mandirs
    for i in range(1, 8):
        self.install_dir("usr/share/man/man" + str(i))

    # /var dirs
    for d in ["empty", "log", "opt", "cache", "lib", "mail", "spool", "www", "home", "mnt", "usrlocal", "srv"]:
        self.install_dir("var/" + d)

    # /var/usrlocal dirs
    for d in ["bin", "include", "lib", "share", "src"]:
        self.install_dir("var/usrlocal/" + d)

    # /var symlinks
    self.install_link("var/lock", "var/run/lock")
    self.install_link("run", "var/run")
    self.install_link("mail", "var/spool/mail")
    self.install_link("usr/local", "var/usrlocal")
    self.install_link("mnt", "var/mnt")
    self.install_link("home", "var/home")
    self.install_link("opt", "var/opt")
    self.install_link("srv", "var/srv")

    # root's home dir
    self.install_dir("var/roothome")
    (self.destdir / "var/roothome").chmod(0o750)

    # root's home symlink
    self.install_link("root", "var/roothome")

    # /sysroot dirs
    for d in ["ostree", "tmp", "var/tmp"]:
        self.install_dir("sysroot/" + d)
        self.install_link(d, "sysroot/" + d)
    (self.destdir / "sysroot/tmp").chmod(0o777)

    # Create bin and lib dirs and symlinks
    for d in ["bin", "lib"]:
        self.install_dir("usr/" + d)
        self.install_link(d, "usr/" + d)

    # Symlink sbin paths to /usr/bin
    self.install_link("sbin", "usr/bin")
    self.install_link("usr/sbin", "usr/bin")
    self.install_link("var/usrlocal/sbin", "usr/bin")

    # Users and tmpfiles
    self.install_sysusers(self.files_path / "sysusers.conf")
    self.install_tmpfiles(self.files_path / "tmpfiles.conf")

    # Mutable files not to be tracked by apk
    for f in [
        "fstab",
        "hosts",
        "issue",
        "nsswitch.conf",
        "securetty",
    ]:
        self.install_file(self.files_path / "etc" / f, "usr/share/base-files")

    # Mutable files to be tracked by apk
    for f in [
        "profile",
        "passwd",
        "group",
    ]:
        self.install_file(self.files_path / "etc" / f, "etc")

    # Files that should usually not be changed
    for f in [
        "chimera-release",
        "os-release",
        "profile.path",
        "protocols",
        "services",
    ]:
        self.install_file(self.files_path / "etc" / f, "etc")

    self.install_dir("etc/profile.d")

    for f in (self.files_path / "profile.d").glob("*.sh"):
        self.install_file(f, "etc/profile.d")

    # Install common licenses
    self.install_dir("usr/share/licenses")

    for f in (self.files_path / "licenses").iterdir():
        self.install_file(f, "usr/share/licenses")

    self.install_bin(self.files_path / "lsb_release")

    # Create /proc/self/mounts -> /etc/mtab symlink
    self.install_link("etc/mtab", "../proc/self/mounts")

# TODO: Uncomment once apk-ostree exists
# def post_install(self):
#     # Make root dirs read-only
#     for d in [
#         "boot",
#         "dev",
#         "etc",
#         "media",
#         "proc",
#         "run",
#         "sys",
#         "sysroot",
#         "usr",
#         "var",
#     ]:    
#         if d is not "etc" and d is not "var":
#             (self.destdir / d).chmod(0o444)

@subpackage("base-ostree-devel")
def _(self):
    self.pkgdesc = "Base package for development packages"
    self.depends = []
    self.options = ["empty"]
    self.provides = ["base-devel"]

    return []


@subpackage("base-ostree-devel-static")
def _(self):
    self.pkgdesc = "Base package for static development packages"
    self.depends = []
    self.install_if = []
    self.options = ["empty"]
    self.provides = ["base-devel-static"]

    return []


@subpackage("base-ostree-doc")
def _(self):
    self.pkgdesc = "Base package for documentation"
    self.depends = []
    self.options = ["empty"]
    self.provides = ["base-doc"]

    return []
