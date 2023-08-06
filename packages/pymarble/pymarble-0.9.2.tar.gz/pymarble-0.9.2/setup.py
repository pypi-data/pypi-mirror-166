# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymarble',
 'pymarble.backend',
 'pymarble.frontend',
 'pymarble.frontend.static',
 'pymarble.frontend.view']

package_data = \
{'': ['*'], 'pymarble.frontend.static': ['images/*']}

install_requires = \
['PyQt5>=5.15.6,<6.0.0',
 'h5py>=3.6.0,<4.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'pandas>=1.4.1,<2.0.0',
 'prettytable>=3.2.0,<4.0.0',
 'sortedcontainers>=2.4.0,<3.0.0']

entry_points = \
{'console_scripts': ['marble-cli = pymarble.rff:main',
                     'marble-gui = pymarble.frontend.app:main']}

setup_kwargs = {
    'name': 'pymarble',
    'version': '0.9.2',
    'description': 'Scientific instruments produce proprietary binary data that contains a multitude of primary and metadata. This project aims to create a software that supports the domain scientist in deciphering this data and metadata as well as taking full advantage of all instrument measurements.',
    'long_description': '# Documentation on software for deciphering proprietary binary data-files\nScientific instruments produce proprietary binary data that contains a multitude of primary and metadata. This project aims to create a software that supports the domain scientist in deciphering this data and metadata as well as taking full advantage of all instrument measurements.\n\nMARBLE is open und free software and can be found at a [Repository](https://jugit.fz-juelich.de/marble)\n\n## Contributors\n- Steffen Brinckmann (IEK-2, FZJ) [Principal investigator]\n- Volker Hofmann (IAS-9 and HMC, FZJ)\n- Fiona D.Mello (IAS-9 and HMC, FZJ)\n\n## Introduction into proprietary binary data-files and MARBLE\n\nAll data in all files is stored sequential, similar to a book in which chapters are sequential. In proprietary binary files, the **sections** can have very different lengths: some section only contains the name of the operator while another section contains thousands of temperature values. These files are called **binary** because they are not human readable but are a list of 1s and 0s and they are called **proprietary** because the instrument vendor has designed them particularly for this company or even instrument. As such, these files cannot be deciphered manually and MARBLE supports the scientist in this task.\n\nMARBLE reads the proprietary binary files and - with the help of the scientist - outputs a **python converter**. This python converter can then be used to translate all proprietary binary files from this instrument into an hdf5-file format, which can be easily read by any computer language. The python converter also acts as verification tool: if a binary file A can be converted by this specific converter, then this file A comes from this instrument. This verification ability is helpful in finding files from a particular instrument.\n\nIn MARBLE, data in proprietary binary files is grouped into classes:\n- **Metadata** is data that describes the experiment. Examples are the name of the operator, the instrument vendor, the start time of the experiment. This metadata is commonly stored in **key-value-pairs**. For instance, "operator" is the key and "Peter Smith" is the value as both form an inseparable pair. Generally, the first parts of proprietary binary files contain lots of metadata.\n- **Primary data** is the data that the operator wanted to measure and this primary data has a form of a list. Lets say we want to measure the temperature at our house every 1min and store this information; then temperature is a primary data and stored in a long list. Generally, the instrument also saves the time increment after the measurement start and stores these time increments in a separate list, which is also primary data. Primary data can be of two types floating point numbers with normal or high precision.\n- **Undefined** sections are those sections of the file which the scientist and MARBLE have not identified yet. Some of these sections might be important or unimportant. Unimportant sections are those where the programmer at the instrument vendor was lazy and did included garbage or empty space. These might also be linked to specific languages the instrument vendor used for programming.\n\n## How to install MARBLE\nCertain versions of MARBLE will be uploaded to the pypi repository and one can install MARBLE with\n``` bash\npip install pymarble\n```\n\nAlternatively, MARBLE is under development and one can install the latest version by following these steps in a terminal.\n``` bash\ncd <new directory>\ngit pull https://jugit.fz-juelich.de/marble/software.git\ncd software\npoetry shell\n```\n\nTo start graphical user interface (GUI), run the following command in the terminal:\n``` bash\nmarble-gui\n```\n\n## How to use the GUI\n1. Open file by using the first button. File opening takes some time for large files as the file content is automatically analysed.\n1. After automatic analysis, there are lots of undefined sections and it is good to filter these sections out by presssing the filter button (one but last button).\n1. Now go through the sections and label them by entering a "key" and "unit" where applicable\n   - Use the "draw" button for primary data, aka lists, because it helps you to identify them.\n   - If you want that the converter uses certain data, ensure that the "important" checkbox is ticked.\n   - For keeping track of your own progress, you can use the "certainty" traffic-light. If you are unsure use red, medium-sure is yellow and very sure is green.\n1. Especially, for primary data, you can move the beginning and end of a section by clicking the up-down-button and then changing the start and length of the section. This dialog is aware of the binary structure and helps the user make sensible changes.\n1. Once you are done, click the save button (last one) to save a python converter into the directory of the proprietary binary file that you analysed.\n1. Go into the directory and use python converter to convert all files from this instrument by executing the command "python <converter.py> <proprietary_binary_file.dat>". You can add the "-v" option to the command to make the converter more verbose during tranlation. If all the conversions are successful, you deciphered this proprietary binary file successfully.\n\n## How to use the command line interface (CLI)\n``` bash\nmarble-cli\n```\nThere is a number of tutorials for the CLI:\n- [Tensile machine](https://jugit.fz-juelich.de/marble/software/-/raw/main/tests/tutorial_05mvl.sh)\n- [Tensile machine, large file](https://jugit.fz-juelich.de/marble/software/-/raw/main/tests/tutorial_08mvl.sh)\n- [Image data](https://jugit.fz-juelich.de/marble/software/-/raw/main/tests/tutorial_emi.sh)\n- [Data of multiple tests in one file](https://jugit.fz-juelich.de/marble/software/-/raw/main/tests/tutorial_idr.sh)\n- [Tensile machine from above but larger file, that coincidentally requires more understanding](https://jugit.fz-juelich.de/marble/software/-/raw/main/tests/tutorial_08mvl.sh)\n\nYou can read them and follow those commands. Howevery, you can also just execute them with the argument "m", without the quotation marks.\nAll of these tutorials are in the form of linux scripts, which are used for verification of the code at each development step.\n\n## Future features\n1. Add a GUI indicator that primary section has a count & shape property\n1. Change GUI to allow multiple tests in one file\n1. GUI for file-type metadata: instrument, software\n   - More metadata from user (more than instrument, software) key-values\n1. Change GUI and backend to identify/check images in files\n1. Directly push translater to repository\n1. Use the comparison of files to identify more metadata\n   - ensure that the python import works by doing a diff of present and imported data\n',
    'author': 'Steffen Brinckmann',
    'author_email': 'sbrinckm@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
