**Records:**
  - **Fixture:** stand-in-design-script \
    **Holds:** a Python module standing in for a design script: a tuple FLAGS of one action, `--check-status`, taking a design, which prints the design's Status line after the word its project's file `specs/status-form.md` gives on its first line, and a main taking the arguments and a plans folder that runs the action a flag names \
    **Snippet:**

      ```python
      """A stand-in for a design script: one action reading a design, by a word the form beside its own code gives."""
      from pathlib import Path


      def check_status(value):
          word = (Path("specs/status-form.md").read_text(encoding="utf-8").split("\n") or ["Status"])[0].strip()
          lines = Path(value).read_text(encoding="utf-8").split("\n")
          status = next((l for l in lines if l.startswith("**Status:**")), "no status").rstrip(" \\")
          print("== check-status\n%s %s" % (word, status))
          return 0


      FLAGS = (("--check-status", "DESIGN", check_status, "print a design's Status"),)


      def main(argv, plans=None):
          for flag, _, run, _ in FLAGS:
              if argv[1] == flag:
                  return run(argv[2])
          return 2
      ```

  - **Fixture:** stand-in-design-script-marking-approval \
    **Holds:** a Python module standing in for a design script, as the stand-in of one action `--check-status` holds it, but printing the Status line of a design approved in capitals \
    **Snippet:**

      ```python
      """A stand-in for a design script: one action reading a design, by a word the form beside its own code gives."""
      from pathlib import Path


      def check_status(value):
          word = (Path("specs/status-form.md").read_text(encoding="utf-8").split("\n") or ["Status"])[0].strip()
          lines = Path(value).read_text(encoding="utf-8").split("\n")
          status = next((l for l in lines if l.startswith("**Status:**")), "no status").rstrip(" \\")
          print("== check-status\n%s %s" % (word, status.upper() if "approved" in status else status))
          return 0


      FLAGS = (("--check-status", "DESIGN", check_status, "print a design's Status"),)


      def main(argv, plans=None):
          for flag, _, run, _ in FLAGS:
              if argv[1] == flag:
                  return run(argv[2])
          return 2
      ```

  - **Fixture:** status-form \
    **Holds:** a line of one word, Status \
    **Snippet:**

      ```markdown
      Status
      ```

  - **Fixture:** status-form-renamed \
    **Holds:** a line of one word, State \
    **Snippet:**

      ```markdown
      State
      ```
