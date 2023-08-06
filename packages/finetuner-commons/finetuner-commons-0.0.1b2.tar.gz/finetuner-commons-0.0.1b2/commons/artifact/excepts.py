class ArtifactNotFound(Exception):
    ...


class CorruptedArtifact(Exception):
    ...


class CorruptedMetadata(Exception):
    ...


class NoSuchModel(Exception):
    ...


class SelectModelRequired(Exception):
    ...


class CorruptedONNXModel(Exception):
    ...
