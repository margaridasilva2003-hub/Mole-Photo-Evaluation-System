import reflex as rx
from app.states.auth_state import AuthState
from app.states.doctor_state import DoctorState
from app.models.mole_image import MoleImage
from app.pages.patient_dashboard import status_badge
from app.components.sidebar import sidebar


def evaluation_modal() -> rx.Component:
    """Modal for a doctor to view an AI-evaluated mole image."""
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.content(
            rx.radix.primitives.dialog.title("View AI Evaluation"),
            rx.radix.primitives.dialog.description(
                f"Image: {DoctorState.selected_image.filename.split('_')[-1]} for patient {DoctorState.selected_image.patient_name}",
                class_name="mb-4",
            ),
            rx.el.image(
                src=rx.get_upload_url(DoctorState.selected_image.filename),
                class_name="w-full rounded-lg mb-4 h-64 object-contain bg-gray-100",
            ),
            rx.el.div(
                rx.el.h3(
                    "Patient Information", class_name="text-md font-semibold mb-2"
                ),
                rx.el.p(f"Age: {DoctorState.selected_image.age}"),
                rx.el.p(f"Sex: {DoctorState.selected_image.sex}"),
                rx.cond(
                    DoctorState.selected_image.social_number != "",
                    rx.el.p(
                        f"Social Number: {DoctorState.selected_image.social_number}"
                    ),
                    None,
                ),
                class_name="mb-4 p-3 bg-gray-50 rounded-lg border",
            ),
            rx.el.div(
                rx.el.h3(
                    "AI Analysis Results", class_name="text-md font-semibold mb-2"
                ),
                rx.el.p(
                    f"Risk Score: {DoctorState.selected_image.evaluation_score}/10"
                ),
                rx.el.p(f"Notes: {DoctorState.selected_image.evaluation_notes}"),
                class_name="mb-6 p-3 bg-blue-50 rounded-lg border border-blue-200",
            ),
            rx.el.div(
                rx.radix.primitives.dialog.close(
                    rx.el.button(
                        "Close",
                        on_click=DoctorState.close_image_modal,
                        class_name="w-full rounded-md bg-white px-3.5 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50",
                    )
                ),
                class_name="flex justify-end",
            ),
            style={"max_width": "550px"},
        ),
        open=DoctorState.is_modal_open,
    )


def doctor_image_card(image: MoleImage) -> rx.Component:
    """Card to display a mole image for the doctor."""
    return rx.el.li(
        rx.el.div(
            rx.el.div(
                rx.el.image(
                    src=rx.get_upload_url(image.filename),
                    class_name="aspect-[16/9] w-full rounded-t-lg bg-gray-100 object-cover group-hover:opacity-75",
                ),
                class_name="group aspect-h-7 aspect-w-10 block w-full overflow-hidden rounded-t-lg bg-gray-100",
            ),
            rx.el.div(
                rx.el.div(
                    status_badge(image.status),
                    rx.el.p(
                        f"Patient: {image.patient_name}",
                        class_name="text-xs text-gray-500",
                    ),
                    class_name="flex items-center justify-between",
                ),
                rx.el.p(
                    image.filename.split("_")[-1],
                    class_name="mt-2 block truncate text-sm font-medium text-gray-900",
                ),
                class_name="p-4",
            ),
            class_name="relative rounded-lg border border-gray-200 bg-white shadow-sm cursor-pointer transition-shadow hover:shadow-md",
        ),
        on_click=lambda: DoctorState.open_image_modal(image),
    )


def doctor_dashboard() -> rx.Component:
    """Dashboard for the doctor user role."""
    page_content = rx.el.div(
        evaluation_modal(),
        rx.el.header(
            rx.el.h1(
                "Pending Evaluations", class_name="text-2xl font-bold text-gray-900"
            ),
            class_name="py-6",
        ),
        rx.cond(
            DoctorState.all_images.length() > 0,
            rx.el.ul(
                rx.foreach(DoctorState.all_images, doctor_image_card),
                class_name="grid grid-cols-1 gap-x-4 gap-y-8 sm:grid-cols-2 sm:gap-x-6 lg:grid-cols-3 xl:gap-x-8",
            ),
            rx.el.div(
                rx.icon("folder-check", class_name="mx-auto h-12 w-12 text-gray-400"),
                rx.el.h3(
                    "All caught up!",
                    class_name="mt-2 text-sm font-semibold text-gray-900",
                ),
                rx.el.p(
                    "There are no new photos to evaluate.",
                    class_name="mt-1 text-sm text-gray-500",
                ),
                class_name="relative block w-full rounded-lg border-2 border-dashed border-gray-300 p-12 text-center",
            ),
        ),
    )
    return sidebar(main_content=page_content)