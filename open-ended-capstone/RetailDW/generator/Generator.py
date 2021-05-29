from typing import List
from collections import namedtuple

GeneratorItem = namedtuple("GeneratorItem", ["table_object", "n_inserts", "n_updates"])

class Generator():

    def __init__(self) -> None:
        # get postgres connection
        pass

    def run(self, batch : List[GeneratorItem]) -> None:
        for b in batch:
            print(b)
            # opSystem open
            # while get next update (generator function) looping factor
                # save local
                # call opsystemUpdate
            # while get next insert (generator function)
                # save local
                # call opsystemInsert
            # opsystem close
        pass

    def close():
        pass

