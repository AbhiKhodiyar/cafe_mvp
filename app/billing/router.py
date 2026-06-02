from fastapi import APIRouter, HTTPException, status
from app.billing.schemas import InvoiceRequest, InvoiceResponse
from app.billing.service import BillingService

router = APIRouter()

@router.post("/invoice", response_model=InvoiceResponse, status_code=status.HTTP_200_OK)
async def generate_invoice(payload: InvoiceRequest):
    try:
        return BillingService.generate_invoice(payload)
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))