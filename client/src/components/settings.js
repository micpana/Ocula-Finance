import React, { Component, useReducer } from 'react';
import {
    Collapse, 
    Nav, NavItem, NavLink, 
    UncontrolledDropdown, Dropdown, DropdownToggle, DropdownMenu, DropdownItem, 
    Input, InputGroup, InputGroupText,
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
import { ToastContainer, toast } from 'react-toastify';
import { Platform_Name } from '../platform_name';
import { Backend_Server_Address } from '../backend_server_url';
import { Access_Token_Cookie_Name } from '../access_token_cookie_name';
import axios from 'axios';
import { Unknown_Non_2xx_Message, Network_Error_Message, No_Network_Access_Message } from '../network_error_messages';
import LoadingScreen from './loading_screen';
import InputErrors from './input_errors';
import Notification from './notification_alert';
import { IsEmailStructureValid, IsPasswordStructureValid } from './input_syntax_checks'
import { FaUserAlt, FaUsers, FaUserAstronaut, FaAt, FaPhoneAlt, FaUserLock, FaKey } from 'react-icons/fa';

class Settings extends Component{
    static propTypes = {
        cookies: instanceOf(Cookies).isRequired
    };
    constructor(props) { 
        super(props);
        this.state = {
            loading: false,
            input_errors: {},
            on_mobile: false,
            user_details: {},
            firstname: 'Michael',
            lastname: 'Mudimbu',
            username: 'micpana',
            email: 'michaelmudimbu@gmail.com',
            phonenumber: '+263782464219',
            password: '',
            new_password: '',
            new_password_confirmation: '',
            country: 'Zimbabwe'
        };

        this.HandleChange = (e) => {
            this.setState({[e.target.name]: e.target.value});
        };

        this.SetInputError = (field, error) => { // error -> required / invalid
            // existing errors
            var existing_errors = this.state.input_errors

            // existing errors modified
            existing_errors[field] = error

            // update state
            this.setState({input_errors: existing_errors})
        }

        this.ClearInputErrors = () => {
            // existing errors
            var existing_errors = this.state.input_errors
            // array of existing error field names
            var existing_error_fields = Object.keys(existing_errors)
            // set existing error fields to undefined, clearing them
            existing_error_fields.map((item, index) => {
                existing_errors[item] = undefined
            })
            this.setState({input_errors: existing_errors})
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
                        Notification(notification_message, 'error')
                    }
                }else if (error.request){ // request was made but no response was received ... network error
                    Notification('Oops! It seems there was a problem with the network while processing your request. Please check your internet connection and try again.', 'error')
                }else{ // error occured during request setup ... no network access
                    Notification("We're sorry but it appears that you don't have an active internet connection. Please connect to the internet and try again.", 'error')
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

        this.EditProfile = (e) => {
            e.preventDefault()
            
            // initialize variable to store input validation status
            var data_checks_out = true

            // clear existing input errors if any
            this.ClearInputErrors()

            // validate input data
            if (this.state.firstname === ''){ this.SetInputError('firstname', 'required'); data_checks_out = false }
            if (this.state.lastname === ''){ this.SetInputError('lastname', 'required'); data_checks_out = false }
            if (this.state.username === ''){ this.SetInputError('username', 'required'); data_checks_out = false }
            if (this.state.email === ''){ this.SetInputError('email', 'required'); data_checks_out = false }
            if (IsEmailStructureValid(this.state.email) === false){ this.SetInputError('email', 'invalid'); data_checks_out = false }
            if (this.state.phonenumber === ''){ this.SetInputError('phonenumber', 'required'); data_checks_out = false }
            if (this.state.password === ''){ this.SetInputError('password', 'required'); data_checks_out = false }
            if (this.state.country === ''){ this.SetInputError('country', 'required'); data_checks_out = false }
            // only validate if a new password has been set
            if (this.state.new_password != '' || this.state.new_password_confirmation != ''){
                if (IsPasswordStructureValid(this.state.new_password) === false){ this.SetInputError('new_password', 'invalid'); data_checks_out = false }
                if (this.state.new_password_confirmation === ''){ this.SetInputError('new_password_confirmation', 'required'); data_checks_out = false }
                if (this.state.new_password != this.state.new_password_confirmation){ this.SetInputError('new_password_mismatch', 'invalid'); data_checks_out = false }
            }

            // check data collection status
            if (data_checks_out === false){ // user needs to check their input data
                Notification('Check input fields for errors.', 'error')
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
                        Notification('Profile edit successful.', 'success')
                    }else if (result === 'ok, email verification sent'){
                        Notification("Profile edit successful. We've sent you an email at " + this.state.email + " to verify if its truly yours. Follow its instructions to verify your new email.", 'success')
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
                            notification_message = Unknown_Non_2xx_Message + ' (Error '+status_code.toString()+': '+result+')'
                        }
                        Notification(notification_message, 'error')
                    }else if (error.request){ // request was made but no response was received ... network error
                        Notification(Network_Error_Message, 'error')
                    }else{ // error occured during request setup ... no network access
                        Notification(No_Network_Access_Message, 'error')
                    }
                    this.setState({loading: false})
                })
            }
        }
    }

    componentDidMount() {
        if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
            this.setState({
                on_mobile: true
            })
        }
        // get user details
        // this.GetUserDetails()
    }

    render() {
        return (
            <div>
                <Helmet>
                    <title>Settings | {Platform_Name}</title>
                    {/* <meta name="description" content="" /> */}
                </Helmet>
                <ToastContainer />
                {
                    this.state.loading === true
                    ? <LoadingScreen />
                    : <div>
                        <br/>
                        <h5 style={{fontWeight: 'bold'}}>
                            Settings
                        </h5>
                        <br/><br/>
                        <Form onSubmit={this.EditProfile}>
                            <Row>
                                <Col sm='6'>
                                    <Label>Firstname <span style={{color: 'red'}}>*</span></Label>
                                    <InputGroup>
                                        <InputGroupText addonType="prepend">
                                            <FaUserAlt style={{margin:'10px'}}/>
                                        </InputGroupText>
                                        <Input style={{border: 'none', borderBottom: '1px solid #828884', backgroundColor: 'inherit'}}
                                            placeholder="Firstname" name="firstname" id="firstname"
                                            value={this.state.firstname} onChange={this.HandleChange} type="text" 
                                        />
                                    </InputGroup>
                                    <InputErrors field_error_state={this.state.input_errors['firstname']} field_label='Firstname' />
                                    <br/>
                                </Col>
                                <Col>
                                    <Label>Lastname <span style={{color: 'red'}}>*</span></Label>
                                    <InputGroup>
                                        <InputGroupText addonType="prepend">
                                            <FaUsers style={{margin:'10px'}}/>
                                        </InputGroupText>
                                        <Input style={{border: 'none', borderBottom: '1px solid #828884', backgroundColor: 'inherit'}}
                                            placeholder="Lastname" name="lastname" id="lastname"
                                            value={this.state.lastname} onChange={this.HandleChange} type="text" 
                                        />
                                    </InputGroup>
                                    <InputErrors field_error_state={this.state.input_errors['lastname']} field_label='Lastname' />
                                    <br/>
                                </Col>
                            </Row>
                            <br/>
                            <Row>
                                <Col sm='6'>
                                    <Label>Username <span style={{color: 'red'}}>*</span></Label>
                                    <InputGroup>
                                        <InputGroupText addonType="prepend">
                                            <FaUserAstronaut style={{margin:'10px'}}/>
                                        </InputGroupText>
                                        <Input style={{border: 'none', borderBottom: '1px solid #828884', backgroundColor: 'inherit'}}
                                            placeholder="Username" name="username" id="username"
                                            value={this.state.username} onChange={this.HandleChange} type="text" 
                                        />
                                    </InputGroup>
                                    <InputErrors field_error_state={this.state.input_errors['username']} field_label='Username' />
                                    <br/>
                                </Col>
                                <Col>
                                    <Label>Email <span style={{color: 'red'}}>*</span></Label>
                                    <InputGroup>
                                        <InputGroupText addonType="prepend">
                                            <FaAt style={{margin:'10px'}}/>
                                        </InputGroupText>
                                        <Input style={{border: 'none', borderBottom: '1px solid #828884', backgroundColor: 'inherit'}}
                                            placeholder="Email" name="email" id="email"
                                            value={this.state.email} onChange={this.HandleChange} type="text" 
                                        />
                                    </InputGroup>
                                    <InputErrors field_error_state={this.state.input_errors['email']} field_label='Email' />
                                    <br/>
                                </Col>
                            </Row>
                            <br/>
                            <Row>
                                <Col sm='6'>
                                    <Label>Phonenumber <span style={{color: 'red'}}>*</span></Label>
                                    <InputGroup>
                                        <InputGroupText addonType="prepend">
                                            <FaPhoneAlt style={{margin:'10px'}}/>
                                        </InputGroupText>
                                        <Input style={{border: 'none', borderBottom: '1px solid #828884', backgroundColor: 'inherit'}}
                                            placeholder="Phonenumber" name="phonenumber" id="phonenumber"
                                            value={this.state.phonenumber} onChange={this.HandleChange} type="text" 
                                        />
                                    </InputGroup>
                                    <InputErrors field_error_state={this.state.input_errors['phonenumber']} field_label='Phonenumber' />
                                    <br/>
                                </Col>
                                <Col>
                                    <Label>Password <span style={{color: 'red'}}>*</span></Label>
                                    <InputGroup>
                                        <InputGroupText addonType="prepend">
                                            <FaUserLock style={{margin:'10px'}}/>
                                        </InputGroupText>
                                        <Input style={{border: 'none', borderBottom: '1px solid #828884', backgroundColor: 'inherit'}}
                                            placeholder="Password" name="password" id="password"
                                            value={this.state.password} onChange={this.HandleChange} type="password" 
                                        />
                                    </InputGroup>
                                    <InputErrors field_error_state={this.state.input_errors['password']} field_label='Password' />
                                    <br/>
                                </Col>
                            </Row>
                            <br/>
                            <p style={{fontWeight: 'bold'}}>
                                Use the input fields below only if you wish to change your account password
                            </p>
                            <br/>
                            <Row>
                                <Col sm='6'>
                                    <Label>New Password <span style={{color: 'red'}}>*</span></Label>
                                    <InputGroup>
                                        <InputGroupText addonType="prepend">
                                            <FaKey style={{margin:'10px'}}/>
                                        </InputGroupText>
                                        <Input style={{border: 'none', borderBottom: '1px solid #828884', backgroundColor: 'inherit'}}
                                            placeholder="New Password" name="new_password" id="new_password"
                                            value={this.state.new_password} onChange={this.HandleChange} type="password" 
                                        />
                                    </InputGroup>
                                    <InputErrors field_error_state={this.state.input_errors['new_password']} field_label='New Password' />
                                    <br/>
                                </Col>
                                <Col>
                                    <Label>New Password Confirmation <span style={{color: 'red'}}>*</span></Label>
                                    <InputGroup>
                                        <InputGroupText addonType="prepend">
                                            <FaKey style={{margin:'10px'}}/>
                                        </InputGroupText>
                                        <Input style={{border: 'none', borderBottom: '1px solid #828884', backgroundColor: 'inherit'}}
                                            placeholder="New Password Confirmation" name="new_password_confirmation" id="new_password_confirmation"
                                            value={this.state.new_password_confirmation} onChange={this.HandleChange} type="password" 
                                        />
                                    </InputGroup>
                                    <InputErrors field_error_state={this.state.input_errors['new_password_confirmation']} field_label='New Password Confirmation' />
                                    <br/>
                                </Col>
                            </Row>
                            <br/><br/><br/>
                            <Button type="submit"
                                style={{border: '1px solid #00539C', borderRadius: '20px', color: '#ffffff', fontWeight: 'bold', backgroundColor: '#00539C'}}
                            >
                                Edit Profile
                            </Button>
                        </Form>
                    </div>
                }
            </div>
        );
    }

};

export default withCookies(Settings);