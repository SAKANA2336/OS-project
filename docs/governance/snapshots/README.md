# Controlled document snapshots

A snapshot preserves the exact bytes of a controlled document in its original path context. The active protocol is [`docs/PROTOCOL.md`](../../PROTOCOL.md). The active file management policy is [`docs/governance/FILE_MANAGEMENT.md`](../FILE_MANAGEMENT.md).

Use the [protocol version archive](../../PROTOCOL_VERSION_ARCHIVE.md) or [file management version archive](../FILE_MANAGEMENT_VERSION_ARCHIVE.md) to locate a version's snapshot file or historical Git commit and path. The archives record the expected SHA-256 of each documented recovery copy. A historical Git reference can preserve the original without a duplicate snapshot file in the current tree.

Preserve embedded `current_*` roles and relative links as recorded. Interpret them from the original document path. To recover a version, verify its bytes against the recorded SHA-256 before restoring it to the declared original path. Snapshots must remain byte-for-byte intact.
