# test arguments from command line
import sys
import RetailDW.demo1 as demo1

if __name__ == '__main__':

    print(f"Arguments count: {len(sys.argv)}")
    for i, arg in enumerate(sys.argv):
        print(f"Argument {i:>6}: {arg}")

    demo1.run()