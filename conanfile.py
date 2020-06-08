import os
from conans import ConanFile, CMake, tools


class CppCheckConan(ConanFile):
    name = "cppcheck_installer"
    url = "https://github.com/bincrafters/conan-cppcheck_installer"
    homepage = "https://github.com/danmar/cppcheck"
    topics = ("Cpp Check", "static analyzer")
    author = "Mark Jan van Kampen (@mjvk)"
    description = "Cppcheck is an analysis tool for C/C++ code."
    license = "GPL-3.0-or-later"
    exports_sources = ["CMakeLists.txt", "patches/*"]
    generators = "cmake"
    settings = "compiler", "arch", "os_build", "arch_build"
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = "cppcheck-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        for p in self.conan_data["patches"][self.version]:
            tools.patch(**p)
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
