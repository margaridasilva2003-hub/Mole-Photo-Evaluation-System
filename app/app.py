import reflex as rx
from app.states.auth_state import AuthState
from app.components.login_page import login_page
from app.pages.patient_dashboard import patient_dashboard
from app.pages.doctor_dashboard import doctor_dashboard
from app.pages.admin_dashboard import admin_dashboard
from app.pages.settings_page import settings_page


def index() -> rx.Component:
    """
    The main app component that renders pages based on authentication status and user role.
    """
    return rx.el.main(
        rx.cond(
            AuthState.is_authenticated,
            rx.match(
                AuthState.user_role,
                ("patient", patient_dashboard()),
                ("doctor", doctor_dashboard()),
                ("admin", admin_dashboard()),
                login_page(),
            ),
            login_page(),
        ),
        class_name="font-['Open_Sans']",
    )


from app.states.patient_state import PatientState
from app.states.doctor_state import DoctorState
from app.states.settings_state import SettingsState
from app.states.admin_state import AdminState

app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(
    index, on_load=[PatientState.on_load, DoctorState.on_load, AdminState.on_load]
)
app.add_page(settings_page, route="/settings", on_load=[SettingsState.on_load])