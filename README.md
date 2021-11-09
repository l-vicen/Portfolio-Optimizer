# App Documentation

## Contributing

In order to contribute to the project, you should create a conda environment using the __*requirements.txt*__ file which you find in the root of the repository. The following command should do this:

```conda env create --file bio-env.txt ```

Now, with the repository in hand, I believe this can be useful guidelines based on the fact that changes in the master branch of our github repository will automatically change our app. Meaning, a bug will kill the app and we don't want that.

### Guidelines

1. Always work on a different branch than master branch. Only one person should control what can be merge with master branch. I hope you understand. E.g. Lucas works and pushes changes to *LUCAS_BRANCH_TOPICx*.

2. In case you work on something new that depends on a new library which is not part of the env, let me know because I have constructed the app in a way that I always have to notify the server about the dependencies that we are working with.

3. In case you are not familiar with git commands, please have a look on this link: https://git-scm.com/docs/gittutorial . Git is fundamental for working on github in a collaborative and productive way.

4. Save your ```.py```  files within the folder __*testing*__ . There you are free to do whatever you'd like to. Final implementation of your ideas should be signalized, and I will add them to the app. 

5. These are the resources that I am using to build the app:

    5.1 Portfolio Optimizers: https://pyportfolioopt.readthedocs.io/en/latest/UserGuide.html

    5.2 Frontend Interface: https://docs.streamlit.io/

    5.3 Heroku Server: https://devcenter.heroku.com/categories/reference

6. Short Project Description:

    The idea is to use Model-View-Controller Design.

        i. Controler: controls inputs, which will come from yahooFinance API.  [TODO 01]
        ii. Model: stores the optmizers that we want to have in the app.       [TODO 02]
        iii. View: visualizes the app.                                         [TODO 03]
        iv. Testing: is our playground, where we can experiment with anything.
        v. Data: is where we have .csv files to play in Testing.

### Commit Style
Please also consider writting meaningful messages in your commits. 

        API: an (incompatible) API change
        BENCH: changes to the benchmark suite
        BLD: change related to building numpy
        BUG: bug fix
        DEP: deprecate something, or remove a deprecated object
        DEV: development tool or utility
        DOC: documentation
        ENH: enhancement
        MAINT: maintenance commit (refactoring, typos, etc.)
        REV: revert an earlier commit
        STY: style fix (whitespace, PEP8)
        TST: addition or modification of tests
        REL: related to releasing numpy