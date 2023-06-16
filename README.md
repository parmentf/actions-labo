# actions-labo

To learn/experiment with GitHub Actions.

First PR is #1, which apply the
[Quickstart](https://docs.github.com/en/actions/quickstart) example.

In fact, although colleagues told me that only workflows in the `main` branch are taken into account, this seems to be wrong: I added `.github/workflows/actions-demo.yml` in the `parmentf-patch-1` branch, and it worked.  
I think it depends the `on:` rule (which, in that case, was `push`).
