// GET CREDENTIALS FROM ENVIRONMENT VARIABLES: -----------------------------------------------------------------------------------

// EmailJs ***********************************************************************************************************************
export const EmailJsServiceID = () => {
    // get service id
    const service_id = process.env.EmailJsServiceID

    // return service id
    return service_id
}

export const EmailJsTemplateID = () => {
    // get template id
    const template_id = process.env.EmailJsTemplateID

    // return template id
    return template_id
}

export const EmailJsAPIKey = () => {
    // get api key
    const api_key = process.env.EmailJsAPIKey

    // return api key
    return api_key
}