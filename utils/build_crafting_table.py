import logging
import sys
import json


# logging.basicConfig(stream=sys.stdout, level=logging.ERROR)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

with open(sys.argv[1], 'r', encoding="utf-8") as jsonfile:
    try:
        parsed = json.load(jsonfile)
    except ImportError:
        sys.exit("\033[0;31mInvalid JSON File :\033[00m " + sys.argv[1])

print("\033[0;32mValid JSON File :\033[00m " + sys.argv[1])
#print(json.dumps(parsed, indent=2, sort_keys=True))

#
# return a list of crafting benches
#
def get_bench_list():
    bench_list = set()

    for recipe in parsed["Rows"]:
        for r_bench in recipe["RecipeSets"]:
            bench_list.add(r_bench['RowName'])

    return sorted(bench_list)

#
# return a list of raw_items used at a spcific bench
#
def get_raw_items(BENCHNAME):
    raw_items = set()
    craft_items = set()


    #
    # The Skinning_Bench is (currently) the only bench that provides more Outputs then the Inputs
    # Needed a way to swap the inputs/outputs
    #

    INPUTS = "Inputs"
    OUTPUTS = "Outputs"

    if BENCHNAME == 'Skinning_Bench':
        INPUTS = "Outputs"
        OUTPUTS = "Inputs"

    # lets go through the file and go to elements under the title 'Rows' (which are the recipes)
    for recipe in parsed["Rows"]:


        # Figure out which workbench the recipe is crafted at
        for r_bench in recipe["RecipeSets"]:

            # Only build the tables the chosen workbench
            if r_bench['RowName'] == BENCHNAME:
                # Print the recipe name
                logging.debug("Recipe: %s", recipe['Name'])
                logging.debug("B: %s", r_bench['RowName'])

                # find the inputs to the recipe (loop through them all)
                for r_inputs in recipe[INPUTS]:
                    RECIPEINPUT = r_inputs['Element']['RowName']
                    RECIPEINPUTCOUNT = r_inputs['Count']
                    raw_items.add(RECIPEINPUT)
                    logging.debug("I: %sx %s", RECIPEINPUTCOUNT, RECIPEINPUT)

                # find the outputs to the recipe (loop through them all)
                # check if there are no outputs and switch to resource outputs instead
                #print(f"OutLength: {len(recipe['Outputs'])}")
                if len(recipe['Outputs']) == 0:
                    for r_outputs in recipe["ResourceOutputs"]:
                        RECIPEOUTPUT = r_outputs['Type']
                        RECIPEOUTCOUNT = r_outputs['RequiredUnits']
                        craft_items.add(RECIPEOUTPUT)
                        logging.debug("O: %sx %s", RECIPEOUTCOUNT, RECIPEOUTPUT)
                else:
                    for r_outputs in recipe[OUTPUTS]:
                        RECIPEOUTPUT = r_outputs['Element']['RowName']
                        RECIPEOUTCOUNT = r_outputs['Count']
                        craft_items.add(RECIPEOUTPUT)
                        logging.debug("O: %sx %s", RECIPEOUTCOUNT, RECIPEOUTPUT)

                logging.debug("\n")

    logging.debug("%s\n%s\n", len(raw_items), raw_items)
    logging.debug("%s\n%s\n", len(craft_items), craft_items)
    # logging.debug("\n")

    return sorted(raw_items)


#
# Given Crafting Bench name generate CSV output
#
def gen_csv_output(BENCHNAME):

    (raw_items) = get_raw_items(BENCHNAME)

    # Now we have a list of raw_items (items used for crafting) and the size of that list
    num_of_raw_items = len(raw_items)

    #
    # The Skinning_Bench is (currently) the only bench that provides more Outputs then the Inputs
    # Needed a way to swap the inputs/outputs
    #

    INPUTS = "Inputs"
    OUTPUTS = "Outputs"

    if BENCHNAME == 'Skinning_Bench':
        INPUTS = "Outputs"
        OUTPUTS = "Inputs"

    #
    # Output the CSV header
    #
    OUTLIST=str(raw_items)[1:-1].replace('\'','')    # strip any single quotes
    print(f"({BENCHNAME}) - Recipe Name, Output, Output Qty, {OUTLIST}")


    #
    # Build CSV list with the given header
    #

    # lets go through the file and go to elements under the title 'Rows' (which are the recipes)
    for recipe in parsed["Rows"]:

        # Create and empty list based on the number of raw items
        recipe_list = [''] * num_of_raw_items

        # Figure out which workbench the recipe is crafted at
        for r_bench in recipe["RecipeSets"]:

            # Only build the tables the chosen workbench
            if r_bench['RowName'] == BENCHNAME:
                #print(f"B: {r_bench['RowName']}")

                # find the inputs to the recipe (loop through them all)
                for r_inputs in recipe[INPUTS]:
                    RECIPEINPUT = r_inputs['Element']['RowName']
                    RECIPEINPUTCOUNT = r_inputs['Count']
                    #print(f"I: {RECIPEINPUTCOUNT}x {RECIPEINPUT}")
                    # find the location of the item in the raw_items set
                    item_index=raw_items.index(RECIPEINPUT)
                    # update the recipe_list list with the qty at the appropriate index location
                    recipe_list[item_index]=RECIPEINPUTCOUNT

                # find the outputs to the recipe (loop through them all)
                # check if there are no outputs and switch to resource outputs instead
                if len(recipe[OUTPUTS]) == 0:
                    for r_outputs in recipe["ResourceOutputs"]:
                        RECIPEOUTPUT = r_outputs['Type']
                        RECIPEOUTCOUNT = r_outputs['RequiredUnits']
                        #print(f"O: {r_outputs['RequiredUnits']}x {r_outputs['Type']}")
                else:
                    for r_outputs in recipe[OUTPUTS]:
                        RECIPEOUTPUT = r_outputs['Element']['RowName']
                        RECIPEOUTCOUNT = r_outputs['Count']
                        #print(f"O: {r_outputs['Count']}x {r_outputs['Element']['RowName']}")

                # Output CSV for the recipe
                OUTLIST=str(recipe_list)[1:-1].replace('\'','')     # strip any single quotes
                print(f"{recipe['Name']}, {RECIPEOUTPUT}, {RECIPEOUTCOUNT}, {OUTLIST}")

    print(f"\n")

    return


###############################################################################
# main
###############################################################################

# BENCHNAME = 'Character'
# BENCHNAME = 'Campfire'
# BENCHNAME = 'Crafting_Bench'
# BENCHNAME = 'Drying_Rack'
# BENCHNAME = 'Skinning_Bench'

#
# If crafting bench is passed on the command line, use it
# ?FIXME? probably a better way to pull & validate the bench argument
#
if len(sys.argv) == 3 :
    BENCHNAME=sys.argv[2]
    gen_csv_output(BENCHNAME)
else:
    for BENCHNAME in get_bench_list():
        gen_csv_output(BENCHNAME)
