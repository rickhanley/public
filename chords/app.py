# imports
import os
import datetime
import time
import sqlite3

from flask import Flask, flash, redirect, render_template, request, session, url_for

# from cs50 import SQL
from itertools import groupby
from dicts import (
    circle_of_fifths,
    scales_dict,
    guitar_neck,
    guitar_neck_flats,
)

app = Flask(__name__)

open_or_not_flag = False


# Open or not
# is called from the grid template
# takes 4 inputs. 3 from the database and also takes in fret_number after that has been calculated by a call from the template
# the function returns a boolean and simply determines if the chord shape will include
# any open notes i.e. is at the lowest position on the neck it could be.


@app.template_filter("open_or_not")
def open_or_not(root, string, fret_modifier, fret_number):
    try:
        if root in guitar_neck:
            if guitar_neck[string].index(root) == 0 and fret_number == 0:
                return True
    except ValueError:
        if guitar_neck_flats[string].index(root) == 0 and fret_number == 0:
            return True
    try:
        if guitar_neck[string].index(root) + fret_modifier == 0:
            return True
    except ValueError:
        if guitar_neck_flats[string].index(root) + fret_modifier == 0:
            return True
    else:
        return False


# intervals_from_formula
# returns a list of values which represent the chord formula
# as intervals

# each list in roots represents a string, and each entry
# represents how many intervals UP the NEXT STRING is.

# This interval list is looped over
# @app.template_filter("intervals_from_formula")
# def intervals_from_formula(chord_formula, root_string, fret_modifier):
#     intervals_to_return_b = [0] * 6
#     roots = {
#         1: [-24, -19, -14, -9, -5, 0],
#         2: [-19, -14, -9, -4, 0, 5],
#         3: [-15, -10, -5, 0, 4, 9],
#         4: [-10, -5, 0, 5, 9, 14],
#         5: [-5, 0, 5, 10, 14, 19],
#         6: [0, 5, 10, 15, 19, 24],
#     }
#     index = 6 - root_string - 1
#     for i in range(len(chord_formula)):
#         if chord_formula[i] != "X":
#             intervals_to_return_b[i] = master_intervals[
#                 (chord_formula[i] + roots[root_string][i]) + 12 + fret_modifier
#             ]
#         else:
#             intervals_to_return_b[i] = ""
#         index += 1
#     print(intervals_to_return_b)
#     return intervals_to_return_b


# Calculates the fret number for the chord diagram
# takes the root, string and fret_modifier from the database
# it returns an integer by looking up the .index(root) on the given string
# in the guitar_neck dictionary
# the fret modifier also needs ot be accounted for.
# if guitar_neck[string].index(root) + int(fret_modifier) >= 0:
# if it is >=0 it means the shape isn't running off the neck.
# if the integer is not greater than zero then we add 12 to it
# to place it higher up the neck at the next available position
# where there is space for all the notes
def fret_number(root, string, fret_modifier):
    neck_dict = {}
    if root in (circle_of_fifths):
        neck_dict = circle_of_fifths[root]
    if neck_dict == "guitar_neck":
        if int(fret_modifier) == 0:
            return guitar_neck[string].index(root)
        if guitar_neck[string].index(root) + int(fret_modifier) >= 0:
            return guitar_neck[string].index(root)
        if root in guitar_neck[string]:
            return guitar_neck[string].index(root) + 12
    if neck_dict == "guitar_neck_flats":
        if int(fret_modifier) == 0:
            return guitar_neck_flats[string].index(root)
        if guitar_neck_flats[string].index(root) + int(fret_modifier) >= 0:
            return guitar_neck_flats[string].index(root)
        if root in guitar_neck_flats[string]:
            return guitar_neck_flats[string].index(root) + 12


resolved_chord_test_1 = ["X", 1, 0, 1, 3, 3]

chord_main = [0, 2, 2, 0, 2, 2]

# splits out the chord data into 5 lists
# each lists represents 1 fret on the chord diagram
# so for example [0,2,2,0,2,2] would give us
# [0,'','',0,'','']
# ['','','','','','']
# ['','2','2','','2','2']
# ['','','','','','']
# ['','','','','','']


