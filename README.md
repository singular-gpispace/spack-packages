# Spack packages for Singular and GPI-Space

This repository contains Spack package recipes for Singular, GPI-Space, and
packages built on top of them.

The recipes are intended for current Spack releases. The instructions below use
Spack 1.1.1. Linux is supported for the full GPI-Space stack. macOS is supported
for Singular and for GPI-Space without IML/GPI-2 support.

## Setup

Choose a writable directory for Spack and this package repository:

```bash
export software_ROOT=~/singular-gpispace
mkdir -p "$software_ROOT"
```

Set this variable again in each new shell, or add it to your shell profile.

## Install Spack

Clone Spack and check out the 1.1 release branch:

```bash
git clone https://github.com/spack/spack.git "$software_ROOT/spack"
cd "$software_ROOT/spack"
git checkout releases/v1.1
```

To use Spack from the command line:

```bash
. "$software_ROOT/spack/share/spack/setup-env.sh"
```

Run this setup command in each new shell, or add it to your shell profile.

On Ubuntu/Debian, install the common system dependencies first:

```bash
sudo apt update
sudo apt install build-essential ca-certificates coreutils curl environment-modules gfortran git gnupg lsb-release python3 python3-venv unzip zip
```

Spack bootstraps its solver the first time it concretizes a spec:

```bash
spack spec zlib
```

If downloads fail because of a slow connection, increase `connect_timeout` in:

```bash
"$software_ROOT/spack/etc/spack/defaults/config.yaml"
```

## Add This Repository

Clone this repository and add it as a Spack package repository:

```bash
git clone https://github.com/singular-gpispace/spack-packages.git "$software_ROOT/spack-packages"
spack repo add "$software_ROOT/spack-packages"
```

Check that Spack sees the packages:

```bash
spack repo list
spack info singular
spack info gpi-space
```

## Install Packages

Install Singular 4.3.0:

```bash
spack install singular@4.3.0
```

Install GPI-Space 26.3 on Linux:

```bash
spack install gpi-space@26.3
```

Install GPI-Space 26.3 on macOS:

```bash
spack install gpi-space@26.3~iml
```

Load an installed package before using it:

```bash
spack load singular@4.3.0
```

Other packages in this repository, such as `pfd-parallel`, can be installed in
the same way:

```bash
spack install pfd-parallel
spack load pfd-parallel
```

The first install may take a long time because Spack also builds dependencies.

## Uninstall Spack

Spack can be removed by deleting its checkout and user configuration. This is
destructive, so only do it when you really want to remove the installation:

```bash
# cd
# rm -rf "$software_ROOT/spack"
# rm -rf ~/.spack
```
