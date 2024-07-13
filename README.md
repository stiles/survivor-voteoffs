# Survivor vote off reactions
Logging the reactions of players after they're voted off in the American version of Survivor.

## How it works

The `00_create_vote_lookup.py` script creates an ordered tribal council vote-off list with details about seasons and castaways for use with data processing and analysis. It merges two CSVs in the [survivoR](https://github.com/doehm/survivoR) and [survivoR2py](https://github.com/stiles/survivoR2py/tree/main) repositories — vote_history and castaway_details — and stores the resulting file on S3.

The `01_vote_off_reaction.py` script fetches a [Google Sheet](https://docs.google.com/spreadsheets/d/1nys0mCWArUCtPKYIVBrbjmv7eAWkmOce4cBlyHm8b0c/edit?usp=sharing) with hand-collected data detailing the reactions of Survivor contestants after their torches are snuffed at tribal council. It merges it with the vote order table, converts Google's string columns to Boolean values, calculates a tribal acknowledgment score for each castaway based on specific criteria (more on that below), and then cleans and formats the data. 

*Any vote at the council gets logged, even if that person stayed in the game in one of the purgatory seasons. Medical evacuations and castaways who quit were not included.*

### Output format

The resulting castaway file, which logs nearly 700 reactions during 46 seasons, is stored on S3 in [CSV](https://stilesdata.com/survivor/survivor_vote_off_reactions.csv) and [JSON](https://stilesdata.com/survivor/survivor_vote_off_reactions.json) formats using the following structure: 

| Column          | Description                                                                                                    | Type     |
|-----------------|----------------------------------------------------------------------------------------------------------------|----------|
| `season`        | Season number                                                                                                  | `string` |
| `season_name`   | Season name, i.e. "Survivor: Africa"                                                                           | `string` |
| `vote`          | Vote number that season                                                                                        | `string` |
| `episode`       | Episode number that season                                                                                     | `string` |
| `castaway`      | Castaway first name                                                                                            | `string` |
| `full_name`     | Castaway full name                                                                                             | `string` |
| `castaway_id`   | Castaway unique ID code                                                                                        | `string` |
| `gender`        | Castaway gender ("Male" or "Female")                                                                           | `string` |
| `date_of_birth` | Castaway date of birth (%Y-%m-%d)                                                                              | `string` |
| `personality_type` | Castaway's [Myers-Briggs Type Indicator](https://www.mbtionline.com/en-US/How-it-works/Framework) code ("ENTJ", "INFJ", etc.) | `string` |
| `occupation`    | Castaway job outside the game                                                                                  | `string` |
| `acknowledge`   | Did the contestant acknowledge their teammates *in one of these specific ways* after snuffing — or just walk away? | `boolean`|
| `ack_gesture`   | Category of `acknowledge`. See rules below.                                                                    | `boolean`|
| `ack_speak`     | Category of `acknowledge`. See rules below.                                                                    | `boolean`|
| `ack_look`      | Category of `acknowledge`. See rules below.                                                                    | `boolean`|
| `ack_smile`     | Category of `acknowledge`. See rules below.                                                                    | `boolean`|
| `ack_speak_quote` | Optional: What, if anything, the contestant said. **Direct quotes only.**                                   | `string` |

### `Acknowledgment` notes

*Acknowledgment* after being voted off in Survivor is categorized into four Boolean fields (each action is recorded as `True` if performed, otherwise `False`): 

* `ack_gesture`: for any physical gestures towards the tribe *after* torch snuffing
* * Types: wave, nod, wink, bow or prayer sign with hands
* `ack_speak`: for any verbal communication directed at the tribe *after* torch snuffing
* `ack_look`: for making eye contact with one or more members of the tribe *after* torch snuffing
* `ack_smile`: for smiling at the tribe *after* torch snuffing

### Example scenario: Jim!

- Jim, from season 11, was the first person voted off. He acknowledged his team by half-heartedly waving, but his slight glance went down and didn't make eye contact. He also didn't say anything or smile. So, his acknowledgment would be `True`, but his score (see below) would only be 1 because all he did was (sort of) wave. Maybe 0.6. Poor Jim.

| Column           | Example Value            |
|------------------|--------------------------|
| `season`         | 11                       |
| `season_name`    | Survivor: Guatemala      |
| `vote`           | 1                        |
| `episode`        | 1                        |
| `castaway`       | Jim                      |
| `full_name`      | Jim Lynch                |
| `castaway_id`    | US0151                   |
| `gender`         | Male                     |
| `date_of_birth`  | 1942-01-07               |
| `personality_type` | ISTJ                     |
| `occupation`     | Retired Fire Captain     |
| `acknowledge`    | true                     |
| `ack_look`       | false                    |
| `ack_speak`      | false                    |
| `ack_gesture`    | true                     |
| `ack_smile`      | false                    |
| `ack_speak_quote`|                          |
| `ack_score`      | 1                        |

*NOTE: Jim didn't speak, so the `ack_speak_quote` is empty. The parting words of others castaways, such Kane in season 44 ("Enjoy your rice, you bitches."), are listed in almost all cases. If there's text in this item, it should be considered a direct quote that's been confirmed via transcript, broadcast and/or closed captioning.*

### `Acknowledge` score calculation

The score is derived from the four subcategories of acknowledgment: words, look, gesture, and smile. Each `true` value in these categories adds 1 to the score. For example:

* If a contestant says words while looking back, waves, and smiles, their score is 4.
* If a contestant does nothing, their score is 0.

*NOTE: This score doesn't consider season-to-season factors that might have to altered castaways' acknowlegment behavior, such as tribal council design. In "Survivor: Thailand", for example, castaways were required to double back towards the tribe after being dismissed by Jeff. That appeared to make it more difficult for them to leave quietly. Other sets seemingly made that easier. In addition, in earlier seasons, before the mores of this moment in the show evolved, castaways might have felt required to leave quietly after Jeff said, "It's time for you to go."*

### Seasons collected

Seasons 1, 3-46 
(*Watching 2 now!*)


### Related

* [survivoR](https://github.com/doehm/survivoR): The internet's most-detailed Survivor data collection, in R format, created by [David Ohm](https://github.com/doehm), et al. Details about season locations, vote orders and castaway personal information was all derived from the fine work here. 
* [survivoR2py](https://github.com/stiles/survivoR2py): Converting survivoR to CSV format so it plays nice with other data-science tools, such as Python/Pandas.
