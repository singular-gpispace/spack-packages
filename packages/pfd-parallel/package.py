# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PfdParallel(CMakePackage):
    """Singular/GPI-Space package for parallel partial fraction decomposition."""

    homepage = "https://github.com/singular-gpispace/pfd-parallel"
    url = "https://github.com/singular-gpispace/pfd-parallel/archive/refs/tags/v0.4.1.tar.gz"
    git = "https://github.com/singular-gpispace/pfd-parallel.git"

    maintainers("jankoboehm", "lristau", "MHeymann", "mrahn")

    version("master", branch="main")
    version("0.4.1", tag="v0.4.1")
    version("0.4.0", tag="v0.4.0")
    version("0.3.0", tag="v0.3.0")
    version("0.2.0", tag="v0.2.0")
    version("0.1.0", tag="v0.1.0")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on('singular@snapshot_22_03', when='@0.1.0')
    depends_on('singular@snapshot_22_03', when='@0.2.0')
    depends_on('singular@snapshot_22_03', when='@0.3.0')
    depends_on('singular@snapshot_22_03', when='@0.4.0')
    depends_on('singular@snapshot_22_03', when='@0.4.1')
    depends_on('singular@develop', when='@master')

    depends_on('gpi-space@22.03', when='@0.1.0')
    depends_on('gpi-space@22.03', when='@0.2.0')
    depends_on('gpi-space@22.03', when='@0.3.0')
    depends_on('gpi-space@22.03', when='@0.4.0')
    depends_on('gpi-space@24.12', when='@0.4.1')
    depends_on('gpi-space@26.3', when='@master')
    depends_on('gpi-space~iml', when='@master platform=darwin')
    depends_on('gpi-space+monitor', when='@master')
    
    depends_on('flint@2.6.3:')

    def patch(self):
        if self.spec.satisfies("@master"):
            filter_file(
                r"^find_package \(util-cmake REQUIRED\)$",
                "",
                "CMakeLists.txt",
            )
            filter_file(
                r"^include \(util-cmake/add_macros\)$",
                "include (add_macros)",
                "CMakeLists.txt",
            )
            filter_file(
                r"^include \(util-cmake/beautify_find_boost\)$",
                "",
                "CMakeLists.txt",
            )
            filter_file(
                "find_boost (1.61 REQUIRED QUIET FROM_GPISPACE_INSTALLATION COMPONENTS",
                "set (Boost_NO_SYSTEM_PATHS ON)\n"
                "find_package (Boost 1.63.0 REQUIRED QUIET COMPONENTS",
                "CMakeLists.txt",
                string=True,
            )
            filter_file("Util::Generic", "gspc_util", "CMakeLists.txt", string=True)
            filter_file(
                r"^            gspc_util-Headers\n",
                "",
                "CMakeLists.txt",
            )
            filter_file(
                r"^set \(INSTALL_DO_NOT_BUNDLE ON CACHE BOOL \"\"\)$",
                'set (GSPC_INSTALL_DO_NOT_BUNDLE ON CACHE BOOL "" FORCE)',
                "CMakeLists.txt",
            )
            filter_file(
                "LIBRARIES gspc_util\n"
                "            GPISpace::execution",
                "LIBRARIES gspc_util\n"
                "            Boost::filesystem\n"
                "            Boost::system\n"
                "            GPISpace::execution",
                "CMakeLists.txt",
                string=True,
            )
            filter_file(
                r"^            GPISpace::execution$",
                "            Boost::filesystem\n"
                "            Boost::system\n"
                "            GPISpace::execution",
                "CMakeLists.txt",
            )
            filter_file(
                r"^            Singular$",
                "            Singular\n"
                "            Boost::filesystem\n"
                "            Boost::system",
                "interface/CMakeLists.txt",
            )
            filter_file(
                "LIBRARIES SINGULAR-parallel::installation\n"
                "            partial_static_parallel_allpfd_wrapper\n"
                "            gspc_util",
                "LIBRARIES SINGULAR-parallel::installation\n"
                "            partial_static_parallel_allpfd_wrapper\n"
                "            gspc_util\n"
                "            Boost::filesystem\n"
                "            Boost::system",
                "CMakeLists.txt",
                string=True,
            )
            filter_file(
                r"^find_package \(Singular REQUIRED\)$",
                "find_package (Singular REQUIRED)\n"
                "get_filename_component(PFD_SINGULAR_LIBRARY_NAME "
                '"${SINGULAR_LIBRARY}" NAME)',
                "CMakeLists.txt",
            )

            find_singular = [
                "src/cmake/modules/FindSingular.cmake",
                "interface/cmake/modules/FindSingular.cmake",
            ]
            for filename in find_singular:
                filter_file(
                    '"lib/libSingular.so" "include/singular/Singular/libsingular.h"',
                    '"lib/libSingular.so" "lib/libSingular.dylib" '
                    '"lib/libSingular.a" "include/singular/Singular/libsingular.h"',
                    filename,
                    string=True,
                )
                filter_file(
                    'NAMES "libSingular.so"',
                    "NAMES Singular",
                    filename,
                    string=True,
                )

            migrated_sources = [
                "interface/type_aliases.hpp",
                "src/installation.hpp.in",
                "src/bin/SINGULAR-parallel-module.cpp",
                "src/config.hpp.in",
                "src/installation.cpp",
                "interface/singular_functions.cpp",
            ]
            include_replacements = [
                ("#include <util-generic/", "#include <gspc/util/"),
                ("#include <drts/", "#include <gspc/drts/"),
                ("#include <we/", "#include <gspc/we/"),
            ]
            for old, new in include_replacements:
                for filename in migrated_sources:
                    filter_file(old, new, filename, string=True)

            filter_file(
                "fhg::util::current_exception_printer",
                "gspc::util::current_exception_printer",
                "src/bin/SINGULAR-parallel-module.cpp",
                string=True,
            )
            filter_file(
                "fhg::util::read_lines",
                "gspc::util::read_lines",
                "src/bin/SINGULAR-parallel-module.cpp",
                string=True,
            )
            for filename in [
                "interface/type_aliases.hpp",
                "src/bin/SINGULAR-parallel-module.cpp",
                "interface/singular_functions.cpp",
            ]:
                filter_file(
                    "pnet::type::value",
                    "gspc::pnet::type::value",
                    filename,
                    string=True,
                )
            filter_file(
                r"^                   , fhg::util::executable_path$",
                "                   , boost::filesystem::path",
                "src/installation.cpp",
            )
            filter_file(
                r"^                       \(gspc::set_gspc_home\).parent_path\(\).parent_path\(\)$",
                "                       ( gspc::util::executable_path\n"
                "                           (gspc::set_gspc_home).string()\n"
                "                       ).parent_path().parent_path()",
                "src/installation.cpp",
            )
            filter_file(
                "#include <stdexcept>",
                "#include <filesystem>\n#include <stdexcept>",
                "src/installation.cpp",
                string=True,
            )
            filter_file(
                "gspc::set_gspc_home (vm, gspc_home (_gspc_path));",
                "gspc::set_gspc_home "
                "(vm, std::filesystem::path (gspc_home (_gspc_path).string()));",
                "src/installation.cpp",
                string=True,
            )
            filter_file(
                "gspc::set_application_search_path (vm, workflow_path (_path));",
                "gspc::set_application_search_path "
                "(vm, std::filesystem::path (workflow_path (_path).string()));",
                "src/installation.cpp",
                string=True,
            )
            filter_file(
                "gspc::workflow (workflow)",
                "gspc::workflow (std::filesystem::path (workflow.string()))",
                "src/bin/SINGULAR-parallel-module.cpp",
                string=True,
            )
            filter_file(
                "#include <Singular/libsingular.h>",
                "#include <cstdio>\n\n#include <Singular/libsingular.h>",
                "interface/singular_pnet-interface.cpp",
                string=True,
            )
            filter_file(
                r"^std::ifstream open_file \(std::string const& fname\);$",
                "std::ifstream open_file (std::string const& fname);\n\n"
                "char* ssiReadString(const ssiInfo *d)\n"
                "{\n"
                "  int const len = s_readint (d->f_read);\n"
                "  if (len < 0)\n"
                "  {\n"
                "    throw std::runtime_error (\"negative SSI string length\");\n"
                "  }\n"
                "  char* s = static_cast<char*> (omAlloc (len + 1));\n"
                "  s_getc (d->f_read);\n"
                "  s_readbytes (s, len, d->f_read);\n"
                "  s[len] = '\\0';\n"
                "  return s;\n"
                "}",
                "interface/singular_functions.cpp",
            )
            filter_file(
                "#define SSI_VERSION 13",
                "#define SSI_VERSION 15",
                "interface/singular_functions.hpp",
                string=True,
            )
            filter_file(
                "#include <config.hpp>",
                "#include <config.hpp>\n\n#include <gspc/util/dynamic_linking.hpp>",
                "interface/singular_pnet-interface.hpp",
                string=True,
            )
            filter_file(
                "fhg::util::scoped_dlhandle",
                "gspc::util::scoped_dlhandle",
                "interface/singular_pnet-interface.hpp",
                string=True,
            )
            filter_file(
                "      (config::parallelInterfaceLibrary(),",
                "      (std::filesystem::path (config::parallelInterfaceLibrary().string()),",
                "interface/singular_pnet-interface.hpp",
                string=True,
            )

            filter_file(
                "#include <gspc/util/executable_path.hpp>",
                "#include <string>",
                "src/config.hpp.in",
                string=True,
            )
            filter_file(
                'installation / "libexec" / "bundle" / "singular" / "lib" / "libSingular.so"',
                'installation / "libexec" / "bundle" / "singular" / "lib" '
                '/ "@PFD_SINGULAR_LIBRARY_NAME@"',
                "src/config.hpp.in",
                string=True,
            )
            filter_file(
                'installation / "libexec" / "workflow" / "libparallel_implementation.so"',
                'installation / "libexec" / "workflow" '
                '/ "libparallel_implementation@CMAKE_SHARED_MODULE_SUFFIX@"',
                "src/config.hpp.in",
                string=True,
            )
            filter_file(
                'LIB "libSINGULAR-parallel-module.so";',
                'LIB "libSINGULAR-parallel-module@CMAKE_SHARED_LIBRARY_SUFFIX@";',
                "singular/pfd_gspc.lib.in",
                string=True,
            )

            for filename in [
                "workflow/parallel_allpfd.xpnet",
                "workflow/pfd_compute.xpnet",
                "workflow/pfd_fork_compute_step.xpnet",
                "workflow/pfd_serial_compute_pfd.xpnet",
                "workflow/pfd_serial_compute_step.xpnet",
            ]:
                filter_file(
                    'href="util-generic/',
                    'href="gspc/util/',
                    filename,
                    string=True,
                )
            filter_file(
                '            --gen-ldflags="-Wl,-rpath=\'${GSPC_HOME}/external/boost/lib\'"',
                '            --gen-ldflags="-Wl,-rpath=\'${GSPC_HOME}/external/boost/lib\'"\n'
                '            --gen-ldflags="$<TARGET_LINKER_FILE:Boost::filesystem>"\n'
                '            --gen-ldflags="$<TARGET_LINKER_FILE:Boost::system>"',
                "workflow/CMakeLists.txt",
                string=True,
            )
            filter_file(
                r"^            --gen-ldflags=\"-Wl,-rpath='\$\{GSPC_HOME\}/external/boost/lib'\"$",
                '            --gen-ldflags="-Wl,-rpath=\'${GSPC_HOME}/external/boost/lib\'"\n'
                '            --gen-ldflags="$<TARGET_LINKER_FILE:Boost::filesystem>"\n'
                '            --gen-ldflags="$<TARGET_LINKER_FILE:Boost::system>"',
                "workflow/CMakeLists.txt",
            )

    def cmake_args(self):
        spec = self.spec
        print(self.spec)
        args = [ self.define("GSPC_HOME", spec['gpi-space'].prefix)
               , self.define("SINGULAR_HOME", spec['singular'].prefix)
               , self.define("FLINT_HOME", spec['flint'].prefix)
               ]
        if spec.satisfies("@master"):
            args.append(self.define("GSPC_INSTALL_DO_NOT_BUNDLE", True))
        return args

    def setup_run_environment(self, env):
        spec = self.spec
        env.set('SINGULAR_INSTALL_DIR', spec['singular'].prefix)
        env.set('PFD_INSTALL_DIR', self.prefix)
