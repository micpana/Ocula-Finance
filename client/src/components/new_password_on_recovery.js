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
import { Unknown_Non_2xx_Message, Network_Error_Message, No_Network_Access_Message } from '../network_error_messages';
import LoadingScreen from './loading_screen';
import InputErrors from './input_errors';
import { Message, useToaster } from "rsuite";
import {  } from 'react-icons/fa';

class NewPasswordOnRecovery extends Component{
    static propTypes = {
        cookies: instanceOf(Cookies).isRequired
    };
    constructor(props) { 
        super(props);
        this.state = {
            loading: false,
            input_errors: {},
            password: '',
            password_confirmation: '',
            screen: 'new password' // new password / ok / invalid token / expired / used 
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

        this.SetNewPassword = () => {
            // initialize variable to store input validation status
            var data_checks_out = true

            // clear existing input errors if any
            this.ClearInputErrors()

            // validate input data
            if (this.state.password === ''){ this.SetInputError('password', 'required'); data_checks_out = false }
            if (this.IsPasswordStructureValid(this.state.password) === false){ this.SetInputError('password', 'invalid'); data_checks_out = false }
            if (this.state.password_confirmation === ''){ this.SetInputError('password_confirmation', 'required'); data_checks_out = false }
            if (this.state.password != this.state.password_confirmation){ this.SetInputError('password_mismatch', 'invalid'); data_checks_out = false }

            // check data collection status
            if (data_checks_out === false){ // user needs to check their input data
                this.Notification('Check input fields for errors.', 'error')
            }else{ // send data to server
                this.setState({loading: true})

                var data = new FormData()
                data.append('token', this.props.match.params.recovery_token)
                data.append('password', this.state.password)

                axios.post(Backend_Server_Address + 'setNewPassword', data, { headers: { 'access_token': null }  })
                .then((res) => {
                    let result = res.data
                    // set user email to state
                    this.setState({screen: 'ok', loading: false})
                }).catch((error) => {
                    console.log(error)
                    if (error.response){ // server responded with a non-2xx status code
                        let status_code = error.response.status
                        let result = error.response.data
                        var notification_message = ''
                        if(result === 'invalid token'){ this.setState({screen: 'invalid token'}) }
                        else if (result === 'expired'){ this.setState({screen: 'expired'}) }
                        else if (result === 'used'){ this.setState({screen: 'used'}) }
                        else if (result === 'invalid password structure'){ notification_message = "The password you've entered does not have a valid structure."; this.Notification(notification_message, 'invalid') }
                        else{
                            notification_message = Unknown_Non_2xx_Message + ' (Error '+status_code.toString()+': '+result+')'
                            this.Notification(notification_message, 'error')
                        }
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
                    <title>New Password | {Platform_Name}</title>
                    {/* <meta name="description" content="" /> */}
                </Helmet>
                {
                    this.state.loading === true
                    ? <LoadingScreen />
                    : <Container>
                        {
                            screen === 'new password'
                            ? <div>
                                <br/>
                                <h6>
                                    Create a new password below
                                </h6>
                                <br/><br/>
                                <Row style={{margin: '0px'}}>
                                    <Col sm='6'>
                                        <Label>Password <span style={{color: 'red'}}>*</span></Label>
                                        <InputGroup>
                                            <InputGroupAddon addonType="prepend">
                                                <SelectIcon style={{margin:'10px'}}/>
                                            </InputGroupAddon>
                                            <Input style={{border: 'none', borderBottom: '1px solid #828884', backgroundColor: 'inherit'}}
                                                placeholder="Password" name="password" id="password"
                                                value={this.state.password} onChange={this.HandleChange} type="password" 
                                            />
                                        </InputGroup>
                                        <InputErrors field_error_state={this.state.input_errors['password']} field_label='Password' />
                                        <br/>
                                    </Col>
                                    <Col>
                                        <Label>Password Confirmation<span style={{color: 'red'}}>*</span></Label>
                                        <InputGroup>
                                            <InputGroupAddon addonType="prepend">
                                                <SelectIcon style={{margin:'10px'}}/>
                                            </InputGroupAddon>
                                            <Input style={{border: 'none', borderBottom: '1px solid #828884', backgroundColor: 'inherit'}}
                                                placeholder="Password Confirmation" name="password_confirmation" id="password_confirmation"
                                                value={this.state.password_confirmation} onChange={this.HandleChange} type="password" 
                                            />
                                        </InputGroup>
                                        <InputErrors field_error_state={this.state.input_errors['password_confirmation']} field_label='Password Confirmation' />
                                        <br/>
                                    </Col>
                                </Row>
                                <br/><br/>
                                <Button onClick={this.SetNewPassword} 
                                    style={{border: '1px solid #00539C', borderRadius: '20px', color: '#ffffff', fontWeight: 'bold', backgroundColor: '#00539C'}}
                                >
                                    Save new password
                                </Button>
                            </div>
                            : screen === 'ok'
                            ? <div>
                                <br/>
                                <h3 style={{marginTop: '150px'}}>
                                    Your password has been reset successfully.
                                </h3>
                                <h5 style={{marginTop: '50px'}}>
                                    <a href='/signin' style={{color: 'inherit'}}>Click here to signin.</a>
                                </h5>
                            </div>
                            : screen === 'invalid token'
                            ? <div>
                                <br/>
                                <h3 style={{marginTop: '150px'}}>
                                    Invalid password reset token.
                                </h3>
                                <h5 style={{marginTop: '50px'}}>
                                    <a href='/signup' style={{color: 'inherit'}}>Make sure you've followed the instructions stated in the password recovery email you received.</a>
                                </h5>
                            </div>
                            : screen === 'expired'
                            ? <div>
                                <br/>
                                <h3 style={{marginTop: '150px'}}>
                                    This password reset token expired before its use.
                                </h3>
                                <h5 style={{marginTop: '50px'}}>
                                    <a href='/forgot-password' style={{color: 'inherit'}}>Click here to generate another one.</a>
                                </h5>
                            </div>
                            : screen === 'used'
                            ? <div>
                                <br/>
                                <h3 style={{marginTop: '150px'}}>
                                    This password reset token has been used already.
                                </h3>
                                <h5 style={{marginTop: '50px'}}>
                                    <a href='/signin' style={{color: 'inherit'}}>Click here to signin.</a>
                                </h5>
                            </div>
                            : <div>
                                <br/>
                                <h3 style={{marginTop: '150px'}}>
                                    An unknown error has occured
                                </h3>
                                <h5 style={{marginTop: '50px'}}>
                                    <a href='/' style={{color: 'inherit'}}>Click here to visit our homepage instead.</a>
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

export default withCookies(NewPasswordOnRecovery);