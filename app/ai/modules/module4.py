"""Module 4: AI WhatsApp Support Bot
1. Answer order status queries using real database data
2. Handle return policy questions
3. Escalate high-priority or refund-related issues
4. Log AI conversations"""
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.db.models.proposal import Proposal
from app.db.models.log import Log
from app.crud.proposal import get_orders_by_phone
from app.ai.client import generate


RETURN_POLICY = """
Return Policy:
- 30 days from delivery
- Unused items in original packaging
- 100% refund or exchange
- Contact support@rayeva.com for return label
"""

def handle_whatsapp_query(message: str, phone: str, db: Session) -> Dict[str, Any]:
    """
    Handle WhatsApp support query.
    """
    message_lower = message.lower().strip()
    
    response = ""
    escalate = False
    
    # 1. Order status query
    if any(word in message_lower for word in ['status', 'order', 'track', 'delivery', 'where']):
        orders = get_orders_by_phone(db, phone)
        if orders:
            latest = orders[0]
            response = f"Your latest order #{latest.id}: {latest.status.upper()}. Placed {latest.created_at.strftime('%Y-%m-%d')}. "
            if len(orders) > 1:
                response += f"View all ({len(orders)} orders) at rayeva.com/myorders."
        else:
            response = "No orders found for this phone. Place your first order at rayeva.com! Reply HELP for assistance."
    
    # 2. Return policy
    elif any(word in message_lower for word in ['return', 'refund', 'policy', 'exchange']):
        if any(word in message_lower for word in ['refund', 'money back']):
            escalate = True
            response = "Refund requests escalated to our team. They'll review and respond within 24hrs. Provide order ID if available."
        else:
            response = RETURN_POLICY
    
    # 3. High-priority/escalation
    elif any(word in message_lower for word in ['urgent', 'emergency', 'complaint', 'issue', 'problem']):
        escalate = True
        response = "Sorry to hear that! Escalating to priority support. Human agent will reply soon."
    
    # 4. Default AI response
    else:
        # Use LLM for general support query
        prompt = f"User: {message}\\nPhone: {phone}\\nRespond helpfully as WhatsApp support bot for sustainable commerce. Keep short (<100 words). Focus on orders, products, sustainability."
        result = generate("openai", "gpt-4o-mini", prompt, max_tokens=150)
        if result.get("success"):
            response = result.get("content", result.get("data", "Thanks for contacting support!"))
        else:
            response = "Thanks for your message! Our team will respond soon."
    
    # Always log conversation
    log = Log(
        module="whatsapp",
        prompt=message,
        response=response,
        extra_data={"phone": phone, "escalate": escalate}
    )
    db.add(log)
    db.commit()
    
    print(f"WhatsApp query from {phone}: '{message}' -> escalate={escalate}")
    
    return {
        "success": True,
        "response": response,
        "escalate": escalate
    }

