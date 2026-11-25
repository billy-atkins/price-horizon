"""Scale: what a run after one changed file costs, and the memory building an index holds, on a body of files and on
ten times as many. The files are copies of the invented library, each copy's files holding a sentence of their own,
so ten times the copies give ten times the lines, the citations and the passages. The test takes minutes."""
import json
import subprocess
import sys
import time

import pytest

COPIES = (20, 200)   # the copies of the library's ten files each index is built over
MEMORY_BOUND = 1.0   # GB: the model and its working memory, with room, whatever the count of files

# Builds the whole index of the files a listing names and prints the seconds it took and the most memory the process
# held, in GB, as the system counts it. It is run as a process of its own, since the most memory a process held never
# falls again and the process running the tests has held other indexes before.
BUILD = r'''
import ctypes, json, os, sys, time
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import search


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
    return held / (2 ** 30 if sys.platform == "darwin" else 2 ** 20)  # bytes on macOS, kilobytes elsewhere


started = time.perf_counter()
search.Search(Path(sys.argv[2]), cover=json.loads(Path(sys.argv[4]).read_text(encoding="utf-8")), scratch=Path(sys.argv[3]), quiet=True).db.close()
print(f"{time.perf_counter() - started:.1f} {most_memory():.3f}")
'''


@pytest.mark.action("--show-citers")
@pytest.mark.passes
@pytest.mark.reads("search-library-lending.md", "library-membership", "library-loans", "library-overdue", "library-holds", "library-catalogue")
@pytest.mark.reads("search-library-premises.md", "library-donations", "library-opening", "library-volunteers", "library-rooms", "library-events")
def test_a_run_after_one_changed_file_costs_no_more_on_ten_times_the_files(fixtures, tools, search, opened, checkout, work, check):
    times, memory = {}, {}
    for copies in COPIES:
        root, scratch, cover = work / f"files-{copies}", work / f"index-{copies}", []
        for c in range(copies):
            for key, rel in tools.LIBRARY.items():
                # the test's variant of each fixture: a sentence of the copy's own added, so no two copies hold the
                # same content and each copy's content is the index's own to hold
                tools.put(root, f"c{c}/{rel}", fixtures[key] + f"\nThis sentence stands in copy {c} of {rel} alone, so no two copies hold the same content.\n")
                cover.append(f"c{c}/{rel}")
        listing = work / f"cover-{copies}.json"
        listing.write_text(json.dumps(cover), encoding="utf-8")
        built = subprocess.run([sys.executable, "-B", "-c", BUILD, str(checkout / ".ai" / "skills" / "lib"), str(root), str(scratch), str(listing)], capture_output=True, text=True, encoding="utf-8")
        assert built.returncode == 0, built.stderr
        seconds, memory[copies] = (float(x) for x in built.stdout.split())
        print(f"{len(cover)} files: the whole index built in {seconds:.1f} seconds, holding at most {memory[copies]:.2f} GB")
        runs = []
        for attempt in range(3):
            with open(root / "c0" / "specs" / "library" / "events.md", "a", encoding="utf-8", newline="\n") as f:
                f.write(f"\nA sentence added for run {attempt}, so this one file has changed.\n")
            started = time.perf_counter()
            s = opened(root, cover=cover, scratch=scratch)
            s.citers("c0/specs/library/loans.md § Renewals")
            runs.append(time.perf_counter() - started)
            assert s.read_count == 1, s.read_count
            s.db.close()
        times[copies] = min(runs)
        print(f"{len(cover)} files: a run after one changed file took {times[copies]:.2f} seconds")
    small, large = COPIES
    check("on a corpus ten times the size, a run after one changed file takes no more than three times as long", times[large] <= 3 * times[small], times)
    check(f"building the whole index holds no more than {MEMORY_BOUND} GB of memory, on a body of files and on ten times as many",
          all(m <= MEMORY_BOUND for m in memory.values()), memory)
