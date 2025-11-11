import reflex as rx
from app.states.auth_state import AuthState


def login_form() -> rx.Component:
    """The login form component."""
    return rx.el.form(
        rx.el.div(
            rx.el.label(
                "Email Address",
                html_for="email",
                class_name="block text-sm font-medium text-gray-700",
            ),
            rx.el.div(
                rx.el.input(
                    type="email",
                    name="email",
                    id="email",
                    placeholder="you@example.com",
                    class_name="block w-full appearance-none rounded-lg border border-gray-300 px-3 py-2 placeholder-gray-400 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500 sm:text-sm",
                ),
                class_name="mt-1",
            ),
            class_name="space-y-1",
        ),
        rx.el.div(
            rx.el.label(
                "Password",
                html_for="password",
                class_name="block text-sm font-medium text-gray-700",
            ),
            rx.el.div(
                rx.el.input(
                    type="password",
                    name="password",
                    id="password",
                    placeholder="••••••••",
                    class_name="block w-full appearance-none rounded-lg border border-gray-300 px-3 py-2 placeholder-gray-400 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500 sm:text-sm",
                ),
                class_name="mt-1",
            ),
            class_name="space-y-1",
        ),
        rx.el.div(
            rx.cond(
                AuthState.login_error != "",
                rx.el.div(
                    rx.icon("badge_alert", class_name="h-5 w-5 text-red-500"),
                    rx.el.p(AuthState.login_error, class_name="text-sm text-red-600"),
                    class_name="flex items-center space-x-2 rounded-md bg-red-50 p-3",
                ),
            ),
            class_name="pt-2",
        ),
        rx.el.div(
            rx.el.button(
                rx.cond(
                    AuthState.is_loading,
                    rx.spinner(class_name="h-5 w-5 text-white"),
                    rx.el.span("Sign in"),
                ),
                type="submit",
                class_name="flex w-full justify-center rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600 disabled:opacity-50",
                disabled=AuthState.is_loading,
            ),
            class_name="pt-4",
        ),
        on_submit=AuthState.login,
        reset_on_submit=False,
        class_name="space-y-6",
    )


def login_page() -> rx.Component:
    """The main login page view."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("flask-conical", class_name="h-8 w-auto text-blue-600"),
                rx.el.h2(
                    "Sign in to your account",
                    class_name="mt-6 text-2xl font-bold tracking-tight text-gray-900",
                ),
                rx.el.p(
                    "Welcome to the Mole Evaluation Platform.",
                    class_name="mt-2 text-sm text-gray-600",
                ),
                class_name="sm:mx-auto sm:w-full sm:max-w-md",
            ),
            rx.el.div(login_form(), class_name="mt-8"),
            class_name="bg-white px-6 py-12 shadow-lg sm:rounded-2xl sm:px-12 border border-gray-100",
        ),
        class_name="flex min-h-full flex-col justify-center bg-gray-50 py-12 sm:px-6 lg:px-8",
    )