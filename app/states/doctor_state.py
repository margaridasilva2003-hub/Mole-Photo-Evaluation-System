import reflex as rx
from typing import Optional
from app.models.mole_image import MoleImage
from app.states.auth_state import AuthState
from app.states.patient_state import mock_mole_images


class DoctorState(rx.State):
    """Manages the doctor's dashboard, including viewing and evaluating images."""

    all_images: list[MoleImage] = []
    selected_image: Optional[MoleImage] = None
    is_modal_open: bool = False

    @rx.event
    async def on_load(self):
        """Load all images for the doctor to review."""
        auth_state = await self.get_state(AuthState)
        if auth_state.is_authenticated and auth_state.user_role == "doctor":
            self.all_images = sorted(
                [img for img in mock_mole_images if img.status != "Archived"],
                key=lambda img: img.upload_date,
                reverse=True,
            )

    @rx.event
    def open_image_modal(self, image: MoleImage):
        """Open the modal to view a specific image and its AI evaluation."""
        self.selected_image = image
        self.is_modal_open = True

    @rx.event
    def close_image_modal(self):
        """Close the image details modal."""
        self.is_modal_open = False
        self.selected_image = None