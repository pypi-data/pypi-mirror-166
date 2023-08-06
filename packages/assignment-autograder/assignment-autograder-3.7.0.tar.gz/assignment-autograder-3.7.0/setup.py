# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autograder',
 'autograder.plagiarism_detection',
 'autograder.plagiarism_detection.lexers',
 'autograder.plagiarism_detection.test.java.decaf2many',
 'autograder.plagiarism_detection.test.java.decaf2many.decaf2many',
 'autograder.plagiarism_detection.test.java.decaf2many.decaf2many.lang',
 'autograder.plagiarism_detection.test.java.decaf2many.tests',
 'autograder.plagiarism_detection.test.java.decaf2many.tests.expected',
 'autograder.testcase_types.cpython',
 'autograder.testcase_types.cpython.helpers',
 'autograder.testcase_types.cpython.templates',
 'autograder.testcase_types.gcc',
 'autograder.testcase_types.javac',
 'autograder.testcase_utils']

package_data = \
{'': ['*'],
 'autograder.plagiarism_detection': ['test/java/*'],
 'autograder.plagiarism_detection.test.java.decaf2many': ['.git/*',
                                                          '.git/hooks/*',
                                                          '.git/info/*',
                                                          '.git/logs/*',
                                                          '.git/logs/refs/heads/*',
                                                          '.git/logs/refs/remotes/origin/*',
                                                          '.git/objects/pack/*',
                                                          '.git/refs/heads/*',
                                                          '.git/refs/remotes/origin/*',
                                                          '.github/*',
                                                          '.github/workflows/*',
                                                          'decaf2many.egg-info/*'],
 'autograder.plagiarism_detection.test.java.decaf2many.tests': ['cases/*'],
 'autograder.testcase_types.gcc': ['c++_templates/*',
                                   'c_templates/*',
                                   'helpers/*',
                                   'memleak/*'],
 'autograder.testcase_types.javac': ['extra/*', 'helpers/*', 'templates/*']}

install_requires = \
['antlr4-python3-runtime==4.9.2',
 'numba>=0.56.2,<0.57.0',
 'numpy>=1.22.4,<2.0.0',
 'tomlkit>=0.11.4,<0.12.0']

entry_points = \
{'console_scripts': ['autograder = autograder.__main__:main']}

