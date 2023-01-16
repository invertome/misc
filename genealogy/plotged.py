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

try:
    print(f"Trying to parse GEDCOM file at: {args.ged}")
    with ged4py.parser.Parser(args.ged) as parser:
        tree = ged4py.model.Gedcom(parser)
    print("Successfully parsed GEDCOM file.")
except Exception as e:
    print("An error occurred while trying to parse the GEDCOM file:", e)
    exit()

try:
    # Create plot
    fig, ax = plt.subplots()
    ax.set_title("Family Tree of {}".format(args.id))

    # Get ancestors for the individual
    ind = tree.get_individual(args.id)
    ancestors = ind.get_ancestors(gen=args.gen)
    ancestors = ancestors[:100] # limiting the number of generations to 100
    print(f"Successfully got ancestors for individual with ID: {args.id}.")

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
            print(f"Saved family tree plot to {args.out}/family_tree.pdf")
        if args.format in ("text", "both"):
            with open(args.out + "/family_tree.txt", "w") as f:
                for ancestor in ancestors:
                    f.write(ancestor.get_name().get_value() + ": " + birth_date + ' ' + birth_place + ' ' + marriage_date + ' ' + marriage_place + ' ' + death_date + ' ' + death_place + "\n")
                print(f"Saved family tree text file to {args.out}/family_tree.txt")
    else:
        if args.format in ("pdf", "both"):
            plt.show()
            print("Displaying family tree plot.")
        if args.format in ("text", "both"):
            with open("family_tree.txt", "w") as f:
                for ancestor in ancestors:
                    f.write(ancestor.get_name().get_value() + ": " + birth_date + ' ' + birth_place + ' ' + marriage_date + ' ' + marriage_place + ' ' + death_date + ' ' + death_place + "\n")
                print("Saved family tree text file to family_tree.txt")
except Exception as e:
    print("An error occurred: ", e)
