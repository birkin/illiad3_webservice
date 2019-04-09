### overview ###

This is a [django](https://www.djangoproject.com) web-app that provides an internal-api that interfaces with the [ILLiad](http://www.atlas-sys.com/illiad/) hosted API.

This internal-api allows multiple applications that programmatically interface with ILLiad (the article part of [easyAccess](https://github.com/Brown-University-Library/easyaccess_project), and [easyBorrow](https://github.com/birkin/easyborrow_controller), for example) -- to continue to work as-is if/when the programmatic interface to ILLiad changes.

And it has.

In April 2019, we changed our programmatic-access to ILLiad from a [module](https://github.com/birkin/illiad3_client) that simulated web-requests on behalf of a user -- to, instead, use ILLiad's official api. We made this change as part of a migration from an end-of-life self-hosted version of ILLiad -- to a newer version of ILLiad only available via [OCLC hosting](https://www.oclc.org/en/illiad/features.html).

Useful references...

- [api documentation](https://support.atlas-sys.com/hc/en-us/articles/360011809394-The-ILLiad-Web-Platform-API)

- [table documentation](https://support.atlas-sys.com/hc/en-us/articles/360011812074) -- used to apply field-length limits when calling the official-illiad-api

---


### usage ###

- check user: better example coming; for now [see these tests](https://github.com/Brown-University-Library/illiad3_webservice/blob/0da33e12fe709218903ba0b5968e643a2baddafe/illiad_app/tests.py#L63-L64)

- create user: [see sample script](https://github.com/Brown-University-Library/illiad3_webservice/blob/master/sample_scripts/sample_newuser_submission.py)

- request item: [see sample script](https://github.com/Brown-University-Library/illiad3_webservice/blob/master/sample_scripts/sample_transaction_submission.py)


---
