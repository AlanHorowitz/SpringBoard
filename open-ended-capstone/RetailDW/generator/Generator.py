from .proto import TableBatch
from typing import List

class Generator():

    def __init__(self) -> None:
        # get postgres connection
        pass

    def run(self, batch : List[TableBatch]) -> None:
        for b in batch:
            pass
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

