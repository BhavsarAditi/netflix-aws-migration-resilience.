# Local PostgreSQL vs Managed Database Cost Comparison

| Dimension | PostgreSQL in Docker on VM | Managed database (e.g. Amazon RDS) |
|---|---|---|
| Billing | Included in VM compute/storage | Separate database instance, storage and backup charges |
| Operations | Team handles patching, backups and recovery | Provider automates many routine database tasks |
| Availability | Depends on VM and configured backups | Multi-AZ options are available at additional cost |
| Scaling | Manual VM/storage sizing | Managed instance/storage scaling options |
| Control | More OS/database control | Less host-level control |
| Best fit | Low-cost prototype and learning | Managed operations and production-oriented workloads |

Actual prices depend on AWS Region, instance class, storage, backup retention, Multi-AZ and data transfer. Record current values from the AWS Pricing Calculator for the chosen configuration; do not treat this qualitative comparison as a quote.
