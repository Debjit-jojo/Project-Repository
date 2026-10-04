"""Flask application for Image Processing Lab."""

import os
import time

from flask import Flask, request, render_template, redirect, url_for

from backend import (
    PRACTICALS,
    POST_LABS,
    OP_INFO,
    calculate_statistics,
    image_to_base64,
    process_image,
    read_uploaded_image,
)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 12 * 1024 * 1024


def page_context(**overrides):
    """Shared template values for the lab page."""
    context = {
        "practicals": PRACTICALS,
        "post_labs": POST_LABS,
        "op_info": OP_INFO,
        "selected_operation": "rgb",
        "selected_operation_name": "RGB Image",
        "operation_info": OP_INFO["rgb"],
        "output_image": None,
        "statistics": None,
        "processing_message": None,
        "error_message": None,
    }
    context.update(overrides)
    return context


@app.route("/")
def home():
    return redirect(url_for("index"))


@app.route("/lab")
def index():
    return render_template("index.html", **page_context())


@app.route("/process", methods=["POST"])
def process():
    start_time = time.perf_counter()
    operation = request.form.get("operation", "rgb")
    selected_name = operation

    for practical in PRACTICALS:
        for op_id, op_name in practical["operations"]:
            if op_id == operation:
                selected_name = op_name

    for op_id, op_name in POST_LABS:
        if op_id == operation:
            selected_name = op_name

    try:
        image = read_uploaded_image(request.files.get("image"))

        second_image = None
        second_file = request.files.get("second_image")
        if second_file and second_file.filename:
            second_image = read_uploaded_image(second_file)

        result, message = process_image(
            image, operation, request.form, second_image
        )

        elapsed = time.perf_counter() - start_time
        output_base64 = image_to_base64(result)
        statistics = calculate_statistics(result)
        message += f" Processing time: {elapsed:.3f} seconds."

        return render_template(
            "index.html",
            **page_context(
                selected_operation=operation,
                selected_operation_name=selected_name,
                operation_info=OP_INFO.get(
                    operation, "Image processing operation."
                ),
                output_image=output_base64,
                statistics=statistics,
                processing_message=message,
            ),
        )

    except Exception as error:
        elapsed = time.perf_counter() - start_time
        return render_template(
            "index.html",
            **page_context(
                selected_operation=operation,
                selected_operation_name=selected_name,
                operation_info=OP_INFO.get(
                    operation, "Image processing operation."
                ),
                processing_message=f"Processing time: {elapsed:.3f} seconds.",
                error_message=str(error),
            ),
        )


@app.errorhandler(413)
def file_too_large(error):
    return (
        render_template(
            "index.html",
            **page_context(
                error_message=(
                    "Uploaded file is too large. Maximum allowed size is 12 MB."
                )
            ),
        ),
        413,
    )


@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for("index"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    print("Image Processing Lab starting...")
    print(f"Open http://127.0.0.1:{port}/lab")
    app.run(host="0.0.0.0", port=port, debug=False)
