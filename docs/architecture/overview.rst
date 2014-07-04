.. _overview:

=====================
Architecture Overview
=====================

Spidy consists of the following packages and modules:

- **common**   : error handling, logging, utilities
- **document** : document loading, parsing and XPath (depends on *common*)
- **language** : script parser and runtime  (depends on *common* and *document*)
- **shell**    : shell to check and run scripts (depends on *common*, *document* and *language*)