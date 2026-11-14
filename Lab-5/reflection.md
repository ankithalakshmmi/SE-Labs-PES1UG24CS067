# Lab 5 – Reflection

**1. Which issues were the easiest to fix, and which were the hardest? Why?**

The easiest were the style issues from Flake8, such as missing blank lines and long lines, and Pylint's naming and docstring warnings. They were mechanical and didn't change how the program behaves. The hardest were the logic bugs that no tool reported. The program accepted seat 25 for a 20-seat show, accepted negative seats, and accepted "A7". It also treated user input "4" (a string) as different from seat 4 (an int). Fixing these meant understanding what the program is supposed to do and adding validation, not just following a tool message.

**2. Did the static analysis tools report any false positives? If so, describe one example.**

Not really a false positive, but Bandit's MD5 warning (B324) is context-dependent. Here the hash only generates a short ticket code, not a password or signature, so MD5 isn't a real security hole in this script. Switching to SHA-256 (or passing `usedforsecurity=False`) still made sense, because it removes the warning and avoids the code being copied into a security-sensitive context later. Pylint's warning about the `global` statement is also a design suggestion rather than a bug.

**3. How would you integrate static analysis tools into your actual software development workflow?**

I would run Flake8 and Pylint automatically through a pre-commit hook, so badly formatted code never gets committed, and enable them in VS Code so issues show while typing. In CI (e.g. GitHub Actions), I would run all three tools on every pull request and fail the build on Bandit high/medium issues or if the Pylint score drops below a set threshold. That way problems are caught before code review instead of after.

**4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?**

The Pylint score went from 5.87 to 10.00, Bandit went from 3 issues (2 High) to 0, and Flake8 went from 11 errors to 0. The program is more robust: invalid seats and unknown shows are rejected instead of being booked or crashing, files are always closed, logs no longer leak between calls through the mutable default argument, and the seat file is no longer world-writable. It is also more readable, with snake_case names, docstrings and f-strings, and the module can be imported without running `main()`. The main lesson is that tools catch a lot, but you still have to run the program and read its output to find logic bugs.
