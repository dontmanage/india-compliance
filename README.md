<div align="center">

<!-- TODO: add link to website once it is ready -->
<h1>India Compliance</h1>

Simple, yet powerful compliance solutions for Indian businesses

[![Server Tests](https://github.com/resilient-tech/india-compliance/actions/workflows/server-tests.yml/badge.svg)](https://github.com/resilient-tech/india-compliance/actions/workflows/server-tests.yml)

</div>



## Introduction

India Compliance has been designed to make compliance with Indian rules and regulations simple, swift and reliable. To this end, it has been carefully integrated with GST APIs to simplify recurring compliance processes.

It builds on top of [DontManageErp](https://github.com/dontmanage/dontmanageerp) and the [DontManage Framework](https://github.com/dontmanage/dontmanage) - incredible FOSS projects built and maintained by the incredible folks at DontManage. Go check these out if you haven't already!

## Key Features

- End-to-end GST e-Waybill management
- Automated GST e-Invoice generation and cancellation
- Autofill Party and Address details by entering their GSTIN
- Configurable features based on business needs
- Powerful validations to ensure correct compliance

For a detailed overview of these features, please [refer to the documentation](https://docs.dontmanageerp.com/docs/v14/user/manual/en/regional/india).

## Installation

Once you've [set up a DontManage site](https://dontmanageframework.com/docs/v14/user/en/installation/), installing India Compliance is simple:


1. Download the app using the Bench CLI.

    ```bash
    bench get-app --branch [branch name] https://github.com/resilient-tech/india-compliance.git
    ```

    Replace `[branch name]` with the appropriate branch as per your setup:

    | DontManage Branch | India Compliance Branch |
    |---------------|-------------------------|
    | version-14    | version-14              |
    | develop       | next                    |

    If it isn't specified, the `--branch` option will default to `next`.

2. Install the app on your site.

    ```bash
    bench --site [site name] install-app india_compliance
    ```

## In-app Purchases

Some of the automation features available in India Compliance require access to [GST APIs](https://discuss.dontmanageerp.com/t/introducing-india-compliance/86335#a-note-on-gst-apis-3). Since there are some costs associated with these APIs, they can be accessed by signing up for an India Compliance Account after installing this app.

## Planned Features

- Advanced purchase reconciliation based on GSTR-2B and GSTR-2A
- Quick and easy filing process for GSTR-1 and GSTR-3B

## Contributing

- [Issue Guidelines](https://github.com/dontmanage/dontmanageerp/wiki/Issue-Guidelines)
- [Pull Request Requirements](https://github.com/dontmanage/dontmanageerp/wiki/Contribution-Guidelines)

## License

[GNU General Public License (v3)](https://github.com/resilient-tech/india-compliance/blob/develop/license.txt)
