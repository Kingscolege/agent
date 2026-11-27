# Backward Call Stack & Data Flow Tracing

When an error originates deep in a call stack or data processing pipeline:

```
[Crash/Symptom Site]  <-- Error manifests here
        ▲
        │ Bad value passed in
[Intermediate Helper]
        ▲
        │ Incorrect transformation
[Calling Function]
        ▲
        │ Origin of invalid state / unexpected input
[Source of Defect]    <-- MUST FIX HERE, NOT AT CRASH SITE
```

## Step-by-Step Tracing Technique

1. **Identify the Symptom Variable:**
   - What variable had an illegal, null, undefined, or unexpected value at the failure point?
2. **Identify Direct Origin:**
   - Was the variable passed as an argument, returned from a function call, or read from state?
3. **Step One Level Up:**
   - Locate the caller that supplied the value.
   - Check the caller's inputs and local state at the invocation line.
4. **Repeat Until Boundary Reached:**
   - Continue tracing upward until you reach:
     - An unvalidated external input (API request, config file, CLI argument).
     - A logic flaw in data transformation or state mutation.
     - A broken invariant or unhandled edge case.
5. **The Golden Rule:**
   - Never add a defensive check (e.g. `if (val == null) return;`) at the crash site if the contract specifies `val` must not be null! Fix the upstream caller that allowed `val` to become null.
