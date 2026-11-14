# Lab 5 – Issues Found in `theater_system.py`

Before: Pylint 5.87/10, Bandit 3 issues (2 High, 1 Low), Flake8 11 issues.
After: Pylint 10.00/10, Bandit 0 issues, Flake8 0 issues.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Insecure file permissions (Bandit B103) | Security – High | 55 | `os.chmod("seats.json", 0o777)` makes the file world-writable and executable | Changed to `0o600` (owner read/write only) |
| Weak hash MD5 (Bandit B324) | Security – High | 25 | MD5 is broken and flagged for security use | Replaced with `hashlib.sha256` |
| Try/except/pass + bare except (Bandit B110, Pylint W0702, Flake8 E722) | Bug / Security – Low | 19–22 | Bare `except: pass` swallows every error, incl. typos and KeyboardInterrupt | Catch only `KeyError, ValueError`; return False so the caller knows it failed |
| Mutable default argument (Pylint W0102) | Bug – Medium | 9 | `system_logs=[]` is shared across all calls, so logs leak between calls | Default to `None`, create a new list inside |
| No seat validation (logic bug, no tool flags it) | Bug – High | 9–16 | Seats 25 (show has 20), -1 and "A7" are all accepted; unknown show_id crashes with KeyError | Added `_valid_seat()` check: show exists, seat is int, 1 ≤ seat ≤ capacity |
| String vs int seat from `input()` (logic bug) | Bug – Medium | 50–51 | User input stored as `"4"`, so seat `4` and `"4"` can both be booked | Convert with `int()`, handle `ValueError` |
| Files opened without `with`/encoding (Pylint R1732, W1514) | Bug – Medium | 28, 33 | File in `dump_reservations` is never closed; no encoding given | Use `with open(..., encoding="utf-8")` and `json.dump/json.load` |
| `global` statement (Pylint W0603) | Quality – Low | 32 | Reassigning the global dict | Update dict in place with `shows.clear(); shows.update(data)` |
| Code runs on import | Quality – Low | 57 | `main()` executes when the module is imported | Wrapped in `if __name__ == "__main__":` |
| Naming (Pylint C0103) | Style | 37 | `printSeatingSummary` is not snake_case | Renamed to `print_seating_summary` |
| Missing docstrings (Pylint C0114/C0116) | Style | 1, all functions | No module/function docstrings | Added docstrings |
| `%` formatting (Pylint C0209) | Style | 12, 15 | Old-style formatting | Switched to f-strings |
| Blank lines (Flake8 E302/E305) | Style | 9–57 | Need 2 blank lines around top-level defs | Added blank lines |
| Line too long (Flake8 E501, Pylint C0301) | Style | 12, 40 | Lines over 79 chars | Split lines |
