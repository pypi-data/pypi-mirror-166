# remotemanager

Modular serialisation and management package for handling the running of functions on remote machines

Based off of the BigDFT RemoteRunner concept, remotemanager represents an improvement and expansion on the concepts based there.

Primary usage is via a `Dataset`, which connects to a remote machine via `URL`

You can think of the `Dataset` as a "container" of sorts for a calculation, to which "runs" are attached. These runs are then executed on the remote machine described by the provided `URL`

See the [documentation](https://ljbeal.gitlab.io/remotemanager/) for further information, tutorials and api documentation.
