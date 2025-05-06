# Unknown_Possibilities

![Unknown_Possibilities](media/readme_images/mockup-up.png)

[Visit Unknown Possibilities Here](https://unknown-possibilities-846f26e3e4d7.herokuapp.com/)

---

Testing was ongoing throughout the entire build. During development I made use of Googles Developer Tools to ensure everything was working as expected and to assist me with troubleshooting when things didn't work as they should.

I have gone through each page of the site using the Chrome Developer Tools to ensure each page is responsive on a variety of different screen sizes and devices, as well as manually testing this using a variety of devices in person.

---

## Validation Testing

### HTML

[W3C](https://validator.w3.org/) was used to validate the HTML on all pages of the site. It was also used to validate the CSS. As the site is created with Django and utilises Django templating language within the HTML, I have checked the HTML by inspecting the page source and then running this through the validator.

| Page | Result | Evidence |
| :--- | :--- | :---: |
| Home Page | Pass | [Home Page Validation](https://validator.w3.org/nu/?doc=https%3A%2F%2Funknown-possibilities-846f26e3e4d7.herokuapp.com%2F) |
| Products Page | Pass | [Products Page Validation](https://validator.w3.org/nu/?doc=https%3A%2F%2Funknown-possibilities-846f26e3e4d7.herokuapp.com%2Fproducts%2F) |
| Products Detail Page | Pass | [Products Detail Validation](documentation/testing/validation/html/products-details-w3c.png) |
| Daily Card Page | Pass | [Daily-Card Page Validation](https://validator.w3.org/nu/?doc=https%3A%2F%2Funknown-possibilities-846f26e3e4d7.herokuapp.com%2Fdaily_card%2F) |
| Profile Page | Pass | [Profile Page Validation](https://validator.w3.org/nu/?doc=https%3A%2F%2Funknown-possibilities-846f26e3e4d7.herokuapp.com%2Faccounts%2Flogin%2F%3Fnext%3D%2Faccounts%2F) |
| Product management Page | Pass | [Product management Page validation](https://validator.w3.org/nu/?doc=https%3A%2F%2Funknown-possibilities-846f26e3e4d7.herokuapp.com%2Faccounts%2Fproduct-management%2F) |
| Bag Page | Pass | [Bag Page Validation](https://validator.w3.org/nu/?showsource=yes&doc=https%3A%2F%2Funknown-possibilities-846f26e3e4d7.herokuapp.com%2Fbag%2F) |
| Checkout Page | Pass | [Checkout Page Validation](https://validator.w3.org/nu/?showsource=yes&doc=https%3A%2F%2Funknown-possibilities-846f26e3e4d7.herokuapp.com%2Fcheckout%2F) |
| Checkout Success Page | Pass | [Checkout Success Page](https://validator.w3.org/nu/?showsource=yes&doc=https%3A%2F%2Funknown-possibilities-846f26e3e4d7.herokuapp.com%2Fcheckout%2Fcheckout_success%2F80DD2658845D4AB5BB287F3C290BD1DF%2F) |
| Edit Product Page | Pass | [Edit Product Page](https://validator.w3.org/nu/?showsource=yes&doc=https%3A%2F%2Funknown-possibilities-846f26e3e4d7.herokuapp.com%2Faccounts%2Fproduct%2F6%2Fedit%2F) |
| Add Product Page | Pass | [Add Product Page Validation](https://validator.w3.org/nu/?doc=https%3A%2F%2Funknown-possibilities-846f26e3e4d7.herokuapp.com%2Faccounts%2Flogin%2F%3Fnext%3D%2Faccounts%2Fproduct%2Fadd%2F) |
---


### CSS

[W3C](https://validator.w3.org/) was used to validate the CSS.

| File | Result | Evidence |
| :--- | :--- | :---: |
| Base.CSS | Pass | [Base.css Validation](documentation/testing/validation/css/base-css-w3c.png) |
| Checkout.CSS | Pass | [Checkout.css Validation](documentation/testing/validation/css/checkout-css.png) |
| Bag.CSS | Pass | [Bag.css Validation](documentation/testing/validation/css/bag-css.png) |
---

### JavaScript

[JS Hint](https://jshint.com/) was used to validate the JavaScript.

| File | Result | Evidence |
| :--- | :--- | :---: |
| Stripe Elements JS | Pass | [Stripe  Element JS Validation](documentation/testing/validation/js/jshint-stripe.png) |
| Card Of The Day JS | Pass | [Card Of The Day JS Validation](documentation/testing/validation/js/jshint-card-of-day.png) |
---

### Python

[Code Institute Python Linter](https://pep8ci.herokuapp.com/) was used to validate the python. I have also installed [PyCodeStyle](https://pycodestyle.pycqa.org/en/latest/intro.html#configuration) in my IDE to enable me to check my code meets PEP8 guidelines during development.

| File | Result | Evidence |
| :--- | :--- | :---: |
|**Unknown_Possibilities**|
| unknown_possibilities/settings.py | Pass | [settings.py validation](documentation/testing/validation/python/pep8-settings.png) |
| unknown_possibilities/urls.py | Pass | [urls.py validation](documentation/testing/validation/python/pep8-up-urls.png) |
| **BAG** |
| bag/contexts.py | Pass | [contexts.py validation](documentation/testing/validation/python/pep8-bag-contexts.png) |
| bag/urls.py | Pass | [urls.py validation](documentation/testing/validation/python/pep-8-bag-urls.png) |
| bag/views.py | Pass | [views.py validation](documentation/testing/validation/python/pep-8-bag-views.png) |
| bag/test.py | Pass | [test.py validation](documentation/testing/validation/python/pep-8-bag-test.png) |
| **CHECKOUT** |
| checkout/admin.py | Pass | [admin.py validation](documentation/testing/validation/python/pep-8-checkout-admin.png) |
| checkout/forms.py | Pass | [forms.py validation](documentation/testing/validation/python/pep-8-checkout-forms.png) |
| checkout/models.py | Pass | [models.py validation](documentation/testing/validation/python/pep-8-ceckout-models.png) |
| checkout/signals.py | Pass | [signals.py validation](documentation/testing/validation/python/pep-8-ceckout-signals.png) |
| checkout/urls.py | Pass | [urls.py validation](documentation/testing/validation/python/pep-8-checkout-urls.png) |
| checkout/views.py | Pass | [views.py](documentation/testing/validation/python/pep-8checkout-views.png) |
| checkout/webhooks.py | Pass| [webhooks.py](documentation/testing/validation/python/pep-8-checkout-webhooks.png) |
| checkout/test_forms.py | Pass | [test_forms.py validation](documentation/testing/validation/python/pep-8-checkout-test.png)|
| **HOME** |
| home/contexts_processors.py | Pass | [contexts_processors.py validation](documentation/testing/validation/python/pep8-h-context.png) |
| home/urls.py | Pass | [urls.py validation](documentation/testing/validation/python/pep8-h-urls.png)|
| home/views.py | Pass | [views.py validation](documentation/testing/validation/python/pep8-h-views.png) |
| home/test.py | Pass | [test.py validation](documentation/testing/validation/python/pep8-h-test.png) |
| **PRODUCTS** |
| products/admin.py | Pass | [admin.py validation](documentation/testing/validation/python/pep8-products-admin.png) |
| products/forms.py | Pass | [forms.py validation](documentation/testing/validation/python/pep8-products-forms.png) |
| products/models.py | Pass | [models.py validation](documentation/testing/validation/python/pep8-products-models.png) |
| products/urls.py | Pass | [urls.py validation](documentation/testing/validation/python/pep8-products-urls.png) |
| products/views.py | Pass | [views.py validation](documentation/testing/validation/python/pep8-products-views.png) |
| products/tests.py | Pass | [tests.py](documentation/testing/validation/python/pep8-products-test.png) |
| **ACCOUNTS** |
| accounts/apps.py | Pass | [apps.py validation](documentation/testing/validation/python/pep8-account-apps.png) |
| accounts/admin.py | Pass | [forms.py validation](documentation/testing/validation/python/pep8-account-admin.png) |
| accounts/forms.py | Pass | [forms.py validation](documentation/testing/validation/python/pep8-account-forms.png) |
| accounts/models.py | Pass | [models.py validation](documentation/testing/validation/python/pep8-account-models.png) |
| accounts/urls.py | Pass | [urls.py validation](documentation/testing/validation/python/pep8-account-urls.png) |
| accounts/views.py | Pass | [views.py validation](documentation/testing/validation/python/pep8-account-views.png) |
| accounts/tests.py | Pass | [tests.py validation](documentation/testing/validation/python/pep-8-accounts-test.png) |
| accounts/signals.py | Pass | [signals.py validation](documentation/testing/validation/python/pep8-account-signals.png) |
| **DAILY-CARDS** |
| daily-card/admin.py | Pass | [admin.py validation](documentation/testing/validation/python/pep-8-daily-admin.png) |
| daily-card/models.py | Pass | [models.py validation](documentation/testing/validation/python/pep8-dc-models.png) |
| daily-card/urls.py | Pass | [urls.py validation](documentation/testing/validation/python/pep8-dc-urls.png) |
| daily-card/views.py | Pass | [views.py validation](documentation/testing/validation/python/pep8-dc-views.png) |
| daily-card/tests.py | Pass | [tests.py validation](documentation/testing/validation/python/pep8-dc-test.png) |
| **READINGS** |
| readings/admin.py | Pass | [admin.py validation](documentation/testing/validation/python/pep8-read-admin.png) |
| readings/models.py | Pass | [models.py validation](documentation/testing/validation/python/pep8-read-models.png) |
| readings/tests.py | Pass | [tests.py validation](documentation/testing/validation/python/pep8-read-test.png) |
| readings/urls.py | Pass | [urls.py validation](documentation/testing/validation/python/pep8-read-urls.png) |
| readings/views.py | Pass | [views.py validation](documentation/testing/validation/python/pep8-read-views.png) |
| readings/forms.py | Pass | [forms.py validation](documentation/testing/validation/python/pep8-read-forms.png) |


### Lighthouse

I have used Googles Lighthouse testing to test the performance, accessibility, best practices and SEO of the site.

#### Desktop Results

| Page | Result |
| :--- | :--- |


#### Mobile Results

| Page | Result |
| :--- | :--- |


## Manual Testing

### Testing User Stories

| User Story ID | As a/an | I want to be able to ... | So that I can... | How is this achieved? | Evidence |
| :--- | :--- | :--- | :---| :--- | :---: |

### Full Testing

Full testing was performed on the following devices:
| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
| :--- | :--- | :--- | :--- | :--- |


## Bugs

### Solved Bugs

| No | Bug | How I solved the issue | Evidence |
|:--- | :--- | :--- | :---: |


### Known Bugs

| No | Bug | Evidence |
|:--- | :--- | :---: |