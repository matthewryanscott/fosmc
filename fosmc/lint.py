import sys

from .db import load_data


def main():
	print 'lint'
	path = sys.argv[1]
	print 'path:', path
	db = load_data(path)
	sys.exit(0)


if __name__ == '__main__':
	main()
