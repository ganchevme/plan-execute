# Using an external logs-wrapper

Read when the resolved setting permits wrapper use and an existing executable needs selection, invocation, configuration or diagnosis. Direct capture follows [execution.md](execution.md#logs-and-wrapper) and does not need this reference.

## Select the executable

The wrapper is a separate tool. This skill ships no wrapper binaries, runner profiles or build tooling, and needs none for normal operation. The default `logging.wrapper = "none"` skips discovery and captures command output directly.

The wrapper filters test and other command output into concise summaries, failures and relevant diagnostics for the executing agent, reducing the log text added to its context. Complete raw output remains in a log file for diagnosis; filtering must not discard the only evidence of a failure.

For `auto`, check PATH for `logs-wrapper` (`logs-wrapper.exe` on Windows), using only usable executables permitted by applicable instructions and tool permissions. An explicit `logging.wrapper` path selects that executable; resolve a relative configured path as described in [settings.md](settings.md). Do not recursively search private directories or install, download, copy or build missing tooling automatically. If no suitable permitted wrapper is available, follow execution mode's direct-capture fallback.

An explicit user request to install the wrapper may authorize obtaining it from the supplied source or release location and configuring it, subject to the resolved environment policy and host permissions. Merely enabling `auto` or finding the wrapper unavailable is not an installation request. Do not treat this as authorization to install unrelated tooling.

The executable must match the OS and architecture where it runs. Containers require a compatible executable and any necessary paths already available inside the container. A wrapper installed on the host is not automatically available inside it.

## Inspect and invoke

Read the installed wrapper's help and documentation before assuming options, supported runners, configuration paths or output semantics. Use only interfaces supported by that version. Profiles and configuration belong to the external installation; never refer to a bundle path inside this skill.

Use a fresh exclusive raw-output log for each command. Preserve the child exit status and absolute raw-log path, distinguish wrapper failures from expected RED, and inspect relevant log excerpts when the summary is insufficient. Use direct capture if the installed wrapper cannot preserve the required evidence or support the command, including interactive input when needed.

Keep complete diagnostics in the raw log and return concise test evidence as described in [execution.md](execution.md#concise-test-evidence). Reading logs to produce or inspect a summary is allowed; append-only writing does not prohibit diagnostic reads.
