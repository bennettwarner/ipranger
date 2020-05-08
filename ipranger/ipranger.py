#! /usr/bin/env python3
import ipcalc
import math
import random
import argparse
import time
from socket import inet_aton, inet_ntoa

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

version = "2005"
header = bcolors.WARNING+r'''
  _____ _____  _____                             
 |_   _|  __ \|  __ \                            
   | | | |__) | |__) |__ _ _ __   __ _  ___ _ __ 
   | | |  ___/|  _  // _` | '_ \ / _` |/ _ \ '__|
  _| |_| |    | | \ \ (_| | | | | (_| |  __/ |   
 |_____|_|    |_|  \_\__,_|_| |_|\__, |\___|_|   
                                  __/ |          
  ''' + bcolors.OKBLUE + '''By @b_e_n    Version: ''' + version + bcolors.WARNING + \
  '''      |___/           \n'''+bcolors.ENDC


def sample_size_calc(N):
    z = 1.96  # Z Score 95% industry standard
    e = .01  # margin of error
    p = 0.5  # sample proportion
    return math.ceil(((z**2 * p * (1-p))/(e ** 2))/(1+((z**2*p*(1-p))/(e**2*N))))

def ips_from_cidr(cidr):
    population_ips = []
    for x in ipcalc.Network(cidr):
        population_ips.append(str(x))
    return population_ips

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output",
                        nargs='?',
                        help="Specify where to write the hosts file. Defaults to ./ipranger-[date].txt",
                        default="./ipranger-{}.txt".format(time.strftime("%Y%m%d-%H%M%S")))
    parser.add_argument("-i", "--input",
                        nargs='?',
                        help="Specify a CIDR range. (eg. 192.168.0.1/24)")
    args = parser.parse_args()
    if not args.output or not args.input:
        print(header)
        parser.print_help()
        exit()
    population_ips = ips_from_cidr(args.input)
    sample_size = sample_size_calc(len(population_ips))
    sample_ips = random.sample(population_ips, k=sample_size)
    sample_ips = list(map(inet_ntoa, sorted(map(inet_aton, sample_ips))))
    print(header)
    print("{} IP addresses were identified in {}{}{}.".format(len(population_ips), bcolors.OKGREEN, args.input, bcolors.ENDC))
    print("{} of those IP addresses were randomly selected as a sample.".format(len(sample_ips)))
    print("This sample represents the original IP block with a 1% margin of error.\n")
    print("Outputting hosts file to {}{}{}".format(bcolors.OKGREEN, args.output, bcolors.ENDC))
    with open(args.output, "w") as outfile:
        outfile.write("\n".join(sample_ips))


if __name__ == '__main__':
    main()