The purpose of `uiflow` is to build standard html components with reactivity using the `IDOM` python library. `uiflow` is to be carved out into a separate python library that can be installed via `pip`, this means the following code does not belong to `uiflow`:

* any import from other folders of timeflow outside of the `uiflow` folder, including code in `appflow` and `applications`
* any component that is custom to a specific app in `applications`, custom components belong to apps, not to `uiflow`