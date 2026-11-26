**Records:**
  - **Fixture:** prose-naming-no-working-file \
    **Holds:** a Markdown file on a bus timetable naming a file of its own folder, and holding a fenced block that names a plans folder under a hidden folder \
    **Snippet:**

      ````markdown
      # The Timetable

      The winter times stand in `specs/winter.md`.

      ```text
      draft times: .ai/plans/winter.md
      ```
      ````

  - **Fixture:** prose-naming-the-plans-folder \
    **Holds:** a Markdown file on a bus timetable whose paragraph names the plans folder under the hidden ai folder \
    **Snippet:**

      ```markdown
      # The Timetable

      The draft times are kept in `.ai/plans/`.
      ```

  - **Fixture:** prose-naming-the-follow-ups-file \
    **Holds:** a Markdown file on a bus timetable whose paragraph names the follow-ups file under the hidden ai folder \
    **Snippet:**

      ```markdown
      # The Timetable

      A late bus is noted in `.ai/follow-ups.md`.
      ```

  - **Fixture:** prose-naming-the-tmp-folder \
    **Holds:** a Markdown file on a bus timetable whose paragraph names the tmp folder under the hidden ai folder \
    **Snippet:**

      ```markdown
      # The Timetable

      A rough draft of the times sits in `.ai/tmp/times.txt`.
      ```
