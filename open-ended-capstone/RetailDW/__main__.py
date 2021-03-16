import sys
from RetailDW.demo import demo1

demos_available = {'demo1' : (demo1, "Initial and incremental load of source system")}

if len(sys.argv) > 1:
    arg1 = sys.argv[1]
    if arg1 in demos_available:
        demo = demos_available[arg1][0]
        demo()
    else:
        print(f"{arg1} not found\n")
else:
    print("Usage RetailDW [demo name]")
    print("Available demo(s) are:")
    print(*demos_available.keys())
