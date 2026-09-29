# PriceHorizon — Agent Instructions

## What this project is

PriceHorizon is a proposed technical approach to a Revenue Growth Management (RGM) problem: how an AI capability could answer plain-language business questions (for example, a competitor pricing forecast) with a repeatable, evidence-grounded, layered answer, designed as a standalone product for a fictional client, Acme AI. This repo is the working spec and supporting design research for that approach, written by Billy Atkins as an applied exercise in spec-driven system design.

## Product naming and positioning
- Product name: PriceHorizon. A single, standalone RGM offering, not a module extending or positioned against any other product.
- PriceHorizon owns its own vocabulary end to end, its own natural language interface, its own trust and confidence model, its own harmonized data foundation. Nothing in the specs should describe it as consuming, extending, or surfacing through another platform's infrastructure.

## Spec of Record

This project is specified with Spec of Record, whose entry point is `specs/AGENTS.md`: read it before any work under `specs/`, with a skill the method registers, or on a working file. What the method governs is `specs/methodology/scope.md`.

## Repo conventions

- This is a proposal and research repo, not a codebase. Do not scaffold application code here unless explicitly asked to build a prototype.
- This project's instructions are held to `specs/methodology/scope.md § Agent Agnostic`. Its opt-in helpers are `scripts/setup-claude-skills.ps1` and `scripts/setup-claude-skills.sh`, which link `.ai/skills/` into the directory Claude Code loads skills from; `README.md` says how to run them.
