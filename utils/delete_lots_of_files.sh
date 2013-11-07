#!/bin/bash
find /tmp -name core -type f -print0 | xargs -0 /bin/rm -f
