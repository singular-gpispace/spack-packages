    # Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Singular(AutotoolsPackage):
    """
    Singular is a computer algebra system for polynomial computations, with
    special emphasis on commutative and non-commutative algebra, algebraic
    geometry, and singularity theory. It is free and open-source under the GNU
    General Public Licence.
    """

    homepage = "https://www.singular.uni-kl.de"
    url      = "https://github.com/Singular/Singular/archive/refs/tags/Release-4-4-0.tar.gz"
    git      = "https://github.com/Singular/Singular.git"

    maintainers = ['hannes14', 'jankoboehm', 'MHeymann']

    version('develop', branch='spielwiese')

    version('4.4.1p5', tag='Release-4-4-1p5')
    version('4.4.1', tag='Release-4-4-1')
    version('4.4.0p7', tag='Release-4-4-0p7')
    version('4.4.0p6', tag='Release-4-4-0p6')
    version('4.4.0p5', tag='Release-4-4-0p5')
    version('4.4.0p4', tag='Release-4-4-0p4')
    version('4.4.0p2', tag='4.4.0p2')
    version('4.4.0', tag='Release-4-4-0')
    version('4.3.2p16', tag='Release-4-3-2p16')
    version('4.3.2p15', tag='4.3.2p15')
    version('4.3.2p14', tag='Release-4-3-2p14')
    version('4.3.2p10', tag='Release-4-3-2p10')
    version('4.3.2p9', tag='Release-4-3-2p9')
    version('4.3.2p8', tag='Release-4-3-2p8')
    version('4.3.2p7', tag='Release-4-3-2p7')
    version('4.3.2p6', tag='Release-4-3-2p6')
    version('4.3.2p5', tag='Release-4-3-2p5')
    version('4.3.2p4', tag='Release-4-3-2p4')
    version('4.3.2p3', tag='Release-4-3-2p3')
    version('4.3.2p2', tag='Release-4-3-2p2')
    version('4.3.2p1', tag='Release-4-3-2p1')
    version('4.3.2', tag='Release-4-3-2')
    version('4.3.1', tag='Release-4-3-1')
    version('4.3.0', tag='Release-4-3-0')
    version('4.2.1p3', tag='Release-4-2-1p3')
    version('4.2.1p2', tag='Release-4-2-1p2')
    version('4.2.1', tag='Release-4-2-1')
    version('4.2.0p3', tag='Release-4-2-0p3')
    version('4.2.0', tag='Release-4-2-0')
    version('4.1.3p2', tag='Release-4-1-3p2')
    version('4.1.3', tag='Release-4-1-3')
    version('4.1.2', tag='Release-4-1-2')
    version('4.1.1', tag='Release-4-1-1')
    version('4.1.0', tag='Release-4-1-0')
    version('4.0.3', tag='Release-4-0-3')
    version('4.0.1', tag='Release-4-0-1')
    version('4.0.0', tag='Singular_4.0.0')

    version('snapshot_22_03', commit='e12a8af3d7330a34cb43811e28ecde25afe83a4f')


    depends_on('c', type='build')
    depends_on('cxx', type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('m4', type='build')

    depends_on('readline@8.1:')
    depends_on('ntl@11.5.1:+shared')
    depends_on('flint@2.6.3:')
    depends_on('cddlib@0.94m')
    depends_on('4ti2@=1.6')

    def autoreconf(self, spec, prefix):
        autogen_script = Executable("./autogen.sh")
        autogen_script()

    def configure_args(self):
        spec = self.spec
        args = [ '--with-flint={0}'.format(spec['flint'].prefix)
               , '--with-ntl={0}'.format(spec['ntl'].prefix)
               , '--enable-gfanlib'
               ]
        return args
