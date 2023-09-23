from typing import Optional

import pandas as pd

from pb24exporter.record import Record


class XlsxExporterStrategy:
    def __init__(self, filename: str, chunk_size: int = 1000, columns: Optional[list[str]] = None):
        self._filename = filename
        self._chunk_size = chunk_size
        self._buffer = []
        self._current_row = 0
        self._columns = columns or None

    def save(self, rec: Record) -> None:
        self._buffer.append(rec)
        if len(self._buffer) >= self._chunk_size:
            self.flush()

    def flush(self) -> None:
        df = pd.DataFrame(self._buffer)
        if self._current_row == 0:
            self._write_new(df)
        else:
            self._write_append(df)
        print(f"flushed {len(self._buffer)}")
        self._buffer = []

    def close(self) -> None:
        if self._buffer:
            self.flush()

    def _write_new(self, df):
        with pd.ExcelWriter(self._filename, mode="w") as writer:
            df.to_excel(writer, index=False)
        self._current_row += len(df) + 1
        if self._columns is None:
            self._columns = df.columns

    def _write_append(self, df):
        df = df[self._columns]
        with pd.ExcelWriter(self._filename, mode="a", if_sheet_exists="overlay") as writer:
            df.to_excel(writer, index=False, startrow=self._current_row, header=False)
        self._current_row += len(df)
