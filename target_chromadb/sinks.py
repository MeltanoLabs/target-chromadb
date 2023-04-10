"""Chroma target sink class, which handles writing streams."""

from __future__ import annotations

import chromadb
from singer_sdk.sinks import BatchSink


class ChromaSink(BatchSink):
    """Chroma target sink class."""

    max_size = 10000  # Max records to write in one batch

    def start_batch(self, context: dict) -> None:
        """Start a batch.

        Developers may optionally add additional markers to the `context` dict,
        which is unique to this batch.

        Args:
            context: Stream partition or context dictionary.
        """
        self.client = chromadb.Client(
            chromadb.config.Settings(
                chroma_db_impl="duckdb+parquet",
                persist_directory=self.chroma_directory,
            )
        )
        # try:
        self.collection = self.client.create_collection(
            self.collection_name,
            embedding_function=self.embedding_function,
            get_or_create=True,
        )
        # except ValueError as ex:
        #     self.logger.warn(str(ex))
        #     self.collection = self.client.get_collection(
        #         self.config["collection_name"],
        #         embedding_function=self.embedding_function,
        #     )

    @property
    def embedding_function(self) -> str | None:
        return None

    @property
    def collection_name(self) -> str:
        return self.config["collection_name"]

    @property
    def chroma_directory(self) -> str:
        return self.config["db_directory"]

    @property
    def document_text_property(self) -> str:
        return self.config["document_text_property"]

    @property
    def metadata_property(self) -> str:
        return self.config["metadata_property"]

    @property
    def embeddings_property(self) -> str:
        return self.config["embeddings_property"]

    def process_record(self, record: dict, context: dict) -> None:
        """Process the record.

        Developers may optionally read or write additional markers within the
        passed `context` dict from the current batch.

        Args:
            record: Individual record in the stream.
            context: Stream partition or context dictionary.
        """
        self.collection.add(
            embeddings=[record[self.embeddings_property]],
            metadatas=[record[self.metadata_property]],
            documents=[record[self.document_text_property]],
            ids=[":".join([record[key] for key in self.key_properties])],
        )

    def process_batch(self, context: dict) -> None:
        """Write out any prepped records and return once fully written.

        Args:
            context: Stream partition or context dictionary.
        """
        # Sample:
        # ------
        # client.upload(context["file_path"])  # Upload file
        # Path(context["file_path"]).unlink()  # Delete local copy
