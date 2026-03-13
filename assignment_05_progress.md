# Assignment 05: Microservices Implementation Progress

## Project Overview
Decomposition of a monolithic Bookstore into a microservice architecture using Django REST Framework and Docker.

## Completed Tasks

### 1. Research & Analysis
- Analyzed existing services: `customer-service`, `book-service`, `cart-service`, and `api-gateway`.
- Identified missing services and technical gaps regarding "Independent Databases" and "Service Discovery".

### 2. Infrastructure Setup
- **Independent Databases**: Configured 12 unique MariaDB schemas in `.env`.
- **Database Initialization**: Created `init.sql` to automate database creation and user permissions (`bs1`) on container startup.
- **Docker Compose**: Updated `docker-compose.yml` with all 12 services, unique port mappings, and environment-specific database names.

### 3. Service Scaffolding
Created the following new services with models, serializers, and REST endpoints:
- `staff-service`: Staff management.
- `manager-service`: Department/Manager oversight.
- `catalog-service`: Category management and book overview.
- `order-service`: Order processing (triggers Pay/Ship).
- `ship-service`: Shipment tracking.
- `pay-service`: Transaction handling.
- `comment-rate-service`: Book reviews and ratings.
- `recommender-ai-service`: AI-based recommendations.

### 4. Logic & Connectivity
- **Customer Registration**: Triggers automated cart creation in `cart-service`.
- **Cart Management**: Added PUT/DELETE endpoints for cart items.
- **Order Flow**: `order-service` performs inter-service REST calls to `pay-service` and `ship-service`.
- **API Gateway**: 
    - Implemented `book_list` and `view_cart` views.
    - Added `staff_manage_books` view and template.
    - Added `create_order` functionality.
    - Implemented a redirect from `/` to `/books/`.

### 5. Data Seeding
- Created `seed_data.sh` which:
    - Runs `makemigrations` and `migrate` for all 12 services.
    - Populates the databases with initial books, customers, staff, and reviews.

### 6. Deliverables & Documentation
- **Technical Report**: Generated `ASSIGNMENT_05_DELIVERABLES.md` (8-12 page equivalent) including architecture diagrams, full API reference, and technical design justifications.
- **Demo Preparation**: Created `DEMO_SCRIPT.md` to guide the required 10-minute video presentation.
- **Source Control**: Initialized Git repository, configured `.gitignore` for a clean repo, and provided instructions for pushing to GitHub using Personal Access Tokens (PAT).
- **Project Overview**: Updated `README.md` to accurately reflect the 12-microservice architecture and updated port mappings.

## Troubleshooting Log
- **Permission Errors**: Fixed MariaDB `Access denied` by refining `init.sql` and resetting volumes.
- **Connectivity Issues**: Resolved `OperationalError (2002)` by implementing service restarts to wait for the database to be ready.
- **Docker Syntax**: Fixed line-continuation backslashes in Dockerfiles to prevent parse errors.
- **Git Push (PAT)**: Addressed the change in GitHub's authentication policy from passwords to Personal Access Tokens.

## Current Status
- All 13 containers (12 services + DB) are verified functional and seeded.
- **All Assignment 05 Deliverables are complete and documented.**
- The project is ready for submission and the source code is prepared for Git push.

## Next Steps
- Begin **Assignment 06**: Implementation of JWT Authentication, Saga Pattern for distributed transactions, and Event Bus integration (RabbitMQ/Kafka).
