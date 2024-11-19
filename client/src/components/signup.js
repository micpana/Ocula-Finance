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
import NetworkErrorScreen from './network_error_screen';
import { IsEmailStructureValid, IsPasswordStructureValid } from './input_syntax_checks'
import Signup1 from '../images/signup_1.svg'
import { FaUserAlt, FaUsers, FaUserAstronaut, FaAt, FaPhoneAlt, FaUserLock, FaKey } from 'react-icons/fa';
import PhoneInput from 'react-phone-input-2'
import 'react-phone-input-2/lib/style.css'

class Signup extends Component{
    static propTypes = {
        cookies: instanceOf(Cookies).isRequired
    };
    constructor(props) { 
        super(props);
        this.state = {
            loading: false,
            network_error_screen: false,
            network_error_message: '',
            retry_function: null,
            input_errors: {},
            on_mobile: false,
            country_iso_code_by_ip_address: '',
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

        this.LoadingOn = () => {
            this.setState({loading: true})
        }

        this.LoadingOff = () => {
            this.setState({loading: false})
        }

        this.NetworkErrorScreenOn = (error_message, retry_function) => {
            this.setState({network_error_screen: true, network_error_message: error_message, retry_function: retry_function})
        }

        this.NetworkErrorScreenOff = () => {
            this.setState({network_error_screen: false, network_error_message: '', retry_function: null})
        }

        this.Signup = (e) => {
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
            if (IsPasswordStructureValid(this.state.password) === false){ this.SetInputError('password', 'invalid'); data_checks_out = false }
            if (this.state.password_confirmation === ''){ this.SetInputError('password_confirmation', 'required'); data_checks_out = false }
            if (this.state.password != this.state.password_confirmation){ this.SetInputError('password_confirmation', 'invalid'); data_checks_out = false }
            if (this.state.country === ''){ this.SetInputError('country', 'required'); data_checks_out = false }

            // check data collection status
            if (data_checks_out === false){ // user needs to check their input data
                Notification('Check input fields for errors.', 'error')
            }else{ // send data to server
                this.LoadingOn()

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
                        Notification(notification_message, 'error')
                    }else if (error.request){ // request was made but no response was received ... network error
                        Notification(Network_Error_Message, 'error')
                    }else{ // error occured during request setup ... no network access
                        Notification(No_Network_Access_Message, 'error')
                    }
                    this.LoadingOff()
                })
            }
        }

        this.ChangeCountryAndPhonenumber = (value, country, e, formattedValue) => {
            this.setState({
                country: country.name,
                phonenumber: value.toString()
            })
        }

        this.GetCountryByIP = () => {
            axios.get('https://ipapi.co/json/').then((response) => {
                let data = response.data;
                let country_code = data.country_code
                this.setState({
                    country_iso_code_by_ip_address: country_code.toLowerCase()
                });
            }).catch((error) => {
                console.log(error);
                this.GetCountryByIP()
            });
        }
    }

    componentDidMount() {
        if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
            this.setState({
                on_mobile: true
            })
        }

        // check access token existance
        const { cookies } = this.props;
        if(cookies.get(Access_Token_Cookie_Name) != null){
            let port = (window.location.port ? ':' + window.location.port : '');
            window.location.href = '//' + window.location.hostname + port + '/dashboard';
        }

        // get country by user ip address
        this.GetCountryByIP()
    }

    render() {
        return (
            <div>
                <Helmet>
                    <title>Signup | {Platform_Name}</title>
                    {/* <meta name="description" content="" /> */}
                </Helmet>
                <ToastContainer />
                {
                    this.state.loading === true
                    ? <LoadingScreen />
                    : this.state.network_error_screen === true
                    ? <NetworkErrorScreen error_message={this.state.network_error_message} retryFunction={this.state.retry_function} />
                    : <div>
                        <Row>
                            <Col sm='6'>
                                <img src={Signup1} onError={(e) => e.target.src = Signup1} style={{width: '100%'}} />
                                <a href='https://storyset.com/user'
                                    style={{marginTop: '10px', color: 'grey', fontSize: '13px'}} target='_blank'  rel='noreferrer'
                                >
                                    User illustrations by Storyset
                                </a>
                            </Col>
                            <Col>
                                <Container>
                                    <br/><br/><br/><br/>
                                    <h2 style={{color: '#00539C'}}>Signup</h2>
                                    <br/><br/>
                                    <Form onSubmit={this.Signup}>
                                        <Row style={{margin: '0px'}}>
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
                                        <Row style={{margin: '0px'}}>
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
                                        <Row style={{margin: '0px'}}>
                                            <Col sm='6'>
                                                <Label>Country and Phonenumber <span style={{color: 'red'}}>*</span></Label>
                                                <PhoneInput
                                                    country={this.state.country_iso_code_by_ip_address}
                                                    value={this.state.phonenumber}
                                                    onChange={(value, country, e, formattedValue) => this.ChangeCountryAndPhonenumber(value, country, e, formattedValue)}
                                                    placeholder='Phonenumber'
                                                    autoFormat={true}
                                                    enableSearch={true}
                                                    countryCodeEditable={false}
                                                    searchPlaceholder={'Search'}
                                                    inputStyle={{
                                                        border: 'none',
                                                        borderBottom: '1px solid #828884',
                                                        width: '100%'
                                                    }}
                                                    buttonStyle={{
                                                        border: 'none'
                                                    }}
                                                    containerStyle={{
                                                        width: '100%',
                                                        marginTop: '13px'
                                                    }}
                                                />
                                                <InputErrors field_error_state={this.state.input_errors['country']} field_label='Country' />
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
                                                <div style={{fontSize: '10px', fontWeight: 'bold'}}>
                                                    (8 characters at minimum, with at least 1: uppercase letter, lowercase letter, number, and special character)
                                                </div>
                                                <InputErrors field_error_state={this.state.input_errors['password']} field_label='Password' />
                                                <br/>
                                            </Col>
                                        </Row>
                                        <br/>
                                        <Row style={{margin: '0px'}}>
                                            <Col sm='6'>
                                                <Label>Password Confirmation <span style={{color: 'red'}}>*</span></Label>
                                                <InputGroup>
                                                    <InputGroupText addonType="prepend">
                                                        <FaKey style={{margin:'10px'}}/>
                                                    </InputGroupText>
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
                                            By signing up, you're agreeing to {Platform_Name}'s <a href='/terms-of-service' target='_blank'  rel='noreferrer'>
                                            Terms of Service</a> and acknowledge its <a href='/privacy-policy' target='_blank'  rel='noreferrer'>Privacy Policy</a>.
                                        </h6>
                                        <br/>
                                        <a>Click the highlighted text for further information.</a>
                                        <br/><br/>
                                        <Button type="submit"
                                            style={{border: '1px solid #00539C', borderRadius: '20px', color: '#ffffff', fontWeight: 'bold', backgroundColor: '#00539C', width: '180px'}}
                                        >
                                            Signup
                                        </Button>
                                    </Form>
                                    <br/><br/>
                                    <a href='/signin' style={{color: '#00539C'}}>
                                        Already have an account? Click here to signin.
                                    </a>
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