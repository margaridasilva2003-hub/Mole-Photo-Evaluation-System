import reflex as rx
from typing import Optional
from app.models.user import User

mock_users: list[User] = [
    User(
        id=1,
        email="patient@example.com",
        password="password",
        role="patient",
        name="John Patient",
    ),
    User(
        id=2,
        email="doctor@example.com",
        password="password",
        role="doctor",
        name="Dr. Ada Heals",
    ),
    User(
        id=3,
        email="admin@example.com",
        password="password",
        role="admin",
        name="Eva Admin",
    ),
]


class AuthState(rx.State):
    """Manages user authentication and session."""

    logged_in_user: Optional[User] = None
    login_error: str = ""
    is_loading: bool = False
    is_sidebar_open: bool = False

    @rx.var
    def is_authenticated(self) -> bool:
        """Check if a user is currently logged in."""
        return self.logged_in_user is not None

    @rx.var
    def user_role(self) -> str:
        """Get the role of the logged-in user."""
        if self.logged_in_user is None:
            return ""
        if isinstance(self.logged_in_user, dict):
            user_obj = User.model_validate(self.logged_in_user)
            return user_obj.role
        return self.logged_in_user.role

    @rx.var
    def logged_in_user_id(self) -> int:
        """Get the ID of the logged-in user."""
        if self.logged_in_user is None:
            return -1
        if isinstance(self.logged_in_user, dict):
            user_obj = User.model_validate(self.logged_in_user)
            return user_obj.id
        return self.logged_in_user.id

    @rx.var
    def user_name(self) -> str:
        """Get the name of the logged-in user."""
        if self.logged_in_user is None:
            return ""
        if isinstance(self.logged_in_user, dict):
            user_obj = User.model_validate(self.logged_in_user)
            return user_obj.name
        return self.logged_in_user.name

    @rx.event
    def login(self, form_data: dict[str, str]):
        """Handle the login form submission."""
        self.is_loading = True
        yield
        email = form_data.get("email", "").lower()
        password = form_data.get("password", "")
        for user in mock_users:
            if user.email.lower() == email and user.password == password:
                self.logged_in_user = user
                self.login_error = ""
                self.is_loading = False
                return
        self.login_error = "Invalid email or password. Please try again."
        self.is_loading = False

    @rx.event
    def toggle_sidebar(self):
        """Toggle the sidebar on mobile."""
        self.is_sidebar_open = not self.is_sidebar_open

    @rx.event
    def logout(self):
        """Log the user out and redirect to the login page."""
        self.logged_in_user = None
        return rx.redirect("/")

    @rx.event
    def force_rerender(self):
        """A dummy event to force state updates across the app."""
        pass