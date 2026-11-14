# Final submission checklist

## Deliverable 1 — Lift-and-Shift
- [ ] EC2 instance created and running.
- [ ] Docker app and local PostgreSQL deployed on EC2.
- [ ] App opens at EC2 public IPv4.
- [ ] `/health` reports database connected.
- [ ] Screenshots captured without secrets.

## Deliverable 2 — Managed database refactor
- [ ] RDS PostgreSQL instance created.
- [ ] RDS security group accepts 5432 only from EC2 security group.
- [ ] App environment points to RDS endpoint.
- [ ] Migration service succeeds against RDS.
- [ ] App opens on EC2 and `/health` reports database connected.
- [ ] My List / playback data persists in RDS after web container restart.
- [ ] Screenshots captured without secrets.

## Deliverable 3 — Cost and effort
- [ ] AWS Pricing Calculator estimate saved for local-DB design.
- [ ] AWS Pricing Calculator estimate saved for RDS design.
- [ ] Region, instance types, storage, backups and transfer assumptions recorded.
- [ ] Team's actual setup/maintenance effort estimated and documented.
- [ ] Cost and effort worksheet completed.

## Resilience demonstration (supporting evidence)
- [ ] Restart web container and verify recovery.
- [ ] Stop/restart database in local test and capture `/health` behavior.
- [ ] Record logs, expected behavior, observed behavior and recovery time.
- [ ] Do not run destructive tests against production or important data.
