#!/usr/bin/env python

import argparse
import sys
import time
from .helpers import * 

def main(): 

  parser = argparse.ArgumentParser()
  parser.add_argument("repo_name", help="githubuser/repo")
  parser.add_argument("-g", "--generate-html", action='store_true', help="Generate output as HTML")
  parser.add_argument("-l", "--limit", help="Limit to the last x Issues/Pull Requests", type=int, default=0)
  parser.add_argument("-c", "--show-contributors", action='store_true', help="Output the code contributors as well")
  parser.add_argument("-n", "--show-names", action='store_true', help="")
  parser.add_argument("-o", "--open", help="TESTING - load code/non-code from file") #, type=argparse.FileType('r'))
  parser.add_argument("-s", "--save", help="TESTING - save code/non-code to file") #, type=argparse.FileType('w'))
  args = parser.parse_args()  

  repo_name = args.repo_name

  if args.open:
      contents = json.load(open(args.open))
      code_contributors = contents["code"]
      non_code_contributors = contents["non_code"]

  else: 
    if not repo_exists(repo_name): 
      print("Repo does not exist: %s" % repo_name)
      sys.exit(1)

    code_contributors = get_code_contributors(repo_name)
    code_commentors = get_code_commentors(repo_name, args.limit)

    non_code_contributors = []
    for user in code_commentors:
      user_name, avatar, name = user 
      if user not in code_contributors:
        non_code_contributors.append(user)

  if args.save:
    contents = { 'code': code_contributors, 'non_code': non_code_contributors }
    f = open(args.save, "w")
    f.write(json.dumps(contents))
    f.close

  print("Code contributions: %d" % len(code_contributors))

  if args.show_contributors:
    for user in code_contributors: 
      display_user_name(user, args)
    print()
  
  print("Non-code contributions: %d" % len(non_code_contributors))

  for user in non_code_contributors: 
    display_user_name(user, args)

  if args.generate_html:

    if not args.show_contributors and len(non_code_contributors) == 0:
      print("No non-code contributors for %s. No HTML output being generated." % repo_name)
      sys.exit(0)

    html_file = "%s_contrib.html" % repo_name.replace("/", "_")
    f = open(html_file, "w")

    f.write("<style>div.contributors > div {display:inline-block; padding: 10px;} div.contributors > div > div { text-align: center; padding: 5px} footer {padding-top: 40px}</style>")
    f.write("<h1>Non-code contributions for %s</h1>" % repo_name)
    f.write("<div class='contributors'>")

    for user in non_code_contributors: 
      f.write(display_user_html(user, args))
    f.write("</div>")
  
    if args.show_contributors:
      f.write("<h1>Code contributions for %s</h1>\n" % repo_name)
      f.write("<div class='contributors'>")
      for user in code_contributors:
        f.write(display_user_html(user, args))
      f.write("</div>")

    f.write("<footer>")
    gen_time = time.strftime('%Y-%m-%d %H:%M:%S %Z', time.gmtime())
    f.write("Generated by <a href='https://github.com/glasnt/octohat'>octohat</a> at %s" % gen_time)
    if args.limit > 0:
      f.write("<br>Results limited to the most recent %d issues/pull requests." % args.limit)
    f.write("</footer>")
    
    f.close()

    print("Generated HTML representation, saved to %s" % html_file)

if __name__ == "__main__":
    main()
