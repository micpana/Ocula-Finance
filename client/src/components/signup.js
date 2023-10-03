import React, { Component, useReducer } from 'react';
import {
    Collapse, 
    Nav, NavItem, NavLink, 
    UncontrolledDropdown, Dropdown, DropdownToggle, DropdownMenu, DropdownItem, 
    Input, InputGroup, InputGroupAddon,
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
import axios from 'axios';
import { Unknown_Non_2xx_Message, Network_Error_Message, No_Network_Access_Message } from '../network_error_messages';
import LoadingScreen from './loading_screen';
import InputErrors from './input_errors';
import { Message, useToaster } from "rsuite";
import Signup1 from '../images/signup_1.svg'
import { FaUserAlt, FaUsers, FaUserAstronaut, FaAt, FaPhoneAlt, FaUserLock, FaKey } from 'react-icons/fa';

class Signup extends Component{
    static propTypes = {
        cookies: instanceOf(Cookies).isRequired
    };
    constructor(props) { 
        super(props);
        this.state = {
            loading: false,
            input_errors: {},
            firstname: '',
            lastname: '',
            username: '',
            email: '',
            phonenumber: '',
            password: '',
            password_confirmation: '',
            country: ''
        };

        this.HandleChange = (e) => {
            this.setState({[e.target.name]: e.target.value});
        };

        this.SetInputError = (field, error) => { // error -> required / invalid
            // if field error state doesn't already exist
            if (this.state.input_errors[field] == undefined){
                // new error
                var new_error = {
                    [field]: error
                }

                // existing errors + new
                var updated_input_errors = {
                    ...this.state.input_errors,
                    ...new_error
                }

                // update state
                this.setState({input_errors: updated_input_errors})
            }else{ // field error state already exists
                // existing errors
                var existing_errors = this.state.input_errors

                // existing errors modified
                existing_errors[field] = error

                // update state
                this.setState({input_errors: existing_errors})
            }
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

        this.Signup = () => {
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
            if (this.IsPasswordStructureValid(this.state.password) === false){ this.SetInputError('password', 'invalid'); data_checks_out = false }
            if (this.state.password_confirmation === ''){ this.SetInputError('password_confirmation', 'required'); data_checks_out = false }
            if (this.state.password != this.state.password_confirmation){ this.SetInputError('password_mismatch', 'invalid'); data_checks_out = false }
            if (this.state.country === ''){ this.SetInputError('country', 'required'); data_checks_out = false }

            // check data collection status
            if (data_checks_out === false){ // user needs to check their input data
                this.Notification('Check input fields for errors.', 'error')
            }else{ // send data to server
                this.setState({loading: true})

                var data = new FormData()
                data.append('firstname', this.state.firstname)
                data.append('lastname', this.state.lastname)
                data.append('username', this.state.username)
                data.append('email', this.state.email)
                data.append('phonenumber', this.state.phonenumber)
                data.append('password', this.state.password)
                data.append('country', this.state.country)

                axios.post(Backend_Server_Address + 'signup', data, { headers: { 'access_token': null }  })
                .then((res) => {
                    let result = res.data
                    var account_id = result
                    // redirect to email verification notice page
                    let port = (window.location.port ? ':' + window.location.port : '')
                    window.location.href = '//' + window.location.hostname + port + '/email-verification-sent/'  + account_id
                }).catch((error) => {
                    console.log(error)
                    if (error.response){ // server responded with a non-2xx status code
                        let status_code = error.response.status
                        let result = error.response.data
                        var notification_message = ''
                        if(result === 'email in use'){ notification_message = "The email you've entered is already in use on this platform." }
                        else if (result === 'invalid email structure'){ notification_message = "The email you've entered does not have a valid structure." }
                        else if (result === 'invalid password structure'){ notification_message = "The password you've entered does not have a valid structure." }
                        else if (result === 'phonenumber in use'){ notification_message = "The phonenumber you've entered is already in use on this platform." }
                        else if (result === 'username in use'){ notification_message = "The username you've entered is already in use on this platform." }
                        else{
                            notification_message = Unknown_Non_2xx_Message + ' (Error '+status_code.toString()+': '+result+')'
                        }
                        this.Notification(notification_message, 'error')
                    }else if (error.request){ // request was made but no response was received ... network error
                        this.Notification(Network_Error_Message, 'error')
                    }else{ // error occured during request setup ... no network access
                        this.Notification(No_Network_Access_Message, 'error')
                    }
                    this.setState({loading: false})
                })
            }
        }
    }

    componentDidMount() {
        // check access token existance
        const { cookies } = this.props;
        if(cookies.get(Access_Token_Cookie_Name) != null){
            let port = (window.location.port ? ':' + window.location.port : '');
            window.location.href = '//' + window.location.hostname + port + '/dashboard';
        }
    }

    render() {
        return (
            <div>
                <Helmet>
                    <title>Signup | {Platform_Name}</title>
                    {/* <meta name="description" content="" /> */}
                </Helmet>
                {
                    this.state.loading === true
                    ? <LoadingScreen />
                    : <div>
                        <Row>
                            <Col sm='6'>
                                <img src={Signup1} style={{width: '100%'}} />
                            </Col>
                            <Col>
                                <Container>
                                    <br/>
                                    <h2 style={{color: '#00539C'}}>Signup</h2>
                                    <br/><br/>
                                    <Form onSubmit={this.Signup}>
                                        <Row>
                                            <Col sm='6'>
                                                <Label>Firstname <span style={{color: 'red'}}>*</span></Label>
                                                <InputGroup>
                                                    <InputGroupAddon addonType="prepend">
                                                        <FaUserAlt style={{margin:'10px'}}/>
                                                    </InputGroupAddon>
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
                                                    <InputGroupAddon addonType="prepend">
                                                        <FaUsers style={{margin:'10px'}}/>
                                                    </InputGroupAddon>
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
                                                    <InputGroupAddon addonType="prepend">
                                                        <FaUserAstronaut style={{margin:'10px'}}/>
                                                    </InputGroupAddon>
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
                                                    <InputGroupAddon addonType="prepend">
                                                        <FaAt style={{margin:'10px'}}/>
                                                    </InputGroupAddon>
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
                                                    <InputGroupAddon addonType="prepend">
                                                        <FaPhoneAlt style={{margin:'10px'}}/>
                                                    </InputGroupAddon>
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
                                                    <InputGroupAddon addonType="prepend">
                                                        <FaUserLock style={{margin:'10px'}}/>
                                                    </InputGroupAddon>
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
                                        <Row>
                                            <Col sm='6'>
                                                <Label>Password Confirmation <span style={{color: 'red'}}>*</span></Label>
                                                <InputGroup>
                                                    <InputGroupAddon addonType="prepend">
                                                        <FaKey style={{margin:'10px'}}/>
                                                    </InputGroupAddon>
                                                    <Input style={{border: 'none', borderBottom: '1px solid #828884', backgroundColor: 'inherit'}}
                                                        placeholder="Password Confirmation" name="password_confirmation" id="password_confirmation"
                                                        value={this.state.password_confirmation} onChange={this.HandleChange} type="password" 
                                                    />
                                                </InputGroup>
                                                <InputErrors field_error_state={this.state.input_errors['password_confirmation']} field_label='Password Confirmation' />
                                                <br/>
                                            </Col>
                                            <Col>

                                            </Col>
                                        </Row>
                                        <br/>
                                        <h6>
                                            By signing up, you're agreeing to {Platform_Name}'s <a href='/terms-of-service' target='_blank'>
                                            Terms of Service</a> and acknowledge its <a href='/privacy-policy' target='_blank'>Privacy Policy</a>.
                                        </h6>
                                        <br/>
                                        <a>Click the highlighted text for further information.</a>
                                        <br/><br/>
                                        <Button type="submit"
                                            style={{border: '1px solid #00539C', borderRadius: '20px', color: '#ffffff', fontWeight: 'bold', backgroundColor: '#00539C'}}
                                        >
                                            Signup
                                        </Button>
                                    </Form>
                                </Container>
                                <br/><br/><br/>
                            </Col>
                        </Row>
                    </div>
                }
            </div>
        );
    }

};

export default withCookies(Signup);