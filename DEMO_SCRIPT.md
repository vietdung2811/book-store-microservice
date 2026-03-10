# Assignment 05 Demo Script (10 Minutes)

This script helps you record the 10-minute demo video required for deliverable #4.

## 1. Setup & Architecture (2 Minutes)
- **Action**: Show `docker-compose.yml` and run `docker ps`.
- **Talk**: Explain that the system is composed of 12 microservices and 1 MariaDB instance.
- **Key Point**: Mention "Independent Databases per Service" and "REST Communication".
- **Action**: Open the `ASSIGNMENT_05_DELIVERABLES.md` to show the architecture diagram.

## 2. Customer Registration & Auto-Cart (2 Minutes)
- **Action**: Open Browser to `http://localhost:8001/customers/` (API).
- **Action**: Use a tool like Postman or `curl` to create a new customer.
- **Talk**: "When I create a new customer here, the Customer Service makes a REST call to the Cart Service to initialize a cart automatically."
- **Action**: Show the `cart-service` database or API (`http://localhost:8003/carts/`) to prove the cart was created.

## 3. Book Management - Staff View (2 Minutes)
- **Action**: Open `http://localhost:8000/manage/books/`.
- **Action**: Add a new book (e.g., "Microservices in Action").
- **Talk**: "This is the API Gateway communicating with the Book Service. Staff can manage the inventory through this centralized interface."
- **Action**: Refresh `http://localhost:8000/books/` to show the new book.

## 4. Shopping Experience (2 Minutes)
- **Action**: Go to `http://localhost:8000/books/`.
- **Action**: Show the "View Cart" for a specific customer (`http://localhost:8000/cart/1/`).
- **Talk**: "The API Gateway fetches cart items from the Cart Service and book details from the Book Service to render this view."

## 5. Order Placement & Triggering (2 Minutes)
- **Action**: Submit an order via the Gateway or `curl` to `http://localhost:8007/orders/`.
- **Talk**: "Placing an order is the most complex flow. The Order Service receives the request, then triggers the Payment Service and the Shipping Service via REST."
- **Action**: Show logs or `http://localhost:8009/payments/list/` to confirm a payment was logged for the new order.
- **Conclusion**: Summarize that all services are decoupled and running in separate containers.
