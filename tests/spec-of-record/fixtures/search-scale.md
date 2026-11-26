**Records:**
  - **Fixture:** measure-a-search-by-meaning \
    **Holds:** a Python program taking the folder of the search's code, a project's root, a scratch folder, a JSON file of texts by path and a number of copies; it writes that many copies of the texts under the root, each copy's files under a folder of its own and each file followed by a sentence naming its copy and its path, searches them by meaning once, and prints the vectors the index then holds and the most memory the process held, in GB, as the system counts it \
    **Snippet:**

      ```python
      import ctypes
      import json
      import os
      import sys
      from pathlib import Path

      sys.path.insert(0, sys.argv[1])
      import search

      root, scratch, texts, copies = Path(sys.argv[2]), Path(sys.argv[3]), json.loads(Path(sys.argv[4]).read_text(encoding="utf-8")), int(sys.argv[5])


      def most_memory():
          if os.name == "nt":
              from ctypes import wintypes

              class Counters(ctypes.Structure):
                  _fields_ = [("cb", wintypes.DWORD), ("PageFaultCount", wintypes.DWORD)] + [(n, ctypes.c_size_t) for n in (
                      "PeakWorkingSetSize", "WorkingSetSize", "QuotaPeakPagedPoolUsage", "QuotaPagedPoolUsage", "QuotaPeakNonPagedPoolUsage",
                      "QuotaNonPagedPoolUsage", "PagefileUsage", "PeakPagefileUsage")]

              counters = Counters()
              counters.cb = ctypes.sizeof(counters)
              ctypes.windll.kernel32.GetCurrentProcess.restype = wintypes.HANDLE
              ctypes.windll.psapi.GetProcessMemoryInfo.argtypes = [wintypes.HANDLE, ctypes.POINTER(Counters), wintypes.DWORD]
              ctypes.windll.psapi.GetProcessMemoryInfo(ctypes.windll.kernel32.GetCurrentProcess(), ctypes.byref(counters), counters.cb)
              return counters.PeakWorkingSetSize / 2 ** 30
          import resource
          held = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
          return held / (2 ** 30 if sys.platform == "darwin" else 2 ** 20)


      cover = []
      for copy in range(copies):
          for path, text in texts.items():
              placed = root / f"c{copy}" / path
              placed.parent.mkdir(parents=True, exist_ok=True)
              placed.write_text(text + f"\nThis sentence stands in copy {copy} of {path} alone, so no two copies hold the same content.\n", encoding="utf-8", newline="\n")
              cover.append(f"c{copy}/{path}")
      found = search.Search(root, cover=cover, scratch=scratch, quiet=True)
      found.meaning("A book that is out on loan may be kept longer only when no one else has asked for it.")
      print(found.db.execute("select count(*) from embeddings").fetchone()[0], f"{most_memory():.3f}")
      found.db.close()
      ```
