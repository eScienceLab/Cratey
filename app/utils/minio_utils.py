"""Utility methods for interacting with MinIO."""

# Author: Alexander Hambley
# License: MIT
# Copyright (c) 2025 eScience Lab, The University of Manchester

from minio import Minio, S3Error
import os
import tempfile
import logging

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


def fetch_ro_crate_from_minio(crate_id: str) -> str:
    """
    Fetches an RO-Crate from MinIO based on the provided crate ID.
    Downloads the crate as a file and returns the local file path.

    :param crate_id: The ID of the RO-Crate to fetch from MinIO.
    :return: The local file path where the RO-Crate is saved.
    :raises S3Error: If an error occurs during the MinIO operation.
    :raises ValueError: If the required environment variables are not set.
    :raises Exception: If an unexpected error occurs during the operation.
    """
    load_dotenv()

    try:
        minio_client = Minio(
            endpoint=os.environ.get("MINIO_ENDPOINT"),
            access_key=os.environ.get("MINIO_ROOT_USER"),
            secret_key=os.environ.get("MINIO_ROOT_PASSWORD"),
            secure=False,
        )
        logging.info("MinIO client initialised successfully.")

        bucket_name = os.environ.get("MINIO_BUCKET_NAME")

        if not bucket_name:
            raise ValueError(
                "RO Crate MINIO_BUCKET_NAME is not set in the environment variables."
            )

        object_name = f"{crate_id}.zip"

        # Prepare temporary file path to store RO Crate for validation:
        temp_dir = tempfile.mkdtemp()
        file_path = os.path.join(temp_dir, object_name)

        logging.info(
            f"Fetching RO-Crate {object_name} from MinIO bucket {bucket_name}. File path: {file_path}"
        )
        minio_client.fget_object(bucket_name, object_name, file_path)
        logging.info(
            f"RO-Crate {object_name} fetched successfully and saved to {file_path}."
        )

        return file_path

    except S3Error as s3_error:
        logging.error(f"MinIO S3 Error: {s3_error}")
        raise
    except ValueError as value_error:
        logging.error(f"Configuration Error: {value_error}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error fetching RO-Crate from MinIO: {e}")
        raise
