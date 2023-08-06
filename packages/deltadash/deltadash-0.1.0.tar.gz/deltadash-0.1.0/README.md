# deltadash.py
A simple, dependency-less library for programatically interfacing with DeltaDash's file formats.

## Current features
deltadash.py currently includes the following features:
- Difficulty reading and deserialisation
- Difficulty writing and deserialisation

## Example
Here is an example of how to read, modify and write a DeltaDash map through the deltadash.py library!
```py
# deltadash.py map reading example
from deltadash.maps.difficulty import Difficulty

# Read a .dd file
diff = Difficulty.from_file("test_res/debug.dd")

# Print the difficulty's full name
print(diff.full_name)

# Change the difficulty name
diff.name = "New Name"

# Write the difficulty to a new file
diff.into_file("test_res/debug_new.dd")
```

You may view more examples in the `examples` directory of this repo!
