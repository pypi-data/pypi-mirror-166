import csv


class CoquiTTSDialect(csv.Dialect):
    """
    The dialect of Coqui STT CSV files.
    """
    delimiter = '|'
    quotechar = None
    escapechar = None
    doublequote = None
    skipinitialspace = False
    lineterminator = '\n'
    quoting = csv.QUOTE_NONE
