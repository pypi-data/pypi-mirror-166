# Bash completion for Pythons unittest

Running single test cases with the unittest module is a bit fiddly.
At least for me it often looks a bit like this:

I know that the test resides somewhere in the **tests** directory.
Therefore, I need to find the correct file: **tests/test_foo.py**.
But damn it! There are multiple test case classes in it.
But I only want to run one of them.
So I type: `python -m unittest tests.test_foo.SomeFancyTestCase`.
Now I notice that this test case has multiple methods and each method takes ages to complete.
But I only want to run this one test case that is repeatedly failing.
So I need to open the file in order to get the full method name.
Nice, the command now looks like this: `python -m unittest tests.test_foo.SomeFancyTestCase.test_a_specific_edge_case_with_a_long_name`
If I made a mistake during copy & paste I get an unhelpful error.

As long as running `python -m unittest discover` is sufficient this isn't a problem. But there are situations when this is not desired:

- the whole test suite takes a long time to complete
- some test cases do not run on my machine locally
- the application that is being tested is overly chatty and I only want logs regarding this one test case
- ...

Therefore, I created this little helper script to add Bash autocompletion.

## How does it work?

The program looks recursively for test case files matching the **test_*.py** pattern relative to the current working directory. It parses each file into an [abstract syntax tree AST](https://en.wikipedia.org/wiki/Abstract_syntax_tree) to offer completions for class names and/or method names.

The unittest module expects the identifier of a test case in the following format:

`<MODULE>.<TEST_CLASS>.<TEST_METHOD>`

where **<TEST_CLASS>** and **<TEST_METHOD>** are additional specifications to limit the number of executed tests. But these are optional.

Calling `unittest-autocomp` without any arguments will print all test case files relative to the current working dir:

```bash
$ unittest-autocomp
test.test_completions test.test_utils
```

Calling `unittest-autocomp` with a full path to a test case file will print all classes of this file:

```bash
$ unittest-autocomp test.test_completions.

test.test_completions.MethodnameCompletionTestCase test.test_completions.ClassnameCompletionTestCase test.test_completions.ModuleCompletionTestCase
```

(*The trailing dot is required, so that the program knows to search the file*)



Calling `unittest-autocomp` with a full path to a unittest class will print all test methods of that given class:

```bash
$ unittest-autocomp test.test_completions.MethodnameCompletionTestCase.


test.test_completions.MethodnameCompletionTestCase.test_completion_with_empty_partial test.test_completions.MethodnameCompletionTestCase.test_completion_with_only_folder_or_module test.test_completions.MethodnameCompletionTestCase.test_completion_with_missing_classname test.test_completions.MethodnameCompletionTestCase.test_completion_with_only_classname test.test_completions.MethodnameCompletionTestCase.test_completion_with_only_classname_and_half_method_name test.test_completions.MethodnameCompletionTestCase.test_completion_with_only_full_method_name
```
(*The trailing dot is required, so that the program knows to search the class for methods*)


## Installation?

1. Make sure **bash-completion** is installed:
   - `sudo apt install bash-completion`
2. Install this module:
   - `pip install unittest-autocomp`
3. Activate the completion:
   - paste the file: ./unittest-completion to **/etc/bash_completion.d**:
     - `sudo wget https://github.com/M0r13n/unittest-autocomp/blob/main/unittest-completion -P /etc/bash_completion.d`

By default this installation will yield completions for the command `python -m unittest`. If you invoke the unittest module otherwise you need to change the line `CMD="python -m unittest"` locally on your machine to match your invocation.
