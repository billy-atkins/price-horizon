**Records:**
  - **Fixture:** python-without-fastembed \
    **Holds:** a Python site customization, loaded by an interpreter that finds it on its path under the name `sitecustomize.py`, after which the module fastembed is found by no import in that process \
    **Snippet:**

      ```python
      import sys

      sys.modules["fastembed"] = None
      ```
