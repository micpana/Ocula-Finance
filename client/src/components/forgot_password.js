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

class ForgotPassword extends Component{
    static propTypes = {
        cookies: instanceOf(Cookies).isRequired
    };
    constructor(props) { 
        super(props);
        this.state = {
            loading: false,
            input_errors: {},
            email: '',
            screen: 'ok' // ok / email not registered / banned / try again in n minutes
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

        this.ForgotPassword = () => {
            // initialize variable to store input validation status
            var data_checks_out = true

            // clear existing input errors if any
            this.ClearInputErrors()

            // validate input data
            if (this.state.email === ''){ this.SetInputError('email', 'required'); data_checks_out = false }
            if (this.IsEmailStructureValid(this.state.email) === false){ this.SetInputError('email', 'invalid'); data_checks_out = false }

            // check data collection status
            if (data_checks_out === false){ // user needs to check their input data
                this.Notification('Check input fields for errors.', 'error')
            }else{ // send data to server
                this.setState({loading: true})

                var data = new FormData()
                data.append('email', this.state.email)

                axios.post(Backend_Server_Address + 'recoverPassword', data, { headers: { 'access_token': null }  })
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
                        if(result === 'email not registered'){ this.setState({screen: 'email not registered'}) }
                        else if (result === 'banned'){ this.setState({screen: 'banned'}) }
                        else if (result.includes('try again in') === true){ this.setState({screen: result}) }
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
                    <title>Forgot Password | {Platform_Name}</title>
                    {/* <meta name="description" content="" /> */}
                </Helmet>
                {
                    this.state.loading == true
                    ? <LoadingScreen />
                    : <div>
                        
                    </div>
                }
                <br/><br/><br/>
            </div>
        );
    }

};

export default withCookies(ForgotPassword);