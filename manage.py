#!/usr/bin/env python
import os
import sys
import eventlet


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'airdjango.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    eventlet.monkey_patch()
    main()
