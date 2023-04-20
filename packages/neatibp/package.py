# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Neatibp(Package):

    homepage = "https://github.com/yzhphy/NeatIBP/"
    git      = "https://github.com/yzhphy/NeatIBP.git"

    maintainers = ['Wu-Zihao', 'yzhphy', 'RWUSTC']

    version('1.0.1.3', branch='main')

    depends_on('git@2.38.1')
    depends_on('spasm@1.2')
    depends_on('singular@snapshot_22_03')

    def install(self, spec, prefix):
        with working_dir(prefix):
            git = which('git')
            git('clone', self.git)
        with working_dir("Spack_scripts"):
            copy = Executable("./spack_script_cp.sh")
            copy()


    def setup_run_environment(self, env):
        spec = self.spec
        env.set('SINGULAR_INSTALL_DIR', spec['singular'].prefix)
        env.set('SPASM_INSTALL_DIR', spec['spasm'].prefix)
        env.set('NEATIBP_INSTALL_DIR', self.prefix)

