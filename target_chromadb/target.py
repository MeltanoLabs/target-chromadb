"""Chroma target class."""

from __future__ import annotations

from singer_sdk import typing as th
from singer_sdk.target_base import Target

from target_chromadb.sinks import (
    ChromaSink,
)


class TargetChroma(Target):
    """Sample target for Chroma."""

    name = "target-chromadb"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "collection_name",
            th.StringType,
            required=True,
            default="vector-db",
        ),
        th.Property(
            "db_directory",
            th.StringType,
            required=True,
            default="output",
        ),
        th.Property(
            "document_text_property",
            th.StringType,
            description="The property containing the document text.",
            default="page_content",
            required=True,
        ),
        th.Property(
            "embeddings_property",
            th.StringType,
            description="The property containing the embeddings.",
            default="embeddings",
        ),
        th.Property(
            "metadata_property",
            th.StringType,
            description="The property containing the document metadata.",
            default="metadata",
        ),
    ).to_dict()

    default_sink_class = ChromaSink


if __name__ == "__main__":
    TargetChroma.cli()
