from flask import Blueprint, request, jsonify, Response
from werkzeug.utils import secure_filename
import tempfile
import os

from app.tasks.validation_tasks import (
    process_validation_task_by_id,
    process_validation_task_by_zip,
)


ro_crates_bp = Blueprint("ro_crates", __name__)


@ro_crates_bp.route("/validate_by_id", methods=["POST"])
def validate_ro_crate_from_id() -> tuple[Response, int]:
    """
    Endpoint to validate an RO-Crate using its ID from MinIO.

    This function extracts the crate ID, profile name, and webhook URL from the request form data and queues a
    background task to perform the validation.

    :return: A JSON response with a success message and HTTP 202 status if the validation task is successfully
        queued, or an error message with an appropriate status code in case of an error.
    """
    # Extract request data:

    crate_id = request.form.get("id")
    profile_name = request.form.get("profile_name")
    webhook_url = request.form.get("webhook_url")

    if not crate_id or not profile_name or not webhook_url:
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        # Queue the background task
        process_validation_task_by_id.delay(crate_id, profile_name, webhook_url)

        return jsonify({"message": "Validation in progress"}), 202

    except Exception as e:
        return jsonify({"error": str(e)}), 500
