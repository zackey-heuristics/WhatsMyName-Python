#!/usr/bin/env python3
# File name       : whatsmyname.py
# By              : C3n7ral051nt4g3ncy (aka OSINT Tactical) https://github.com/C3n7ral051nt4g3ncy
# Usage           : 1.Scan for Username | 2.Current supported sites list | 3.Total number of sites | 4. Single Search
# Version         : Version 1.1
# Support         : Please do not support me, Support this project --> https://github.com/WebBreacher/WhatsMyName
#
# ----------------------------------------------------------------------
# Modified by     : zackey-heuristics https://github.com/zackey-heuristics
# Modification on : 2025-02-06
# Changes         : 
# 1. Added quiet mode for logging: implemented a mode that outputs only essential logs.
# 2. Added option for JSON output: introduced an option to output results in JSON format.
# 3. Added output destination option: implemented an option to specify the output destination.
# ----------------------------------------------------------------------

import argparse
import contextlib
import datetime
import json
import sys
import time

import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError


# script banner
def banner():
    print(
        """\033[39m\033[1m
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⢀⠀⠀⣰⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⠃⣾⣿⡄⠹⢿⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⣶⣤⣼⣿⣿⣿⣿⣶⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀   ⢀⣴⡶⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣟⢿⠇⢀ ⣶⡆⢰⣶⣄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀  ⢀⣴⡿⠋⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣇⢻⣿⣮⣀ ⣘⠻⠀  ⠙⢿⣷⣄⠀⠀⠀⠀⠀
⠀⠀⠀ ⢀⣴⡿⠋⠀⠀⠀⠀⠀⠀⠀⠈⠉⣽⣿⣿⣿⣌⠛⠻⠿⠿⠿⠇⠀⠀⠀⠀⠀⠀ ⠙⢿⣷⣄⠀⠀⠀
⠀⢀⣴⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⢿⣿⣿⡖⣰⣶⠂⠀⠀⠀⠀⠀⠀⠀⠀ ⠀ ⠙⢿⣷⣄⠀
⠀⠻⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⡀⠈⠙⢠⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀ ⢀⣴⣿⠟⠀
⠀⠀ ⠈⠻⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡇⠀⢀⣿⡟⣰⡄⠀⠀⠀⠀⠀⠀⠀ ⢀⣴⣿⠟⠁⠀⠀
⠀⠀⠀⠀  ⠈⠻⣿⣦⡀⠀⠀⠀⠀⠀⢀⣿⣿⠇⠀⣾⡿⢠⣿⡇⠀⠀⠀⠀⠀⢀⣴⣿⠟⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀   ⠈⠻⣿⣦⠀⠀⠀⢸⣿⣿⠀⣼⣿⠁⠈⠉⠀⠀⠀⠀⢰⣿⠟⠁⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⠙⠉⠀⠙⠁⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠀
             < WebBreacher >
         \033[32m\033[1m
       ╦ ╦┬ ┬┌─┐┌┬┐┌─┐╔╦╗┬ ┬╔╗╔┌─┐┌┬┐┌─┐
       ║║║├─┤├─┤ │ └─┐║║║└┬┘║║║├─┤│││├┤ 
       ╚╩╝┴ ┴┴ ┴ ┴ └─┘╩ ╩ ┴ ╝╚╝┴ ┴┴ ┴└─┘ Version 1.2
        \033[39m\033[1m
       by C3n7ral051nt4g3ncy
       github.com/WebBreacher/WhatsMyName\n\n
      \033[32m\033[1mUsage: python3 whatsmyname.py -h\033[0m\n\n"""
    )

def check_site(site, username, headers):
    site_name = site["name"]
    uri_check = site["uri_check"].format(account=username)
    try:
        res = requests.get(uri_check, headers=headers, timeout=10)
        estring_pos = site["e_string"] in res.text
        estring_neg = site["m_string"] in res.text

        if res.status_code == site["e_code"] and estring_pos and not estring_neg:
            return site_name, uri_check
    except:
        pass
    return None

#generate .HTML Report at the end of the username scan
def generate_html_report(username, found_sites):
    html_content = f"""
    <html>
    <head>
        <title>WhatsMyName Report for {username}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>
    <body>
        <h1>WhatsMyName Report for {username}</h1>
        <table>
            <tr>
                <th>Website Name</th>
                <th>Profile URL</th>
            </tr>"""
    for site_name, uri_check in found_sites:
        html_content += f"""
            <tr>
                <td>{site_name}</td>
                <td><a href="{uri_check}" target="_blank">{uri_check}</a></td>
            </tr>"""
    html_content += """
        </table>
    </body>
    </html>"""

    with open(f"whatsmyname_report_{username}.html", "w") as report_file:
        report_file.write(html_content)


def output_destination(value):
    """
    If the user passes 'stdout' or 'stderr', return the corresponding stream.
    Otherwise, treat the value as a filename and attempt to open it for writing.
    """
    if value.lower() == 'stdout':
        return sys.stdout
    elif value.lower() == 'stderr':
        return sys.stderr
    else:
        try:
            # Open the file for writing.
            return open(value, 'w')
        except Exception as e:
            raise argparse.ArgumentTypeError(f"Cannot open file '{value}' for writing: {e}")

