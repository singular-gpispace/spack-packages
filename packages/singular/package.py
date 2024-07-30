    # Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


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

    version('latest', branch='spielwiese')
    
    version('4.3.2p15', commit='4cf733b2521a0ad9cb602f3dd16c7a81ab977991')
    version('4.4.0p2', commit='d735977bc4c759f0ed30bd5cdc57a5b212075497')
    version('Release-4-0-1', commit='1993ad5f66aaca4421aa2deaac5f4a010acc9844')
    version('Release-4-0-3', commit='b4e678f4ebbc2cbfb443db3205b1e086ba00bb4c')
    version('Release-4-1-0', commit='0c5e11f67ef050ccd28acec5dc47d0249ecd11e7')
    version('Release-4-1-1', commit='7161cff60410d893038585a5a94be6dff96f8a2c')
    version('Release-4-1-2', commit='c717a0d94de0f701587bc5adbfab65df74dd599a')
    version('Release-4-1-3', commit='396fd5153d1fe81e12f0b41fc72717aa2d3012d2')
    version('Release-4-1-3p2', commit='2e69cf919d22bd231e8ebe47715df4939b14961b')
    version('Release-4-2-0', commit='8cf4d31bb708e264c0e6082a13985538a2acd84f')
    version('Release-4-2-0p3', commit='0dabbb616c7d95f0c9e81e9f51b857e3a0bb9e7c')
    version('Release-4-2-1', commit='114df81a398fed5ea1f07adb4747217784b0b5e4')
    version('Release-4-2-1p2', commit='a15b7fe3ec918262cec68ec40637e9f1c2a4b6cf')
    version('Release-4-2-1p3', commit='74d235a25eae63942f942c50a042d010129ed19a')
    version('Release-4-3-0', commit='d895b0f1f543c61eb03adddad20f08655a419d4e')
    version('Release-4-3-1', commit='13640e8c400cbee504e7e26868152daf7c464261')
    version('Release-4-3-2', commit='de205cd8b01e66230d37eb4b0a1daed463db7f3b')
    version('Release-4-3-2p1', commit='a800fe4b3e9d37a38c5a10cc0ae9dfa0c15a4ee6')
    version('Release-4-3-2p10', commit='68fda8e4cf88047a5f398868488e6ba6dc062a65')
    version('Release-4-3-2p14', commit='9413e2181e45f7e7c2764bcb39f0487b97f4d3ba')
    version('Release-4-3-2p16', commit='dd3cdb9dea0b3e0019893c63ecefd4871d0b52d4')
    version('Release-4-3-2p2', commit='0d6b7fcd9813a1ca1ed4220cfa2b104b97a0a003')
    version('Release-4-3-2p3', commit='0a26a76e93bb0b8f2930faa550fb3a480d3faeb8')
    version('Release-4-3-2p4', commit='3ddd70d17690c54ce186c280630a2a0e67cc929f')
    version('Release-4-3-2p5', commit='0d1d9fa1420e6a2f70b36f04bd1da52e8ba3ba00')
    version('Release-4-3-2p6', commit='325bd3a618cf9f3e66b6f2455dd74132f1185af2')
    version('Release-4-3-2p7', commit='c0a55395d8cad2c626515ab8b66dda36bf89b6d6')
    version('Release-4-3-2p8', commit='8e0ad00ce244dfd0756200662572aef8402f13d5')
    version('Release-4-3-2p9', commit='1105792e563fca1ff238275b14b79718887f63c9')
    version('Release-4-4-0', commit='73c62e0961bcfc8f1a00420b41eec2ea3c0ef6e9')
    version('Singular_4.0.0', commit='b2cb7b48301812323aeeb1e1bd6dd5fce53626b4')


    version('snapshot_22_03', commit='e12a8af3d7330a34cb43811e28ecde25afe83a4f')
    version('4-3-0', sha256='9189ef41e91317f4de2b4e5d83ae257a26a0bd009a2a4a133b4477212a1f6fd2')


    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    depends_on('readline@8.1:')
    depends_on('ntl@11.5.1: +shared')
    depends_on('flint@2.6.3:')
    depends_on('cddlib@0.94m')
    depends_on('4ti2@1.6')

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
