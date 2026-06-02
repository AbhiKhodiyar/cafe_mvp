import os
import logging
from google import genai
from google.genai import types
from app.inventory.schemas import IdentityExtractionSchema

logger = logging.getLogger("uvicorn.error")

class InventoryService:
    def __init__(self):
        self._stock_ledger = {"Arabica Beans": 10, "Paper Cups": 150}
        
        # Pull environment entry and strip any empty string padding cleanly
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        
        # Strict guard check: Only initialize SDK client if an actual key string is present
        if not api_key:
            logger.warning("No GEMINI_API_KEY detected in environment configurations. Running app in sandbox simulation fallback mode.")
            self.client = None
        else:
            self.client = genai.Client(api_key=api_key)

    async def analyze_and_log_image(self, file_bytes: bytes) -> dict:
        # Gracefully fall back to local mock parsing if no client is initialized
        if self.client is None:
            logger.warning("Executing sandbox fallback container simulation for asset tracking.")
            detected_item = "Arabica Beans"
        else:
            try:
                # Direct structured schema generation configuration
                response = self.client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=[
                        types.Part.from_bytes(data=file_bytes, mime_type="image/jpeg"),
                        "Identify the single café inventory item or bean bag visible in this image."
                    ],
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=IdentityExtractionSchema,
                        temperature=0.1
                    ),
                )
                parsed_result = IdentityExtractionSchema.model_validate_json(response.text)
                detected_item = parsed_result.item_name
            except Exception as e:
                logger.error(f"Upstream processing failure: {str(e)}")
                raise RuntimeError("External Vision API interface error or timeout encountered.")

        self._stock_ledger[detected_item] = self._stock_ledger.get(detected_item, 0) + 1
        return {"item": detected_item, "updated_stock": self._stock_ledger[detected_item]}

inventory_service = InventoryService()