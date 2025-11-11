import reflex as rx
from app.states.auth_state import AuthState, mock_users
from app.models.user import User


class SettingsState(rx.State):
    """Manages user profile settings."""

    name: str = ""
    email: str = ""
    password: str = ""
    confirm_password: str = ""
    is_editing: bool = False
    success_message: str = ""

    @rx.event
    async def on_load(self):
        """Load user data into the form when the page loads."""
        auth_state = await self.get_state(AuthState)
        if auth_state.logged_in_user:
            self.name = auth_state.user_name
            if isinstance(auth_state.logged_in_user, dict):
                self.email = auth_state.logged_in_user.get("email", "")
            else:
                self.email = auth_state.logged_in_user.email
            self.is_editing = False
            self.success_message = ""

    @rx.event
    async def toggle_edit(self):
        """Toggle the form editing state, reset fields if canceling."""
        self.is_editing = not self.is_editing
        if not self.is_editing:
            await self.on_load()

    @rx.event
    async def save_profile(self):
        """Save updated profile information."""
        auth_state = await self.get_state(AuthState)
        user_id = auth_state.logged_in_user_id
        if user_id == -1:
            yield rx.toast.error("Could not save profile. User not found.")
            return
        if self.password and self.password != self.confirm_password:
            yield rx.toast.error("Passwords do not match.")
            return
        if any((u.email == self.email and u.id != user_id for u in mock_users)):
            yield rx.toast.error("Email is already in use by another account.")
            return
        user_to_update = next((u for u in mock_users if u.id == user_id), None)
        if not user_to_update:
            yield rx.toast.error("User not found in mock database.")
            return
        user_to_update.name = self.name
        user_to_update.email = self.email
        if self.password:
            user_to_update.password = self.password
        auth_state.logged_in_user = user_to_update
        self.is_editing = False
        self.password = ""
        self.confirm_password = ""
        self.success_message = "Profile updated successfully!"
        yield rx.toast.success("Profile updated!")
        yield auth_state.force_rerender