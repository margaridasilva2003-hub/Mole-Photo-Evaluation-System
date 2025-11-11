import reflex as rx
from app.states.auth_state import AuthState


def nav_item(icon: str, text: str, href: str) -> rx.Component:
    """A single navigation item in the sidebar."""
    is_active = rx.State.router.page.raw_path == href.split("?")[0]
    return rx.el.a(
        rx.icon(icon, class_name="h-5 w-5"),
        rx.el.span(text, class_name="truncate"),
        href=href,
        class_name=rx.cond(
            is_active,
            "flex items-center gap-3 rounded-lg bg-gray-100 px-3 py-2 text-gray-900 transition-all hover:text-gray-900",
            "flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 transition-all hover:text-gray-900",
        ),
    )


def mobile_sidebar() -> rx.Component:
    """The sidebar for mobile view, which is a drawer that slides from the left."""
    return rx.el.div(
        rx.radix.primitives.dialog.root(
            rx.radix.primitives.dialog.trigger(
                rx.el.button(
                    rx.icon("menu", class_name="h-6 w-6"),
                    class_name="p-2 rounded-md hover:bg-gray-100 md:hidden",
                    variant="ghost",
                )
            ),
            rx.radix.primitives.dialog.portal(
                rx.radix.primitives.dialog.overlay(
                    class_name="fixed inset-0 bg-black/50 z-40"
                ),
                rx.radix.primitives.dialog.content(
                    rx.el.div(
                        rx.radix.primitives.dialog.close(
                            rx.el.div(
                                rx.icon(
                                    "flask-conical", class_name="h-8 w-8 text-blue-600"
                                ),
                                rx.el.span(
                                    "MoleScope", class_name="text-xl font-semibold"
                                ),
                                class_name="flex items-center gap-2 p-4 border-b",
                            )
                        ),
                        rx.radix.primitives.dialog.close(
                            rx.el.nav(
                                nav_item("layout-dashboard", "Dashboard", "/"),
                                nav_item("settings", "Settings", "/settings"),
                                class_name="flex-1 flex flex-col items-start p-4 text-sm font-medium gap-2",
                            )
                        ),
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.el.p(
                                    AuthState.user_name,
                                    class_name="text-sm font-semibold",
                                ),
                                rx.el.p(
                                    AuthState.user_role.to_string().capitalize(),
                                    class_name="text-xs text-gray-500",
                                ),
                                class_name="grid gap-0.5",
                            ),
                            rx.el.button(
                                rx.icon("log-out", class_name="h-4 w-4"),
                                on_click=AuthState.logout,
                                class_name="ml-auto rounded-md p-2 hover:bg-gray-100",
                                variant="ghost",
                            ),
                            class_name="flex items-center gap-2",
                        ),
                        class_name="mt-auto p-4 border-t",
                    ),
                    class_name="flex flex-col h-full bg-white p-0 m-0 w-64 z-50",
                    style={"position": "fixed", "top": 0, "bottom": 0, "left": 0},
                ),
            ),
        ),
        class_name="md:hidden",
    )


def sidebar(main_content: rx.Component) -> rx.Component:
    """A sidebar component that wraps the main content of a page."""
    return rx.el.div(
        rx.el.aside(
            rx.el.div(
                rx.el.div(
                    rx.icon("flask-conical", class_name="h-8 w-8 text-blue-600"),
                    rx.el.span("MoleScope", class_name="text-xl font-semibold"),
                    class_name="flex items-center gap-2 p-4 border-b",
                ),
                rx.el.nav(
                    nav_item("layout-dashboard", "Dashboard", "/"),
                    nav_item("settings", "Settings", "/settings"),
                    class_name="flex-1 flex flex-col items-start p-4 text-sm font-medium gap-2",
                ),
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            AuthState.user_name, class_name="text-sm font-semibold"
                        ),
                        rx.el.p(
                            AuthState.user_role.to_string().capitalize(),
                            class_name="text-xs text-gray-500",
                        ),
                        class_name="grid gap-0.5",
                    ),
                    rx.el.button(
                        rx.icon("log-out", class_name="h-4 w-4"),
                        on_click=AuthState.logout,
                        class_name="ml-auto rounded-md p-2 hover:bg-gray-100",
                        variant="ghost",
                    ),
                    class_name="flex items-center gap-2",
                ),
                class_name="mt-auto p-4 border-t",
            ),
            class_name="hidden border-r bg-gray-50/40 md:flex md:flex-col w-64 h-screen",
        ),
        rx.el.div(
            rx.el.header(
                mobile_sidebar(), class_name="flex items-center h-14 px-4 border-b"
            ),
            rx.el.main(
                main_content, class_name="flex-1 p-4 sm:p-6 lg:p-8 overflow-y-auto"
            ),
            class_name="flex flex-col flex-1",
        ),
        class_name="flex min-h-screen w-full bg-white",
    )