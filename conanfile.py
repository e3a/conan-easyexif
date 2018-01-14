from conans import ConanFile, CMake, tools
from conans.tools import download, untargz, unzip
import os

class EasyexifConan(ConanFile):
    name = "Easyexif"
    version = "master"
    license = "BSD"
    url = "https://github.com/mayanklahiri/easyexif"
    description = "A tiny ISO-compliant C++ EXIF parsing library."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    FOLDER_NAME = 'easyexif-%s' % version
 
    def run_bash(self, cmd):
        if self.settings.os == "Windows":
            tools.run_in_windows_bash(self, cmd)
        else:
            self.run(cmd)

    def source(self):
        tarball_name = 'easyexif.zip'
        download("https://github.com/mayanklahiri/easyexif/archive/%s.zip" % (self.version),
                 tarball_name)
        unzip(tarball_name)
        os.unlink(tarball_name)

    def build(self):
        with tools.chdir(self.FOLDER_NAME) :
            self.run_bash("make")

    def package(self):
        self.copy("*.h", dst="include", src="%s" % (self.FOLDER_NAME))
        if self.options.shared:
            if self.settings.os == "Macos":
                self.copy(pattern="*.dylib", dst="lib", keep_path=False)
            else:
                self.copy(pattern="*.so*", dst="lib", keep_path=False)
        else:
            self.copy(pattern="*.o", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["easyexif"]

