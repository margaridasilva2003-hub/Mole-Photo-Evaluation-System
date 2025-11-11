import reflex as rx
from app.states.auth_state import AuthState
from app.states.patient_state import PatientState
from app.models.mole_image import MoleImage
from app.components.sidebar import sidebar

UPLOAD_ID = "upload_mole_images"


def status_badge(status: rx.Var[str]) -> rx.Component:
    """A badge component to display the evaluation status of an image."""
    return rx.el.div(
        rx.match(
            status,
            (
                "Pending",
                rx.el.span(
                    "Pending",
                    class_name="whitespace-nowrap rounded-md bg-yellow-100 px-2 py-1 text-xs font-medium text-yellow-800 ring-1 ring-inset ring-yellow-600/20 w-fit",
                ),
            ),
            (
                "Evaluated",
                rx.el.span(
                    "Evaluated",
                    class_name="whitespace-nowrap rounded-md bg-green-100 px-2 py-1 text-xs font-medium text-green-700 ring-1 ring-inset ring-green-600/20 w-fit",
                ),
            ),
            (
                "Archived",
                rx.el.span(
                    "Archived",
                    class_name="whitespace-nowrap rounded-md bg-gray-100 px-2 py-1 text-xs font-medium text-gray-600 ring-1 ring-inset ring-gray-500/10 w-fit",
                ),
            ),
            rx.el.span("Unknown"),
        )
    )


def image_card(image: MoleImage) -> rx.Component:
    """A card component to display an uploaded mole image and its details."""
    return rx.el.li(
        rx.el.div(
            rx.el.div(
                rx.el.image(
                    src=rx.get_upload_url(image.filename),
                    class_name="aspect-[16/9] w-full rounded-t-lg bg-gray-100 object-cover",
                ),
                class_name="group aspect-h-7 aspect-w-10 block w-full overflow-hidden rounded-t-lg bg-gray-100",
            ),
            rx.el.div(
                rx.el.div(
                    status_badge(image.status),
                    rx.el.p(
                        f"Uploaded on {image.upload_date}",
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
            class_name="relative rounded-lg border border-gray-200 bg-white shadow-sm",
        )
    )


def upload_section() -> rx.Component:
    """Component for uploading new mole images."""
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Upload New Photo", class_name="text-lg font-semibold"),
            rx.el.p(
                "Fill in your data and select images for evaluation.",
                class_name="mt-1 text-sm text-gray-600",
            ),
            class_name="pb-4 border-b border-gray-200",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.label("Age", class_name="text-sm font-medium text-gray-700"),
                rx.el.input(
                    placeholder="e.g., 34",
                    type="number",
                    on_change=PatientState.set_patient_age,
                    class_name="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm",
                    default_value=PatientState.patient_age,
                ),
            ),
            rx.el.div(
                rx.el.label("Sex", class_name="text-sm font-medium text-gray-700"),
                rx.el.select(
                    ["Male", "Female", "Other"],
                    placeholder="Select...",
                    value=PatientState.patient_sex,
                    on_change=PatientState.set_patient_sex,
                    class_name="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm",
                ),
            ),
            rx.el.div(
                rx.el.label(
                    "Social Number (Optional)",
                    class_name="text-sm font-medium text-gray-700",
                ),
                rx.el.input(
                    placeholder="e.g., 123-456-7890",
                    on_change=PatientState.set_patient_social_number,
                    class_name="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm",
                    default_value=PatientState.patient_social_number,
                ),
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-4 my-4",
        ),
        rx.upload.root(
            rx.el.div(
                rx.icon("cloud_upload", class_name="mx-auto h-12 w-12 text-gray-400"),
                rx.el.p(
                    "Drag & drop files here, or click to select files",
                    class_name="mt-2 text-sm text-gray-600",
                ),
                class_name="mt-6 flex flex-col items-center justify-center rounded-lg border-2 border-dashed border-gray-300 bg-gray-50 px-6 py-10 text-center",
            ),
            id=UPLOAD_ID,
            accept={"image/png": [".png"], "image/jpeg": [".jpg", ".jpeg"]},
            multiple=True,
            max_files=5,
            class_name="w-full cursor-pointer",
        ),
        rx.el.div(
            rx.foreach(
                rx.selected_files(UPLOAD_ID),
                lambda file: rx.el.div(
                    rx.icon("file-image", class_name="h-5 w-5 text-gray-500"),
                    rx.el.p(file, class_name="text-sm text-gray-700 truncate"),
                    class_name="flex items-center space-x-2 rounded-md border bg-gray-50 px-3 py-2",
                ),
            ),
            class_name="mt-4 space-y-2",
        ),
        rx.el.div(
            rx.el.button(
                "Clear",
                on_click=rx.clear_selected_files(UPLOAD_ID),
                class_name="rounded-md bg-white px-3.5 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50",
            ),
            rx.el.button(
                rx.cond(
                    PatientState.is_uploading,
                    rx.spinner(class_name="h-5 w-5 text-white"),
                    rx.el.span("Upload"),
                ),
                on_click=PatientState.handle_upload(
                    rx.upload_files(upload_id=UPLOAD_ID)
                ),
                disabled=PatientState.is_uploading,
                class_name="flex items-center justify-center rounded-md bg-blue-600 px-3.5 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600 disabled:opacity-50 min-w-[80px]",
            ),
            class_name="mt-6 flex justify-end space-x-3",
        ),
        class_name="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm",
    )


def patient_dashboard() -> rx.Component:
    """Dashboard for the patient user role."""
    page_content = rx.el.div(
        rx.el.header(
            rx.el.h1("My Evaluations", class_name="text-2xl font-bold text-gray-900"),
            class_name="py-6",
        ),
        rx.el.div(
            rx.el.div(upload_section(), class_name="w-full xl:w-1/3 xl:max-w-md"),
            rx.el.div(
                rx.el.div(
                    rx.el.h3("Submission History", class_name="text-lg font-semibold"),
                    class_name="pb-4",
                ),
                rx.cond(
                    PatientState.user_images.length() > 0,
                    rx.el.ul(
                        rx.foreach(PatientState.user_images, image_card),
                        class_name="grid grid-cols-1 gap-x-4 gap-y-8 sm:grid-cols-2 sm:gap-x-6 xl:grid-cols-2 2xl:grid-cols-3 xl:gap-x-8",
                    ),
                    rx.el.div(
                        rx.icon(
                            "image-off", class_name="mx-auto h-12 w-12 text-gray-400"
                        ),
                        rx.el.h3(
                            "No photos submitted",
                            class_name="mt-2 text-sm font-semibold text-gray-900",
                        ),
                        rx.el.p(
                            "Get started by uploading a new photo.",
                            class_name="mt-1 text-sm text-gray-500",
                        ),
                        class_name="relative block w-full rounded-lg border-2 border-dashed border-gray-300 p-12 text-center",
                    ),
                ),
                class_name="w-full xl:flex-1",
            ),
            class_name="flex flex-col xl:flex-row gap-8",
        ),
    )
    return sidebar(main_content=page_content)