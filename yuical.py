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
from requests import get
from re import findall
from icalendar import Calendar


class YUiCalException(Exception):
    pass

DIR_TEMPLATE = "%s_%s_%s"
REGEX = "%s_[^\.]+\.ics"
REGEX_NUMBER = "%s_[^_]+_%s_[^\.]+\.ics"

def search(args):
    dirName = DIR_TEMPLATE % (args.year, args.faculty, args.subject)
    r = get("%s/%s" % (ROOT, dirName))
    if r.status_code != 200:
        raise YUiCalException("Get directory failed, status code (%s)"
                                  % r.status_code)
    if args.number:
        regex = REGEX_NUMBER % (dirName, args.number)
    else:
        regex = REGEX % dirName
    courses = findall(regex, r.text)
    courses = [c[:-4] for c in courses]
    print "\n".join(courses)
    return


def calculate_time(event):
    start = event['DTSTART'].dt
    end = event['DTEND'].dt
    return end - start

def display(code):
    dirName = code[:12]
    print dirName, code
    r = get("%s/%s/%s.ics" % (ROOT, dirName, code))
    if r.status_code != 200:
        raise YUiCalException("Get ical failed, status code (%s)"
                                  % r.status_code)
    ical = Calendar.from_ical(r.text)
    for component in ical.walk('vevent'):
        for item in component.sorted_items():
            if item[0] in ('SUMMARY', 'LOCATION', 'UID'):
                print '%s: %s' % (item[0], item[1])
            if item[0] == 'RECURRENCE-ID':
                reoccur_item = item[1]
                print reoccur_item.params
                print reoccur_item.dt
                continue
            if item[0] in ('DTSTART', 'DURATION', 'DTEND'):
                print '%s: %s' % (item[0], item[1].dt)                
                continue
            if item[0] in ('RRULE'):
                print '%s: %s' % (item[0], item[1])                
                continue
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
        display(args.code)

                
        
