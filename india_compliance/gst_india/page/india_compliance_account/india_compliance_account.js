dontmanage.pages["india-compliance-account"].on_page_load = async function (wrapper) {
    await dontmanage.require([
        "india_compliance_account.bundle.js",
        "india_compliance_account.bundle.css",
    ]);

    new india_compliance.pages.IndiaComplianceAccountPage(wrapper);
};
