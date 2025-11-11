import reflex as rx
from app.states.settings_state import SettingsState
from app.components.sidebar import sidebar


def profile_form() -> rx.Component:
    """Form for editing user profile."""
    return rx.el.div(
        rx.cond(
            SettingsState.is_editing,
            rx.el.div(
                rx.el.div(
                    rx.el.label(
                        "Full Name",
                        html_for="name",
                        class_name="block text-sm font-medium text-gray-700",
                    ),
                    rx.el.input(
                        id="name",
                        default_value=SettingsState.name,
                        on_change=SettingsState.set_name,
                        class_name="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm",
                    ),
                ),
                rx.el.div(
                    rx.el.label(
                        "Email Address",
                        html_for="email",
                        class_name="block text-sm font-medium text-gray-700",
                    ),
                    rx.el.input(
                        id="email",
                        type="email",
                        default_value=SettingsState.email,
                        on_change=SettingsState.set_email,
                        class_name="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm",
                    ),
                ),
                class_name="space-y-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Full Name", class_name="text-sm font-medium text-gray-700"
                    ),
                    rx.el.p(
                        SettingsState.name,
                        class_name="mt-1 p-2 bg-gray-50 rounded-md text-sm",
                    ),
                ),
                rx.el.div(
                    rx.el.h3(
                        "Email Address",
                        class_name="text-sm font-medium text-gray-700 mt-4",
                    ),
                    rx.el.p(
                        SettingsState.email,
                        class_name="mt-1 p-2 bg-gray-50 rounded-md text-sm",
                    ),
                ),
            ),
        ),
        rx.cond(
            SettingsState.is_editing,
            rx.el.div(
                rx.el.div(
                    rx.el.label(
                        "New Password",
                        html_for="password",
                        class_name="block text-sm font-medium text-gray-700",
                    ),
                    rx.el.input(
                        id="password",
                        type="password",
                        placeholder="Leave blank to keep current password",
                        on_change=SettingsState.set_password,
                        class_name="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm",
                    ),
                ),
                rx.el.div(
                    rx.el.label(
                        "Confirm New Password",
                        html_for="confirm_password",
                        class_name="block text-sm font-medium text-gray-700",
                    ),
                    rx.el.input(
                        id="confirm_password",
                        type="password",
                        placeholder="Confirm new password",
                        on_change=SettingsState.set_confirm_password,
                        class_name="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm",
                    ),
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-6 pt-6 border-t mt-6",
            ),
            None,
        ),
        rx.el.div(
            rx.cond(
                SettingsState.success_message != "",
                rx.el.p(
                    SettingsState.success_message, class_name="text-sm text-green-600"
                ),
                None,
            ),
            class_name="pt-4",
        ),
        class_name="mt-6",
    )


def settings_page() -> rx.Component:
    """The user settings page."""
    page_content = rx.el.div(
        rx.el.div(
            rx.el.h1("Settings", class_name="text-2xl font-bold text-gray-900"),
            rx.el.div(
                rx.el.button(
                    rx.cond(SettingsState.is_editing, "Cancel", "Edit Profile"),
                    on_click=SettingsState.toggle_edit,
                    class_name="rounded-md bg-white px-3.5 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50",
                ),
                rx.cond(
                    SettingsState.is_editing,
                    rx.el.button(
                        "Save Changes",
                        on_click=SettingsState.save_profile,
                        class_name="rounded-md bg-blue-600 px-3.5 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-500",
                    ),
                    None,
                ),
                class_name="flex gap-3",
            ),
            class_name="flex items-center justify-between pb-6 border-b",
        ),
        profile_form(),
        class_name="max-w-3xl mx-auto",
    )
    return sidebar(main_content=page_content)