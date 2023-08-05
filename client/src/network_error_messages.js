import { Platform_Name } from './platform_name';

// server responded with a unknown non-2xx status code ... to be appended by actual server error message received
const unknown_non_2xx_message = 'Apologies! The server encountered an error while processing your request. Please try again later or contact our team for further assistance if the problem persists.'
export const Unknown_Non_2xx_Message = unknown_non_2xx_message

// request was made but no response was received ... network error
const network_error_message = 'Oops! It seems there was a problem with the network while processing your request. Please check your internet connection and try again.'
export const Network_Error_Message = network_error_message

// error occured during request setup ... no network access
const no_network_access_message = "We're sorry but it appears that you don't have an active internet connection. Please connect to the internet and try again."
export const No_Network_Access_Message = no_network_access_message