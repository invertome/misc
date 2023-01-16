import argparse
import ged4py
import matplotlib.pyplot as plt
import os

# Set up command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--ged", help="GEDCOM file to read in", required=True)
parser.add_argument("--id", help="ID of individual to create family tree for", required=True)
parser.add_argument("--gen", help="Number of generations to include in the plot", default=3)
parser.add_argument("--clean", help="Only display ancestors' names", default=False, action="store_true")
parser.add_argument("--out", help="Output folder for the plots and text files")
args = parser.parse_args()

with ged4py.parser.Parser(args.ged) as parser:
    tree = ged4py.model.Gedcom(parser)

# Create plot
fig, ax = plt.subplots()
ax.set_title("Family Tree of {}".format(args.id))

# Get ancestors for the individual
ind = tree.get_individual(args.id)
ancestors = ind.get_ancestors(gen=args.gen)

for ancestor in ancestors:
    if args.clean:
        ax.text(ancestor.x_coord, ancestor.y_coord, ancestor.name)
    else:
        ax.text(ancestor.x_coord, ancestor.y_coord, ancestor.name + ": " + ancestor.get_birth_date().get_value() + ' ' + ancestor.get_birth_place().get_value())

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
    plt.savefig(args.out + "/family_tree.pdf")
else:
    plt.show()

# create a text file based family tree
with open(args.out + "/family_tree.txt", "w") as f:
    for ancestor in ancestors:
        f.write(ancestor.get_name().get_value() + ": " + ancestor.get_birth_date().get_value() + ' ' + ancestor.get_birth_place().get_value() + "\n")

# create more detailed version of the text file
with open(args.out + "/family_tree_detailed.txt", "w") as f:
    for ancestor in ancestors:
        f.write(ancestor.get_name().get_value() + '\n')
        f.write('Birth: '+ ancestor.get_birth_date().get_value() + ' ' + ancestor.get_birth_place().get_value() + '\n')
        f.write('Marriage: '+ ancestor.get_marriage_date().get_value() + ' ' + ancestor.get_marriage_place().get_value() + '\n')
        f.write('Death: '+ ancestor.get_death_date().get_value() + ' ' + ancestor.get_death_place().get_value() + '\n\n')

