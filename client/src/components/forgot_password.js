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
import { Message, useToaster } from "rsuite";

class ForgotPassword extends Component{
    static propTypes = {
        cookies: instanceOf(Cookies).isRequired
    };
    constructor(props) { 
        super(props);
        this.state = {
            loading: false,
            input_errors: {}
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

export default withCookies(ForgotPassword);