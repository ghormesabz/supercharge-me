---
name: promptmaxx
description: Rewrite a task prompt into a deeper version by asking what a top professional would do differently. User-invoked only via /promptmaxx.
disable-model-invocation: true
argument-hint: "[task or prompt to deepen — defaults to the current task]"
---

<goal>
Make the task deeper, not bigger. Raise the standard of the work; don't widen its scope.
</goal>

<input>
The task is $ARGUMENTS. If empty, use the most recent task or prompt in this conversation and quote it back in one line.
</input>

<steps>
Before rewriting, answer each in a few lines, specific to this task's field. Generic answers ("use best practices", "test thoroughly") fail the step.

1. **Professional standard** — what a top professional in this field would do here that I'm not asking for.
2. **Raw material** — the rawest source they'd start from (primary data, source code, spec, original paper, logs) instead of what's already been digested for me (summaries, blog posts, my own framing).
3. **Methods and tools** — the specific methods and tools they'd use, named concretely.
4. **External check** — what, other than you or me, would show the result is right (a test, a reference output, a benchmark, a domain expert, a real-world outcome).

If something isn't knowable without looking, say what you'd need to check. Read files or search only to answer these four, never to start the task.
</steps>

<output>
1. The four answers.
2. The rewritten prompt in a fenced block, asking for exactly what steps 1–4 imply, ready to paste or run.
3. One line on what got cut or deferred to keep it deeper rather than bigger.

Stop there. Don't execute the rewritten prompt. I decide whether to run it.
</output>
