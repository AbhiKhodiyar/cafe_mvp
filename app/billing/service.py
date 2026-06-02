from app.billing.schemas import InvoiceRequest, DiscountType

class BillingService:
    @staticmethod
    def generate_invoice(payload: InvoiceRequest) -> dict:
        subtotal = sum(item.quantity * item.unit_price for item in payload.items)
        discount_amount = 0.0
        
        # Invoicing and deduction core logic processing [cite: 9]
        if payload.discount:
            if payload.discount.type == DiscountType.PERCENTAGE:
                if payload.discount.value > 100.0:
                    raise ValueError("Discount percentage cannot exceed 100%.")
                discount_amount = subtotal * (payload.discount.value / 100.0)
            elif payload.discount.type == DiscountType.FIXED:
                discount_amount = min(payload.discount.value, subtotal)

        post_discount_total = max(0.0, subtotal - discount_amount)
        tax_amount = post_discount_total * (payload.tax_percentage / 100.0)
        final_total = post_discount_total + tax_amount

        return {
            "order_id": payload.order_id,
            "subtotal": round(subtotal, 2),
            "discount_applied": round(discount_amount, 2),
            "tax_applied": round(tax_amount, 2),
            "total_due": round(final_total, 2)
        }