@app.template_filter("resolved_chord")
def resolved_chord(chord):
    rows = 5
    cols = 6
    chord_object = []
    for i in range(rows):
        chord_object.append([""] * cols)
    # loop over rows and cols plugging in the number of the fret if the row number matches
    # elif plugs in the X once only on the "0" row
    for i in range(rows):
        for j in range(cols):
            if chord[j] == i:
                chord_object[i][j] = chord[j]
            elif chord[j] == "X":
                chord_object[i][j] = "X"
    # print(chord_object)
    return chord_object


# single_note_lists
# this takes the chord_object from resolved_chord
# and returns a list of lists
# each sub-list is based on each note. An input of:
# [0,'','',0,'','']
# ['','','','','','']
# ['','2','2','','2','2']
# ['','','','','','']
# ['','','','','','']

# gives:

# [[0,0,0],[0,3,3],[2,1,1],[2,2,2],[2,4,4],[2,5,5]]

# in other words, for each note:
# what fret the note is (or if it's an "X")
# the index of where it starts i.e. the string number
# the index of where it ends i.e. the string number
# this is critical in working out the spans of any potential
# barres


@app.template_filter("single_note_lists")
def single_note_lists(input_chord):
    # print(input_chord)
    start = None
    end = None
    new_range = []
    for i in range(len(input_chord)):
        for j in range(len(input_chord[i])):
            if input_chord[i][j] != "" and input_chord[i][j] != "X":
                if start == None:
                    start = j
                    end = j
                if start != None and end != None:
                    new_range.append([input_chord[i][j], start, end])
                    start = None
                    end = None
    # print(new_range)
    return new_range


received_chord = resolved_chord(chord_main)


# finger_counter
# takes in the chord formula and returns the number of
# DISTINCT notes and thereofre the NUMBER OF FINGERS REQUIRED
# It detects if a barre at 0 is present (i.e. multiple 0's appear in the formula)
# and if so only adds 1 to the finger count in those instances.
# all other notes >0 add +1 to the overall count


@app.template_filter("finger_counter")
def finger_counter(chord_formula):
    # print(chord_formula)
    notes_greater_than_zero = 0
    zero_start_index = None
    zero_end_index = None
    zero_count = 0
    x_instances = []
    zero_flag = False
    for index, note in enumerate(chord_formula):
        if note != "X" and int(note) > 0:
            notes_greater_than_zero += 1
        if note == "X":
            x_instances.append(index)
        if note == 0 and zero_flag == False:
            zero_count += 1
            zero_flag = True
    zero_start_index = chord_formula.index(0)
    zero_end_index = len(chord_formula) - 1 - chord_formula[::-1].index(0)
    for x in x_instances:
        if x > zero_start_index and x < zero_end_index:
            zero_count = 2
        else:
            zero_count = 1
    # print(notes_greater_than_zero + zero_count)
    return notes_greater_than_zero + zero_count


# note_spans
# takes in the chord and for each fret referred to in the formula
# creates a dictionary where the starting string is recorded, plus the number of
# strings spanned. It also determines if that span
# should be barred. Take this input: [0,2,2,0,2,2].
# gives ({0: [[0,1], [3,1], 2: [[1,2,True], [4,2]], 2, False, [], 6})
# this is saying:
# on the sero fret there is a zero at position 0 for 1 string and position 3 for 1 string -therefore matches the position of 0's in the input chord
# at fret 2 we have a 2 at position 1 spanning 2 strings (the first pair of 2's in the formula)
# the true here indidates to the template this should be barred.
# then at position 4 we have a 2 that spans 2 strings (the second pair of 2's). The porgram has determined these
# not be a barre
# everything is returned to the template in a tuple containing the dictionary so it can be indexed and used


