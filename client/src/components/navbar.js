import React, { Component, useReducer } from 'react';
import {
    Collapse, 
    Navbar, Nav, NavbarToggler, NavbarBrand, NavItem, NavLink, 
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
import Notification from './notification_alert';
import Logo from '../images/logo.png'

class NavBar extends Component{
    static propTypes = {
        cookies: instanceOf(Cookies).isRequired
    };
    constructor(props) { 
        super(props);
        this.state = {
            isOpen: false,
            dropdownOpen: false,
            on_mobile: false,
            loading: false,
            user_details: {
                firstname: 'Michael Panashe',
                lastname: 'Mudimbu',
                subscribed: true
            }
        };    
        
        this.HandleChange = (e) =>{
            this.setState({[e.target.name]: e.target.value});
        };

        this.LoadingOn = () => {
            this.setState({loading: true})
        }

        this.LoadingOff = () => {
            this.setState({loading: false})
        }

        this.toggle = () => {
            this.setState({
                isOpen: !this.state.isOpen
            });
        };

        this.dtoggle = () => {
            this.setState(prevState => ({
                dropdownOpen2: !prevState.dropdownOpen
            }));
        }
  
        this.onMouseEnter = () => {
            this.setState({dropdownOpen: true});
        };
      
        this.onMouseLeave = () => {
            this.setState({dropdownOpen: false});
        };

        this.GetUserDetails = () => {
            const { cookies } = this.props;
            this.LoadingOn()

            axios.post(Backend_Server_Address + 'getUserDetailsByAccessToken', null, { headers: { 'access_token': cookies.get(Access_Token_Cookie_Name) }  })
            .then((res) => {
                let result = res.data
                // set user details to state
                this.setState({user_details: result})
                this.LoadingOff()
            }).catch((error) => {
                console.log(error)
                if (error.response){ // server responded with a non-2xx status code
                    let status_code = error.response.status
                    let result = error.response.data
                    var notification_message = ''
                    if(
                        result === 'access token disabled via signout' ||
                        result === 'access token expired' ||
                        result === 'not authorized to access this' ||
                        result === 'invalid token'
                    ){ 
                        // delete token from user cookies
                        cookies.remove(Access_Token_Cookie_Name, { path: '/' });
                        // redirect to sign in
                        let port = (window.location.port ? ':' + window.location.port : '');
                        window.location.href = '//' + window.location.hostname + port + '/signin';
                    }else{
                        // notification_message = Unknown_Non_2xx_Message + ' (Error '+status_code.toString()+': '+result+')'
                        // Notification(notification_message, 'error')
                        this.GetUserDetails()
                    }
                }else if (error.request){ // request was made but no response was received ... network error
                    // Notification(Network_Error_Message, 'error')
                        this.GetUserDetails()
                }else{ // error occured during request setup ... no network access
                    // Notification(No_Network_Access_Message, 'error')
                        this.GetUserDetails()
                }
                this.LoadingOff()
            })

            this.Signout = () => {
                const { cookies } = this.props;
                this.LoadingOn()
        
                axios.post(Backend_Server_Address + 'signout', null, { headers: { 'access_token': cookies.get(Access_Token_Cookie_Name) }  })
                .then(res => { 
                    let result = res.data
                    // delete token from user cookies
                    cookies.remove(Access_Token_Cookie_Name, { path: '/' });
                    // redirect to sign in
                    let port = (window.location.port ? ':' + window.location.port : '');
                    window.location.href = '//' + window.location.hostname + port + '/signin';
                })
                .catch((error) => {
                    console.log(error)
                    if (error.response){ // server responded with a non-2xx status code
                        let status_code = error.response.status
                        let result = error.response.data
                        var notification_message = ''
                        if(
                            result === 'access token disabled via signout' ||
                            result === 'access token expired' ||
                            result === 'not authorized to access this' ||
                            result === 'invalid token'
                        ){ 
                            // delete token from user cookies
                            cookies.remove(Access_Token_Cookie_Name, { path: '/' });
                            // redirect to sign in
                            let port = (window.location.port ? ':' + window.location.port : '');
                            window.location.href = '//' + window.location.hostname + port + '/signin';
                        }else{
                            notification_message = Unknown_Non_2xx_Message + ' (Error '+status_code.toString()+': '+result+')'
                            Notification(notification_message, 'error')
                        }
                    }else if (error.request){ // request was made but no response was received ... network error
                        Notification(Network_Error_Message, 'error')
                    }else{ // error occured during request setup ... no network access
                        Notification(No_Network_Access_Message, 'error')
                    }
                    this.LoadingOff()
                });
            }
        }
    }

    componentDidMount() {
        if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
            this.setState({
                on_mobile: true
            })
        }
        // get user details if an access token is detected
        const { cookies } = this.props;
        if (cookies.get(Access_Token_Cookie_Name) != null){
            this.GetUserDetails()
        }
    }

    render() {
        // user
        var user_details = this.state.user_details

        return (
            <Navbar light expand="md" sticky='top' style={{backgroundColor: '#EEECEC'}}>
                <NavbarBrand href="/" style={{marginBottom: '0px', height: '70px', width: '150px', marginLeft: '10px'}}>
                    <img src={Logo} style={{width: '100%'}} /> 
                </NavbarBrand>
                <NavbarToggler onClick={this.toggle} style={{backgroundColor: '#EEECEC'}}/>
                <Collapse isOpen={this.state.isOpen} navbar style={{position: 'relative'}}>
                    <Nav className="ml-auto" navbar style={{position: 'absolute', right: 0, backgroundColor: '#EEECEC'}}>
                        <NavItem>
                            <NavLink href='/' style={{color: '#005fc9', fontWeight: 'bold', fontSize: '15px'}}>
                                Home
                            </NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink></NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink href='/how-it-works' style={{color: '#005fc9', fontWeight: 'bold', fontSize: '15px'}}>
                                How it works
                            </NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink></NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink href='/pricing' style={{color: '#005fc9', fontWeight: 'bold', fontSize: '15px'}}>
                                Pricing
                            </NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink></NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink href='/about-us' style={{color: '#005fc9', fontWeight: 'bold', fontSize: '15px'}}>
                                About us
                            </NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink></NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink href='/contact-us' style={{color: '#005fc9', fontWeight: 'bold', fontSize: '15px'}}>
                                Contact us
                            </NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink></NavLink>
                        </NavItem>
                        {
                            user_details === null
                            ? <>
                                <NavItem style={{border: '1px solid #005fc9', borderRadius: '20px', width: '100px'}}>
                                    <NavLink href='/signin' style={{color: '#005fc9', fontWeight: 'bold', fontSize: '15px'}}>
                                        Signin
                                    </NavLink>
                                </NavItem>  
                                <NavItem>
                                    <NavLink></NavLink>
                                </NavItem>
                                <NavItem  style={{border: '1px solid #005fc9', borderRadius: '20px', width: '100px', backgroundColor: '#005fc9'}}>
                                    <NavLink href='/signup' style={{color: '#ffffff', fontWeight: 'bold', fontSize: '15px'}}>
                                        Signup
                                    </NavLink>
                                </NavItem>
                            </>
                            : <>
                                <NavItem style={{border: '1px solid #005fc9', borderRadius: '20px', maxHeight: '45px'}}>
                                    <NavLink href='/dashboard' style={{color: '#005fc9', fontWeight: 'bold', fontSize: '15px'}}>
                                        Dashboard
                                    </NavLink>
                                </NavItem> 
                                <NavItem>
                                    <NavLink></NavLink>
                                </NavItem>
                                <NavItem>
                                    <Dropdown className="d-inline-block" onMouseOver={this.onMouseEnter} onMouseLeave={this.onMouseLeave} isOpen={this.state.dropdownOpen} toggle={this.dtoggle}>
                                        <DropdownToggle  style={{marginTop: '', backgroundColor:  'inherit', border: 'none', color: 'inherit'}}>
                                            <span style={{fontSize: '10px', color: '#005fc9', fontWeight: 'bold'}}>{user_details.firstname} {user_details.lastname}</span>
                                            <br/>
                                            {
                                                user_details.subscribed === true
                                                ? <span style={{fontWeight: 'bold', fontSize: '10px'}}>Subscribed</span>
                                                : <span style={{fontWeight: 'bold', fontSize: '10px'}}>Not subscribed</span>
                                            }
                                        </DropdownToggle>
                                        <DropdownMenu>
                                            <DropdownItem  onClick={this.Signout}>
                                                <NavLink style={{color: 'inherit', backgoundColor: 'inherit', fontWeight: 'bold'}} >
                                                    Signout
                                                </NavLink>
                                            </DropdownItem>
                                        </DropdownMenu>
                                    </Dropdown>
                                </NavItem>
                            </>
                        }
                        <NavItem>
                            <NavLink></NavLink>
                        </NavItem>
                    </Nav>
                </Collapse>
            </Navbar>
        );
    }

};

export default withCookies(NavBar);