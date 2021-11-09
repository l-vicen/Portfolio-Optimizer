# App Documentation

## Contributing

In order to contribute to the project, you should create a conda environment using the __*requirements.txt*__ file which you find in the root of the repository. The following command should do this:

```conda env create --file bio-env.txt ```

Now, with the repository in hand, I believe this can be useful guidelines based on the fact that changes in the master branch of our github repository will automatically change our app. Meaning, a bug will kill the app and we don't want that.

### Guidelines

1. Always work on a different branch than master branch. Only one person should control what can be merge with master branch. I hope you understand. E.g. Lucas works and pushes changes to *LUCAS_BRANCH_TOPICx*.

2. In case you work on something new that depends on a new library which is not part of the env, let me know because I have constructed the app in a way that I always have to notify the server about the dependencies that we are working with.

3. In case you are not familiar with git commands, please have a look on this link: https://git-scm.com/docs/gittutorial . Git is fundamental for working on github in a collaborative and productive way.

4. Finally, this is how I am building the app:

    4.1 Portfolio Optimizers: https://pyportfolioopt.readthedocs.io/en/latest/UserGuide.html

    4.2 Frontend Interface: https://docs.streamlit.io/

    4.3 Heroku Server: https://devcenter.heroku.com/categories/reference


