# Survivor Vote Off Reactions
Logging the reactions of players after they're voted off in Survivor.

## Vote-off Logs

- `scripts/vote_off_reaction.py`: Fetches a [public Google Sheet](https://docs.google.com/spreadsheets/d/1nys0mCWArUCtPKYIVBrbjmv7eAWkmOce4cBlyHm8b0c/edit?usp=sharing) where vote-off reactions are being hand-logged. This is growing *slowly* and needs contributors. The goal is to build a dataset that shows all voted-off players' reactions *after* Jeff snuffed their torches and *before* they walked out of the Tribal Council. *Any vote at the council gets logged here, even if that person stayed in the game in one of the purgatory seasons.*

### Data Collection

To ensure accurate data collection and validation, I'm considering using a controlled method like a Google Form for submitted entries. For now, I'm doing it by hand in a [public Google Sheet](https://docs.google.com/spreadsheets/d/1nys0mCWArUCtPKYIVBrbjmv7eAWkmOce4cBlyHm8b0c/edit?usp=sharing) where previous entries are protected. My plan is to add one a day from recaps and/or transcripts until I finish all the seasons. (I've seen almost all the seasons but I can't recall specific details so I'm going vote by vote).

### Data Format

| Column         | Description                                                                                               | Type    |
|----------------|-----------------------------------------------------------------------------------------------------------|---------|
| season         | Season number                                                                                             | `string`  |
| vote           | Vote number that season                                                                                   | `string`  |
| castaway       | First name                                                                                                | `string`  |
| acknowledge    | Did the contestant acknowledge their teammates *in one of these specific ways* after snuffing — or just walk away?            | `boolean` |
| ack_gesture    | Category of `acknowledge`. See rules below. | `boolean` |
| ack_speak      | Category of `acknowledge`. See rules below.                            | `boolean` |
| ack_look       | Category of `acknowledge`. See rules below.                      | `boolean` |
| ack_smile      | Category of `acknowledge`. See rules below.                                   | `boolean` |
| ack_speak_notes| Optional: What, if anything, the contestant said. **Direct quotes only.**              | `string`  |
| notes          | Optional: Any notes about the moment, caveats about the log, etc.                                         | `string`  |
| source         | Optional: Any notes about source, i.e., youtube vote-off compilation url, "watched in person", etc.       | `string`  |
| log            | Date when data was logged (%Y-%m-%d)                                                                      | `date`    |

### Notes about Acknowledgment

*Acknowledgment* after being voted off in Survivor is categorized into four Boolean fields (each action is recorded as TRUE if performed, otherwise FALSE): 

- `ack_gesture`: for any physical gestures towards the tribe (a wave, nod, bow or prayer sign with hands) *after* torch snuffing
- `ack_speak`: for any verbal communication directed at the tribe *after* torch snuffing
- `ack_look`: for making eye contact with one or more members of the tribe *after* torch snuffing
- `ack_smile`: for smiling at the tribe *after* torch snuffing

### Dataset Example

| season | vote | contestant | acknowledge | ack_gesture | ack_speak | ack_look | ack_smile | ack_speak_notes | notes               | source        | log        |
|--------|------|------------|-------------|-------------|-----------|----------|-----------|-----------------|---------------------|------------|------------|
| 11     | 1    | Jim        | TRUE        | TRUE        | FALSE     | FALSE    | FALSE     |                 | Waved and turned head but didn't make eye contact | https://youtu.be/-D6JL6myJ_0?si=784e_2VAhRDk8OwC |2024-06-06|

### Scenario Explanation

- Jim, from season 11, was the first person voted off. He acknowledged his team by half-heartedly waving, but his slight glance went down and didn't make eye contact. He also didn't say anything or smile. So, his acknowledgment would be TRUE, but his score (see below) would only be 1 because all he did was (sort of) wave. Maybe 0.6. Poor Jim.

### Acknowledge Score Calculation

The score is derived from the four subcategories of acknowledgment: words, look, gesture, and smile. Each `true` value in these categories adds 1 to the score. For example:

- If a contestant says words while looking back, waves, and smiles, their score is 4.
- If a contestant does nothing, their score is 0.

### Seasons Collected

~~1~~, 2, 3, ~~4~~, ~~5~~, ~~6~~, ~~7~~, ~~8~~, ~~9~~, ~~10~~, ~~11~~, ~~12~~, ~~13~~, ~~14~~, ~~15~~, ~~16~~, ~~17~~, ~~18~~, ~~19~~, ~~20~~, ~~21~~, ~~22~~, ~~23~~, ~~24~~, ~~25~~, ~~26~~, ~~27~~, ~~28~~, 29, ~~30~~, ~~31~~, ~~32~~, ~~33~~, ~~34~~, ~~35~~, ~~36~~, ~~37~~, ~~38~~, ~~39~~, ~~40~~, ~~41~~, ~~42~~, ~~43~~, ~~44~~, ~~45~~, ~~46~~
