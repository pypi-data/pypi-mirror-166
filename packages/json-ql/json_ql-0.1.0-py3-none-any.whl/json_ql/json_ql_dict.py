from typing import Any, Dict
from collections.abc import MutableMapping
from .driver import JSONQL


class JSONQLDict(MutableMapping):

    def __init__(self, mapping: Dict = None) -> None:
        self.dict_store = mapping if mapping is not None else {}
        self.json_ql_obj = JSONQL(self.dict_store)
   
    def __getitem__(self, key: str) -> Any:
        """
        query the json same way as JSONQL
        with dict like syntax
        """
        return self.json_ql_obj.pick(key=key).exec()

    def __setitem__(self, __k: Any, __v: Any) -> None:
        """
        Read only: not implemented
        """
        raise NotImplementedError("Read Only: Setting value is not currently supported")

    def __delitem__(self, __v: Any) -> None:
        """
        Read only: not implemented
        """
        raise NotImplementedError("Read Only: Deleting value is not currently supported")

    def __len__(self) -> int:
        """
        Use the passed dictionary __len__
        """
        return self.dict_store.__len__()

    def __iter__(self) -> Any:
        """
        Use the passed dictionary __iter__
        """
        return self.dict_store.__iter__()

    def __repr__(self) -> str:
        """
        Use the passed dictionary __repr__
        """
        return self.dict_store.__repr__()
