from fastapi import APIRouter

system_state_router = APIRouter(tags=["System State"])


@system_state_router.get("/health_check")
async def health_check_view() -> str:
    """Check if the system is running OK."""
    return "Shipay to the moon!"
