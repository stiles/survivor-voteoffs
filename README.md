# Survivor vote off reactions
Logging the reactions of players after they're voted off in Survivor.

## How it works

The `vote_off_reaction.py` script is designed to fetch, process, and score hand-collected data on the reactions of Survivor contestants after their torches are snuffed at Tribal Council. *Any vote at the council gets logged, even if that person stayed in the game in one of the purgatory seasons. (Medical evacuations and castaways who quit were not included).*

The script authenticates with personal Google credentials to access a specified [Google Sheet](https://docs.google.com/spreadsheets/d/1nys0mCWArUCtPKYIVBrbjmv7eAWkmOce4cBlyHm8b0c/edit?usp=sharing) where vote-off reactions are logged. The script retrieves this data, combines it with a [generic castaway order list](https://github.com/stiles/survivor-voteoffs/blob/main/data/processed/survivor_voteoff_order.csv) derived from the the [survivoR repo](https://github.com/doehm/survivoR) and  ensures data consistency through various checks. 

The script also converts columns to boolean values, calculates a tribal acknowledgment score for each castaway based on specific criteria (gestures, speech, eye contact and smiles), and then cleans and formats the data. Finally, the processed data is saved in both CSV and JSON formats for further analysis and use.

### Output formats

The resulting castaway file, which logs nearly 700 reactions during 46 seasons, is stored on S3 in [CSV](https://stilesdata.com/survivor/survivor_vote_off_reactions.csv) and [JSON](https://stilesdata.com/survivor/survivor_vote_off_reactions.json) format using the following structure: 

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

### Notes about `acknowledgment`

*Acknowledgment* after being voted off in Survivor is categorized into four Boolean fields (each action is recorded as `True` if performed, otherwise `False`): 

- `ack_gesture`: for any physical gestures towards the tribe (a wave, nod, bow or prayer sign with hands) *after* torch snuffing
- `ack_speak`: for any verbal communication directed at the tribe *after* torch snuffing
- `ack_look`: for making eye contact with one or more members of the tribe *after* torch snuffing
- `ack_smile`: for smiling at the tribe *after* torch snuffing

### Dataset example

| season | vote | contestant | acknowledge | ack_gesture | ack_speak | ack_look | ack_smile | ack_speak_notes | notes               | source        | log        |
|--------|------|------------|-------------|-------------|-----------|----------|-----------|-----------------|---------------------|------------|------------|
| 11     | 1    | Jim        | TRUE        | TRUE        | FALSE     | FALSE    | FALSE     |                 | Waved and turned head but didn't make eye contact | https://youtu.be/-D6JL6myJ_0?si=784e_2VAhRDk8OwC |2024-06-06|

### Example scenario

- Jim, from season 11, was the first person voted off. He acknowledged his team by half-heartedly waving, but his slight glance went down and didn't make eye contact. He also didn't say anything or smile. So, his acknowledgment would be TRUE, but his score (see below) would only be 1 because all he did was (sort of) wave. Maybe 0.6. Poor Jim.

### Acknowledge score calculation

The score is derived from the four subcategories of acknowledgment: words, look, gesture, and smile. Each `true` value in these categories adds 1 to the score. For example:

- If a contestant says words while looking back, waves, and smiles, their score is 4.
- If a contestant does nothing, their score is 0.

### Seasons ~~collected~~/**remaining**

~~1~~, **2**, **3**, ~~4~~, ~~5~~, ~~6~~, ~~7~~, ~~8~~, ~~9~~, ~~10~~, ~~11~~, ~~12~~, ~~13~~, ~~14~~, ~~15~~, ~~16~~, ~~17~~, ~~18~~, ~~19~~, ~~20~~, ~~21~~, ~~22~~, ~~23~~, ~~24~~, ~~25~~, ~~26~~, ~~27~~, ~~28~~, ~~29~~, ~~30~~, ~~31~~, ~~32~~, ~~33~~, ~~34~~, ~~35~~, ~~36~~, ~~37~~, ~~38~~, ~~39~~, ~~40~~, ~~41~~, ~~42~~, ~~43~~, ~~44~~, ~~45~~, ~~46~~

### Related repositories

- [survivoR2py](https://github.com/stiles/survivoR2py)