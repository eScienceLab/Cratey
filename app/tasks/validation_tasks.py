"""Tasks and helper methods for processing RO-Crate validation."""

# Author: Alexander Hambley
# License: MIT
# Copyright (c) 2025 eScience Lab, The University of Manchester

import logging
import os

from rocrate_validator import services

from app.celery_worker import celery
from app.utils.minio_utils import fetch_ro_crate_from_minio
from app.utils.webhook_utils import send_webhook_notification

logger = logging.getLogger(__name__)


@celery.task
def process_validation_task_by_id(
    crate_id: str, profile_name: str | None, webhook_url: str | None
) -> None:
    """
    Background task to process the RO-Crate validation by ID.

    :param crate_id: The ID of the RO-Crate to validate.
    :param profile_name: The name of the validation profile to use. Defaults to None.
    :param webhook_url: The webhook URL to send notifications to. Defaults to None.
    :raises Exception: If an error occurs during the validation process.

    :todo: Replace the Crate ID with a more comprehensive system, and replace profile name with URI.
    """

    file_path = None

    try:
        # Fetch the RO-Crate from MinIO using the provided ID:
        file_path = fetch_ro_crate_from_minio(crate_id)

        logging.info(f"Processing validation task for {file_path}")

        # Perform validation:
        validation_result = perform_ro_crate_validation(file_path, profile_name)

        # TODO: Prepare validation result and update RO-Crate on MinIO with the validation status
        # TODO: Prepare the data to send to the webhook, and send the webhook notification.

    except Exception as e:
        logging.error(f"Error processing validation task: {e}")

        # Send failure notification via webhook
        error_data = {"profile_name": profile_name, "error": str(e)}
        send_webhook_notification(webhook_url, error_data)

    finally:
        # Clean up the temporary file if it was created:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)


def perform_ro_crate_validation(file_path: str, profile_name: str | None) -> str | None:
    """
    Validates an RO-Crate using the provided file path and profile name.
    :param file_path: The path to the RO-Crate file to validate
    :param profile_name: The name of the validation profile to use. Defaults to None. If None, the CRS4 validator will
        attempt to determine the profile.
    :return: A string containing the validation result.
    :raises Exception: If an error occurs during the validation process.
    """
    try:
        logging.info(f"Validating {file_path} with profile {profile_name}")

        full_file_path = os.path.join(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            ),
            file_path,
        )
        settings = services.ValidationSettings(
            data_path=full_file_path,
            rocrate_uri=full_file_path,
            # Only include profile_identifier if the profile_name is provided:
            **({"profile_identifier": profile_name} if profile_name else {}),
        )

        result = services.validate(settings)

        if not result.has_issues():
            logging.info(f"RO Crate {file_path} is valid.")
            # TODO: Return to update RO Crate on MinIO with validation status.

        else:
            logging.info(f"RO Crate {file_path} is invalid.")
            # TODO: Return to implement invalid RO Crate logic.

            for issue in result.get_issues():
                print(
                    f'Detected issue of severity {issue.severity.name} with check "{issue.check.identifier}": {issue.message}'
                )

    except Exception as e:
        logging.error(f"Unexpected error during validation: {e}")
        return str(e)
