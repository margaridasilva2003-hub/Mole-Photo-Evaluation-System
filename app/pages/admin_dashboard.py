import reflex as rx
from app.states.admin_state import AdminState
from app.models.user import User
from app.components.sidebar import sidebar


def create_user_modal() -> rx.Component:
    """Modal for creating a new user."""
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.content(
            rx.radix.primitives.dialog.title("Create New User"),
            rx.radix.primitives.dialog.description(
                "Fill in the details to create a new user account.", class_name="mb-4"
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.label("Full Name", class_name="text-sm font-medium"),
                    rx.el.input(
                        placeholder="John Doe",
                        name="name",
                        class_name="w-full mt-1 p-2 border rounded-md",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label("Email", class_name="text-sm font-medium"),
                    rx.el.input(
                        placeholder="user@example.com",
                        type="email",
                        name="email",
                        class_name="w-full mt-1 p-2 border rounded-md",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label("Password", class_name="text-sm font-medium"),
                    rx.el.input(
                        placeholder="********",
                        type="password",
                        name="password",
                        class_name="w-full mt-1 p-2 border rounded-md",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label("Role", class_name="text-sm font-medium"),
                    rx.el.select(
                        ["patient", "doctor", "admin"],
                        default_value="patient",
                        name="role",
                        class_name="w-full mt-1 p-2 border rounded-md",
                    ),
                    class_name="mb-4",
                ),
                on_submit=AdminState.create_user,
                reset_on_submit=True,
            ),
            rx.el.div(
                rx.el.button(
                    "Cancel",
                    on_click=lambda: AdminState.set_is_modal_open(False),
                    class_name="rounded-md bg-white px-3.5 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50",
                    type="button",
                ),
                rx.el.button(
                    "Create User",
                    type="submit",
                    class_name="rounded-md bg-blue-600 px-3.5 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-500",
                ),
                class_name="flex justify-end gap-3 mt-4",
            ),
            style={"max_width": "450px"},
        ),
        open=AdminState.is_modal_open,
        on_open_change=AdminState.set_is_modal_open,
    )


def user_table_row(user: User) -> rx.Component:
    """A row in the user management table."""
    return rx.el.tr(
        rx.el.td(
            user.name,
            class_name="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900",
        ),
        rx.el.td(
            user.email, class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
        ),
        rx.el.td(
            rx.el.span(
                user.role.capitalize(),
                class_name=rx.cond(
                    user.role == "admin",
                    "px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800",
                    rx.cond(
                        user.role == "doctor",
                        "px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800",
                        "px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800",
                    ),
                ),
            ),
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        rx.el.td(
            rx.el.button(
                "Edit", class_name="text-blue-600 hover:text-blue-900 text-sm"
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right text-sm font-medium",
        ),
    )


def admin_dashboard() -> rx.Component:
    """Dashboard for the admin user role."""
    page_content = rx.el.div(
        create_user_modal(),
        rx.el.header(
            rx.el.div(
                rx.el.h1(
                    "Admin Dashboard", class_name="text-2xl font-bold text-gray-900"
                ),
                rx.el.p(
                    "Manage users and system settings.", class_name="text-gray-500"
                ),
            ),
            rx.el.button(
                "Create User",
                on_click=lambda: AdminState.set_is_modal_open(True),
                class_name="rounded-md bg-blue-600 px-3.5 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-500",
            ),
            class_name="flex items-center justify-between py-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h3("All Users", class_name="text-lg font-semibold"),
                rx.el.div(
                    rx.el.div(
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    rx.el.th(
                                        "Name",
                                        scope="col",
                                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Email",
                                        scope="col",
                                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Role",
                                        scope="col",
                                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        rx.el.span("Actions", class_name="sr-only"),
                                        scope="col",
                                        class_name="relative px-6 py-3",
                                    ),
                                )
                            ),
                            rx.el.tbody(
                                rx.foreach(AdminState.all_users, user_table_row),
                                class_name="bg-white divide-y divide-gray-200",
                            ),
                            class_name="min-w-full divide-y divide-gray-200 table-auto",
                        ),
                        class_name="-my-2 overflow-x-auto sm:-mx-6 lg:-mx-8",
                    ),
                    class_name="py-2 align-middle inline-block min-w-full sm:px-6 lg:px-8",
                ),
                class_name="mt-8 flex flex-col",
            ),
            class_name="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg bg-white p-4 sm:p-6",
        ),
    )
    return sidebar(main_content=page_content)