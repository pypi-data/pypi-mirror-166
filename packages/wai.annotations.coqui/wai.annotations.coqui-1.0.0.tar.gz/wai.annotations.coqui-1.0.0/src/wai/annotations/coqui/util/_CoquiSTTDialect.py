import csv


class CoquiSTTDialect(csv.Dialect):
    """
    The dialect of Coqui STT CSV files.
    """
    delimiter = ','
    quotechar = '"'
    escapechar = None
    doublequote = None
    skipinitialspace = False
    lineterminator = '\n'
    quoting = csv.QUOTE_MINIMAL
