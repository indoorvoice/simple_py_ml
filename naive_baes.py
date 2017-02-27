# Naive Baes: Naive implementation of a simple NB classifier in base python.
# Uses dictionaries for basically everything. Currently does not handle integers sensibly.
# Mostly an exercise in using dictionaries. Intended as a first draft.
from collections import defaultdict

file = 'swimming_nv_tutorial_bigger.csv'
# file = input('Please specify the name of the file to read in:\n')
class_dict = {} # holds the names of the target classes
con_tab = defaultdict(lambda: defaultdict(int))
class_counts = defaultdict(int) # holds class counts, used to calculate probabilities
class_probabilities = {}

# reads the first line as headers, does basic parsing, populates class dict.
with open(file) as f:
    first_line = f.readline()
    first_line = first_line.split(',')
    num_cols = len(first_line)
    for i, class_name in enumerate(first_line):
        class_dict[i] = class_name.strip('\n') + '_' # {5: 'rainy'}, used to index later

    # takes each line, parses, then makes an entry for that combination
    total_rows = 0
    for line_count, other_lines in enumerate(f):
        other_lines = other_lines.split(',')
        for i, elem in enumerate(other_lines):
            elem = elem.strip('\n')
            target_class = other_lines[num_cols-1].strip('\n')
            con_tab[target_class][class_dict[i] + elem] += 1

        line_count += 1
        class_counts[target_class] += 1

    # take line count, modify class class to get class probabilities
    for outcome in class_counts.keys():
        class_probabilities[outcome] = (class_counts[outcome] / line_count)
    print(class_probabilities)

# divide each entry in the contingency table by its probability
# i.e. {'yes': {'rain_none': 40} where yes = 100 becomes {'rain_none': .4}
# update is used to modify in place.
for each_dict in con_tab:
    con_tab[each_dict].update({k: (v/class_counts[each_dict])
                               for k, v in con_tab[each_dict].items()})

# data = input('Please input new data, separated by commas. Headings are: \n')
data = 'moderate, moderate, warm, light, some'
data = data.replace(' ', '').split(',')

# copy class_counts with 0 values to give us a new class dict.
# class_counts could just be overwritten to save space but that's not necessary
probabilities = {k: 1 for k, v in class_counts.items()}

# take each data value, take each outcome in the data, product the outcomes
# and return the value with the largest probability
# if a value not in training data occurs, prints notice and sets class prob to 0
for i, value in enumerate(data):
    for outcome in con_tab:
        try:
            probabilities[outcome] *= con_tab[outcome][class_dict[i] + value]
        except:
            print('value:', value, 'not recognised. P('+ outcome + ') = 0.')
            probabilities[outcome] *= 0
            continue


# revise naming: ensure logic is correct. Can it be folded into upper loop?
for probability in class_probabilities:
    probabilities[probability] *= class_probabilities[probability]

print('Predicted class:', max(probabilities))
