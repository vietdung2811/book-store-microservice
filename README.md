# Bookstore Microservice System (Assignment 05 & 06)

This project is a Bookstore management system designed with a **Microservices Architecture** using Django and Django Rest Framework (DRF). It fulfills the requirements for Assignment 05 and provides a foundation for Assignment 06.

## 1. System Architecture & Flow

The system is decomposed into **12 independent microservices**, each with its own dedicated database and Docker container.

### Core Microservices:
- **API Gateway (Port 8000):** The primary entry point. Orchestrates calls to other services and renders HTML templates.
- **Customer Service (Port 8001):** Manages customer profiles and registration.
- **Book Service (Port 8002):** Manages book inventory, pricing, and stock.
- **Cart Service (Port 8003):** Manages temporary shopping carts and items.
- **Order Service (Port 8007):** Processes orders and triggers payment/shipping workflows.

### Support Microservices:
- **Staff Service (Port 8004):** Staff and role management.
- **Manager Service (Port 8005):** Departmental oversight.
- **Catalog Service (Port 8006):** Book categories and metadata.
- **Ship Service (Port 8008):** Logistics and tracking.
- **Pay Service (Port 8009):** Financial transactions.
- **Comment-Rate Service (Port 8010):** User reviews and ratings.
- **Recommender-AI Service (Port 8011):** AI-based book recommendations.

### Key Workflows:
1. **User Registration:** Creating a customer in `customer-service` automatically triggers cart creation in `cart-service`.
2. **Book Management:** Staff can add/update books via the API Gateway which communicates with `book-service`.
3. **Checkout Flow:** Creating an order in `order-service` triggers synchronous REST calls to `pay-service` (for payment) and `ship-service` (for shipping).

---

## 2. Getting Started (Docker Compose)

### Prerequisites:
- **Docker** and **Docker Compose** installed.

### Installation:
1. Clone the repository and navigate to the root folder.
2. Build and start all 13 containers (12 services + 1 MongoDB):
   ```bash
   docker-compose up --build
   ```
3. Initialize and seed the databases (Migrations + Sample Data):
   ```bash
   ./seed_data.sh
   ```

### Accessing the UI:
- **Book Catalog:** [http://localhost:8000/books/](http://localhost:8000/books/)
- **Staff Management:** [http://localhost:8000/manage-books/](http://localhost:8000/manage-books/)
- **Customer Cart (ID 1):** [http://localhost:8000/cart/1/](http://localhost:8000/cart/1/)

---

## 3. Technical Report & Documentation

For detailed information on the architecture, API endpoints, and design decisions, please refer to:
- **[ASSIGNMENT_05_DELIVERABLES.md](ASSIGNMENT_05_DELIVERABLES.md)**: Full Technical Report for Assignment 05.
- **[assignment_05_progress.md](assignment_05_progress.md)**: Implementation progress and troubleshooting log.
