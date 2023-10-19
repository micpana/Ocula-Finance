export const IsEmailStructureValid = (email) => {
    // regex
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    // return true if email has proper structure
    return regex.test(email)
}

export const IsPasswordStructureValid = (password) => {
    // regex structures
    var uppercase_regex = /[A-Z]/
    var lowercase_regex = /[a-z]/
    var number_regex = /[0-9]/
    var special_character_regex = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/

    // check if password contains at least one character from each type
    var has_uppercase = uppercase_regex.test(password)
    var has_lowercase = lowercase_regex.test(password)
    var has_number = number_regex.test(password)
    var has_special_character = special_character_regex.test(password)

    // return true if password has at least 8 characters that include at least 1: number, uppercase letter, lowercase letter, special character
    return password.length >= 8 && has_uppercase && has_lowercase && has_number && has_special_character
}