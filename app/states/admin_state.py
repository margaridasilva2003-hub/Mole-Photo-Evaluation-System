import reflex as rx
from app.states.auth_state import AuthState, mock_users
from app.models.user import User
import random


class AdminState(rx.State):
    """Manages admin-specific functionality like user management."""

    all_users: list[User] = []
    is_modal_open: bool = False

    @rx.event
    async def on_load(self):
        """Load all users when the admin dashboard loads."""
        auth_state = await self.get_state(AuthState)
        if auth_state.is_authenticated and auth_state.user_role == "admin":
            self.all_users = sorted(mock_users, key=lambda u: u.id)

    @rx.event
    def create_user(self, form_data: dict):
        """Create a new user and add to the mock database."""
        name = form_data.get("name")
        email = form_data.get("email")
        password = form_data.get("password")
        role = form_data.get("role")
        if not name or not email or (not password) or (not role):
            return rx.toast.error("Please fill all fields.")
        if any((u.email.lower() == email.lower() for u in mock_users)):
            return rx.toast.error(f"User with email '{email}' already exists.")
        new_id = max((u.id for u in mock_users)) + 1 if mock_users else 1
        new_user = User(id=new_id, name=name, email=email, password=password, role=role)
        mock_users.append(new_user)
        self.is_modal_open = False
        yield AdminState.on_load
        yield rx.toast.success(f"User '{name}' created successfully.")