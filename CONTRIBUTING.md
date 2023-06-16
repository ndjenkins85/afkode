# Contributing

This is a personal project open to contributors.

Best place to start is with the issues, either raising questions or contributing to discussion.

# Codeowners

Add yourself as a CODEOWNER for specific folders or file types under `.github/CODEOWNERS`.

# Branch conventions

This project uses Git Flow, with the exception that releases are cut directly from master.

- Main/master branch is protected for releases as discussed in [releases.md](RELEASE.md).
- Dev branch is where work is merged into until ready for release.
- Working branches should follow the naming conventions mentioned below
  - feature/ - adding functionality to project
  - bugfix/ or bug/ - addressing issues with current process
  - docs/ - for documentation improvements
  - infra/ - for CI/CD and tooling
  - hotfix/ - only for fixing broken releases
  - experiment/ - for testing and experiments, not to be merged (formalize as feature)

Labels are automatically managed through a github action. Using these branch names helps [pr-labeler](.github/pr-labeler.yml) to automatically label pull requests, which in turn helps [release-drafter](.github/release-drafter.md) create nice release notes related to the pull request information.

# Issuing releases

Releases to be carried out from the main/master branch with a tagged commit.
Recommended to use https://semver.org/ versioning definitions.
We have Github actions which will:

- Run all tests
- Publish codebase to pypi
- Publish documentation to Github pages (`gh-pages` branch)

The process for performing a release is as follows:

- [ ] Merge all feature branches into dev branch
- [ ] On local dev branch, increment the project version by updating `afkode.__init__.py`. This is useful to have the changelog, importable version, and in setuptools process.
- [ ] If using `poetry`, use `poetry version {major|minor|patch}`. This is used for poetry build versioning.
- [ ] Ensure the project README is current
- [ ] Commit changes, and use `git tag` to tag the commit
- [ ] Push to Github using `git push origin master --tags`
- [ ] Raise a pull request for `dev -> master`
- [ ] Draft new release, referencing the latest tag
