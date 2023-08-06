import argparse
from configparser import ConfigParser

def read_user_cli_args():
  
    parser = argparse.ArgumentParser(prog ='gfg',
                                     description ='GfG article demo package.')
  
    parser.add_argument('integers', metavar ='N', type = int, nargs ='+',
                        help ='an integer for the accumulator')
    parser.add_argument('-greet', action ='store_const', const = True,
                        default = False, dest ='greet',
                        help ="Greet Message from Geeks For Geeks.")
    parser.add_argument('--sum', dest ='accumulate', action ='store_const',
                        const = sum, default = max,
                        help ='sum the integers (default: find the max)')
  
    args = parser.parse_args()
  
    if args.greet:
        print("Welcome to GeeksforGeeks !")
        if args.accumulate == max:
            print("The Computation Done is Maximum")
        else:
            print("The Computation Done is Summation")
        print("And Here's your result:", end =" ")   
  
    print(args.accumulate(args.integers))

def test():
    print("Hello World")


# if __name__ == "__main__":
#     test()