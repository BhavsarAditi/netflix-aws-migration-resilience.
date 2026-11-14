# Deliverable 3 — Cost and effort comparison worksheet

Use the AWS Pricing Calculator for the exact Region, instance classes, storage, backup retention and hours used in your deployment. Do not submit generic internet estimates as your actual bill.

## Cost comparison

| Cost item | Local PostgreSQL on EC2 VM | Amazon RDS PostgreSQL |
|---|---|---|
| Compute | EC2 instance cost (shared with app + DB) | RDS DB instance cost (separate from EC2 app VM) |
| Storage | EC2 EBS volume allocation | RDS allocated storage / autoscaling if enabled |
| Backups | Configure and pay/plan for EBS snapshots and backup process | Automated backup retention and snapshots; verify applicable charges |
| Availability | Single VM unless you design redundancy | Multi-AZ option can improve availability at extra cost |
| Data transfer | Depends on same-host/local networking | Consider EC2-to-RDS data transfer and cross-AZ traffic where applicable |
| Operations | Team patches, monitors, backs up and restores DB | AWS manages much of the DB host maintenance; team still manages schema, access, tuning and recovery choices |

## Enter your actual project estimates

| Input | Value to fill |
|---|---|
| AWS Region | __________________ |
| EC2 instance type and monthly estimate | __________________ |
| RDS instance class and monthly estimate | __________________ |
| EBS storage size and estimate | __________________ |
| RDS storage and backup estimate | __________________ |
| Estimated monthly data transfer | __________________ |
| Total local-DB architecture / month | __________________ |
| Total RDS architecture / month | __________________ |

Calculation:
- Local-DB monthly total = EC2 + EBS + snapshots/backups + applicable data transfer.
- RDS monthly total = EC2 app VM + RDS instance + RDS storage + backup/snapshot charges + applicable data transfer.
- Difference = RDS monthly total − local-DB monthly total.

## Effort comparison (record your team's actual time)

| Task | Local PostgreSQL | Managed RDS |
|---|---:|---:|
| Initial database setup | ____ hours | ____ hours |
| Patching and maintenance per month | ____ hours | ____ hours |
| Backup and restore management per month | ____ hours | ____ hours |
| Monitoring and troubleshooting per month | ____ hours | ____ hours |
| Scaling effort | ____ hours | ____ hours |
| Total estimated monthly operations effort | ____ hours | ____ hours |

## Interpretation template
The local database approach reduces separate managed-service charges and can be economical for a small demonstration, but the team owns database host maintenance, backup and recovery. Amazon RDS adds a separate service cost but reduces routine infrastructure administration and offers managed backup and availability options. State the actual estimate inputs and operational hours used in your experiment.
