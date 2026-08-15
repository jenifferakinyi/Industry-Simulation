"""
Views for Northstar Support Deflection Chatbot MVP.
Pure Django — renders chatbot.html and responds via chat_api JSON endpoint.
"""
import re
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from .models import Order, ReturnRequest, StockItem


def chatbot(request):
    """Renders the main chatbot interface."""
    return render(request, 'support/chatbot.html')


@csrf_exempt
def chat_api(request):
    """
    Intelligent Swahili & English support deflection chatbot endpoint.
    Queries the seeded SQLite database for orders, returns, and stock items.
    Provides clear, helpful responses for items not in the inventory.
    """
    if request.method != 'POST':
        return JsonResponse({'reply': 'Send a POST request.'}, status=405)

    try:
        data = json.loads(request.body)
        raw_msg = data.get('message', '').strip()
    except Exception:
        return JsonResponse({'reply': 'Could not read message.'}, status=400)

    if not raw_msg:
        return JsonResponse({'reply': 'Tafadhali andika swali lako! (Please type your message!)'})

    msg = raw_msg.lower()

    # ── 1. EXTRACT ORDER NUMBER (e.g. NS-1001, NS 1002, ns1003) ────────────────
    order_match = re.search(r'\bns[-\s]?(\d{4})\b', msg, re.IGNORECASE)
    order_number = f"NS-{order_match.group(1)}" if order_match else None

    # ── 2. ORDER STATUS INTENT (English & Swahili) ─────────────────────────────
    order_keywords = ['order', 'track', 'where', 'shipped', 'delivery', 'arrive', 'status', 'iko wapi', 'mzigo']
    if any(k in msg for k in order_keywords) or (order_number and 'return' not in msg and 'refund' not in msg):
        if order_number:
            try:
                o = Order.objects.get(order_number__iexact=order_number)
                if o.status == 'processing':
                    reply = f"📦 Order **{o.order_number}** (Customer: {o.customer_name}) is being packed in our warehouse.\n📅 Estimated delivery: {o.estimated_delivery or 'TBC'}"
                elif o.status == 'shipped':
                    reply = f"🚚 Order **{o.order_number}** is on its way!\n• Carrier: {o.carrier or 'DHL'}\n• Tracking: {o.tracking_number or 'N/A'}\n📅 ETA: {o.estimated_delivery or 'TBC'}"
                elif o.status == 'delivered':
                    reply = f"✅ Order **{o.order_number}** was delivered!\n📍 Shipped to: {o.shipping_address}"
                else:
                    reply = f"❌ Order **{o.order_number}** was cancelled. Any charge will be refunded within 5 business days."
                return JsonResponse({'reply': reply, 'intent': 'order_status'})
            except Order.DoesNotExist:
                return JsonResponse({
                    'reply': f"❌ We couldn't find order **{order_number}** in our system.\n\n💡 Try one of our seeded demo orders: **NS-1001**, **NS-1002**, **NS-1003**, or **NS-1004**.",
                    'intent': 'order_status'
                })
        
        sample = ', '.join(o.order_number for o in Order.objects.all()[:5])
        return JsonResponse({
            'reply': f"📦 To check an order status, include your order number!\n\nExample: *'Where is my order NS-1002?'*\n💡 Available demo orders: {sample}",
            'intent': 'order_status'
        })

    # ── 3. RETURNS & REFUNDS INTENT ──────────────────────────────────────────
    return_keywords = ['return', 'refund', 'money back', 'rudisha', 'badilisha', 'rma', 'exchange']
    if any(k in msg for k in return_keywords):
        if order_number:
            try:
                o = Order.objects.get(order_number__iexact=order_number)
                ret = o.return_requests.first()
                if ret:
                    status_map = {
                        'pending':  f"⏳ Return for **{order_number}** is under review. We will email you within 1 business day.",
                        'approved': f"✅ Return for **{order_number}** is approved! Prepaid return label sent to {o.customer_email}.",
                        'refunded': f"💚 Refund for **{order_number}** has been processed! Allow 3–5 business days to show on your statement.",
                        'rejected': f"❌ Return for **{order_number}** was not approved. Please contact support.",
                    }
                    return JsonResponse({'reply': status_map.get(ret.status, f"Return status: {ret.status}"), 'intent': 'returns'})
                return JsonResponse({
                    'reply': f"ℹ️ Order **{order_number}** currently has no return request.\n\nOur Return Policy:\n• 30-day return window\n• 5 business days for refund once returned",
                    'intent': 'returns'
                })
            except Order.DoesNotExist:
                pass
        return JsonResponse({
            'reply': "↩️ **Northstar Return & Refund Policy:**\n• 30-day return window from delivery date\n• 5 business days to process refund upon receipt\n• Items must be unworn in original packaging\n\nTo check a specific return, include your order number e.g. *'Return for NS-1001'*",
            'intent': 'returns'
        })

    # ── 4. STOCK & PRODUCT INTENT (English + Swahili synonyms) ───────────────
    # Swahili translations: kiatu/viatu -> sneaker/shoe, nguo/tisheti -> tee/hoodie, ziko/iko -> availability
    swahili_mapping = {
        'kiatu': 'sneakers',
        'viatu': 'sneakers',
        'iatu': 'sneakers',
        'shoe': 'sneakers',
        'shoes': 'sneakers',
        'tisheti': 'tee',
        'tshirt': 'tee',
        't-shirt': 'tee',
        'sweater': 'hoodie',
        'koti': 'hoodie',
        'suruali': 'joggers',
        'trouser': 'joggers',
        'pants': 'joggers',
    }

    # Replace swahili keywords in query for search
    search_query = msg
    for s_word, en_word in swahili_mapping.items():
        if s_word in msg:
            search_query += f" {en_word}"

    stock_keywords = ['stock', 'available', 'iko', 'ziko', 'mna', 'size', 'hoodie', 'sneaker', 'tee', 'jogger', 'kiatu', 'viatu', 'shoes', 'have', 'buy', 'price']
    
    if any(k in msg for k in stock_keywords) or any(w in search_query for w in ['hoodie', 'sneakers', 'tee', 'joggers']):
        results = []
        for word in search_query.split():
            if len(word) >= 3 and word not in ['have', 'where', 'like', 'this', 'that', 'from']:
                items = StockItem.objects.filter(
                    Q(product_name__icontains=word) | Q(sku__icontains=word) | Q(variant__icontains=word)
                )
                if items.exists():
                    results.extend(list(items))

        # Deduplicate results
        unique_results = {item.pk: item for item in results}.values()

        if unique_results:
            lines = ["🔍 **Live Inventory Search Results:**\n"]
            for item in unique_results:
                if item.in_stock:
                    lines.append(f"✅ **{item.product_name}** ({item.variant}) — **{item.quantity} in stock**")
                else:
                    restock = f"expected restock on {item.restock_date}" if item.restock_date else "restock date TBC"
                    lines.append(f"❌ **{item.product_name}** ({item.variant}) — **Out of stock** ({restock})")
            return JsonResponse({'reply': "\n".join(lines), 'intent': 'stock'})

        # ITEM NOT IN DATABASE — Helpful fallback response listing available stock
        db_products = sorted(list(set(StockItem.objects.values_list('product_name', flat=True))))
        product_list = "\n".join([f"• 📦 {p}" for p in db_products]) if db_products else "• Heavyweight Hoodie\n• Court Sneakers\n• Everyday Tee\n• Slim Joggers"

        return JsonResponse({
            'reply': f"🔍 We don't currently stock that item in our catalog.\n\n🛒 **Products currently available at Northstar Retail:**\n{product_list}\n\nTry asking: *'Is the Hoodie in stock?'* or *'kiatu iko?'*",
            'intent': 'stock_not_found'
        })

    # ── 5. GREETINGS (English & Swahili) ────────────────────────────────────
    greetings = ['hi', 'hello', 'hey', 'habari', 'mambo', 'sasa', 'jambo', 'start', 'help', 'assist']
    if any(k in msg for k in greetings):
        return JsonResponse({
            'reply': "👋 Habari! Welcome to Northstar Support Bot.\n\nI can instantly help you with:\n📦 **Order Status** — e.g. *'Where is NS-1002?'*\n↩️ **Returns** — e.g. *'Refund status for NS-1001'*\n🔍 **Stock Availability** — e.g. *'Kiatu iko?'* or *'Is Hoodie in stock?'*\n\nClick any button on the screen or type a question!",
            'intent': 'greeting'
        })

    # ── 6. GENERAL FALLBACK WITH HELPFUL SUGGESTIONS ───────────────────────
    db_products = sorted(list(set(StockItem.objects.values_list('product_name', flat=True))))
    product_str = ", ".join(db_products) if db_products else "Court Sneakers, Heavyweight Hoodie, Everyday Tee, Slim Joggers"

    return JsonResponse({
        'reply': f"🤖 I couldn't quite find what you were looking for.\n\nHere are things I can help you with:\n• 📦 **Check an order:** e.g. *'Where is NS-1002?'*\n• ↩️ **Track a return:** e.g. *'Return for NS-1001'* \n• 🔍 **Check stock:** e.g. *'Kiatu iko?'* or search for {product_str}.\n\nTry clicking one of the sample buttons on your screen!",
        'intent': 'fallback'
    })
