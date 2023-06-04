## Preamble

Pull requests are a great mechanism to collaborate on codebases.
They are used to document and explain code changes, get additional (possibly more expert) eyes on the code, and share responsibility.
The following sections provide some suggestions for information to include.
Pull requests need not be exhaustive, a few sentences usually does the job.

## PR details

* What issues does it fix (link to issues)?
* What problem does this solve?
* What features and benefits does this PR add?
* What alternative designs were considered for this problem and why rejected?

## Review

* What do you want the reviewer to help with? Specific requests mean better feedback:
- [ ] Test code runs as indicated
- [ ] Check code for logic errors
- [ ] Comprehend documentation, does it make sense?
- [ ] Feedback on approach used and alternatives
* Anything else?
* When is the review due by (any timing constraints)?

## Checklist

- [ ] The PR is marked as [WIP] or [Ready]
- [ ] The title of the PR is an effective summary of all PR work, suitable to add directly to a changelog
- [ ] The branch name conforms to standards in [`CONTRIBUTING.md`](../CONTRIBUTING.md)
- [ ] Pre-commit and nox tests were run locally in the latest poetry environment
