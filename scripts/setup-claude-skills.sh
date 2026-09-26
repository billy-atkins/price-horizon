#!/bin/sh
set -eu

# This script lives in <project-root>/scripts/
project_root=$(cd "$(dirname "$0")/.." && pwd)
shared_skills="$project_root/.ai/skills"
claude_directory="$project_root/.claude"
claude_skills="$claude_directory/skills"

# Relative, so the link survives the project folder being moved or synced.
link_target="../.ai/skills"

mkdir -p "$shared_skills" "$claude_directory"

# Leave existing folders or links untouched.
if [ -L "$claude_skills" ]; then
    if [ "$(readlink "$claude_skills")" = "$link_target" ]; then
        echo "Skills symlink is already configured."
        exit 0
    fi
    echo "$claude_skills is a symlink to somewhere else. Remove it before running again." >&2
    exit 1
fi

if [ -e "$claude_skills" ]; then
    echo "$claude_skills already exists. Move any skills into $shared_skills, then rename or remove the existing entry before running again." >&2
    exit 1
fi

ln -s "$link_target" "$claude_skills"
echo "Linked $claude_skills -> $shared_skills"
