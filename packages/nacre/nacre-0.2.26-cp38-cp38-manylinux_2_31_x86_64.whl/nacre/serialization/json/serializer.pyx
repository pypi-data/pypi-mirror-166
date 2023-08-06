from typing import Any

import orjson

from nautilus_trader.core.correctness cimport Condition
from nautilus_trader.serialization.base cimport _OBJECT_FROM_DICT_MAP
from nautilus_trader.serialization.base cimport _OBJECT_TO_DICT_MAP
from nautilus_trader.serialization.base cimport Serializer


cdef class JsonSerializer(Serializer):
    """
    Provides a serializer for the `MessagePack` specification.

    Parameters
    ----------
    timestamps_as_str : bool
        If the serializer converts `int64_t` timestamps to `str` on serialization,
        and back to `int64_t` on deserialization.
    """

    def __init__(self, bint timestamps_as_str=False):
        self.timestamps_as_str = timestamps_as_str

    cpdef bytes serialize(self, object obj):
        """
        Serialize the given object to `MessagePack` specification bytes.

        Parameters
        ----------
        obj : object
            The object to serialize.

        Returns
        -------
        bytes

        Raises
        ------
        RuntimeError
            If `obj` cannot be serialized.

        """
        Condition.not_none(obj, "obj")


        cdef dict obj_dict
        delegate = _OBJECT_TO_DICT_MAP.get(type(obj).__name__)
        if delegate is None:
            if hasattr(obj, "to_dict") and callable(getattr(obj, "to_dict")):
                obj_dict = obj.to_dict()
            else:
                raise RuntimeError("cannot serialize object: unrecognized type")
        else:
            obj_dict = delegate(obj)

        cdef str field_name
        if self.timestamps_as_str:
            for field_name in ("ts_event", "ts_init", "ts_last", "ts_opened", "ts_closed"):
                field = obj_dict.get(field_name)
                if field is not None:
                    obj_dict[field_name] = str(field)

        for key, value in obj_dict.items():
            if type(value) == bytes:
                try:
                    obj_dict[key] = orjson.loads(value)
                except orjson.JSONDecodeError as e:
                    del obj_dict[key]

        return orjson.dumps(obj_dict)

    cpdef object deserialize(self, bytes obj_bytes):
        """
        Deserialize the given `MessagePack` specification bytes to an object.

        Parameters
        ----------
        obj_bytes : bytes
            The object bytes to deserialize.

        Returns
        -------
        Instrument

        Raises
        ------
        RuntimeError
            If `obj_bytes` cannot be deserialized.

        """
        Condition.not_none(obj_bytes, "obj_bytes")

        cdef dict obj_dict = orjson.loads(obj_bytes)  # type: dict[str, Any]
        if self.timestamps_as_str:
            ts_event = obj_dict.get("ts_event")
            if ts_event is not None:
                obj_dict["ts_event"] = int(ts_event)

            ts_init = obj_dict.get("ts_init")
            if ts_init is not None:
                obj_dict["ts_init"] = int(ts_init)

        delegate = _OBJECT_FROM_DICT_MAP.get(obj_dict["type"])
        if delegate is None:
            raise RuntimeError("cannot deserialize object: unrecognized type")

        return delegate(obj_dict)
