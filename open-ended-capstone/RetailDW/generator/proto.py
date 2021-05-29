from collections import namedtuple
from .InStoreOperationalSystem import InStoreOperationalSystem
from .ECommerceOperationalSystem import ECommerceOperationalSystem
from .ProductOperationalSystem import ProductOperationalSystem
from .Generator import Generator
from ..sqltypes import Table
from ..product import PRODUCT_TABLE

GeneratorItem = namedtuple("GeneratorItem", ["table_object", "n_inserts", "n_updates"])

eCommerceOpSystem = ECommerceOperationalSystem() 
inStoreOpSystem = InStoreOperationalSystem() 
productOpSystem = ProductOperationalSystem()

# Associate tables with operational systems;  
eCommerceOpSystem.add_tables([PRODUCT_TABLE]) 
# inStoreOpSystem.add_tables([table1, table2])
# productOpSystem.add_tables([table1, table2])

b = GeneratorItem(PRODUCT_TABLE, 5, 50)

gen = Generator()
gen.run(b)

for batch in batch_list:
    gen.run(batch)
    # ping ETL service to do daily update
    # work on CSV coordination later
    #  get user input for next day will allow me to test incremental before rest service 

gen.close()
## what is my ETL going to do?

eCommerceOpSystem.remove_tables([table1, table2]) 
inStoreOpSystem.remove_tables([table1, table2])
inventoryOpSystem.remove_tables([table1, table2])


