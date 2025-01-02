const PAGE_NAME = "india-compliance-account";
let icAccountPage;

dontmanage.pages[PAGE_NAME].on_page_load = async function (wrapper) {
    await dontmanage.require([
        "india_compliance_account.bundle.js",
        "india_compliance_account.bundle.css",
    ]);

    icAccountPage = new india_compliance.pages.IndiaComplianceAccountPage(wrapper, PAGE_NAME);
};
