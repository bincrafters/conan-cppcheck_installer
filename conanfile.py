import os
from conans import ConanFile, CMake, tools


class CppCheckConan(ConanFile):
    name = "cppcheck_installer"
    version = "1.89"
    url = "https://github.com/bincrafters/conan-protoc_installer"
    homepage = "https://github.com/danmar/cppcheck"
    topics = ("Cpp Check", "static analyzer")
    author = "Mark Jan van Kampen (@mjvk)"
    description = ("Cppcheck is an analysis tool for C/C++ code.")
    license = "GPL-3.0"
    exports = ["LICENSE.txt"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "compiler", "arch", "os_build", "arch_build"

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def source(self):
        sha256 = "37452d378825c7bd78116b4d7073df795fa732207d371ad5348287f811755783"
        tools.get("{0}/archive/{1}.tar.gz".format(self.homepage, self.version), sha256=sha256)
        os.rename("cppcheck-%s" % self.version, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["FLATBUFFERS_BUILD_TESTS"] = False
        cmake.definitions["FLATBUFFERS_BUILD_FLATLIB"] = False
        cmake.definitions["FLATBUFFERS_BUILD_FLATHASH"] = False
        cmake.definitions["FLATBUFFERS_INSTALL"] = True
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("COPYING", dst="licenses", src=self._source_subfolder)
        self.copy("*", dst=os.path.join("bin","cfg"), src=os.path.join(self._source_subfolder,"cfg"))
        cmake = self._configure_cmake()
        cmake.install()
        tools.rmdir(os.path.join(self.package_folder, "share"))

    def package_id(self):
        del self.info.settings.compiler
        del self.info.settings.arch
        self.info.include_build_settings()

    def package_info(self):
        bin_folder = os.path.join(self.package_folder, "bin")
        self.output.info("Append %s to environment variable PATH" % bin_folder)
        self.env_info.PATH.append(bin_folder)