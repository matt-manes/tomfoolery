# tomfoolery

Tool to generate Python dataclasses that model and load toml files (or other can-representated-as-a-dict files).<br>
Primarily aimed at configuration type files.

## Installation

Install with:

<pre>
pip install tomfoolery
</pre>


## Usage

Given the following file (`venue.toml`):<br><br>
![](imgs/toml.png)

Running the command
<pre>
tomfoolery venue.toml
</pre>

will produce this file (`venue.py`):<br><br>
![](imgs/dataclass.png)

which can then be used:
<pre>
>from venue import Venue
>venue = Venue.load()
>print(venue.address.city)
'Chicago'
>venue.calendar.start_month = "March"
>venue.dump()
</pre>

### Current Caveats

* Only works with `.toml` and `.json` files.
* All keys must be valid Python variable names.