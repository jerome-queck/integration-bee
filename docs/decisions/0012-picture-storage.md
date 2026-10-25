# Photo files stay next to the tracker

A photo mark can name a chat file in `image`. `scripts/control-integration-bee` copies that file to `submissions/<IB_USER>/` under the data directory. The stored relative path is on the attempt, on `mark.picture`, in `progress show`, and in the `pictures` list of `progress.local.json`.

`IB_DATA_DIR` is one learner. `IB_USER` only names the folder inside it and defaults to `default`. The copy is gitignored with `trackers/live/`. It is not uploaded.
