#!/usr/bin/python3

"""Creates a unique instance of the FileStorage model."""

from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
