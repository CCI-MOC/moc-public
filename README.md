# Massachusetts Open Cloud Public Repository

This repository contains some tools and other files we find useful at
the MOC. Here is a brief tour:

* `attic` - old stuff, much of it disorganized. Some of it isn't
  completely irrelevant, but most of it has some bit-rot.
* `ks.cfg` - a kickstart file which we use to image compute nodes for the
  [mocpoc-head][1] cluster.
* `puppet-modules` - puppet modules we've written. Most of this is very
  experimental, much of it doesn't work yet at all.
* `python-mocutils` - Various tools written in python, including power
  cycle scripts for our test clusters' compute nodes, and the SPL. This
  directory needs some reorganization. If you decide to take this on,
  please update this README when you're done as well.

[1]: https://github.com/CCI-MOC/moc-public/wiki/MOCPOC-Nomenclature
