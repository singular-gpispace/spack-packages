# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Framework(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://github.com/singular-gpispace/framework"
    git      = "https://github.com/singular-gpispace/framework"

    maintainers = ['MHeymann', 'jankoboehm', 'lristau', 'mrahn']

    version('latest', branch='main')

    depends_on('singular@snapshot_22_03')
    depends_on('gpi-space@22.03:')

    def cmake_args(self):
        spec = self.spec
        print(self.spec)
        args = [ self.define("GSPC_HOME", spec['gpi-space'].prefix)
               , self.define("SINGULAR_HOME", spec['singular'].prefix)
               ]
        return args

    def setup_run_environment(self, env):
        spec = self.spec
        env.set('SINGULARPATH', self.prefix)
