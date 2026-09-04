<#-- Standard Article Template -->
<div class="content-article-wrapper py-5">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-8 col-md-10">
                
                <#-- Check if highlighted -->
                <#if highlightBanner.getData()?? && highlightBanner.getData() == "true">
                    <div class="alert alert-info text-center rounded mb-4" role="alert">
                        <strong class="text-uppercase tracking-wide">Hot Topic</strong>
                    </div>
                </#if>

                <#-- Headline -->
                <h1 class="display-3 font-weight-bold mb-4 text-dark">${headline.getData()}</h1>

                <#-- Image banner -->
                <#if featureImage.getData()?? && featureImage.getData() != "">
                    <div class="img-banner rounded-lg shadow overflow-hidden mb-5">
                        <img 
                            src="${featureImage.getData()}" 
                            class="img-fluid w-100" 
                            alt="${featureImage.getAttribute("alt")!""}" 
                        />
                    </div>
                </#if>

                <#-- Body -->
                <div class="article-text-content lead lh-lg text-secondary">
                    ${contentBody.getData()}
                </div>

            </div>
        </div>
    </div>
</div>
