During the interactive lectures of the OTC 2023 shore-based course, you will
need to install tools and libraries for reading, processing and visualizing
data.

Among these tools are the SEAScope viewer and the associated Python packages:
these instructions will only cover the installation of the Python packages as
the installation of the SEAScope viewer is already documented on the
`SEAScope website`_ and illustrated in `Youtube videos`_.

SEAScope Python packages depend on software components (shared libraries, other
Python packages, etc...) that may already be installed on your system but could
either be too old or too recent. Replacing these software components by a
version compatible with the SEAScope Python packages could break other
applications on your system, but keeping the currently installed versions would
prevent you from installing the SEAScope Python packages required for the
interactive lectures.
Fortunately, Python virtual environments come to our rescue!

A Python virtual environment is simply an isolated context where you will be
able to install Python packages without interfering with the software
components installed on your main system, thus avoiding the aforementioned
conflicts with other applications. You can think of it as a sandbox where you
can install and test Python things without breaking your system.

When you open a brand new terminal, the Python environment is the one installed
on your system (so, not a **virtual** environment) and the Python modules that
you import from a Python prompt are the same as the ones used by the
applications installed on your system.

On the other, when you open a new terminal and activate a Python virtual
environment (i.e. you are **in** the isolated context), the Python modules that
you import from a Python prompt come (almost) exclusively from packages that
you installed in the virtual environment (i.e. while the Python virtual
environment was active).


Requirements
============

- Latest version of the SEAScope viewer
- Python version 3.7 or above
- Network connection for downloading packages

To check the version installed on you system, you can open a terminal and type:

.. code:: bash

   python --version

Please note that if both Python 2 and Python 3 are installed on your system,
you may need to use ``python3`` instead of ``python``

If Python is not installed on your system:

- on Linux you should use the package manager that handles your system (apt,
  yum, pacman, ...).

- on macOS we recommend using `brew`_:

  .. code:: bash

     brew install python

- on Windows we recommend to install `Miniconda`_.

For macOS users there is an additional requirement: you need to install the
``proj`` software if it is not already available on your system. Here again we
recommend using `brew`_ for the installation:

.. code:: bash

   brew install proj

Installation
============

1. First you need to start the SEAScope viewer and leave it open so we can
   check that everything is working at the end of the installation process.

2. Next open a terminal where the ``python`` (or ``python3``) command is
   available.

   On Windows it could mean clicking on the `Anaconda Prompt` item in the
   applications list of Windows start menu.

3. Then you need to go to the directory that SEAScope uses as workspace using
   the ``cd`` (a.k.a. change directory) command.

   On Linux and on Windows, this is the directory named **seascope** that you
   extracted from the tar.gz or zip archive.

   On macOS, this is the **SEAScope-workspace** directory that can be found in
   your user's home.

4. Once you are inside the SEAScope workspace directory, list its content with
   the ``ls`` command (you might need to use ``dir`` instead on older versions
   of Windows).

   Make sure that the listing contains a subfolder named **colormaps** and a
   file named **state.db**. If they are not listed, then you are probably not
   in the expected directory and you should look for another location on your
   hard disk. Also please make sure that you started the SEAScope viewer (step
   1.) otherwise the workspace directory may not exist yet.

   Now that you are in the SEAScope workspace directory, you can use the
   following command to create a Python virtual environment named
   **otc2023_env** where we will install the packages that we need to interact
   with SEAScope:

   .. code:: bash

      python -m venv otc2023_env  # or python3

5. In order for packages to be installed **inside** the isolated context
   instead of the main system, we need to activate environment. To do so,
   execute the following command:

   - Linux and macOS

     .. code:: bash

        source otc2023_env/bin/activate

     If you are using ``csh``, use the following instead:

     .. code:: bash

        source otc2023_env/bin/activate.csh

   - Windows

     .. code:: Batch

       otc2023_env\Scripts\activate

   You should see that your terminal prompt now starts with **(otc2023_env)**.

      IMPORTANT
      During the interactive lectures based on SEAScope, make sure that your
      terminal prompt starts with this prefix otherwise it means that your are
      using your system environment instead of the isolated context: in that
      case execute the "activate" command (see 5. above) because following the
      SEAScope-based lectures while using the system environment will fail
      (Python packages impossible to import, missing commands, etc...).

6. Now that we are in the Python virtual environment, we can start to install
   new (or alternative versions of) packages without messing with the rest of
   the operating system.

   .. code:: bash

      python -m pip install --upgrade pip
      python -m pip install --upgrade setuptools
      python -m pip install SEAScope-env-OTC2023

   It should download and install many packages, make sure that there is no
   error message at the end. If it fails and you cannot fix the problem by
   yourself, please copy the error message and send it to us by email with as
   many details as possible (operating system, Python version, how you
   installed Python, etc...) at <support-otc2023@oceandatalab.com>.

7. Almost done! The last step is to check that everything is working correctly.
   All you need to do is to execute the following command while the SEAScope
   viewer is running (remember step 1.):

   .. code:: bash

      otc2023-check-environment

   It might take some time depending on your computer but at the end it should
   open a Jupyter notebook in your web browser. Please follow the instructions
   mentioned in the notebook to determine whether or not the tests were
   successful.

      In case the ``otc2023-check-environment`` command is not available
      although all the previous steps have been completed successfully, you
      may need to refresh the list of available executables by executing the
      ``rehash`` or ``hash`` command in your terminal on Linux.

8. Close the notebook in your web browser. You can also stop the SEAScope
   viewer and close your terminal.

   You're ready for the interactive lectures! :)

.. _SEAScope website: https://seascope.oceandatalab.com
.. _Youtube videos: https://youtube.com/playlist?list=PL_Nrq3gZvmM_C8baJBiNEzMjg0Hg7FIgK
.. _brew: https://brew.sh/
.. _Miniconda: https://docs.conda.io/en/latest/miniconda.html
