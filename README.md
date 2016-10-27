# nephelaiio.cloudformation
Cloudformation templates for fun and work.

# Requirements
Code is written in Python 3; see the 
[requirements file](/requirements.txt) for detailed information on 
required packages

# Templates
Compiled templates are found on the [templates](/templates) directory.
[Troposphere](https://github.com/cloudtools/troposphere) template 
generators are found on the nephelaiio.cloudformation.templates package

# Testing
Smoke and template tests are located in the [/test](directory). 
All templates are tested for successful deployment using boto3.
Tests can be run using paver with `paver test` or directly using `pytest`

# Deployment
Please add active stack definitions to the deploy section of the 
[paver configuration file](pavement.txt). 
Travis will create the defined stacks by executing `paver deploy` with 
relevant credentials after every successful build.
