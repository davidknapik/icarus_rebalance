import sys
import json

with open(sys.argv[1], 'r') as jsonfile:
    try:
        parsed = json.load(jsonfile)
    except:
        sys.exit("\033[0;31mInvalid JSON File :\033[00m " + sys.argv[1])


#print(json.dumps(parsed, indent=2, sort_keys=True))
#print("Valid JSON file : "  + sys.argv[1])

print("\033[0;32mValid JSON File :\033[00m " + sys.argv[1])
