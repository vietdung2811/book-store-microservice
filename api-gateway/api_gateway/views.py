from django.shortcuts import render, redirect
import requests

BOOK_SERVICE_URL = "http://book-service:8000"
CART_SERVICE_URL = "http://cart-service:8000"
ORDER_SERVICE_URL = "http://order-service:8000"
STAFF_SERVICE_URL = "http://staff-service:8000"
CUSTOMER_SERVICE_URL = "http://customer-service:8000"

def book_list(request):
    try:
        r = requests.get(f"{BOOK_SERVICE_URL}/books/", timeout=10)
        r.raise_for_status()
        books = r.json()
    except Exception as e:
        print(f"Error fetching books: {e}")
        books = []
    return render(request, "books.html", {"books": books, "customer": request.session.get('customer')})

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            r = requests.post(f"{CUSTOMER_SERVICE_URL}/login/", json={"email": email, "password": password}, timeout=10)
            if r.status_code == 200:
                customer = r.json()
                request.session['customer'] = customer
                return redirect('book_list')
            else:
                return render(request, "login.html", {"error": "Invalid email or password"})
        except Exception:
            return render(request, "login.html", {"error": "Authentication service unavailable"})
    return render(request, "login.html")

def logout(request):
    request.session.flush()
    return redirect('book_list')



def add_to_cart(request, book_id):
    customer = request.session.get('customer')
    if not customer:
        return redirect('login')
    
    customer_id = customer['id']
    if request.method == "POST":
        data = {
            "customer_id": customer_id,
            "book_id": book_id,
            "quantity": 1
        }
        try:
            requests.post(f"{CART_SERVICE_URL}/cart-items/", json=data, timeout=10)
        except Exception:
            pass
    return redirect('book_list')

def view_cart(request, customer_id=None):
    if not customer_id:
        customer = request.session.get('customer')
        if not customer:
            return redirect('login')
        customer_id = customer['id']
    
    try:
        r = requests.get(f"{CART_SERVICE_URL}/carts/{customer_id}/", timeout=10)
        r.raise_for_status()
        # The cart-service now returns a list of enriched items directly.
        items = r.json()
        total_price = sum(float(item['book']['price']) * item['quantity'] for item in items)
    except Exception as e:
        print(f"Error viewing cart: {e}")
        items = []
        total_price = 0
    return render(request, "cart.html", {"items": items, "total_price": total_price, "customer_id": customer_id, "customer": request.session.get('customer')})

def checkout(request, customer_id):
    # On POST, create the order and redirect to confirmation
    if request.method == "POST":
        data = {
            "customer_id": customer_id,
            "total_amount": request.POST.get("total_amount"),
        }
        try:
            requests.post(f"{ORDER_SERVICE_URL}/orders/", json=data, timeout=10)
            # Clear the cart after checkout by deleting the cart object in cart-service
            # Note: A more robust implementation would be a dedicated endpoint in cart-service
            cart_r = requests.get(f"{CART_SERVICE_URL}/carts/{customer_id}/", timeout=10)
            if cart_r.status_code == 200:
                cart_id = cart_r.json().get('id')
                if cart_id:
                     requests.delete(f"{CART_SERVICE_URL}/carts/{cart_id}/", timeout=10)
        except Exception as e:
            print(f"Error during checkout: {e}")
            # Decide how to handle a failed order creation
            pass
        return redirect('order_confirmation')

    # On GET, show the checkout summary page
    try:
        r = requests.get(f"{CART_SERVICE_URL}/carts/{customer_id}/", timeout=10)
        r.raise_for_status()
        items = r.json()
        total_price = sum(float(item['book']['price']) * item['quantity'] for item in items)
    except Exception as e:
        print(f"Error fetching cart for checkout: {e}")
        items = []
        total_price = 0
        
    return render(request, "checkout.html", {
        "items": items,
        "total_price": total_price,
        "customer_id": customer_id,
        "customer": request.session.get('customer')
    })

def my_orders(request):
    customer = request.session.get('customer')
    if not customer:
        return redirect('login')

    customer_id = customer['id']
    orders = []
    try:
        r = requests.get(f"{ORDER_SERVICE_URL}/orders/customer/{customer_id}/", timeout=10)
        r.raise_for_status()
        orders = r.json()
    except Exception as e:
        print(f"Error fetching orders for customer {customer_id}: {e}")
        # Handle error, maybe show an empty list or an error message on the page
    
    return render(request, "orders.html", {"orders": orders, "customer": customer})


def order_confirmation(request):
    return render(request, "order_confirmation.html", {"customer": request.session.get('customer')})

def delete_cart(request, customer_id):
    if request.method == "POST":
        try:
            requests.delete(f"{CART_SERVICE_URL}/carts/{customer_id}/delete/", timeout=10)
        except Exception as e:
            print(f"Error deleting cart: {e}")
            pass
    return redirect('view_cart')
