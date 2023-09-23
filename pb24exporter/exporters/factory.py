import typing

from pb24exporter.record import Record


class ExporterStrategy(typing.Protocol):
    def save(self, rec: Record) -> None:
        ...

    def flush(self) -> None:
        ...

    def close(self) -> None:
        ...


def create_exporter(format, path) -> ExporterStrategy:
    if format == "xlsx":
        from pb24exporter.exporters.xlsx import XlsxExporterStrategy

        return XlsxExporterStrategy(path, chunk_size=100)
    else:
        raise ValueError(f"Unknown format: {format}")
