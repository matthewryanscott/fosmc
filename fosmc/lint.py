import sys

from fosmc.db import load_data


def lint(db):
    found_lint = False
    for data_type, objects in db.iteritems():
        for slug, obj in objects.iteritems():
            for key, value in obj.iteritems():
                if key.startswith('lint_'):
                    lint_type = key[5:]
                    print 'type={data_type} slug={slug} lint={lint_type}'.format(**locals())
                    found_lint = True
    return found_lint


def main():
    if len(sys.argv) != 2:
        print 'Usage: fosmc-lint <DATABASE-PATH>'
        sys.exit(1)
    path = sys.argv[1]
    db = load_data(path)
    sys.exit(1 if lint(db) else 0)


if __name__ == '__main__':
    main()
