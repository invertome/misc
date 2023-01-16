import argparse
import gedcom
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

# Read in GEDCOM file and create family tree
ged = gedcom.parse(args.ged)
tree = gedcom.FamilyTree(ged)
ind = tree.individuals[args.id]
ancestors = ind.get_ancestors(gen=args.gen)

# Create plot
fig, ax = plt.subplots()
ax.set_title("Family Tree of {}".format(ind.name))
for ancestor in ancestors:
    if args.clean:
        ax.text(ancestor.x_coord, ancestor.y_coord, ancestor.name)
    else:
        ax.text(ancestor.x_coord, ancestor.y_coord, ancestor.name + ": " + str(ancestor.birth))

# Handle repeated ancestors due to endogamy
repeated_ancestors = set()
for ancestor in ancestors:
    if ancestor.id in repeated_ancestors:
        # Link ancestor to itself with a faint line
        ax.annotate("", xy=(ancestor.x_coord, ancestor.y_coord), xytext=(repeated_ancestors[ancestor.id][0], repeated_ancestors[ancestor.id][1]),
                    arrowprops=dict(facecolor='gray', alpha=0.3))
    else:
        repeated_ancestors[ancestor.id] = (ancestor.x_coord, ancestor.y_coord)

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
        f.write(ancestor.name + ": " + str(ancestor.birth) + "\n")
        
# create more detailed version of the text file
with open(args.out + "/family_tree_detailed.txt", "w") as f:
    for ancestor in ancestors:
        f.write(ancestor.name + '\n')
        f.write('Birth: '+ ancestor.birth_date + ' ' + ancestor.birth_place + '\n')
        f.write('Marriage: '+ ancestor.marriage_date + ' ' + ancestor.marriage_place + '\n')
        f.write('Death: '+ ancestor.death_date + ' ' + ancestor.death_place + '\n\n')

# create different versions of the family tree plot
for i in range(1, args.gen+1):
    fig, ax = plt.subplots()
    ax.set_title("Family Tree of {} - Generation {}".format(ind.name, i))
    for ancestor in ancestors:
        if args.clean:
            ax.text(ancestor.x_coord, ancestor.y_coord, ancestor.name)
        else:
            ax.text(ancestor.x_coord, ancestor.y_coord, ancestor.name + ": " + str(ancestor.birth))
    plt.savefig(args.out + "/family_tree_gen_{}.pdf".format(i))