@app.template_filter("note_spans")
def note_spans(chord):
    # detect any muted strings with x_flag
    x_flag = False
    if "X" in chord:
        x_flag = True
    # record the index positions of the muted strings
    x_indexes = []
    for i in range(len(chord)):
        if chord[i] == "X":
            x_indexes.append(i)
    # not_x records strings that not muted
    spans_dict = {}
    not_x = 6 - len(x_indexes)

    # look at each element once only using a set
    for fret in set(chord):
        spans = []
        barre_flag = False
        # groupby here is used to group consecutive elements
        # which is important to be able to identify potential barres.
        for i, j in groupby(enumerate(chord), lambda index: index[1] == fret):
            # if i is true i.e. index[1] == fret
            if i:
                # assign a list to span of j. For example j could be [0,1,2] showing an element spans these 3 strings
                span = list(j)
                # Now we work out the span as an integer
                # take the index of the beginning string of the span
                first_string = span[0][0]
                # take the index of the end of the span i.e. the string
                last_string = span[-1][0]
                # strings crossed is therefore:
                string_crossed = last_string - first_string + 1
                # append the strings crossed to spans
                spans.append([first_string, string_crossed])
        # spans_dict[fret] gets the fret of the span, and the number of strings spanned
        spans_dict[fret] = spans

        # this if determines if True should be added to the lists in spons_dict
        # based on if we will have enough fingers to play this chord.
        # Basically if the chords requires > 4 fingers we need to
        # draw a secondary barre somewhere and this selects the notes to apply the barre to
        # the function breaks after finding a secondary barre
        if finger_counter(chord) > 4:
            barre_flag = False
            for note in spans_dict:
                if note != "X":
                    if barre_flag == False:
                        for index in range(len(spans_dict[note])):
                            if spans_dict[note][index][1] > 1 and barre_flag == False:
                                spans_dict[note][index].append(True)
                                barre_flag = True
                                break
    return (spans_dict, x_flag, x_indexes, not_x)


note_spans_ = note_spans(
    chord_main
)  # call note_spans and store the results in "note_spans_". Pass note_spans_ to the template down in the route
print(note_spans_)


@app.route("/")
def index():
    return render_template("index.html")


# @app.route("/theory")
# def theory():
#     return render_template("theory.html")


@app.route("/scales", methods=["GET", "POST"])
def scales():
    root = None
    scale = None
    active_page = 'scales.html'
    if request.method == "POST":
        root = request.form.get("root")
        scale = request.form.get("scale")
        print("Form Data:", request.form)  # Print the form data
        print("Root:", root)  # Check if root is retrieved correctly
        print("Scale:", scale)  # Check if scale is retrieved correctly
        if not root or not scale:
            return render_template("error.html")
        # Handle the form data as needed
        # else:
        # print(scales_dict[scale])
    return render_template(
        "scales.html",
        root=root,
        scale=scale,
        guitar_neck=guitar_neck,
        scales_dict=scales_dict,
        active_page=active_page
    )


# @app.route("/keys")
# def keys():
#     return render_template("keys.html")


@app.route("/grid", methods=["POST", "GET"])
def grid():
    db = sqlite3.connect("chords.db")  # set db as the databse object
    db.row_factory = sqlite3.Row  # use row_factory on db variable. Now Sqlite3 returns dictionary objects rather than tuples
    cursor = db.cursor()  # set a cursor so we can traverse the db
    active_page = 'grid.html'
    db_chords = []  # define empty list for the program to use as it's temporary db generated to suit the usder input
    # and to be passed back to the template

    if request.method == "POST":  # if it's a POST request do this
        root = request.form.get("root")  # get user selection root
        family = request.form.get("family")  # get user selection family
        if (
            not root or not family
        ):  # either root or family not selected show an error page
            return render_template("error.html")
        # print(f"guitar_neck_test: {guitar_neck[str(6)].index(root)}")
        cursor.execute(
            "SELECT * FROM chords WHERE family = ?", (family,)
        )  # get all the chord data of the user specified familuy

        rows = cursor.fetchall()  # get ALL family chord data and put into row variable
        # re-creates a dictionary from the chord data from the db
        for row in rows:  # for each row in rows
            chord = {  # chord dictionary =
                "root_string": row[
                    "root_string"
                ],  # key root_string gets row["root_string"]
                "family": row["family"],  # key family get row["family"] etc
                "fret_modifier": row["fret_modifier"],
                # list comprehension.
                # takes each note in row but splits on the | delimeter.
                # for each character of that notes string it then says
                # "if the character is a digit" turn it into an int otherwise
                # it gets left as a character. This helps separate out
                # the fret numbers from "X" which represent a muted string
                "notes": [
                    int(character) if character.isdigit() else character
                    for character in row["notes"].split("|")
                ],
            }
            db_chords.append(
                chord
            )  # db_chords gets the appended chord data for each chord in the family, now with
            # the notes string properley split

        # for chord in db_chords:
        # print(f"chord in db chords: {chord}")

        db.close()  # close db connection

        return render_template(
            "grid.html",
            root=root,
            family=family,
            chords=db_chords,
            fret_number=fret_number,
            guitar_neck=guitar_neck,
            guitar_neck_flats=guitar_neck_flats,
            received_chord=received_chord,
            note_spans_=note_spans_,
            active_page=active_page
        )
