For this refinement, we're making the code more consistent
We're moving to a different state-machine controller to try to handle inputs in a more consistent way
Classes are being isolated so they can be tested individually (eventually we want to be able to run some tests or do TDD). It will also allow us to experiment with gradual typing of a Python program as it currently exists.

This version changes the text editing of state labels to use itemconfigure on the canvas handler - the icursor methods were giving me some grief because I was having trouble removing the damn cursor.

Also, I've been working on the state-machine representation with the dispatcher, and I'd like to implement it now, so this version will include that.