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

class VerifyEmail extends Component{
    static propTypes = {
        cookies: instanceOf(Cookies).isRequired
    };
    constructor(props) { 
        super(props);
        this.state = {
            loading: false,
            input_errors: {},
            screen: 'ok' // ok / invalid token / used / expired
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

        this.VerifyEmail = () => {
            this.setState({loading: true})

            var data = new FormData()
            data.append('token', this.props.match.params.verification_token)

            axios.post(Backend_Server_Address + 'verifyEmail', data, { headers: { 'access_token': null }  })
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
                    else if (result === 'used'){ this.setState({screen: 'used'}) }
                    else if (result === 'expired'){ this.setState({screen: 'expired'}) }
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

    componentDidMount() {
        // check access token existance
        const { cookies } = this.props;
        if(cookies.get(Access_Token_Cookie_Name) != null){
            let port = (window.location.port ? ':' + window.location.port : '');
            window.location.href = '//' + window.location.hostname + port + '/dashboard';
        }else{
            this.VerifyEmail()
        }
    }

    render() {
        var screen = this.state.screen

        return (
            <div>
                <Helmet>
                    <title>Verify Email | {Platform_Name}</title>
                    {/* <meta name="description" content="" /> */}
                </Helmet>
                {
                    this.state.loading === true
                    ? <LoadingScreen />
                    : <Container>
                        {
                            screen === 'ok'
                            ? <div>
                                <br/>
                                <h3 style={{marginTop: '150px'}}>
                                    Your email has been verified successfully.
                                </h3>
                                <h5 style={{marginTop: '50px'}}>
                                    <a href='/signin' style={{color: 'inherit'}}>Click here to signin.</a>
                                </h5>
                            </div>
                            : screen === 'invalid token'
                            ? <div>
                                <br/>
                                <h3 style={{marginTop: '150px'}}>
                                    Invalid verification token.
                                </h3>
                                <h5 style={{marginTop: '50px'}}>
                                    <a href='/signin' style={{color: 'inherit'}}>Make sure you've completed the signup process and clicked the link we sent to the email address you provided upon signing up.</a>
                                </h5>
                            </div>
                            : screen === 'used'
                            ? <div>
                                <br/>
                                <h3 style={{marginTop: '150px'}}>
                                    This verification token has already been used.
                                </h3>
                                <h5 style={{marginTop: '50px'}}>
                                    <a href='/signin' style={{color: 'inherit'}}>Click here to signin.</a>
                                </h5>
                            </div>
                            : screen === 'expired'
                            ? <div>
                                <br/>
                                <h3 style={{marginTop: '150px'}}>
                                    This verification token expired before its use.
                                </h3>
                                <h5 style={{marginTop: '50px'}}>
                                    <a href='/signin' style={{color: 'inherit'}}>Click here to attemp a signin and another one will be generated for you.</a>
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

export default withCookies(VerifyEmail);