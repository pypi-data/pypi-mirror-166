from nautilus_trader.serialization.base cimport Serializer


cdef class JsonSerializer(Serializer):
    cdef readonly bint timestamps_as_str
    """If the serializer converts timestamp int64_t to str.\n\n:returns: `bool`"""
