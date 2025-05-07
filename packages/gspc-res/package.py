from spack import *


class GspcRes(CMakePackage):
    """`gspc-res` is a tool in the GPI-Space/Singular ecosystem for computing 
    resolutions in a parallel fashion, leveraging the GPI-Space workflow engine."""

    homepage = "https://github.com/singular-gpispace/gspc-res"
    git      = "https://github.com/singular-gpispace/gspc-res.git"

    maintainers = ['jankoboehm','santosh']

    version('latest', branch='main')


    depends_on('singular@4.4.0')
    depends_on('singular@snapshot_22_03')
    depends_on('gpi-space@22.06:24.12')

  

    depends_on('flint@2.6.3:')

    def cmake_args(self):
        spec = self.spec
        print(self.spec)
        args = [
            self.define("GSPC_HOME", spec['gpi-space'].prefix),
            self.define("SINGULAR_HOME", spec['singular'].prefix),
            self.define("FLINT_HOME", spec['flint'].prefix),
        ]
        return args

    def setup_run_environment(self, env):
        spec = self.spec
        env.set('SINGULAR_INSTALL_DIR', spec['singular'].prefix)
        env.set('GSPC_RES_INSTALL_DIR', self.prefix)