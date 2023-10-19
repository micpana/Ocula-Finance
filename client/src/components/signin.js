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
import { Platform_Name } from '../platform_name';
import { Backend_Server_Address } from '../backend_server_url';
import { Access_Token_Cookie_Name } from '../access_token_cookie_name';
import axios from 'axios';
import { Unknown_Non_2xx_Message, Network_Error_Message, No_Network_Access_Message } from '../network_error_messages';
import LoadingScreen from './loading_screen';
import InputErrors from './input_errors';
import Notification from './notification_alert';
import Signin1 from '../images/signin_1.svg'
import { FaUserCheck, FaUserLock } from 'react-icons/fa';

class Signin extends Component{
    static propTypes = {
        cookies: instanceOf(Cookies).isRequired
    };
    constructor(props) { 
        super(props);
        this.state = {
            loading: false,
            input_errors: {},
            on_mobile: false,
            email_or_username: '',
            password: ''
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

        this.Signin = (e) => {
            e.preventDefault()
            
            // initialize variable to store input validation status
            var data_checks_out = true

            // clear existing input errors if any
            this.ClearInputErrors()

            // validate input data
            if (this.state.email_or_username === ''){ this.SetInputError('email_or_username', 'required'); data_checks_out = false }
            if (this.state.password === ''){ this.SetInputError('password', 'required'); data_checks_out = false }

            // check data collection status
            if (data_checks_out === false){ // user needs to check their input data
                Notification('Check input fields for errors.', 'error')
            }else{ // send data to server
                this.setState({loading: true})

                var data = new FormData()
                data.append('email_or_username', this.state.email_or_username)
                data.append('password', this.state.password)

                axios.post(Backend_Server_Address + 'signin', data, { headers: { 'access_token': null }  })
                .then((res) => {
                    let result = res.data
                    var user_access_token = result
                    // set user access token to cookies
                    const { cookies } = this.props;
                    cookies.set(Access_Token_Cookie_Name, user_access_token, { 
                        path: '/',
                        sameSite: true,
                        httpOnly: true
                    })
                    // redirect to user dashboard
                    let port = (window.location.port ? ':' + window.location.port : '')
                    window.location.href = '//' + window.location.hostname + port + '/dashboard'
                }).catch((error) => {
                    console.log(error)
                    if (error.response){ // server responded with a non-2xx status code
                        let status_code = error.response.status
                        let result = error.response.data
                        var notification_message = ''
                        if(result === 'incorrect details entered'){ notification_message = "Incorrect details entered." }
                        else if (result === 'email not verified'){ notification_message = "Email address not verified. Please check your mailbox for the verification email we sent you." }
                        else if (result === 'email or username not registered'){ notification_message = "Email address / username not registered on this platform." }
                        else if (result === 'banned'){ notification_message = "User banned from accessing this platform." }
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
                    <title>Signin | {Platform_Name}</title>
                    {/* <meta name="description" content="" /> */}
                </Helmet>
                {
                    this.state.loading === true
                    ? <LoadingScreen />
                    : <div>
                        <Row style={{margin: '0px'}}>
                            <Col sm='6'>
                                <img src={Signin1} style={{width: '100%'}} />
                            </Col>
                            <Col>
                                <Container>
                                    <Form onSubmit={this.Signin}>
                                        <br/><br/><br/><br/>
                                        <h2 style={{color: '#00539C'}}>Signin</h2>
                                        <br/><br/>
                                        <Label>Email or Username <span style={{color: 'red'}}>*</span></Label>
                                        <InputGroup>
                                            <InputGroupText addonType="prepend">
                                                <FaUserCheck style={{margin:'10px'}}/>
                                            </InputGroupText>
                                            <Input style={{border: 'none', borderBottom: '1px solid #828884', backgroundColor: 'inherit'}}
                                                placeholder="Email or Username" name="email_or_username" id="email_or_username"
                                                value={this.state.email_or_username} onChange={this.HandleChange} type="text" 
                                            />
                                        </InputGroup>
                                        <InputErrors field_error_state={this.state.input_errors['email_or_username']} field_label='Email or Username' />
                                        <br/><br/>
                                        <Label>Password <span style={{color: 'red'}}>*</span></Label>
                                        <InputGroup>
                                            <InputGroupText addonType="prepend">
                                                <FaUserLock style={{margin:'10px'}}/>
                                            </InputGroupText>
                                            <Input style={{border: 'none', borderBottom: '1px solid #828884', backgroundColor: 'inherit'}}
                                                placeholder="Password" name="password" id="password"
                                                value={this.state.password} onChange={this.HandleChange} type="text" 
                                            />
                                        </InputGroup>
                                        <InputErrors field_error_state={this.state.input_errors['password']} field_label='Password' />
                                        <br/><br/>
                                        <Button type="submit"
                                            style={{border: '1px solid #00539C', borderRadius: '20px', color: '#ffffff', fontWeight: 'bold', backgroundColor: '#00539C', width: '180px'}}
                                        >
                                            Signin
                                        </Button>
                                    </Form>
                                    <br/><br/>
                                    <a href='/forgot-password' style={{color: '#00539C'}}>
                                        Forgot your password? Click here to reset it.
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

export default withCookies(Signin);