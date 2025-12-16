# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Modular(GitPackage, CMakePackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://github.com/singular-gpispace/modular"
    git      = "https://github.com/singular-gpispace/modular"

    maintainers = ['hobihsina','jankoboehm']

    version('latest', branch='main')

    depends_on('singular@snapshot_22_03')
    depends_on('gpi-space@22.06:')
    depends_on('flint@2.6.3:')

    def cmake_args(self):
        spec = self.spec
        print(self.spec)
        args = [ self.define("GSPC_HOME", spec['gpi-space'].prefix)
               , self.define("SINGULAR_HOME", spec['singular'].prefix)
               , self.define("FLINT_HOME", spec['flint'].prefix)
               ]
        return args

    def setup_run_environment(self, env):
        spec = self.spec
        env.set('SINGULAR_INSTALL_DIR', spec['singular'].prefix)
        env.set('MODULAR_INSTALL_DIR', self.prefix)

