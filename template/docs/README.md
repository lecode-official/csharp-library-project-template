# [[ product_name ]] Documentation

Welcome to the documentation of [[ product_name ]]. [[ product_description ]] This documentation is split into two parts:

1. [Developer Manual](developer-manual/README.md) — for people working on the [[ product_name ]] codebase itself.
2. [User Manual](user-manual/README.md) — for people building something with [[ product_name ]].

It is written for **both human developers and AI coding assistants**. Each article is deliberately small and covers a single topic, so a person can find one thing quickly and an assistant can load only the article it needs. The root [`AGENTS.md`](../AGENTS.md) has a routing table that maps a task to the article to read first.

Articles link to each other and to the actual source files. When something changes, the affected article — and `AGENTS.md` — is updated in the same change.
