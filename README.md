# actions-labo

To learn/experiment with GitHub Actions.

## Quickstart

First PR is [#1](https://github.com/parmentf/actions-labo/pull/1), which applies
the [Quickstart](https://docs.github.com/en/actions/quickstart) example.

In fact, although colleagues told me that only workflows in the `main` branch are taken into account, this seems to be wrong: I added `.github/workflows/actions-demo.yml` in the `parmentf-patch-1` branch, and it worked.  
I think it depends the `on:` rule (which, in that case, was `push`).

The
[docker-publish](https://github.com/actions/starter-workflows/blob/main/ci/docker-publish.yml)
workflow could be of some help later.

The [actions/create-release](https://github.com/actions/create-release) is interesting too.
