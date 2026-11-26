"""A run of the kept tests sized to the machine as it starts: how many processes of tests at once and the threads the
search's model works on in each, and the number handed to each process and read there."""
import os

import pytest

from design_script_set import design_documents as dd, spec_text

import search

GIB = 1 << 30


@pytest.mark.action("--check-kept-tests")
@pytest.mark.parametrize("memory, processors, sized", [
    (16 * GIB, 8, (4, 1)),
    (4 * GIB, 16, (2, 4)),
    (32 * GIB, 2, (1, 1)),
    (1 * GIB, 1, (1, 1)),
])
def test_run_keeps_its_processes_under_half_the_memory_and_its_threads_under_half_the_processors(memory, processors, sized):
    assert search.MODEL_MEMORY == GIB
    assert dd.run_size(memory, processors) == sized


@pytest.mark.action("--check-kept-tests")
@pytest.mark.parametrize("threads, handed", [(3, {spec_text.MODEL_THREADS_NAMED: "3"}), (None, {})])
def test_threads_are_handed_to_a_process_by_its_environment(threads, handed):
    assert dd.model_threads_env(threads) == handed


@pytest.mark.action("--check-kept-tests")
@pytest.mark.parametrize("given, threads", [("3", 3), (None, 4), ("0", 4), ("many", 4)])
def test_search_works_on_the_threads_handed_it_or_on_half_the_processors(monkeypatch, given, threads):
    monkeypatch.setattr(os, "cpu_count", lambda: 8)
    if given is None:
        monkeypatch.delenv(spec_text.MODEL_THREADS_NAMED, raising=False)
    else:
        monkeypatch.setenv(spec_text.MODEL_THREADS_NAMED, given)
    assert search.model_threads() == threads