setup_kwargs = {
    'name': 'assignment-autograder',
    'version': '3.7.0',
    'description': 'Automatic assignment grading for instructor use in programming courses',
    'long_description': 'This utility aims to provide a simple, yet secure and highly configurable way to autograde programming assignments.\n\nI consider it to be finished. Autograder has been tested on a real university class with hundreds of students and has shown to be error-less (in terms of grades), fast, and protected from cheating.\n\n#### Note\nIf you wish to use autograder as a professor/student, configuring and running it through [GUI](https://github.com/Ovsyanka83/autograder_gui) is recommended -- it\'s a lot simpler, just as fast, and just as versatile.\n\nThe command line utility is intended for advanced use cases (extending autograder, grading on a server, or integrating it as a part of a larger utility/app)\n\n#### Table of Contents  \n[Features](#Features)  \n[Platform Support](#Platform-Support)  \n[Installation](#Installation)   \n[Supported Programming Languages](#Supported-Programming-Languages)   \n[Quickstart](#Quickstart)   \n[Usage](#Usage)   \n[Writing testcases](#Writing-testcases)  \n[Helper functions](#Helper-functions)  \n[Limitations](#Limitations)   \n[Anti Cheating](#Anti-Cheating)   \n[Adding Programming Languages](#Adding-Programming-Languages)\n# Features\n* Blazingly fast (can grade hundreads of submissions using dozens of testcases in a few minutes. Seconds if grading python)\n* [Easy to grade](#Usage) \n* [Easy-to-write testcases](#Writing-testcases)  \n* Testcase grade can be based on [student\'s stdout](#Helper-functions)\n* Can grade C, C++, Java, and Python code in regular mode\n* Can grade any programming language in stdout-only mode\n* A file with testcase grades and details can be generated for each student\n* You can customize the total points for the assignment, maximum running time of student\'s program, file names to be considered for grading, formatters for checking student stdout, and [so much more](https://github.com/Ovsyanka83/autograder/blob/master/autograder/default_config.toml).\n* [Anti Cheating capabilities](#Anti-Cheating) that make it nearly impossible for students to cheat\n* Grading submissions in multiple programming languages at once\n* JSON result output supported if autograder needs to be integrated as a part of a larger utility\n* Can check submissions for similarity (plagiarism)\n* Can detect and report memory leaks in C/C++ code\n# Platform Support\n* Linux is fully supported\n* OS X is fully supported\n* Windows is partially supported:\n  * Stdout-testcases that require shebang lines are not and cannot be supported\n# Installation\n* Currently Python >= 3.7 is necessary.\n* Run `pip install assignment-autograder`\n* If you want to update to a newer version, run `pip install -U --no-cache-dir assignment-autograder`\n* To grade various programming languages, you\'d need to install:\n  * `gcc`/`clang` for C/C++ support\n  * `Java JDK` for java support\n  * `make` for compiled stdout-only testcase support\n  * Any interpreter/compiler necessary to run stdout-only testcases. For example, testcases with ruby in their shebang lines will require the ruby interpreter\n# Supported Programming Languages\n* Java\n* C\n* C++\n* CPython (3.6-3.9)\n* Any programming language if stdout-only grading is used\n# Quickstart\n* Run `autograder guide path/to/directory/you\'d/like/to/grade`. The guide will create all of the necessary configurations and directories for grading and will explain how to grade.\n* Read [Usage](#Usage) section\n# Usage\n1) Create tests directory in the same directory as student submissions. Its structure is shown in [examples](https://github.com/Ovsyanka83/autograder/tree/master/examples). (can be automatically created using [--guide](#Quickstart))\n1) __Optional__ files that can be automatically created by [--guide](#Quickstart) CLI option and whose use is demostrated by [examples](https://github.com/Ovsyanka83/autograder/tree/master/examples):\n    1) Input (stdin) and expected output (__stdout__) text files in their respective directories for each testcase. If a test does not require input and/or stdout, the respective text file is also not required.\n    1) Create [config.ini](https://github.com/Ovsyanka83/autograder/blob/master/autograder/default_config.toml) and change configuration to fit your needs (If you do not include some fields, autograder will use the respective fields from default_config.ini)\n    1) Create [stdout_formatters.py](https://github.com/Ovsyanka83/autograder/blob/master/autograder/default_stdout_formatters.py) and edit it to fit your needs. They will format student\'s stdout to allow you to give credit to students even if their stdout is not exactly the same as expected.\n1) Write testcases as described [below](#Writing-testcases) using [examples](https://github.com/Ovsyanka83/autograder/tree/master/examples) as reference.\n1) Run `autograder run path/to/submissions/dir` from command line.\n## Writing testcases\n* Write a main that follows the same structure as one of the examples in your programming language. The main should usually call student\'s code, check its result, and call one of the helper functions (when working with stdout, you don\'t check the result, and simply allow autograder to handle grading by calling CHECK_STDOUT())\n* Assume that student\'s code is available in your namespace. Examples demonstrate exactly how to call students\' functions.\n* Assume that helper functions (decribed below) are predefined and use them to return student scores to the grader\n* Each helper function prints the student\'s score, __validation string__, terminates the execution of the program and returns its respective exit code that signifies to autograder if the testcase ended in a result, cheating attempt, or if stdout checking is necessary.\n* Each testcase is graded out of 100% and each grade is a 64bit double precision floating point number, which means that you can fully control how much partial credit is given in non-stdout checking tests.\n### Helper functions\n  * CHECK_STDOUT() indicates that we do not check student\'s return values for the testcase and that we only care about their output (__stdout__) that will be checked by the autograder automatically using student\'s stdout and the output files with the same name stem as the testcase. (beware: printing anything within your testcase can break this functionality)\n  * RESULT(double r) returns student\'s score r back to the grader (0 - 100)\n  * PASS() returns the score of 100% back to the grader and is equivalent to RESULT(100)\n  * FAIL() returns the score of 0% back to the grader and is equivalent to RESULT(0)\n## Limitations\n* At the point of writing this readme, stdout checking is a PASS or FAIL process (i.e. no partial credit possible). The reason is that allowing for \'partial similarity\' of outputs is too error-prone and could yield too many points for students that did not actually complete the task properly. If you want to increase the chances of students\' stdout matching, you should use stdout formatters described [above](#Usage).\n* If you don\'t prototype student functions you want to test in your C/C++ testcases, you will run into undefined behavior because of how C and C++ handle linking.\n* __Student\'s main functions ARE NOT meant to be accessed because testcase must be the starting point of the program.__ They are, however, accessible if necessary in C/C++ as \\_\\_student_main\\_\\_.\n## Anti Cheating\nOne of the main weaknesses of automatic grading is how prone it is to cheating. Autograder tries to solve this problem with methods described in this section. Currently, (as far as I\'ve read and tested), it is impossible to cheat autograder. However, Java might still have some weird ways of doing this but there are protections against all of the most popular scenarios (decompiling and parsing testcases, using System.exit, trying to read security key from environment variables, using reflection to use private members of the test helper)\n* To restrict the student from exiting the process himself and printing the grade of his/her choice, I validate testcase stdout using a pseudorandom key called __validation string__. Autograder gives the string to the testcase as an environment variable which is erased right after the testcase saves it, and then it is automatically printed on the last line of stdout before the testcase exits. The autograder, then, pops it from stdout and verifies that it is the same string it sent. If it is not, the student will get the respective error message and a 0 on the testcase.\n* To prevent students from simply importing the string from the testcase file, test helper files (described above) all have some way of disallowing imports. For C/C++, it is the static identifier, for Java, it is the private method modifiers and automatic testcase fail if reflection is detected, for python it is throwing an error and deleting the validation string if \\_\\_name\\_\\_ != "\\_\\_main\\_\\_". I assume that similar precautions can be implemented in almost any language.\n* Simply parsing validating string from the testcase file is impossible because it is passed at runtime.\n* As an additional (and maybe unnecessary) security measure, autograder precompiles testcases without linking for all languages except for java, thus decreasing the possibility that the student will simply parse the testcase file and figure out the correct return values if the security measure above doesn\'t work.\n\n# Adding Programming Languages\n* If you want to add a new language for grading, you have to:\n  1. Create a new directory in autograder/testcase_types/\n  2. Create a python module in that directory that contains a subclass of TestCase (from autograder/testcase_utils/abstract_testcase.py)\n  3. Create a helpers directory and write your test helper\n  4. Optionally, add the extra (extra files to be available to each testcase) and templates (examples of testcases written using the new language) directories\n* Use the other testcase subclasses and test helpers as reference\n* This point is optional but if you want full anti-cheating capabilities for your new language, you will need to consider three things:\n              \n  * Does your language support getting and unsetting environment variables? It is required to save validating string in your code without leaking it to students.\n  * Does your language support private-to-file functions/classes/methods/variables? It is required to prevent the student from simply importing helper functions and/or the validating string.\n  * Does your language support precompilation (conversion to bytecode without linking)? It is not as important as other points but could speed up grading and hide testcase code from students. \n* You can extend many other capabilities of autograder using new testcase types. For example, C testcase type adds memory leak detection on its own for both C and C++ testcases.',
    'author': 'Ovsyanka',
    'author_email': 'szmiev2000@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Ovsyanka83/autograder',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
