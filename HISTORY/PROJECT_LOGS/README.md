# Project logs

Historical Polymorph tracking logs are archived here when the active logs are rolled forward. Archive files preserve the exact pre-rollover blobs so current root docs can stay small.

Current archive boundaries:

- through dev.15: original early-history snapshots;
- through dev.19: first compact-log rollover;
- through dev.23: exact pre-handoff `PRE_FLIGHT_Check.md` and `CHANGELOG.md` snapshots;
- `MASTER_DEV23_SNAPSHOT.md`: exact full Master state immediately before the compact `ACTIVE_CONTEXT.md` continuation system was introduced.

These archives are durable reference material, not mandatory startup reading. Current work starts from root `PROJECT_CONTRACT.md` + `ACTIVE_CONTEXT.md`.
