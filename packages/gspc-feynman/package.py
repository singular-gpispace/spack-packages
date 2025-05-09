# Copyright 2013-2021 Lawrence Livermore National Security, LLC
# and other Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import shutil


class GspcFeynman(CMakePackage):
    """A GPI-Space based implementation for computing Feynman integrals.
    
    This package provides parallel computation capabilities for Feynman integrals
    using GPI-Space and Singular. It includes examples demonstrating the usage
    of the Feynman module for various computations."""

    homepage = "https://github.com/singular-gpispace/gspc-feynman"
    git      = "https://github.com/singular-gpispace/gspc-feynman"

    maintainers = ['alitraore', 'jankoboehm']

    version('latest', branch='main')

    depends_on('singular@4.4.0p2')
    depends_on('gpi-space@24.12:')
    depends_on('flint@2.6.3:')
    depends_on('boost@1.63.0: +serialization +system +filesystem +program_options +thread +chrono +date_time +atomic')

    @property
    def root_cmakelists_dir(self):
        return self.stage.source_path + "/template"

    def cmake_args(self):
        spec = self.spec
        return [
            self.define("GSPC_HOME", spec['gpi-space'].prefix),
            self.define("SINGULAR_HOME", spec['singular'].prefix),
            self.define("FLINT_HOME", spec['flint'].prefix)
        ]

    def setup_run_environment(self, env):
        """Set environment variables when the package is loaded."""
        env.set('SINGULAR_INSTALL_DIR', self.spec['singular'].prefix)
        env.set('GSPC_FEYNMAN_INSTALL_DIR', self.prefix)
        env.set('GSPC_FEYNMAN_EXAMPLES_DIR', self.prefix.share.examples)
        # Add lib directory to LD_LIBRARY_PATH
        env.prepend_path('LD_LIBRARY_PATH', os.path.join(self.prefix, 'lib'))

    def setup_dependent_run_environment(self, env, dependent_spec):
        """Set environment variables for packages depending on this one."""
        env.set('GSPC_FEYNMAN_EXAMPLES_DIR', self.prefix.share.examples)
        # Add lib directory to LD_LIBRARY_PATH for dependent packages
        env.prepend_path('LD_LIBRARY_PATH', os.path.join(self.prefix, 'lib'))

    @run_after('install')
    def install_examples(self):
        """Install example files and print final instructions."""
        examples_dir = os.path.join(self.prefix.share, 'examples')
        lib_dir = os.path.join(self.prefix, 'lib')
        libexec_dir = os.path.join(self.prefix, 'libexec')
        mkdirp(examples_dir)
        mkdirp(lib_dir)
        mkdirp(libexec_dir)
        
        # Install examples
        for example in ['templategp.lib', 'templategspc.lib']:
            install(os.path.join(self.stage.source_path, 'examples', example), examples_dir)

        # Move libraries
        for lib in ['libSINGULAR-template-module.so', 'libSINGULAR-template-installation.so']:
            src = os.path.join(self.prefix, lib)
            dst = os.path.join(lib_dir, lib)
            if os.path.exists(src):
                shutil.copy2(src, dst)
                os.remove(src)
                os.chmod(dst, 0o755)

        # Copy setup.sh to libexec directory
        setup_script = os.path.join(self.stage.source_path, 'setup.sh')
        if os.path.exists(setup_script):
            install(setup_script, libexec_dir)
            os.chmod(os.path.join(libexec_dir, 'setup.sh'), 0o755)

      