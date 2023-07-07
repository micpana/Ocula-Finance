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
            if (this.state.phonenumber === ''){ this.SetInputError('phonenumber', 'required'); data_checks_out = false }
            if (this.state.password === ''){ this.SetInputError('password', 'required'); data_checks_out = false }
            if (this.state.password_confirmation === ''){ this.SetInputError('password_confirmation', 'required'); data_checks_out = false }
            if (this.state.password != this.state.password_confirmation){ this.SetInputError('password_mismatch', 'mismatch'); data_checks_out = false }
            if (this.state.country === ''){ this.SetInputError('country', 'required'); data_checks_out = false }

            // check data collection status
            if (data_checks_out === false){ // user needs to check their input data
                alert('Check input fields for errors.')
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
                    let port = (window.location.port ? ':' + window.location.port : '')
                    window.location.href = '//' + window.location.hostname + port + '/email-verification-sent/'  + account_id
                }).catch((error) => {
                    if (error.response){ // server responded with a non-2xx status code
                        let status_code = error.response.status
                        let result = error.response.data
                    }else if (error.request){ // request was made but no response was received ... network error

                    }else{ // error occured during request setup ... no network access

                    }
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

export default withCookies(Signup);