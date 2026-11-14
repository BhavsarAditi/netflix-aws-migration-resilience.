# Netflix-style Streaming Platform Cloud Migration Case Study

This educational project models a streaming service interface under the original project title's cloud migration and resilience theme. It is not affiliated with Netflix.

## Demonstration
- Lift-and-shift: package the Flask app as a Docker image and run it on a cloud VM.
- Refactor: run PostgreSQL as a separate managed database such as Amazon RDS, changing DB environment variables and network configuration.
- Resilience: test web container restarts, database unavailability, health checks and recovery.

## Application features
The StreamFlix demo provides a title catalogue, search, profile-scoped saved list, playback event logging and database health status. The player streams public sample clips only.

## Scope limitations
This is a teaching prototype, not a production streaming service. It does not include licensed media, DRM, payment processing, real identity management, CDN delivery, adaptive bitrate encoding or production-grade authorization.
