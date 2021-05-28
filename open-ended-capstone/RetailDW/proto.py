class Generator:
    pass

eCommerceOpSystem = ECommerceOpSystem() 
inStoreOpSystem = InStoreOpSystem() 
inventoryOpSystem = InventoryOpSystem()

# Associate tables with operational systems;  
eCommerceOpSystem.add_tables([table1, table2]) 
inStoreOpSystem.add_tables([table1, table2])
inventoryOpSystem.add_tables([table1, table2])

gen = Generator()

for batch in batch_list:
    gen.run(batch)
    # ping ETL service to do daily update
    # work on CSV coordination later
    #  get user input for next day will allow me to test incremental before rest service 


## what is my ETL going to do?



