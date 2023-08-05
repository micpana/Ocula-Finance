import React, { Component, useReducer } from 'react';
import {
    Collapse, 
    Nav, NavItem, NavLink, 
    UncontrolledDropdown, Dropdown, DropdownToggle, DropdownMenu, DropdownItem, 
    Input, InputGroup,
    Button, Row, Col, Form, Container, Label
} from "reactstrap";
import { withCookies, Cookies } from 'react-cookie';
import { instanceOf } from 'prop-types';
import { Helmet } from 'react-helmet'
import {
    Audio,
    BallTriangle,
    Bars,
    Circles,
    Grid,
    Hearts,
    Oval,
    Puff,
    Rings,
    SpinningCircles,
    TailSpin,
    ThreeDots,
} from '@agney/react-loading';
import { Platform_Name } from '../platform_name';
import { Backend_Server_Address } from '../backend_server_url';
import { Access_Token_Cookie_Name } from '../access_token_cookie_name';
import { Unknown_Non_2xx_Message, Network_Error_Message, No_Network_Access_Message } from '../network_error_messages';
import { Message, useToaster } from "rsuite";

class Settings extends Component{
    static propTypes = {
        cookies: instanceOf(Cookies).isRequired
    };
    constructor(props) { 
        super(props);
        this.state = {
            loading: false,
            input_errors: {},
            user_details: {},
            firstname: '',
            lastname: '',
            username: '',
            email: '',
            phonenumber: '',
            password: '',
            new_password: '',
            new_password_confirmation: '',
            country: ''
        };

        this.HandleChange = (e) => {
            this.setState({[e.target.name]: e.target.value});
        };

        this.SetInputError = (field, error) => { // error -> required / invalid
            var new_error = {
                [field]: error
            }
            var updated_input_errors = {
                ...this.state.input_errors,
                ...new_error
            }
            this.setState({input_errors: updated_input_errors})
        }

        this.ClearInputErrors = () => {
            this.setState({input_errors: {}})
        }

        this.IsEmailStructureValid = (email) => {
            // regex
            const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

            // return true if email has proper structure
            return regex.test(email)
        }

        this.IsPasswordStructureValid = (password) => {
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
            return password.length > 8 && has_uppercase && has_lowercase && has_number && has_special_character
        }

        this.Notification = (message, message_type) => { // message type -> info / success / warning / error
            const toaster = useToaster();
            
            // push notification message
            toaster.push(<Message>{message}</Message>, {
                placement: 'topCenter',
                closable: true,
                type: message_type,
                showIcon: true,
                duration: 15000
            });
        }

        this.SplitUserDetailsToIndividualStates = (user_details) => {
            this.setState({
                firstname: user_details.firstname,
                lastname: user_details.lastname,
                username: user_details.username,
                email: user_details.email,
                phonenumber: user_details.phonenumber,
                country: user_details.country
            })
        }

        this.GetUserDetails = () => {
            const { cookies } = this.props;
            this.setState({loading: true})

            axios.post(Backend_Server_Address + 'getUserDetailsByAccessToken', null, { headers: { 'access_token': cookies.get(Access_Token_Cookie_Name) }  })
            .then((res) => {
                let result = res.data
                // set user details to state
                this.setState({user_details: result, loading: false})
                // split user details to individual states
                this.SplitUserDetailsToIndividualStates(result)
            }).catch((error) => {
                console.log(error)
                if (error.response){ // server responded with a non-2xx status code
                    let status_code = error.response.status
                    let result = error.response.data
                    var notification_message = ''
                    if(
                        result === 'Access token disabled via signout' ||
                        result === 'Access token expired' ||
                        result === 'Not authorized to access this' ||
                        result === 'Invalid token'
                    ){ 
                        // delete token from user cookies
                        cookies.remove(Access_Token_Cookie_Name, { path: '/' });
                        // redirect to sign in
                        let port = (window.location.port ? ':' + window.location.port : '');
                        window.location.href = '//' + window.location.hostname + port + '/signin';
                    }else{
                        notification_message = 'Apologies! The server encountered an error while processing your request (Error ' + status_code.toString() + ': ' + result + '). Please try again later or contact our team for further assistance.'
                        this.Notification(notification_message, 'error')
                    }
                }else if (error.request){ // request was made but no response was received ... network error
                    this.Notification('Oops! It seems there was a problem with the network while processing your request. Please check your internet connection and try again.', 'error')
                }else{ // error occured during request setup ... no network access
                    this.Notification("We're sorry but it appears that you don't have an active internet connection. Please connect to the internet and try again.", 'error')
                }
                this.setState({loading: false})
            })
        }

        this.UpdateUserDetailsStateToNewInformation = () => {
            // get existing details
            var user_details = this.state.user_details

            // make updates
            user_details['firstname'] = this.state.firstname
            user_details['lastname'] = this.state.lastname
            user_details['username'] = this.state.username
            user_details['email'] = this.state.email
            user_details['phonenumber'] = this.state.phonenumber
            user_details['country'] = this.state.country

            // update user details state
            this.setState({user_details: user_details})
        }

        this.EditProfile = () => {
            // initialize variable to store input validation status
            var data_checks_out = true

            // clear existing input errors if any
            this.ClearInputErrors()

            // validate input data
            if (this.state.firstname === ''){ this.SetInputError('firstname', 'required'); data_checks_out = false }
            if (this.state.lastname === ''){ this.SetInputError('lastname', 'required'); data_checks_out = false }
            if (this.state.username === ''){ this.SetInputError('username', 'required'); data_checks_out = false }
            if (this.state.email === ''){ this.SetInputError('email', 'required'); data_checks_out = false }
            if (this.IsEmailStructureValid(this.state.email) === false){ this.SetInputError('email', 'invalid'); data_checks_out = false }
            if (this.state.phonenumber === ''){ this.SetInputError('phonenumber', 'required'); data_checks_out = false }
            if (this.state.password === ''){ this.SetInputError('password', 'required'); data_checks_out = false }
            if (this.state.country === ''){ this.SetInputError('country', 'required'); data_checks_out = false }
            // only validate if a new password has been set
            if (this.state.new_password != '' || this.state.new_password_confirmation != ''){
                if (this.IsPasswordStructureValid(this.state.new_password) === false){ this.SetInputError('new_password', 'invalid'); data_checks_out = false }
                if (this.state.new_password_confirmation === ''){ this.SetInputError('new_password_confirmation', 'required'); data_checks_out = false }
                if (this.state.new_password != this.state.new_password_confirmation){ this.SetInputError('new_password_mismatch', 'invalid'); data_checks_out = false }
            }

            // check data collection status
            if (data_checks_out === false){ // user needs to check their input data
                this.Notification('Check input fields for errors.', 'error')
            }else{ // send data to server
                const { cookies } = this.props;
                this.setState({loading: true})

                var data = new FormData()
                data.append('firstname', this.state.firstname)
                data.append('lastname', this.state.lastname)
                data.append('username', this.state.username)
                data.append('email', this.state.email)
                data.append('phonenumber', this.state.phonenumber)
                data.append('password', this.state.password)
                data.append('new_password', this.state.new_password)
                data.append('country', this.state.country)

                axios.post(Backend_Server_Address + 'editProfile', data, { headers: { 'access_token': cookies.get(Access_Token_Cookie_Name) }  })
                .then((res) => {
                    let result = res.data
                    // clear password fields
                    this.setState({
                        password: '',
                        new_password: '',
                        new_password_confirmation: ''
                    })
                    // update user details state to new information ... without sending another request to the server
                    this.UpdateUserDetailsStateToNewInformation()
                    // set loading to false
                    this.setState({loading: false})
                    // check result and notify user of successful request accordingly
                    if (result === 'ok'){
                        this.Notification('Profile edit successful.', 'success')
                    }else if (result === 'ok, email verification sent'){
                        this.Notification("Profile edit successful. We've sent you an email at " + this.state.email + " to verify if its truly yours. Follow its instructions to verify your new email.", 'success')
                    }
                }).catch((error) => {
                    console.log(error)
                    if (error.response){ // server responded with a non-2xx status code
                        let status_code = error.response.status
                        let result = error.response.data
                        var notification_message = ''
                        if(
                            result === 'Access token disabled via signout' ||
                            result === 'Access token expired' ||
                            result === 'Not authorized to access this' ||
                            result === 'Invalid token'
                        ){ 
                            // delete token from user cookies
                            cookies.remove(Access_Token_Cookie_Name, { path: '/' });
                            // redirect to sign in
                            let port = (window.location.port ? ':' + window.location.port : '');
                            window.location.href = '//' + window.location.hostname + port + '/signin';
                        }
                        else if (result == 'incorrect password'){ notification_message = "The password you've entered is incorrect." }
                        else if(result === 'new password matches existing'){ notification_message = "The new password you've entered matches your existing password." }
                        else if(result === 'email in use'){ notification_message = "The email you've entered is already in use on this platform." }
                        else if (result === 'username in use'){ notification_message = "The username you've entered is already in use on this platform." }
                        else if (result === 'phonenumber in use'){ notification_message = "The phonenumber you've entered is already in use on this platform." }
                        else if (result === 'invalid email structure'){ notification_message = "The email you've entered does not have a valid structure." }
                        else if (result === 'invalid password structure'){ notification_message = "The password you've entered does not have a valid structure." }
                        else{
                            notification_message = 'Apologies! The server encountered an error while processing your request (Error ' + status_code.toString() + ': ' + result + '). Please try again later or contact our team for further assistance.'
                        }
                        this.Notification(notification_message, 'error')
                    }else if (error.request){ // request was made but no response was received ... network error
                        this.Notification('Oops! It seems there was a problem with the network while processing your request. Please check your internet connection and try again.', 'error')
                    }else{ // error occured during request setup ... no network access
                        this.Notification("We're sorry but it appears that you don't have an active internet connection. Please connect to the internet and try again.", 'error')
                    }
                    this.setState({loading: false})
                })
            }
        }
    }

    componentDidMount() {
        this.GetUserDetails()
    }

    render() {
        return (
            <div>
                <Helmet>
                    <title>Settings | {Platform_Name}</title>
                    {/* <meta name="description" content="" /> */}
                </Helmet>
                {
                    this.state.loading == true
                    ? <div>
                        <br/><br/><br/>
                        <h5 style={{color: '#1faced'}}>Loading...</h5>
                        <br/><br/><br/>
                        <TailSpin width='180px' style={{color: '#1faced'}}/>
                    </div>
                    : <div>
                        
                    </div>
                }
            </div>
        );
    }

};

export default withCookies(Settings);