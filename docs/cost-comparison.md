# Local PostgreSQL vs Managed Database Cost Comparison

## Project configuration

- AWS Region: Asia Pacific (Mumbai), `ap-south-1`
- EC2 application instance: `t3.micro`
- EC2 EBS volume: 20 GiB
- Managed database: Amazon RDS for PostgreSQL
- RDS instance class: `db.t4g.micro`
- RDS allocated storage: 20 GiB
- RDS deployment: Single-AZ
- Estimate basis: 730 hours per month, on-demand pricing, USD

## Estimated monthly cost comparison

| Cost item | PostgreSQL in Docker on EC2 | Amazon RDS PostgreSQL |
|---|---:|---:|
| EC2 `t3.micro` | $8.18 | $8.18 |
| EC2 EBS gp3, 20 GiB | $1.82 | $1.82 |
| RDS `db.t4g.micro`, Single-AZ | — | $15.33 |
| RDS gp3 storage, 20 GiB | — | $2.62 |
| **Estimated monthly total** | **$10.00** | **$27.95** |

The estimated additional cost of using RDS is approximately **$17.95 per month** compared with running PostgreSQL locally on the EC2 instance.

These are indicative public-price estimates for the Mumbai region, not actual billed amounts or an AWS quotation. Backup and snapshot charges, data transfer, public IPv4, taxes, discounts and other applicable charges are excluded. Actual costs should be validated using the AWS Pricing Calculator.

## Qualitative comparison

| Dimension | PostgreSQL in Docker on VM | Managed database (Amazon RDS) |
|---|---|---|
| Billing | Included in VM compute and storage | Separate database instance, storage and backup charges |
| Operations | Team handles patching, backups and recovery | AWS automates many routine database tasks |
| Availability | Depends on VM and configured backups | Multi-AZ options are available at additional cost |
| Scaling | Manual VM and storage sizing | Managed instance and storage scaling options |
| Control | More OS/database control | Less host-level control |
| Best fit | Low-cost prototype and learning | Managed operations and production-oriented workloads |

## Interpretation

The local PostgreSQL architecture is the lower-cost option for this small demonstration, with an estimated monthly cost of $10.00. However, the team is responsible for database host maintenance, backups, monitoring and recovery.

The RDS architecture has an estimated monthly cost of $27.95 for the selected Single-AZ configuration. Although it costs approximately $17.95 more per month, it reduces routine database infrastructure administration and provides managed database capabilities. Multi-AZ deployment can improve availability further, but would increase the cost.

For this project, the comparison demonstrates the trade-off between lower infrastructure cost with self-managed PostgreSQL and higher cost with managed database operations.

