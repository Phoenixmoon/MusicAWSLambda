# MusicAWSLambda

This is a serverless application deployed on AWS Lambda that generates music from a txt file. This is the back-end of the corresponding music generation website, where users can input text (the written notes) and a tempo for the music. The project includes the following files and folders:

- hello_world - Code for the application's Lambda function.
  - `app.py`: contains the Lambda function code
  - `music_function.py`: contains the note generator and music generator functions
  - `note_frequency.csv`: contains a list of the notes and their corresponding frequencies
  - `notesheets.xlsx`: defines the note lengths
  - `requirements.txt`: Lists the required packages and dependencies for the application.
- `template.yaml` - A template that defines the application's AWS resources.

The application uses several AWS resources, including Lambda functions and an API Gateway API. These resources are defined in the `template.yaml` file in this project.

## Description of Music Generator Function
Generates a music mp3 from a txt file input. Note that notes must be typed in this format: 
A4_dotted_quarter, for instance. Flats would be Ab, whereas sharps use the word sharp, as in A_sharp4_dotted_eighth. 
Additionally, notes should be separated by commas and a space; returns/line indents are not supported. 
Example accepted input: "C4_dotted_quarter, Bb5_whole, eighth_rest, G_sharp3_sixteenth". If a note input, for whatever reason, fails, a short rest (silence) will be present in the mp3 file instead. 
Note that (as can be found in note_frequency.csv) the note range is from C0 to B8. C4 is middle C. 

## Tests

### Sample usage of the music generation function:
```python
judge = """

F_sharp4_eighth, F_sharp4_eighth, F_sharp4_eighth, F_sharp4_eighth, D_sharp4_quarter, C_sharp4_eighth, F_sharp4_eighth, F_sharp4_eighth, F_sharp4_eighth, F_sharp4_eighth, G_sharp4_eighth, F_sharp4_quarter, F_sharp4_eighth, A_sharp4_eighth, A_sharp4_eighth, A_sharp4_eighth, B4_quarter, A_sharp4_eighth, G_sharp4_eighth, F_sharp4_eighth, G_sharp4_quarter, G_sharp4_eighth, F_sharp4_eighth, G_sharp4_dotted_eighth, A_sharp4_dotted_eighth, G_sharp4_eighth

"""

with open('judge.txt', 'w') as file:
    file.write(judge)

create_music('judge.txt', 'test.mp3', tempo=120)
```

### Sample inputs for the website:
- C6_eighth, Db5_eighth, F5_eighth, C6_eighth, Bb5_eighth, C5_eighth, Eb5_eighth, Bb5_eighth, Ab5_eighth, Bb4_eighth, Db5_eighth, Ab5_eighth, G5_eighth, Ab4_eighth, C5_eighth, Eb5_eighth, F5_dotted_quarter, F6_dotted_half, G4_quarter, Bb4_quarter, Db5_dotted_quarter, E5_half, C3_half, C4_sixteenth, E4_sixteenth, G4_whole, dotted_half_rest, F4_eighth, G4_eighth, Ab4_quarter, C5_quarter, Bb4_quarter, Db5_quarter, C5_quarter, Ab4_quarter, Bb4_quarter, Ab4_eighth, G4_eighth, F4_quarter, C5_quarter, F4_eighth, Eb4_eighth, Eb4_eighth, Eb4_eighth, F4_quarter, C5_quarter, C5_quarter
  - tempo: 122



- D4_eighth, E4_eighth, F4_half, G4_eighth, A4_eighth, G4_half, A4_eighth, Bb4_eighth, A4_half, F4_quarter, D4_half, D4_eighth, E4_eighth, F4_quarter, G4_quarter, A4_quarter, G4_dotted_quarter, F4_eighth, E4_quarter, D4_dotted_half
  - tempo: 132

- A4_eighth, G_sharp4_eighth, A4_eighth, E4_dotted_whole, eighth_rest, A4_eighth, G_sharp4_eighth, A4_eighth, E4_dotted_whole, A4_eighth, G_sharp4_eighth, F_sharp4_eighth, E4_eighth, quarter_rest, C_sharp5_quarter, A4_dotted_quarter, E4_eighth, B4_eighth, C_sharp5_eighth, B4_eighth, C_sharp5_eighth, eighth_rest, A4_eighth, A4_eighth, B4_eighth, B4_eighth, A4_eighth, A4_eighth, B4_eighth
  - tempo: 120
