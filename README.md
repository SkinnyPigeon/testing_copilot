# Testing Copilot

This is a test of GitHub Copilot. I have tried to be as hands-off as possible using a combination of comments and the chat feature. I have tried to use a variety of problems to test its capabilities.

## Findings

In someways Copilot is quite capable at writing code that works. At least when we are talking about a green-field development. I was able to add a few comments and get it to write functions that quite often worked first try. 

However, when it came to test writing there is still a lot to improve upon. For test file for self-contained models such as the `test_models.py` and `test_password_hash_and_salter.py` it was able to pretty much write everything in one go. I used a __hack__ I have seen where I specified that I had difficulty writing so it would write the entire test for me. 

When it tried to write tests for more complex interactions such as the `test_database_functions.py` it really struggled and had to be guided a lot more. For instance, in its first attempt the `session` fixture it was using wrote to my database, even though it was attempting to use an in-memory database. Once I noticed this, it attempted to convince me to update one of my functions to add a conditional check for whether we were in the `test` environment. I knocked this back and we started to look at patching as an alternative. This still took a bit more work. Its first attempt at doing this did patch the object but it completely missed that it needed to patch the `create_session` function in order for this `session` fixture to be the one that was used in the tests. In end we got all of the tests to pass but it was a lot more work than I would have liked.

## A couple observations

1. It was obsessed with using `monkeypatch` to patch objects. I am not sure why this is. I have never used `monkeypatch` before and have only ever seen it used a few times. I am not sure why it is so obsessed with it. Even when I tried to get it to use `patch` it would still try to use `monkeypatch` instead.

2. There were a few times when it was convinced that i should go back and update my code, including changing the function signatures, to be able to work with the tests it was writing. These changes were often quite clunky and I had to coerce it away from this.

