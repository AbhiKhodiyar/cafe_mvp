from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.inventory.schemas import InventoryLogResponse
from app.inventory.service import inventory_service

router = APIRouter()

@router.post("/upload", response_model=InventoryLogResponse, status_code=status.HTTP_200_OK)
async def upload_inventory_item(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported media format. Endpoint exclusively processes image streams."
        )
        
    try:
        file_bytes = await file.read()
        return await inventory_service.analyze_and_log_image(file_bytes)
    except RuntimeError as err:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(err))
    finally:
        await file.close()