#!/usr/bin/env python
#
# yuical - program to search and display contents of ical files from
# http://ical.uit.yorku.ca
# Coyright (c) 2018 Neal Stephenson neal at yorku dot ca
#
#  This program is free software: you can redistribute it and/or
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

ROOT = 'http://ical.uit.yorku.ca/'

from logging import basicConfig, DEBUG, debug
from argparse import ArgumentParser

class YUiCalException(Exception):
    pass


def search(args):
    return

def list(args):
    return


if __name__ == "__main__":
    basicConfig(level=DEBUG)
    debug("Staring up")
    parser = ArgumentParser(description='Program to search and display ical files')
    parser.add_argument('-y', '--year',
                            help='year to search')
    parser.add_argument('-f', '--faculty',
                            help='faculty to search')
    parser.add_argument('-s', '--subject',
                            help='subject to search')
    parser.add_argument('-n', '--number',
                            help='course number to search')
    parser.add_argument('-c', '--code',
                            help='course code to parse')
    args = parser.parse_args()
    debug("Args: %s" % args)
    if args.year or args.faculty or args.subject:
        errs = []
        if not args.year:
            errs.append("A year is requried")
        if not args.faculty:
            errs.append("A faculty is requried")
        if not args.subject:
            errs.append("A subject is requried")
        if errs:
            print "Error: %s" % ','.join(errs)
            parser.help()
            exit(1)
        else:
            search(args)
    if args.code:
        display(args)

                
        
