import argparse
import ged4py
import matplotlib.pyplot as plt
import os

# Set up command line arguments
parser = argparse.ArgumentParser(description="Create a family tree plot from a GEDCOM file.")
parser.add_argument("--ged", help="GEDCOM file to read in", required=True)
parser.add_argument("--id", help="ID of individual to create family tree for", required=True)
parser.add_argument("--gen", help="Number of generations to include in the plot", default=3)
parser.add_argument("--clean", help="Only display ancestors' names", default=False, action="store_true")
parser.add_argument("--out", help="Output folder for the plots and text files")
parser.add_argument("--format", help="Output format for the plots and text files (pdf, text, both)", default="both", choices=["pdf", "text", "both"])
args = parser.parse_args()

# Load GEDCOM file
try:
    with ged4py.GedcomFile.from_file(args.ged) as gedcom_file:
        tree = ged4py.Model.from_gedcom(gedcom_file)
except Exception as e:
    print(f"An error occurred while trying to parse the GEDCOM file: {e}")
    sys.exit(1)
    
# Get the individual and their ancestors
ind = tree.get_individual_by_pointer(args.id)
if not ind:
    print(f"Could not find individual with id {args.id} in GEDCOM file.")
    sys.exit(1)
ancestors = ind.get_ancestors(gen=args.gen)
ancestors = ancestors[:100] # limiting the number of generations to 100

# Create plot
fig, ax = plt.subplots()
ax.set_title("Family Tree of {}".format(ind.name))

for ancestor in ancestors:
    if args.clean:
        ax.text(ancestor.x_coord, ancestor.y_coord, ancestor.name)
    else:
        # Get birth date, birth place, marriage date, marriage place, death date, death place
        birth_date = ancestor.get_birth_date().get_value() if ancestor.get_birth_date() else 'N/A'
        birth_place = ancestor.get_birth_place().get_value() if ancestor.get_birth_place() else 'N/A'
        marriage_date = ancestor.get_marriage_date().get_value() if ancestor.get_marriage_date() else 'N/A'
        marriage_place = ancestor.get_marriage_place().get_value() if ancestor.get_marriage_place() else 'N/A'
        death_date = ancestor.get_death_date().get_value() if ancestor.get_death_date() else 'N/A'
        death_place = ancestor.get_death_place().get_value() if ancestor.get_death_place() else 'N/A'
        ax.text(ancestor.x_coord, ancestor.y_coord, ancestor.name + ": " + birth_date + ' ' + birth_place + ' ' + marriage_date + ' ' + marriage_place + ' ' + death_date + ' ' + death_place)

    # Handle repeated ancestors due to endogamy
repeated_ancestors = set()
for ancestor in ancestors:
    if ancestor.get_id().get_value() in repeated_ancestors:
        # Link ancestor to itself with a faint line
        ax.annotate("", xy=(ancestor.x_coord, ancestor.y_coord), xytext=(repeated_ancestors[ancestor.get_id().get_value()][0], repeated_ancestors[ancestor.get_id().get_value()][1]),
                    arrowprops=dict(facecolor='gray', alpha=0.3))
    else:
        repeated_ancestors.add(ancestor.get_id().get_value())

# Output the plot to a folder
if args.out:
    if not os.path.exists(args.out):
        os.mkdir(args.out)
    if args.format in ("pdf", "both"):
        plt.savefig(args.out + "/family_tree.pdf")
else:
    if args.format in ("pdf", "both"):
        plt.show()

# create a text file based family tree
if args.format in ("text", "both"):
    with open(args.out + "/family_tree.txt", "w") as f:
        for ancestor in ancestors:
            birth_date = ancestor.get_birth_date().get_value() if ancestor.get_birth_date() else 'N/A'
            birth_place = ancestor.get_birth_place().get_value() if ancestor.get_birth_place() else 'N/A'
            marriage_date = ancestor.get_marriage_date().get_value() if ancestor.get_marriage_date() else 'N/A'
            marriage_place = ancestor.get_marriage_place().get_value() if ancestor.get_marriage_place() else 'N/A'
            death_date = ancestor.get_death_date().get_value() if ancestor.get_death_date() else 'N/A'
            death_place = ancestor.get_death_place().get_value() if ancestor.get_death_place() else 'N/A'
            f.write(ancestor.get_name().get_value() + ": " + birth_date + ' ' + birth_place + ' ' + marriage_date + ' ' + marriage_place + ' ' + death_date + ' ' + death_place + "\n")

# create more detailed version of the text file
if args.format in ("text", "both"):
    with open(args.out + "/family_tree_detailed.txt", "w") as f:
        for ancestor in ancestors:
            birth_date = ancestor.get_birth_date().get_value() if ancestor.get_birth_date() else 'N/A'
            birth_place = ancestor.get_birth_place().get_value() if ancestor.get_birth_place() else 'N/A'
            marriage_date = ancestor.get_marriage_date().get_value() if ancestor.get_marriage_date() else 'N/A'
            marriage_place = ancestor.get_marriage_place().get_value() if ancestor.get_marriage_place() else 'N/A'
            death_date = ancestor.get_death_date().get_value() if ancestor.get_death_date() else 'N/A'
            death_place = ancestor.get_death_place().get_value() if ancestor.get_death_place() else 'N/A'
            f.write(ancestor.get_name().get_value() + '\n')
            f.write('Birth: '+ birth_date + ' ' + birth_place + '\n')
            f.write('Marriage: '+ marriage_date + ' ' + marriage_place + '\n')
            f.write('Death: '+ death_date + ' ' + death_place + '\n\n')

