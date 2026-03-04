from flask import Flask, render_template, request, jsonify
import random
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate/<key>/<mode>/<int:nChords>", methods=["GET"])
def generate(key, mode, nChords):
    cProg=generate_progression(key,mode,nChords)
    return jsonify(cProg)


#Hvala chatgpt
def generate_progression(key, mode, num_chords):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    # Intervals for the scales
    scale_intervals = {
        'maj': [0, 2, 4, 5, 7, 9, 11],
        'min': [0, 2, 3, 5, 7, 8, 10]
    }
    
    # Qualities for the diatonic chords
    qualities = {
        'maj': ['maj7', 'min7', 'min7', 'maj7', '7', 'min7', 'm7b5'],
        'min': ['min7', 'm7b5', 'maj7', 'min7', 'min7', 'maj7', '7']
    }

    # Formulas for the 7th chords (semitones from chord root)
    chord_formulas = {
        'maj7': [0, 4, 7, 11],
        'min7': [0, 3, 7, 10],
        '7':     [0, 4, 7, 10],
        'm7b5':  [0, 3, 6, 10]
    }

    if key not in notes:
        return "Invalid Key"

    start_index = notes.index(key)
    scale_notes = [notes[(start_index + i) % 12] for i in scale_intervals[mode]]
    
    # Create the full list of possible chords in this key
    diatonic_chords = []
    for i in range(7):
        root = scale_notes[i]
        quality = qualities[mode][i]
        
        # Calculate the 4 notes for this specific chord
        root_idx = notes.index(root)
        chord_notes = [notes[(root_idx + semi) % 12] for semi in chord_formulas[quality]]
        
        diatonic_chords.append({
            "chord": f"{root}{quality}",
            "notes": chord_notes
        })

    # Pick random chords from the list
    progression = [random.choice(diatonic_chords) for _ in range(num_chords)]
    return progression
if __name__ == "__main__":
    app.run(debug=True)