<project>
Source of truth: {{SPEC_PATH}}/spec.qmd. This file holds rules only.
</project>

<read_first>
Read the decision register, then the current slice in the build plan, before writing code.
</read_first>

<structure_rules>
- Create only the modules, directories and abstractions the current slice names. Deferred decisions get no code, stubs or directories until their trigger fires.
- Keep behaviour in the core. CLI, API and app are thin adapters over it.
- Prefer deep modules: a small interface over much hidden behaviour. Delete modules that only forward calls.
- Add a seam only where two implementations exist or a test needs the second.
- Fail loud. Let errors surface where they happen. Add exception handling, fallbacks or compatibility shims only when the register has an entry for them.
</structure_rules>

<build_loop>
1. Read the register and the slice's scaffold.
2. Write the acceptance check at the interface.
3. Implement the minimum that passes it.
4. Run the check.
5. Update the register for any trigger that fired.
6. Start the next slice.
Stop and ask on: a failed done-when, a structural decision missing from the register, a fired Deferred trigger.
</build_loop>

<when_unsure>
Do not guess a structural decision. Add it to the register as Open and ask.
</when_unsure>

<spec_upkeep>
Edit register status only. Everything else in the spec stays as written.
</spec_upkeep>
