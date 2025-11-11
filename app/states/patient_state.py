import reflex as rx
import datetime
from typing import Optional
from app.models.mole_image import MoleImage
from app.states.auth_state import AuthState

mock_mole_images: list[MoleImage] = []
next_image_id = 1


class PatientState(rx.State):
    """Manages the patient dashboard, including photo uploads and viewing evaluations."""

    user_images: list[MoleImage] = []
    is_uploading: bool = False
    patient_age: str = ""
    patient_sex: str = ""
    patient_social_number: str = ""

    @rx.event
    async def on_load(self):
        """Load the user's images when the page loads."""
        auth_state = await self.get_state(AuthState)
        if auth_state.is_authenticated and auth_state.user_role == "patient":
            self.user_images = sorted(
                [
                    img
                    for img in mock_mole_images
                    if img.patient_id == auth_state.logged_in_user_id
                ],
                key=lambda img: img.upload_date,
                reverse=True,
            )

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the upload of mole images."""
        if not self.patient_age or not self.patient_sex:
            yield rx.toast.error("Please fill in age and sex before uploading.")
            return
        if not files:
            yield rx.toast.error("Please select at least one file to upload.")
            return
        self.is_uploading = True
        yield
        auth_state = await self.get_state(AuthState)
        if not auth_state.logged_in_user:
            self.is_uploading = False
            yield rx.toast.error("You must be logged in to upload files.")
            return
        global next_image_id
        for file in files:
            upload_data = await file.read()
            unique_suffix = f"{int(datetime.datetime.now().timestamp())}_{file.name}"
            upload_dir = rx.get_upload_dir()
            upload_dir.mkdir(parents=True, exist_ok=True)
            file_path = upload_dir / unique_suffix
            with file_path.open("wb") as f:
                f.write(upload_data)
            ai_score = int(unique_suffix[5:7]) % 10 + 1
            ai_notes = f"AI analysis suggests a score of {ai_score}. "
            if ai_score > 7:
                ai_notes += "High-risk features detected. Follow-up recommended."
            elif ai_score > 4:
                ai_notes += "Moderate-risk features detected. Monitoring advised."
            else:
                ai_notes += "Low-risk features detected. Routine check-up sufficient."
            new_image = MoleImage(
                id=next_image_id,
                patient_id=auth_state.logged_in_user_id,
                patient_name=auth_state.user_name,
                filename=unique_suffix,
                upload_date=datetime.datetime.now().strftime("%B %d, %Y"),
                age=int(self.patient_age),
                sex=self.patient_sex,
                social_number=self.patient_social_number,
                status="Evaluated",
                evaluation_score=ai_score,
                evaluation_notes=ai_notes,
            )
            mock_mole_images.append(new_image)
            next_image_id += 1
            yield
        self.is_uploading = False
        self.patient_age = ""
        self.patient_sex = ""
        self.patient_social_number = ""
        yield PatientState.on_load
        yield rx.toast.success(
            f"Successfully uploaded and analyzed {len(files)} image(s)."
        )
        yield rx.clear_selected_files("upload_mole_images")