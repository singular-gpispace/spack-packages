# Copyright 2015-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Spasm(Package):
    """SpaSM installation."""

    git      = "https://github.com/cbouilla/spasm.git"

    maintainers = ['ClaireDlp', 'cbouilla']
    
    version('1.2', branch='master')

    # Overlap in functionality between gmp and mpir
    # All other dependencies must also be built with
    # one or the other
    # variant('mpir', default=False,
    #         description='Compile with the MPIR library')

    # Build dependencies
    depends_on("m4", type="build")
    depends_on("autoconf",  type="build")
    depends_on("automake",  type="build")
    depends_on("libtool", type="build")

    phases = ['autoreconf', 'configure', 'build', 'install']

    def configure_args(self):
        prefix = self.prefix
        spec = self.spec
        args = ["--prefix=%s" % prefix]

        # if '+mpir' in spec:
        #     args.extend([
        #         "--with-mpir=%s" % spec['mpir'].prefix
        #     ])

        return args

    def autoreconf(self, spec, prefix):
        autoreconf = which("autoreconf")
        automake = which("automake")
        autoreconf("-i")
        automake("--add-missing")

    def configure(self, spec, prefix):
        configure_script = Executable("./configure")
        configure(*self.configure_args())

    def build(self, spec, prefix):
        make()
        if self.run_tests:
            make("check")

    def install(self, spec, prefix):
        #options = ["--prefix=%s" % prefix,
        #           "--with-gmp=%s" % spec['gmp'].prefix,
        #           "--with-mpfr=%s" % spec['mpfr'].prefix]
        #configure(*options)
        #make()
        #if self.run_tests:
        #    make("check")
        make("install")

