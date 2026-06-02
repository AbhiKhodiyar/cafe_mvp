from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from app.ordering.router import router as ordering_router
from app.billing.router import router as billing_router
from app.inventory.router import router as inventory_router

app = FastAPI(
    title="Café Management MVP",
    version="1.0.0",
    docs_url="/docs"
)

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "Validation Error", "detail": str(exc)}
    )

@app.exception_handler(RuntimeError)
async def upstream_error_handler(request: Request, exc: RuntimeError):
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content={"error": "Upstream Gateway Failure", "detail": str(exc)}
    )

# Isolated routing mounts
app.include_router(ordering_router, prefix="/api/v1/ordering", tags=["Ordering"])
app.include_router(billing_router, prefix="/api/v1/billing", tags=["Billing"])
app.include_router(inventory_router, prefix="/api/v1/inventory", tags=["Inventory"])
