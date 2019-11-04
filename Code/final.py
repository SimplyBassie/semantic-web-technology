import sys
import recall
import precision

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 swt_final.py text.txt [--precision or --recall]", file = sys.stderr)
    else:
        evaluation_method = sys.argv[2]
        if evaluation_method == '--recall':
            recall.main()
        elif evaluation_method == '--precision':
            precision.main()
        else:
            print("Usage: python3 swt_final.py text.txt [--precision or --recall]", file = sys.stderr)


if __name__ == '__main__':
    main()