# main
if __name__ == "__main__":
    # Argparse arguments
    parser = argparse.ArgumentParser(
        description="Scan all sites on Project WhatsMyName for a target username "
                    "and wait for\033[32m\033[1m positive\033[0m identification."
    )

    parser.add_argument(
        "-u", "--username", help="\033[32m\033[1m\nTarget Username \033[0m"
    )

    parser.add_argument(
        "-s",
        "--singlesearch",
        nargs="*",
        help="\033[32m\033[1m\nSingle site search\033[0m",
    )

    parser.add_argument(
        "-f",
        "--fulllist",
        action="store_true",
        help="\033[32m\033[1m\nView full sites list on Project WMN | Find site name before doing a single search\033[0m\n\n",
    )

    parser.add_argument(
        "-c",
        "--countsites",
        action="store_true",
        help="\033[32m\033[1m\nNumber of sites currently supported on Project WhatsMyName\033[0m\n",
    )
    
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="\033[32m\033[1m\nQuiet mode: output only essential logs\033[0m\n",
    )
    
    parser.add_argument(
        "-j",
        "--json",
        action="store_true",
        help="\033[32m\033[1m\nOutput results in JSON format\033[0m\n",
    )
    
    parser.add_argument(
        "-o",
        "--output",
        type=output_destination,
        default=sys.stdout,
        help="\033[32m\033[1m\nOutput result destination: specify a filename, 'stdout' for standard output, or 'stderr' for standard error.\033[0m\n",
    )
    
    # args settings
    args = parser.parse_args()
    
    username = args.username
    singlesearch = args.singlesearch
    countsites = args.countsites
    fulllist = args.fulllist
    is_quiet = args.quiet
    json_output_enabled = args.json
    output = args.output
    
    with contextlib.ExitStack() as stack:
        if output not in (sys.stdout, sys.stderr):
            stack.callback(output.close)

        if not json_output_enabled or not is_quiet:
            banner()
        headers = {
            "Accept": "text/html, application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-language": "en-US;q=0.9,en,q=0,8",
            "accept-encoding": "gzip, deflate",
            "user-Agent": "Mozilla/5.0 (Windows NT 10.0;Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        }
        try:
            # Fetch wmn-data from WhatsMyName repository
            response = requests.get("https://raw.githubusercontent.com/WebBreacher/WhatsMyName/main/wmn-data.json")
            # Raise an exception if the response status code is not 200
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"HTTPError - Failed to fetch data from WhatsMyName repository: {e}", file=sys.stderr)
            sys.exit(1)
        except requests.exceptions.Timeout as e:
            print(f"TimeoutError - Failed to fetch data from WhatsMyName repository: {e}", file=sys.stderr)
            sys.exit(1)
        except requests.exceptions.RequestException as e:
            print(f"RequestException - Failed to fetch data from WhatsMyName repository: {e}", file=sys.stderr)
            sys.exit(1)

        try:
            data = response.json()
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON data: {e}", file=sys.stderr)
            sys.exit(1)
        except ValueError as e:
            print(f"Failed to parse JSON data: {e}", file=sys.stderr)
            sys.exit(1)

        found_sites = []

        
        # Get full list of sites supported on Project WhatsMyName
        if fulllist:
            for i in tqdm(range(10)):
                time.sleep(0.06)
            for site in data["sites"]:
                site_name = site["name"]
                print(
                    f"""
        ╔════════════════╦══════════════════════════════════╗
        ║ WEBSITE NAME:  ║ ✅   \033[1m{site_name}                       
        ╚════════════════╩══════════════════════════════════╝"""
                )

        # Get exact number of sites supported on Project WhatsMyName
        if countsites:
            for i in tqdm(range(10)):
                time.sleep(0.1)
            search_word = "uri_check"
            total = sum(1 for site in data["sites"] if search_word in site)
            print(
                "\033[32m\033[1mTotal Number\033[0m\033[32m of sites currently supported on \033[1mProject WhatsMyName --> ",
                total,
            )

        # Scan all websites for the username 
        if username:
            sites = data["sites"]

            total_sites = len(sites)
            found_sites = []

            try:
                with ThreadPoolExecutor(max_workers=20) as executor:
                    futures = {executor.submit(check_site, site, username, headers): site for site in sites}

                    with tqdm(total=total_sites, desc="Checking sites", disable=is_quiet) as pbar:
                        completed = 0
                        for future in as_completed(futures):
                            try:
                                result = future.result()
                                if result:
                                    site_name, uri_check = result
                                    found_sites.append((site_name, uri_check))
                                    if not is_quiet:
                                        print("\033[32m" + "-" * 133)
                                        print(f"\033[32m[+] \033[1mTarget found\033[0m\033[32m ✓ on: \033[1m{site_name}\033[0m")
                                        print(f"\033[32m[+] Profile URL: {uri_check}\033[0m")
                                        print("\033[32m" + "-" * 133)
                            except:
                                pass
                            finally:
                                completed += 1
                                pbar.n = completed
                                pbar.refresh()

            except TimeoutError:
                print("Some sites took too long to respond and were skipped.", file=sys.stderr)

            # Ensure the progress bar reaches 100%
            pbar.n = total_sites
            pbar.refresh()

            if not is_quiet:
                print("\nChecked all sites.")
                
            if found_sites:
                if json_output_enabled:
                    # Tuple to dictionary conversion
                    found_site_dict = {
                        "results": {},
                        "created_at_rfc3339": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    }
                    for site_name, uri_check in found_sites:
                        found_site_dict["results"][site_name] = uri_check
                    json.dump(found_site_dict, output, indent=4)
                    if not is_quiet:
                        print(f"\nJSON output generated: {output.name}")
                else:            
                    print(f"\nThe user \033[1m{username}\033[0m was found on {len(found_sites)} sites:", file=output)
                    for site_name, uri_check in found_sites:
                        print(f"- \033[32m{site_name}\033[0m: {uri_check}", file=output)

                    # Generate HTML report
                    generate_html_report(username, found_sites)
                    if not is_quiet:
                        print(f"\nHTML report generated: whatsmyname_report_{username}.html")
            else:
                print(f"\nNo sites found for the user \033[1m{username}\033[0m.")

