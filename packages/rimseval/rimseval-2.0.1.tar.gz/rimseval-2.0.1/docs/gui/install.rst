============
Installation
============

----------
Executable
----------

To install an executable file of the software on your computer,
download the latest release version for your operating system from
`the GitHub repository <https://github.com/RIMS-Code/RIMSEvalGUI/releases>`_.
You do not need to have an existing python environment,
since all dependencies will be installed along.

.. note:: Issues on macOS

    Once you moved the `RIMSEvaluation` program from the `dmg` archive
    into your `Applications` folder, your macOS might still tell you
    that when opening the program that it is damaged and needs to be
    moved to the trash.
    This happens since the program is not officially signed
    with a valid Apple ID account.
    More information can be found in
    `this issue <https://github.com/RIMS-Code/RIMSEvalGUI/issues/9>`_.
    To still use the `RIMSEvaluation` executable,
    open a terminal and run the following command:

    .. code-block::

        xattr -cr /Applications/RIMSEvaluation.app

    This assumes that the program is in fact installed into
    the main installation folder.
    If not, replace ``/Applications/`` with the path to the correct
    installation folder.
    The `RIMSEvaluation` software should now run.

--------
Anaconda
--------

++++++++++++++++++++++++++
Preapring your Environment
++++++++++++++++++++++++++

If you work with Anaconda3,
you should have the Anaconda Prompt installed on your system.
Open the Anaconda Prompt.
First, we want to set up a virtual environment to use
for the ``rimseval`` GUI.
In the Anaconda Prompt, type:

.. code-block:: shell-session

    conda create -n rimseval python=3.9
    conda activate rimseval

Next let's check if ``git`` is available. Type:

.. code-block:: shell-session

    git version

You should see the version of ``git`` that you have installed.
If you see an error saying that ``git`` was not found,
install it from the Anaconda Prompt via:

.. code-block:: shell-session

    conda install -c anaconda git

.. note:: If you do not have ``git`` installed system wide and install it
    according to the order above, it will only be installed in your virtual environment.
    This is fine, simply ensure that your virtual environment is activated
    in any of the steps below (which it should be anyway).

++++++++++++++++++++++
Installing RIMSEvalGUI
++++++++++++++++++++++

With the ``rimseval`` virtual environment activated,
move to a folder where you want to put the ``RIMSEvalGUI`` source code.
Then clone the GitHub repository by typing:

.. code-block:: shell-session

    git clone https://github.com/RIMS-Code/RIMSEvalGUI.git
    cd RIMSEvalGUI

The last command will enter the newly created folder.
Then install the necessary requirements by typing:

.. code-block:: shell-session

    pip install -r requirements.txt

If everything worked, you should be able to start the GUI
by typing:

.. code-block:: shell-session

    python RIMSEvalGUI.py

+++++++++++++++++++
Running RIMSEvalGUI
+++++++++++++++++++

If you start the Anaconda Prompt anew,
you can run the program the next time by first moving to your installation folder.
Then activate the virtual environment and run the python script.
The following gives a summary of the steps to run the ``RIMSEvalGUI``.
Note that the ``path_to_folder`` should be replaced with the folder
where the ``RIMSEvalGUI`` folder lies.

.. code-block:: shell-session

    cd path_to_folder/RIMSEvalGUI
    conda activate rimseval
    python RIMSEvalGUI.py

The GUI should start.
The Anaconda Prompt in the background will show you any warnings
and errors that the program throws.

++++++++++++++++++++++++++
Updating your installation
++++++++++++++++++++++++++

Updating your installation, e.g., when a new version comes out,
can be easily done with git.
The steps to do so are as following form the Anaconda Prompt.
We assume that you have already activated the ``rimseval`` virtual environment
and changed directory into the ``RIMSEvalGUI`` folder on your computer (see above).

.. code-block:: shell-session

    git pull
    pip install -r requirements.txt --upgrade

Now you can start the new GUI as described above.
Double check that the latest version is indeed displayed in the window title.

The above procedure gives you the latest development version.
If you rather prefer the latest version that was officially released,
check the releases
`here <https://github.com/RIMS-Code/RIMSEvalGUI/releases>`_.
Each release has a so-called tag associated with it,
which is equal to the version number of the release.
For example, to check out version ``v2.0.0`` and not go to the latest development version,
proceed as following:

.. code-block:: shell-session

    git pull
    git checkout tags/v2.0.0
    pip install -r requirements.txt --upgrade

To switch back to the main branch / latest development version,
you can simply type:

.. code-block:: shell-session

    git checkout main
    git pull
    git install -r requirements.txt --upgrade

.. note:: Newer versions of the GUI can depend on development versions
    of ``rimseval``. This means that you might see unexpected and wrong behavior.
    The packaging tool of the GUI does not allow for specifically labeling of such versions.
    Therefore, it is up to he user to ensure that you have the version that you like.
    New versions that depend on development versions of ``rimseval`` will always be labeled
    on GitHub as pre-releases. They will therefore not show up in the update reminder of the software.

------
Python
------

.. note:: If you are used to `git` and `python`, these instructions
    should work great for you.
    Otherwise, it might be recommendable that you install Anaconda
    and follow the instructions above.

To setup the RIMSEval GUI on regular python,
make sure that you have Python 3.9 installed installed.
Then create a virtual environment.
Instructions can, e.g., found
`here <https://devrav.com/blog/create-virtual-env-python>`_.

After activating your new virtual environment,
install the requirements by typing:

.. code-block:: shell-session

    pip install -r requirements

The RIMSEval GUI can then be started by typing:

.. code-block:: shell-session

    python RIMSEvalGUI.py

To update the RIMSEval GUI,
refresh the folder from github and then upgrade the dependencies.
From the shell you can accomplish this from within the RIMSEvalGUI folder,
assuming you have initially cloned the folder from GitHub:

.. code-block:: shell-session

    git pull
    pip install -r requirements.txt --upgrade
