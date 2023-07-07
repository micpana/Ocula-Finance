import { Platform_Name } from './platform_name';

// get platform name
var platform_name = Platform_Name
// remove spaces from platform name
platform_name = platform_name.replace(/\s/g, '')

// compile access token cookie name
export const Access_Token_Cookie_Name = platform_name + 'AccessToken'