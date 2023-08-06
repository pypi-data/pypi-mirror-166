=============================
Pyalmanac Project Description
=============================

.. |nbsp| unicode:: 0xA0
   :trim:

.. |emsp| unicode:: U+2003
   :trim:

Pyalmanac is a **Python 3** script that creates the daily pages of the Nautical Almanac using the UTC timescale,
which is the basis for the worldwide system of civil time. Official Nautical Almanacs employ a UT timescale (equivalent to UT1).

The 'daily pages' are tables that are needed for celestial navigation with a sextant.
Although you are strongly advised to purchase the official Nautical Almanac, this program will reproduce the tables with no warranty or guarantee of accuracy.

Pyalmanac was developed based on the original *Pyalmanac* by Enno Rodegerdts. Various improvements, enhancements and bugfixes have been added since.

This is the **PyPI edition** of `Pyalmanac-Py3 <https://github.com/aendie/Pyalmanac-Py3>`_ (a Changelog can be viewed here).
Version numbering follows the scheme *Major.Minor.Patch*, whereby the *Patch* number represents some small correction to the intended release.

| **NOTE:** Version numbering in PyPI restarted from 1.0 as the previous well-tested versions that exist since early 2019 were never published in PyPI.

Current state of Pyalmanac
--------------------------

Pyalmanac is a somewhat dated program.
Pyalmanac is implemented using the `Ephem <https://rhodesmill.org/pyephem/>`_ astronomical library (originally named PyEphem), which has *Mature* development status.
Ephem was based upon XEphem, which is 'end of life' as no further updates to XEphem are planned.
Elwood Charles Downey, the author of XEphem, generously gave permission for their use in (Py)Ephem.

| **Please note the Software Requirements below for Ephem as the latest versions still contain a software error!**

Pyalmanac contains its own star database, now updated with data from the Hipparcos Star Catalogue.
Star names are chosen to comply with official Nautical Almanacs.
The GHA/Dec star data now matches a sample page from a Nautical Almanac typically to within 0°0.1'.
As of now, (Py)Ephem will continue to receive critical bugfixes and be ported to each new version of Python.
Pyalmanac still has the advantage of speed over other implementations.

One minor limitation of Ephem is in the EOP (Earth Orientation Parameters) (affecting *sidereal time*) which is more accurate in Skyfield-based almanacs as they can employ the IERS (International Earth Rotation Service) EOP published data. This affects *sidereal time*, which minimizes GHA discrepancies (for all celestial objects) in general.

Given the choice, `SFalmanac <https://pypi.org/project/sfalmanac/>`_ is an up-to-date program with more enhanced functionality compared to Pyalmanac, and it uses `Skyfield <https://rhodesmill.org/skyfield/>`_, a modern astronomical library based on the highly accurate algorithms employed in the `NASA JPL HORIZONS System <https://ssd.jpl.nasa.gov/horizons/>`_.
(Pyalmanac and SFalmanac have same formatted pages so differences can easily be spotted by swiching between them in Adobe Acrobat Reader.)

Software Requirements
=====================

|
| Astronomical computation is done by the free Ephem library.
| Typesetting is done typically by MiKTeX or TeX Live.
| These need to be installed:

* `python <https://www.python.org/downloads/>`_ >= 3.4 (the latest version is recommended)
* `ephem <https://pypi.org/project/ephem/>`__ >= 3.7.6 (4.1 is good; 4.1.1, 4.1.2 and 4.1.3 are faulty)
* `MiKTeX <https://miktex.org/>`_ |nbsp| |nbsp| or |nbsp| |nbsp| `TeX Live <http://www.tug.org/texlive/>`_

The fault with ``Ephem 4.1.1, 4.1.2 or 4.1.3`` is an `Endless loop in computing moon rise/set <https://github.com/brandon-rhodes/pyephem/issues/232>`_

Installation
============

Install a TeX/LaTeX program on your operating system so that 'pdflatex' is available.

Ensure that the `pip Python installer tool <https://pip.pypa.io/en/latest/installation/>`_ is installed.
Then ensure that old versions of PyEphem, Ephem and Pyalmanac are not installed before installing SkyAlmanac from PyPI::

  python -m pip uninstall pyephem ephem pyalmanac
  python -m pip install pyalmanac

Thereafter run it with::

  python -m pyalmanac

On a POSIX system (Linux or Mac OS), use ``python3`` instead of ``python`` above.

This PyPI edition also supports installing and running in a `venv <https://docs.python.org/3/library/venv.html>`_ virtual environment.
Finally check or change the settings in ``config.py``.
It's location is printed immediately whenever Pyalmanac runs.

Guidelines for Linux & Mac OS
-----------------------------

Quote from `Chris Johnson <https://stackoverflow.com/users/763269/chris-johnson>`_:

It's best to not use the system-provided Python directly. Leave that one alone since the OS can change it in undesired ways.

The best practice is to configure your own Python version(s) and manage them on a per-project basis using ``venv`` (for Python 3). This eliminates all dependency on the system-provided Python version, and also isolates each project from other projects on the machine.

Each project can have a different Python point version if needed, and gets its own ``site_packages`` directory so pip-installed libraries can also have different versions by project. This approach is a major problem-avoider.

Troubleshooting
---------------

If using MiKTeX 21 or higher, executing 'option 7' (Increments and Corrections) it will probably fail with::

    ! TeX capacity exceeded, sorry [main memory size=3000000].

To resolve this problem (assuming MiKTeX has been installed for all users),
open a Command Prompt as Administrator and enter: ::

    initexmf --admin --edit-config-file=pdflatex

This opens pdflatex.ini in Notepad. Add the following line: ::

    extra_mem_top = 1000000

and save the file. Problem solved. For more details look `here <https://tex.stackexchange.com/questions/438902/how-to-increase-memory-size-for-xelatex-in-miktex/438911#438911>`_.