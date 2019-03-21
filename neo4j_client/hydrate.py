# coding:utf-8
import logging

is_integer = lambda x: isinstance(x, int)
is_numeric = lambda x: isinstance(x, (int, float, complex))
is_string = lambda x: isinstance(x, str)


def hydrate(data):
    """ simple Hydrate a dictionary of data
    :arg data: dictionary of data to hydrate

    """
    if isinstance(data, dict):
        if "self" in data:
            # 暂时不处理
            return data
        elif "nodes" in data and "relationships" in data:
            # 暂时不处理
            return data

        elif "columns" in data and "data" in data:
            return RecordList.hydrate(data)
        elif "neo4j_version" in data:
            return data
        elif "exception" in data and ("stacktrace" in data or "stackTrace" in data):
            message = data.pop("message", "The server returned an error")
            raise Exception(message)
        else:
            logging.warning("Map literals returned over the Neo4j REST interface are ambiguous "
                            "and may be hydrated as graph objects")
            return data

    else:
        return data


class TextTable(object):

    @classmethod
    def cell(cls, value, size):
        if value == "#" or is_numeric(value):
            text = str(value).rjust(size)
        else:
            text = str(value).ljust(size)
        return text

    def __init__(self, header, border=False):
        self.__header = list(map(str, header))
        self.__rows = []
        self.__widths = list(map(len, self.__header))
        self.__repr = None
        self.border = border

    def __repr__(self):
        if self.__repr is None:
            widths = self.__widths
            if self.border:
                lines = [
                    " " + " | ".join(self.cell(value, widths[i]) for i, value in enumerate(self.__header)) + "\n",
                    "-" + "-+-".join("-" * widths[i] for i, value in enumerate(self.__header)) + "-\n",
                ]
                for row in self.__rows:
                    lines.append(" " + " | ".join(self.cell(value, widths[i]) for i, value in enumerate(row)) + "\n")
            else:
                lines = [
                    " ".join(self.cell(value, widths[i]) for i, value in enumerate(self.__header)) + "\n",
                ]
                for row in self.__rows:
                    lines.append(" ".join(self.cell(value, widths[i]) for i, value in enumerate(row)) + "\n")
            self.__repr = "".join(lines)
        return self.__repr

    def append(self, row):
        row = list(row)
        self.__rows.append(row)
        self.__widths = [max(self.__widths[i], len(str(value))) for i, value in enumerate(row)]
        self.__repr = None


class Record(object):
    """ A simple object containing values from a single row of a Cypher
    result. Each value can be retrieved by column position or name,
    supplied as either an index key or an attribute name.

    Consider the record below::

           | person                     | name
        ---+----------------------------+-------
         1 | (n1:Person {name:"Alice"}) | Alice

    If this record is named ``r``, the following expressions
    are equivalent and will return the value ``'Alice'``::

        r[1]
        r["name"]
        r.name

    """

    __producer__ = None

    def __init__(self, values):
        self.__values__ = tuple(values)
        columns = self.__producer__.columns
        for i, column in enumerate(columns):
            setattr(self, column, values[i])

    def __repr__(self):
        out = ""
        columns = self.__producer__.columns
        if columns:
            table = TextTable(columns, border=True)
            table.append([getattr(self, column) for column in columns])
            out = repr(table)
        return out

    def __eq__(self, other):
        try:
            return vars(self) == vars(other)
        except TypeError:
            return tuple(self) == tuple(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __len__(self):
        return len(self.__values__)

    def __iter__(self):
        return iter(self.__values__)

    def __getitem__(self, item):
        if is_integer(item):
            return self.__values__[item]
        elif is_string(item):
            return getattr(self, item)
        else:
            raise LookupError(item)


class RecordList(object):
    """ A list of records returned from the execution of a Cypher statement.
    """
    @classmethod
    def hydrate(cls, data):
        columns = data["columns"]
        rows = data["data"]
        producer = RecordProducer(columns)
        return cls(columns, [producer.produce(hydrate(row)) for row in rows])

    def __init__(self, columns, records):
        self.columns = columns
        self.records = records
        logging.info("result %r %r", columns, len(records))

    def __repr__(self):
        out = ""
        if self.columns:
            table = TextTable([None] + self.columns, border=True)
            for i, record in enumerate(self.records):
                table.append([i + 1] + list(record))
            out = repr(table)
        return out

    def __len__(self):
        return len(self.records)

    def __getitem__(self, item):
        return self.records[item]

    def __iter__(self):
        return iter(self.records)

    @property
    def one(self):
        """ The first record from this result, reduced to a single value
        if that record only consists of a single column. If no records
        are available, :const:`None` is returned.
        """
        try:
            record = self[0]
        except IndexError:
            return None
        else:
            if len(record) == 0:
                return None
            elif len(record) == 1:
                return record[0]
            else:
                return record


class RecordProducer(object):

    def __init__(self, columns):
        self.__columns = tuple(column for column in columns if not column.startswith("_"))
        self.__len = len(self.__columns)
        dct = dict.fromkeys(self.__columns)
        dct["__producer__"] = self
        self.__type = type(str("Record"), (Record,), dct)

    def __repr__(self):
        return "RecordProducer(columns=%r)" % (self.__columns,)

    def __len__(self):
        return self.__len

    @property
    def columns(self):
        return self.__columns

    def produce(self, values):
        """ Produce a record from a set of values.
        """
        return self.__type(values)


if __name__ == '__main__':
    data = {'columns': ['cnt'], 'data': [[66]]}
    result = hydrate(data)
    print(result)
    print(type(result))
    print(result[0]["cnt"])
