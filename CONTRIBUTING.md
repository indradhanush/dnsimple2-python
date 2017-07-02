Contributing
==

1. Fork and clone the repo.
2. Sign up here: https://sandbox.dnsimple.com/
3. In your sandbox account, navigate to the settings page and add
billing info. Under the credit card, add `1` as the number. You can
read more here: https://developer.dnsimple.com/sandbox/#testing-subscriptions
4. Optionally set up your repo to build on
   [Travis CI](http://travis-ci.org/) and to generate coverage reports
   on [CodeCov](https://codecov.io/gh/indradhanush/dnsimple2-python).
5. Setup the dev environment:
6. Set the environment variables in your `.bashrc` or `.bash_profile` equivalent:
   - `DNSIMPLE_ACCOUNT_ID`
   - `DNSIMPLE_V2_ACCESS_TOKEN`
7. Create a virtualenv: `virtualenv venv -p python3.5`
8. Activate the venv: `source venv/bin/activate`
9. Install the dependencies: `pip install -r requirements.txt`
10. Run the tests: `coverage run -m unittest`
11. Add/remove some code. Send a PR!


## Notes

The codebase builds for `python 2.7, 3.3, 3.4, 3.5` and `3.6` along
with `pypy` and `pypy3`. For development you could start on `python
3.5`. While we do want to be able to support all of the versions
above, we must be able to support at least `python2.7` and
`python3.5`. You can develop under `python3.5` and test your builds
for other versions in Travis-CI. There are other workflows for
developing for multiple versions locally, but I have not explored
them. Please feel free to send a patch updating this section if you
think there's a better approach.


## Useful links:

API Docs: https://developer.dnsimple.com/v2/
Builds: https://travis-ci.org/indradhanush/dnsimple2-python
Coverage: https://codecov.io/gh/indradhanush/dnsimple2-python


## Ideas

- Not all the APIs are covered. Pick one, add one?
- Check the issue list.
- Add/improve docs.
- Anything else is also appreciated.
