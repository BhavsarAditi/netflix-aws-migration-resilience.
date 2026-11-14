# Cloud Computing Demonstration Plan

1. Run the local Docker Compose stack and verify `http://localhost:5000/health`.
2. Demonstrate catalogue search and add/remove My List entries.
3. Play a sample clip and show the playback event in PostgreSQL.
4. Build and run the same container on an EC2 VM (Lift and Shift).
5. Refactor the database connection to Amazon RDS using secure environment variables and private networking.
6. Stop/restart the web container and observe recovery.
7. Simulate a temporary database outage in a controlled test environment and inspect health checks/logs.
8. Compare local database operations and managed RDS cost/effort using the selected AWS Region and instance sizes.
