# Contributing

Contributions are welcome and very much appreciated!

## Code contributions

We accept code contributions through pull requests.
In short, this is how that works.

1. Fork [the repository](https://github.com/gramaziokohler/aixd_ara) and clone the fork.
2. Create a virtual environment using your tool of choice (e.g. `virtualenv`, `conda`, etc).
3. Install development dependencies:

   ```bash
   pip install -e ".[dev]"
   ```

4. Make sure all tests pass:

   ```bash
   invoke test
   ```

5. Start making your changes to the **main** branch (or branch off of it).
6. Make sure all tests still pass:

   ```bash
   invoke test
   ```

7. Add yourself to the *Contributors* section of `AUTHORS.md`.
8. Commit your changes and push your branch to GitHub.
9. Create a [pull request](https://help.github.com/articles/about-pull-requests/) through the GitHub website.

During development, use [pyinvoke](http://docs.pyinvoke.org/) tasks on the
command line to ease recurring operations:

* `invoke clean`: Clean all generated artifacts.
* `invoke check`: Run various code and documentation style checks.
* `invoke docs`: Generate documentation.
* `invoke test`: Run all tests and checks in one swift command.
* `invoke build-ghuser-components`: Build Grasshopper components.
* `invoke`: Show available tasks.

## Bug reports

When [reporting a bug](https://github.com/gramaziokohler/aixd_ara/issues) please include:

* Operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

## Feature requests

When [proposing a new feature](https://github.com/gramaziokohler/aixd_ara/issues) please include:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.

# Releasing a new version

Ready to release a new version of the project? Here's how to do it!

We follow [semantic versioning](https://semver.org) principles for our release process.
To create a new release, follow these steps:

1. Ensure all changes intended for the release are merged into the **main** branch.

2. Create a new branch from **main** to prepare the release (replace `x.y.z` with the version number you plan to release):

   ```bash
   git checkout main
   git pull
   git checkout -b prepare-release-x.y.z
   ```
   
3. Ensure all checks and tests pass successfully. Use the `invoke check` and `invoke test` commands to verify.

4. Decide on the versioning increment type for the release based on the changes since the last version:
   - `major` for breaking changes to the API
   - `minor` for adding functionality in a backwards-compatible manner
   - `patch` for backwards-compatible bug fixes

5. Run the release command with the appropriate release type:

   ```bash
   invoke release [release_type]
    ```
6. Create a merge request to merge the branch into **main**. Check the changes and make sure 
   everything looks good, before merging.

7. Celebrate! 💃
