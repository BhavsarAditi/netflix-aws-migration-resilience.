# Team Roles and Responsibilities

## Project: Netflix Application Migration to AWS

The project work is divided among three members. Each member leads a primary workstream and contributes to integration testing and final documentation.

## 1. Aditi — Application Development and Containerization

**Primary responsibility:** Application implementation and packaging.

### Responsibilities
- Develop and maintain the Netflix-style demonstration application.
- Implement application routes, user-facing functionality, and backend integration points.
- Maintain the Flask application code and configuration.
- Build and maintain the application Dockerfile and container setup.
- Ensure configuration is read from environment variables rather than hard-coded credentials.
- Implement and verify application health endpoints and database connectivity status.
- Test the application locally and support integration with the AWS-hosted environment.

### Key deliverables
- Application source code in `app/`.
- Dockerfile and application container configuration.
- Application health endpoint and local execution instructions.
- Application-level testing and integration evidence.

## 2. Yesha — AWS Infrastructure and Deployment

**Primary responsibility:** Cloud environment setup and deployment.

### Responsibilities
- Set up and configure the AWS environment used by the project.
- Manage EC2 instance configuration, access, and deployment prerequisites.
- Configure networking and security groups for application and database communication.
- Support deployment of the containerized application to EC2.
- Coordinate connectivity between EC2 and the private RDS database.
- Maintain deployment configuration and deployment instructions.
- Verify that the deployed application is reachable and that required AWS resources are configured correctly.
- Capture infrastructure and deployment evidence for the report.

### Key deliverables
- EC2 and networking configuration.
- Security group and connectivity configuration.
- Deployment files and deployment documentation.
- AWS deployment and infrastructure evidence.

## 3. Siddharth — RDS Migration, Resilience, Performance and Cost Analysis

**Primary responsibility:** Database integration and evaluation of resilience and operational trade-offs.

### Responsibilities
- Configure and integrate Amazon RDS for PostgreSQL with the application.
- Configure database connection settings and SSL requirements for the RDS connection.
- Verify application-to-RDS connectivity, schema initialization, and data persistence.
- Compare the local PostgreSQL-on-EC2 approach with the managed RDS architecture.
- Plan and execute controlled resilience experiments, including database outage/restoration and application container failure tests.
- Record health-check responses, observed recovery behavior, and experiment limitations.
- Measure application endpoint latency and document the methodology and results.
- Prepare cost and operational-effort comparisons using the selected EC2 and RDS configurations.
- Maintain experiment results and supporting documentation.

### Key deliverables
- RDS integration and database connection configuration.
- Resilience experiment records and screenshots.
- Latency and performance measurements.
- `experiments/results.md`.
- `docs/cost-comparison.md`.
- Final technical findings and limitations.

## Shared Responsibilities

All three members contribute to:
- Integration testing across the application, EC2 deployment, and database.
- Reviewing project documentation and ensuring it reflects the implementation.
- Recording evidence for tests and deployment.
- Checking that credentials and secret values are not committed to the Git repository.
- Reviewing the final branch changes before submission.

## Responsibility Summary

| Member | Primary workstream | Main output |
|---|---|---|
| Aditi | Application development and containerization | Flask application, Docker configuration, application health behavior |
| Yesha | AWS infrastructure and deployment | EC2, networking and security configuration, deployment setup and evidence |
| Siddharth | RDS integration, resilience, performance and cost analysis | RDS connectivity, experiments, latency results and cost documentation |

## Contribution Record

Add commit IDs, dates, screenshots, and any additional contributions here if the submission requires a verified individual contribution log.
