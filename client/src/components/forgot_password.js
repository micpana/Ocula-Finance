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
import { FaAt } from 'react-icons/fa';

class ForgotPassword extends Component{
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
            email: '',
            screen: 'email entry' // email entry / ok / email not registered / banned / try again in n minutes
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

        this.ForgotPassword = (e) => {
            e.preventDefault()
            
            // initialize variable to store input validation status
            var data_checks_out = true

            // clear existing input errors if any
            this.ClearInputErrors()

            // validate input data
            if (this.state.email === ''){ this.SetInputError('email', 'required'); data_checks_out = false }
            if (IsEmailStructureValid(this.state.email) === false){ this.SetInputError('email', 'invalid'); data_checks_out = false }

            // check data collection status
            if (data_checks_out === false){ // user needs to check their input data
                Notification('Check input fields for errors.', 'error')
            }else{ // send data to server
                this.LoadingOn()

                var data = new FormData()
                data.append('email', this.state.email)

                axios.post(Backend_Server_Address + 'recoverPassword', data, { headers: { 'access_token': null }  })
                .then((res) => {
                    let result = res.data
                    // set screen to ok
                    this.setState({screen: 'ok'})
                    this.LoadingOff()
                }).catch((error) => {
                    console.log(error)
                    if (error.response){ // server responded with a non-2xx status code
                        let status_code = error.response.status
                        let result = error.response.data
                        var notification_message = ''
                        if(result === 'email not registered'){ this.setState({screen: 'email not registered'}) }
                        else if (result === 'banned'){ this.setState({screen: 'banned'}) }
                        else if (result.includes('try again in') === true){ this.setState({screen: result}) }
                        else{
                            notification_message = Unknown_Non_2xx_Message + ' (Error '+status_code.toString()+': '+result+')'
                            Notification(notification_message, 'error')
                        }
                    }else if (error.request){ // request was made but no response was received ... network error
                        Notification(Network_Error_Message, 'error')
                    }else{ // error occured during request setup ... no network access
                        Notification(No_Network_Access_Message, 'error')
                    }
                    this.LoadingOff()
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

        // check access token existance
        const { cookies } = this.props;
        if(cookies.get(Access_Token_Cookie_Name) != null){
            let port = (window.location.port ? ':' + window.location.port : '');
            window.location.href = '//' + window.location.hostname + port + '/dashboard';
        }
    }

    render() {
        var screen = this.state.screen

        return (
            <div>
                <Helmet>
                    <title>Forgot Password | {Platform_Name}</title>
                    {/* <meta name="description" content="" /> */}
                </Helmet>
                <ToastContainer />
                {
                    this.state.loading === true
                    ? <LoadingScreen />
                    : this.state.network_error_screen === true
                    ? <NetworkErrorScreen error_message={this.state.network_error_message} retryFunction={this.state.retry_function} />
                    : <Container>
                        <br/><br/><br/><br/>
                        {
                            screen === 'email entry'
                            ? <div>
                                <h6>
                                    Enter the email address you used during signup
                                </h6>
                                <br/><br/>
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
                                <br/><br/><br/>
                                <Button onClick={this.ForgotPassword} 
                                    style={{border: '1px solid #00539C', borderRadius: '20px', color: '#ffffff', fontWeight: 'bold', backgroundColor: '#00539C'}}
                                >
                                    Reset Password
                                </Button>
                            </div>
                            : screen === 'ok'
                            ? <div>
                                <h3 style={{marginTop: '30px'}}>
                                    We've sent you a password reset email at <span style={{color: '#00539C'}}>{this.state.email}</span>
                                </h3>
                                <h5 style={{marginTop: '50px'}}>
                                    Follow the instructions stated in the email inorder to reset your account password.
                                </h5>
                                <h6 style={{marginTop: '70px'}}>
                                    Did not receive our email? Click the button below to resend.
                                </h6>
                                <br/>
                                <Button onClick={this.ForgotPassword} 
                                    style={{border: '1px solid #00539C', borderRadius: '20px', color: '#ffffff', fontWeight: 'bold', backgroundColor: '#00539C'}}
                                >
                                    Resend recovery email
                                </Button>
                                <h6 style={{marginTop: '100px'}}>
                                    Made a typo on your email address? Click the button below to correct it.
                                </h6>
                                <br/>
                                <Button onClick={() => this.setState({screen: 'email entry'})} 
                                    style={{border: '1px solid #00539C', borderRadius: '20px', color: '#ffffff', fontWeight: 'bold', backgroundColor: '#00539C'}}
                                >
                                    Correct email
                                </Button>
                            </div>
                            : screen === 'email not registered'
                            ? <div>
                                <h3 style={{marginTop: '30px'}}>
                                    The email address you've supplied (<span style={{color: '#00539C'}}>{this.state.email}</span>) is not registered on this platform.
                                </h3>
                                <h5 style={{marginTop: '50px'}}>
                                    <a href='/signup' style={{color: '#00539C'}}>Click here to signup.</a>
                                </h5>
                            </div>
                            : screen === 'banned'
                            ? <div>
                                <h3 style={{marginTop: '30px'}}>
                                    The email address you've supplied (<span style={{color: '#00539C'}}>{this.state.email}</span>) belongs to an account that has been 
                                    banned on this platform. 
                                </h3>
                                <h5 style={{marginTop: '50px'}}>
                                    <a href='/contact-us' style={{color: '#00539C'}}>If you have no information why, contact our support team to find out.</a>
                                </h5>
                            </div>
                            : screen.includes('try again in') === true
                            ? <div>
                                <h3 style={{marginTop: '30px'}}>
                                    You've made multiple requests to our server in a short amount of time.
                                </h3>
                                <h5 style={{marginTop: '50px'}}>
                                    <a style={{color: '#00539C'}}>{screen}</a>
                                </h5>
                            </div>
                            : <div>
                                <h3 style={{marginTop: '30px'}}>
                                    An unknown error has occured.
                                </h3>
                                <h5 style={{marginTop: '50px'}}>
                                    <a href='/' style={{color: '#00539C'}}>Click here to visit our homepage instead.</a>
                                </h5>
                            </div>
                        }
                    </Container>
                }
                <br/><br/><br/>
            </div>
        );
    }

};

export default withCookies(ForgotPassword);